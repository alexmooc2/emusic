import ibm_key
import urllib, urllib2, json
from watson_developer_cloud import ToneAnalyzerV3


def getTone(input):
    print "Working..."
    if (input != None):
        tone_analyzer = ToneAnalyzerV3(
            username = ibm_key.username,
            password = ibm_key.password,
            version='2016-05-19 '
            )
        return tone_analyzer.tone(text=input.lyric)['document_tone']['tone_categories'][0]['tones']
    return None
# print json.dumps(getTone("A word is dead when it is said, some say. Emily Dickinson"),  indent=2)