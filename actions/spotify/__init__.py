INTENTS = [
    "SPOTIFY_NEXT",
    "SPOTIFY_PREVIOUS",
    "SPOTIFY_PLAY",
    "SPOTIFY_PAUSE",
    "SPOTIFY_LOUDER",
    "SPOTIFY_SOFTER",
]

from pathlib import Path
import os
import bips

def check_auth():
    return os.path.isfile(os.path.join(str(Path.home()), ".config/spotify-cli/credentials.json"))
    
def auth():
    bips.playError()
    bips.say("Please log into Spotify with command 'spotify auth login'")
    print("Need login: https://pypi.org/project/spotify-cli/")

def next():
    os.system("spotify next")
    return 1

def previous():
    os.system("spotify previous")
    return 1

def play():
    os.system("spotify play")
    return 1

def pause():
    os.system("spotify pause")
    return 1

def louder():
    os.system("spotify volume up 10")
    return 1

def softer():
    os.system("spotify volume down 10")
    return 1

def main(intent, request):
    if check_auth() == False:
        auth()
        return 0
    match intent:
        case "SPOTIFY_NEXT":
            return next()
        case "SPOTIFY_PREVIOUS":
            return previous()
        case "SPOTIFY_PLAY":
            return play()
        case "SPOTIFY_PAUSE":
            return pause()
        case "SPOTIFY_LOUDER":
            return louder()
        case "SPOTIFY_SOFTER":
            return softer()
        case _:
            return 0