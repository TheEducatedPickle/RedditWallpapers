import praw
import ctypes
import configparser
import urllib.request as dl
import os

reddit = praw.Reddit("bot1")
config = configparser.ConfigParser()

#Configuration
config.read("config.ini")
os.chdir(config["Bot"]["downloadDirectory"])

source = ""
subNum = 0
while str(subNum) in config["Sources"]:
    source += config["Sources"][str(subNum)]
    subNum += 1
    if str(subNum) in config["Sources"]:
        source += "+"
print("Downloading from subreddits: " + source)

imgName = 0
subreddit = reddit.subreddit(source)
for submission in subreddit.top("month"):
    print("Downloading " + submission.title)
    dl.urlretrieve(submission.url, str(imgName) + ".jpg")
    imgName += 1
    if (imgName >= config["maxImages"]):
        break
