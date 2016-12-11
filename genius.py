import urllib, urllib2, json, webbrowser
import keys
import tone
import re
import jinja2
import os 
import logging
from bs4 import BeautifulSoup
import requests
from requests.structures import CaseInsensitiveDict
# from google.appengine.api import urlfetch
import genius_key
from difflib import SequenceMatcher

class Track():
    
    def __init__(self, genius_dict):
        self.artist = genius_dict['result']['primary_artist']['name']
        self.track = genius_dict['result']['title']
        path = genius_dict['result']['path']
        song_url = "http://genius.com" + path
        self.lyric = geniusText(song_url)
        self.image = genius_dict['result']['header_image_thumbnail_url']

# Takes in an artist and a song. Returns the URL of p
def search(artist, song):
    search = artist + " " + song
    base_url = "http://api.genius.com/"
    method = "search"
    query = {}
    query['access_token'] = genius_key.token
    query['q'] = search.encode("utf-8")
    url = base_url+method+"?"+urllib.urlencode(query)
    logging.info(url)
    response = safeGet(url)
    if response != None:
        response = response['response']['hits']
        track_object_list = [Track(item) for item in response]
        track_object_list = sorted(track_object_list, key = lambda x: SequenceMatcher(None, x.artist, artist).ratio(), reverse = True)
        for item in track_object_list:
            logging.info(item.artist + " " + str(SequenceMatcher(None, item.artist, artist).ratio()))
        return track_object_list[0]
    else:
        return None

# Takes in the URL of a song lyric page and returns the lyrics as a string
def geniusText(song_url):
    req = urllib2.Request(song_url, headers = {"User-agent":"CompuServe Classic/1.22"})
    file = urllib2.urlopen(req, timeout = 10).read()
    soup = BeautifulSoup(file, "html.parser")
    lyrics = soup.find("lyrics").get_text()
    return lyrics.encode("utf-8")   


def safeGet(request_str):
    try:
        req = urllib2.Request(request_str, headers = {"User-agent":"CompuServe Classic/1.22"})
        return json.load(urllib2.urlopen(req))
    except urllib2.HTTPError, e:
        loggin.info( "Server couldn't fulfill request")
        loggin.info("Error code: ")
        loggin.info(e) 
    except urllib2.URLError, e:
        loggin.info( "Failed to reach server")
        loggin.info("Reason: ")
        loggin.info(e)
    return None
