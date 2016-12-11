import urllib, urllib2, json, webbrowser
import keys
import tone
import re
import jinja2
import os 
import logging
import last_key
import lyrics

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request." 
        print "Error code: ", e.code
    except urllib2.URLError, e:
        print "We failed to reach a server"
        print "Reason: ", e.reason
    return None

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def getTopTracks(user):
    base_url = last_key.url
    api_key = last_key.key
    method = "user.getTopTracks"
    params = {"method": method, "format":"json", "api_key":api_key, "user": user, "page":"3", "period":"7days"}
    url = base_url + "?" + urllib.urlencode(params) 
    logging.info(url)
    response = json.load(safeGet(url))
    if response != None:
        logging.info(response)
        response = response['toptracks']['track'][:8]
        top_tracks = {}
        for item in response:
            top_tracks[item['artist']['name']] = item['name']
        return top_tracks
    else:
        return None
    
def getTones():
    top_tracks = getTopTracks("beef-mo")
    print len(top_tracks)   
    track_ids = [lyrics.searchTrack(item, top_tracks[item])for item in top_tracks]
    print track_ids

    
