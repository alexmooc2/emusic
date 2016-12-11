import webapp2
import jinja2
import lyrics
import os
import logging
import tone
import last
import genius

#second commit yay!

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("home.html")
        self.response.write(template.render())

class SongInfo(webapp2.RequestHandler):
    def post(self):
        req = self.request
        url = req.url
        artist = req.get("artist")
        song = req.get("song")
        track = genius.search(artist, song)
        if track != None:
            tones = tone.getTone(track)
            results = {}
            for item in tones:
                emotion = item['tone_name']
                score = item['score']
                if emotion not in results:
                    results[emotion] = float(score)
                else:
                    results[emotion] = float(results[emotion]) + float(score)
            vals = {}
            vals['artist_name'] = track.artist
            vals['song_name'] = track.track
            vals['song_image'] = track.image
            vals['emotions'] = []
            vals['numbers'] = []
            for item in results:
                vals['emotions'].append(item) 
                vals['numbers'].append(results[item])
            template = JINJA_ENVIRONMENT.get_template("tone_output.html")
        else:
            template = JINJA_ENVIRONMENT.get_template("error.html")
        self.response.write(template.render(vals))

class LastFMHome(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("lastfm.html")
        self.response.write(template.render())
        
class LastFMResult(webapp2.RequestHandler):
    def post(self):
        req = self.request
        user = req.get("username").encode("utf-8")
        top_tracks = last.getTopTracks(user)
        logging.info(top_tracks)
        lyrics_list = []
        lyrics_list = [genius.search(item, top_tracks[item]) for item in top_tracks]
        lyrics_list = [item for item in lyrics_list if item is not None]
        tone_list = [tone.getTone(item) for item in lyrics_list[:5] if item != None]
        results = {}
        for item in tone_list:
            if item != None:
                logging.info(item)
                for x in item:
                    emotion = x['tone_name']
                    score = x['score']
                    if emotion not in results:
                        results[emotion] = float(score)
                    else:
                        results[emotion] = float(results[emotion]) + float(score)
        template = JINJA_ENVIRONMENT.get_template("tone_output2.html")
        vals = {}
        vals['emotions'] = []
        vals['numbers'] = []
        vals['tracks'] = lyrics_list
        vals['username'] = user
        for item in results:
            vals['emotions'].append(item) 
            vals['numbers'].append(results[item])
        self.response.write(template.render(vals))

application = webapp2.WSGIApplication([ 
                                      ('/song_info', SongInfo),
                                      ('/last_home', LastFMHome),
                                      ('/last_result', LastFMResult),
                                      ('/.*', MainHandler),
                                      ],
                                     debug=True)
