import praw
import ctypes
import configparser
import urllib.request as dl
import os

reddit = praw.Reddit("bot1")
config = configparser.ConfigParser()

def getImages():
    print("Downloading from subreddits: " + source)
    imgName = 0
    errorCount = 0
    subreddit = reddit.subreddit(source)
    for submission in subreddit.top("month"):
        print("Downloading " + submission.title)
        try:
            dl.urlretrieve(submission.url, str(imgName) + ".jpg")
            if (imgName >= int(config["Bot"]["maxImages"])):
                print("Downloading completed, " + imgName - errorCount + " images successfully downloaded with " + errorCount + " errors!")
                break
        #Catch error if url fails
        except IOError:
            if errorCount < 5:
                print("Downloading failed, skipping")
            else:
                print("Failed 5 attempts, terminating")
                break
        imgName += 1


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
getImages()