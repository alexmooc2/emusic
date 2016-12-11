class AlbumList(webapp2.RequestHandler):
    def post(self):
        vals = {}
        req = self.request
        artist = req.get("artist_search").encode("UTF-8")
        artist_id = lyrics.getArtistID(artist)
        template = JINJA_ENVIRONMENT.get_template("album_list_template.html")
        if artist_id != None:
            album_list = lyrics.getArtistAlbums(artist_id)
            vals['album_list'] = album_list 
        self.response.write(template.render(vals))
        
class SongInfo(webapp2.RequestHandler):
    def post(self):
#         req = self.request
#         url = req.url
#         album_id = url[-8:]
#         album = lyrics.getAlbum(album_id)
#         artist_name = album['artist_name']
#         album_name = album['album_name']
#         track_list = lyrics.getTrack(album_id)
        req = self.request
        song = req.get("song")
        song_split = song.split("|")
        lyric = genius.search(song_split[0], song_split[1])
        logging.info(lyric.lyric)
#         lyrics_list = []
#         lyrics_list = [genius.search(artist_name, item) for item in track_list]
#         logging.info(len(lyrics_list))
        logging.info("*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************")
        logging.info("*******************NOW WORKING ON GETTING TONES************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************")
#         big_lyric = "".join(lyrics_list)
#         tones = [tone.getTone(item) for item in lyrics_list]
        tones = tone.getTone(lyric)
        results = {}
#         for item in tones:
#             if item != None:
# #                 logging.info(item)
# #                 logging.info(item['document_tone'])
# #                 logging.info(item['document_tone']['tone_categories'])
# #                 logging.info(item['document_tone']['tone_categories'][0])
        tones = tones['document_tone']['tone_categories'][0]['tones']
        for item in tones:
            emotion = item['tone_name']
            score = item['score']
            if emotion not in results:
                results[emotion] = float(score)
            else:
                results[emotion] = float(results[emotion]) + float(score)
        template = JINJA_ENVIRONMENT.get_template("tone_output.html")
        vals = {}
        vals['emotions'] = []
        vals['song'] = song_split
        vals['numbers'] = []
        for item in results:
            vals['emotions'].append(item) 
            vals['numbers'].append(results[item])
#TEST CODE
#          vals['emotions'] = {"joy", "anger"}
#          vals["numbers"] = {4, 5}
#          vals['artist_name'] = "Kanye West"
#          vals['album_name'] = "Graduation" 
        self.response.write(template.render(vals))
        
class LastFMResult(webapp2.RequestHandler):
    def post(self):
        req = self.request
        user = req.get("user_search").encode("utf-8")
        top_tracks = last.getTopTracks(user)
        logging.info(top_tracks)
#         track_list = [lyrics.searchTrack(item, top_tracks[item]) for item in top_tracks]
        lyrics_list = []
        lyrics_list = [genius.search(item, top_tracks[item]) for item in top_tracks]
        lyrics_list = [item for item in lyrics_list if item is not None]
        counter = 0
#         for item in lyrics_list:
#             if len(item) < 2:
#                 logging.info("***************************************************")
        tone_list = [tone.getTone(item) for item in lyrics_list[:5] if item != None]
        results = {}
        for item in tone_list:
            if item != None:
#                 logging.info(item)
#                 logging.info(item['document_tone'])
#                 logging.info(item['document_tone']['tone_categories'])
#                 logging.info(item['document_tone']['tone_categories'][0])
                tones = item['document_tone']['tone_categories'][0]['tones']
                for item in tones:
                    emotion = item['tone_name']
                    score = item['score']
                    if emotion not in results:
                        results[emotion] = float(score)
                    else:
                        results[emotion] = float(results[emotion]) + float(score)
        
        template = JINJA_ENVIRONMENT.get_template("tone_output2.html")
        vals = {}
        vals['emotions'] = []
        vals['numbers'] = []
        vals['tracks'] = lyrics_list
        vals['artist_name'] = "PLACEHOLDER"
        vals['album_name'] = "PLACEHOLDER"
        for item in results:
            vals['emotions'].append(item) 
            vals['numbers'].append(results[item])
        self.response.write(template.render(vals))
        
# LYRIC.PY 
def getTones(track_ids, artist_name, album_name):
    lyrics_list = []
    lyrics_list = [getLyrics(item) for item in track_ids]  
#     for item in track_ids:
#         print lyrics_list
#         lyric = getLyrics(item)
#         lyrics_list.append(lyric)
    tone_list = [tone.getTone(item) for item in lyrics_list]
    results = {}
    for item in tone_list:
        if item != None:
            tones = item['document_tone']['tone_categories'][0]['tones']
            for item in tones:
                emotion = item['tone_name']
                score = item['score']
                if emotion not in results:
                    results[emotion] = float(score)
                else:
                    results[emotion] = float(results[emotion]) + float(score)
    return results
def getArtistAlbums(id):
    method = "artist.albums.get"
    params = {"apikey":keys.key, "artist_id":str(id), "format":"json", 'page_size':'100'}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    response_json = safeGet(request_str)['message']['body']['album_list']
    album_list = {}
    for item in response_json:
        album_name = item['album']['album_name']
        album_id = item['album']['album_id']
        if (item['album']['album_track_count'] > 5 and item['album']['restricted'] != 1):
            current_count = item['album']['album_track_count']
            if (album_list.get(album_name) == None):
                album_list[album_name] = album_id
    album_id_list = []
    album_id_list = [album_list[item] for item in album_list]
#   Only first item in album list will be printed. Find what the key is first and print it
#     working =  album_id_list[0]
#     for key in album_list.keys():
#         if album_list[key] == working:
#             print key
    return album_list
#     album_list = [album['album']["album_name"] for album in response_json['album_list']] 
#     album_list_2 = []
#     [album_list_2.append(x) for x in album_list if x not in album_list_2]   
#     album_id_list = [[album['album']["album_id"] for album in response_json['album_list']] if album['name'] ]
#     print album_list_2

def scrubArtistList(artist):
    return artist['artist']['artist_name']
    
def getArtistID(artist):
    method = "artist.search"
    params = {"apikey":keys.key, "q_artist":artist, "format":"json"}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    response_json = safeGet(request_str)['message']['body']['artist_list']
#     print pretty(response_json)
#     artist_list = [scrubArtistList(artist) for artist in response_json]
#     return response_json[0]['artist']['artist_id']
    trimmed_artists = []
    for artist_item in response_json:
        item_name = artist_item['artist']['artist_name']
        if (re.search("feat", item_name) == None):
            trimmed_artists.append(artist_item)
    if len(response_json) != 0:
        return response_json[0]['artist']['artist_id']
    else: 
        return None
    
def getTrack(album_id):
    method = "album.tracks.get"
    params = {"apikey":keys.key, "album_id":str(album_id), "format":"json", "f_has_lyrics":"true"}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    response_json = safeGet(request_str)['message']['body']['track_list']
    track_list = [item['track']['track_name'] for item in response_json]
    return track_list

def getAlbum(id):
    method = "album.get"
    params = {"apikey":keys.key, "album_id":str(id), "format":"json"}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    logging.info(request_str)
    response_json = safeGet(request_str)['message']['body']['album']
    return response_json
    
def getLyrics(id):
    method = "track.lyrics.get"
    params = {"apikey":keys.key, "track_id":str(id), "format":"json"}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    response_json = safeGet(request_str)['message']['body']
    if (len(response_json) != 0):
        lyric_body = response_json['lyrics']['lyrics_body']
        if (len(lyric_body) != 0):
            return lyric_body
        
def searchTrack(artist, track):
    print "artist: " + artist
    print "track: " + track
    method = "track.search"
    params = {"apikey":keys.key, "format":"json", "s_track_rating": "desc", "q_track": track, "q_artist": artist, "format":"json",}
    request_str = keys.base_url + method + "?" + urllib.urlencode(params)
    print request_str
    response_json = safeGet(request_str)['message']['body']['track_list']
#     return response_json[0]['track']['track_id']
    track = response_json[0]['track']
#     html = urllib.urlopen("http://genius.com/The-weeknd-starboy-lyrics")
#     page = requests.get("http://genius.com/The-weeknd-starboy-lyrics")
#     page = urlfetch.fetch("http://genius.com/The-weeknd-starboy-lyrics")
#     soup = BeautifulSoup(page.content)
#     soup = soup.find("lyrics")
#     soup = soup.find_all("a")
#     for item in soup:
#         lines = item.contents
#         for x in lines:
#             logging.info(x) 
    return track

def searchAlbum():
     artist_name = raw_input("Type in name of artist\n")
     artist_id = pretty(getArtistID(artist_name))
     album_list = getArtistAlbums(artist_id)
     sorted_names = sorted(album_list, key = lambda x: x)
     numbered_names = []
     counter = 1
     for name in sorted_names:
         new_name = "(%s) %s "%(counter, name)
         numbered_names.append(new_name)
         counter += 1
     print pretty(numbered_names)
     number  = raw_input("Please type in number of album from the list above\n")
     number = int(number) - 1
     album_name = sorted_names[number]
     id = album_list[sorted_names[number]]
     getTones(getTrack(id), artist_name, album_name)
     

def getTones(track_ids, artist_name, album_name):
    lyrics_list = []
    lyrics_list = [getLyrics(item) for item in track_ids]
    tone_list = [tone.getTone(item) for item in lyrics_list]
    results = {}
    for item in tone_list:
        if item != None:
            tones = item['document_tone']['tone_categories'][0]['tones']
            for item in tones:
                emotion = item['tone_name']
                score = item['score']
                if emotion not in results:
                    results[emotion] = float(score)
                else:
                    results[emotion] = float(results[emotion]) + float(score)
    return results


#main
class SongList(webapp2.RequestHandler):
    def get(self):
        req = self.request
        url = req.url
        album_id = url[-8:]
        album = lyrics.getAlbum(album_id)
        artist_name = album['artist_name']
        album_name = album['album_name']
        track_list = lyrics.getTrack(album_id)
        template = JINJA_ENVIRONMENT.get_template("song_list_output.html")
        vals = {}
        vals['tracks'] = track_list
        vals['album_name'] = album_name
        vals['artist_name'] = artist_name
        self.response.write(template.render(vals))
        
class SongInfo(webapp2.RequestHandler):
    def post(self):
        req = self.request
        song = req.get("song")
        song_split = song.split("|")
        track = genius.search(song_split[0], song_split[1])
        logging.info("GETTING TONES")
        tones = tone.getTone(track)
        results = {}
        for item in tones:
            emotion = item['tone_name']
            score = item['score']
            if emotion not in results:
                results[emotion] = float(score)
            else:
                results[emotion] = float(results[emotion]) + float(score)
        template = JINJA_ENVIRONMENT.get_template("tone_output.html")
        vals = {}
        vals['emotions'] = []
        vals['song'] = song_split
        vals['numbers'] = []
        for item in results:
            vals['emotions'].append(item) 
            vals['numbers'].append(results[item])
        self.response.write(template.render(vals))