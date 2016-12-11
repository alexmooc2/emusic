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
        
def safeGet(request_str):
    try:
        req = urllib2.Request(request_str, headers = {"User-agent":"CompuServe Classic/1.22"})
        return json.load(urllib2.urlopen(req))
    except urllib2.HTTPError, e:
        print "Server couldn't fulfill request"
        print "Error code: "
        print e 
    except urllib2.URLError, e:
        print "Failed to reach server"
        print "Reason: "
        print e
    return None

def geniusURL(m, artist, song):
    search = artist + " " + song
    base_url = "http://api.genius.com/"
    method = m
    query = {}
    query['access_token'] = genius_key.token
    query['q'] = search.encode("utf-8")
    url = base_url+method+"?"+urllib.urlencode(query)
    logging.info(url)
    response = safeGet(url)['response']['hits']
    track_object_list = [Track(item) for item in response]
#     for item in track_object_list:
#         logging.info(item.artist)
#     track_object_list = [item for item in track_object_list if item.artist.encode("utf-8") == artist.encode("utf-8")]
    track_object_list = sorted(track_object_list, key = lambda x: SequenceMatcher(None, x.artist, artist).ratio(), reverse = True)
    for item in track_object_list:
        logging.info(item.artist + " " + str(SequenceMatcher(None, item.artist, artist).ratio()))
#     logging.info("-->" + artist)
#     logging.info("TRACK DONE")
#     if len(response) > 0:
# #         logging.info(response)
# #         response = [item for item in response if "pageviews" in item['result']['stats']]
# #         logging.info(response)
# #         response = sorted(response, key = lambda x: int(x['result']['stats']['pageviews']), reverse = True)
# #         logging.info(response)
#         path = response[0]['result']['path']
#         song_url = "http://genius.com" + path
#         return song_url.encode("utf-8")
    return track_object_list[0]

def geniusText(song_url):
    req = urllib2.Request(song_url, headers = {"User-agent":"CompuServe Classic/1.22"})
    file = urllib2.urlopen(req, timeout = 10).read()
    soup = BeautifulSoup(file, "html.parser")
    lyrics = soup.find("lyrics").get_text()
    return lyrics.encode("utf-8")   
    
def search(artist, song):
    track_dict = geniusURL("search", artist, song)
    return track_dict
#     logging.info(url)
#     if track_dict != None:
# #         track_dict = geniusText(url)
#         return Track(track_dict)
