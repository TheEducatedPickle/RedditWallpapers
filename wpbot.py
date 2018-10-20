import praw
import ctypes
import configparser
import urllib.request as dl
import os
import mimetypes

reddit = praw.Reddit("bot1")
config = configparser.ConfigParser()
#commandDict = {"fetch": getImages, "next": setDesktop}

def main():
    # Configuration
    config.read("config.ini")
    os.chdir(config["Bot"]["downloadDirectory"])

    print("wpbot ready")
    getInput()

def getImages():
    source = parseSources()
    print("Downloading from subreddits: " + source)
    imgName = 0
    errorCount = 0
    subreddit = reddit.subreddit(source)
    for submission in subreddit.top("month"):
        print("Downloading --- " + submission.title)
        print(submission.url)
        try:
            #If the url does not indicate it contains an image, raise an IOError
            mimetype = mimetypes.guess_type(submission.url)[0]
            if not (mimetype and mimetype.startswith('image')):
                raise IOError
            
            dl.urlretrieve(submission.url, str(imgName) + ".png")
            errorCount = 0
            imgName += 1

            if (imgName >= int(config["Bot"]["maxImages"])):
                print("Downloading completed!")
                break
        # Catch error if url fails
        except IOError:
            if errorCount < 50:
                print("No image detected, skipping")
            else:
                print("No image posts found in 50 tries, make sure to include only image subredddits in config.ini. Terminating...")
                break


def parseSources():
#Creates a string representing all subreddits in config.ini
    source = ""
    subNum = 0
    while str(subNum) in config["Sources"]:
        source += config["Sources"][str(subNum)]
        subNum += 1
        if str(subNum) in config["Sources"]:
            source += "+"
    return source

def setDesktop(img=0): 
    #Selects the next image from imported images and calls setter method
    #Acts as a wrapper for setter that sets next image and catches exceptions
    output = img + 1
    try:
        setter(img)
    except IOError:
        if (img == int(config["Bot"]["maxImages"])-1):
            output = 0
            setter(output)
        else:
            getImages()
            setter(img)
    return output


def setter(img=0):  
    # Helper function for setDesktop that gets the appropriate image
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(
        SPI_SETDESKWALLPAPER, 0, str(img) + ".png", 0)


def getInput():
    #Acts as user interface, gets user input and runs appropriate functions
    print("Type next to update your wallpaper, and help for more information")
    current = 0  # The current wallpaper number
    while True:
        command = input("")
        if (command == "fetch"):
            getImages()
        if (command == "next"):
            current = setDesktop(current)

if __name__ == "__main__":
    main()
