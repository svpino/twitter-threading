import tweepy
import yaml


API_KEY = "YOUR API KEY GOES HERE"
API_KEY_SECRET = "YOUR API KEY SECRET GOES HERE"
ACCESS_TOKEN = "YOUR ACCESS TOKEN GOES HERE"
ACCESS_TOKEN_SECRET = "YOUR ACCESS TOKEN SECRET GOES HERE"

USER = "YOUR USER GOES HERE"


def authenticate():
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True)


def load():
    with open(r'thread.yml') as file:
        thread = yaml.load(file, Loader=yaml.FullLoader)

    return thread


def post(api, thread):
    status = None
    for tweet in thread["thread"]:
        args = {
            "status": tweet["text"],
            "in_reply_to_status_id": (status.id if status else None)
        }

        if "attachment" in tweet:
            status = api.update_status(**args, attachment_url=tweet["attachment"])
        elif "media" in tweet:
            status = api.update_with_media(**args, filename=tweet["media"])
        else:
            status = api.update_status(**args)


if __name__ == "__main__":
    api = authenticate()
    thread = load()
    post(api, thread)
