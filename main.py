from argparse import ArgumentError
import os
import re
import tweepy
import yaml
import sched
import time
import datetime
import argparse
from apscheduler.schedulers.background import BackgroundScheduler # importing APScheduler Library
from airtable import Airtable # importing Airtable library

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.environ["API_KEY"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


def authenticate():
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True)


def load(filename):
    with open(filename) as file:
        thread = yaml.load(file, Loader=yaml.FullLoader)

    return thread["thread"]

def upload_media(api, filename):
    res = api.media_upload(filename)
    return res.media_id

def post(api, thread):
    status = None
    for tweet in thread["tweets"]:
        args = {
            "status": tweet["text"],
            "in_reply_to_status_id": (status.id if status else None),
        }

        if "attachment" in tweet:
            status = api.update_status(**args, attachment_url=tweet["attachment"])
        elif "media" in tweet:
            media_ids = []
            if type(tweet["media"]) is list:
                for filename in tweet["media"]:
                    media_ids.append(upload_media(api, filename))
            else:
                media_ids.append(upload_media(api, tweet["media"]))
            status = api.update_status(**args, media_ids=media_ids)
        else:
            status = api.update_status(**args)


def schedule(api, thread, when):
    when = datetime.datetime.strptime(when, "%Y-%m-%d %H:%M")
    delta = (when - datetime.datetime.now()).total_seconds()

    if delta < 0:
        raise Exception("The value of the when argument is in the past")

    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(delta, 60, post, kwargs={"api": api, "thread": thread})
    schedule.run()


def when_format(arg_value, pat=re.compile(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid format. Expecting yyyy-mm-dd hh:mm")

    return arg_value

''' Start of PR '''

def routine_post_from_airtable():
    '''
    This function will take the top entry in an airtable base and post it on Twitter
    We will then configure the Tweepy library to post it every day at a certain time
    '''
    airtable = Airtable("base_key", "base_name", api_key="API_KEY_SECRET") #authenticate Airtable
    tweet_content = airtable.get_all(view='new', max_records=1) # get tweet from 'new' view, which are tweets that haven't been posted yet
    main_content = tweet_content['fields']['main'] # get params
    hashtags = tweet_content['fields']['hashtags'] # get params
    hyperlink = tweet_content['fields']['link'] # get params
    
    api = authenticate() # authenticate Tweepy
    api.update_status(main_content + "\n \n" + hashtags + "\n \n " + hyperlink) # post Tweet

#setting APScheduler timezone
scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})

#configuring the APScheduler to send out tweets everyday at a certain time (at UTC)
scheduler.add_job(routine_post_from_airtable, "cron", day="*", hour=12, minute=0) 

scheduler.start() #start the scheduler
atexit.register(lambda: scheduler.shutdown()) #shut the scheduler down when exiting the app

''' End of PR '''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--thread", type=str, required=True, help="The yaml file containing the thread"
    )
    parser.add_argument(
        "--when",
        type=when_format,
        required=True,
        help="The date and time when the thread will be posted",
    )
    args = parser.parse_args()

    api = authenticate()
    thread = load(args.thread)
    schedule(api, thread, args.when)
