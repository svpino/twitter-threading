# Automatically posting Twitter threads

Very few services out there let you schedule threads on Twitter. (Yes, I know some do, don't @ me now with the list.)

Through experimentation, I discovered that my best performing threads are the ones I post between 12:30 am and 1:00 am. There may be some confirmation bias here, but that's where I am today.

I can't stay awake every time I want to post a thread to hit that "Tweet" button, so I decided to build this script.

The principle is simple:

1. I write my tweet in a .YAML file.
2. I run my script specifying when I want it posted.
3. I go to sleep as a normal human being, not obsessed with this stuff.
4. The script does its job and posts the thread.

I also wanted to make sure I added support for images in my tweets, and attachments (links to other tweets.) 

## Let's run this thing
If you want to take this for a spin, here is what you need to do:

1. Make sure you have Python 3 installed in your system.
2. Clone this repository.
3. I'd recommend you create a virtual environment for this (I always recommend you do this), but you don't have to.
4. Run `pip3 install -r requirements.txt` to install all the requirements you need.
5. Create a `.env` file in the root directory of the project and add the following content to it (replacing the values by your own keys):

``` shell
API_KEY=<YOUR API_KEY GOES HERE>
API_KEY_SECRET=<YOUR API_KEY_SECRET GOES HERE>
ACCESS_TOKEN=<YOUR ACCESS_TOKEN GOES HERE>
ACCESS_TOKEN_SECRET=<YOUR ACCESS_TOKEN_SECRET GOES HERE>
```

6. Fill out your `thread.yaml` file with the content you want to post.
7. Run the script specifying the date of when you want this posted:

```shell
$ python main.py --thread thread.yaml --when "2020-09-17 22:44"
```

## Want to contribute?

If you want to contribute to the project, check the [Contribution Guidelines](CONTRIBUTING.md).

                                    ##THANKYOU
