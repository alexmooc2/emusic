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
from google.appengine.api import urlfetch

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def safeGet(request_str):
    try:
        return json.load(urllib2.urlopen(request_str))
    except urllib2.HTTPError, e:
        print "Server couldn't fulfill request"
        print "Error code: " + e 
    except urllib2.URLError, e:
        print "Failed to reach server"
        print "Reason: "+ e
    return None
    
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)
    
def searchTrack(artist, track):
    method = "track.search"
    params = {"apikey":keys.key, "format":"json", "s_track_rating": "desc", "q_track": track, "q_artist": artist, "format":"json",}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    print request_str
    response_json = safeGet(request_str)['message']['body']['track_list']
    track = response_json[0]['track']
    return track


