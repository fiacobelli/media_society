import urllib2
import base64
import json
import sys
from pprint import pprint

CONSUMER_KEY = b'6XNYfvFaYys0ty3Bg7vg'
CONSUMER_SECRET = b'BSYKDMUj9XrYRlYZ25TAtkOwLY54skbND6ItHFRVG5M'

#
# Step 1: Encode consumer key and secret
#

base64_consumer_key_secret = base64.b64encode(urllib2.quote(CONSUMER_KEY) + b':' + urllib2.quote(CONSUMER_SECRET))

#
# Step 2: Obtain a bearer token
#

# note: the following line won't verify server certificate; to do so you'll have to
#       use python3 and specify cafile & capauth
#request = urllib2.Request("https://api.twitter.com/oauth2/token")
#request.add_header('Authorization', b'Basic ' + base64_consumer_key_secret)
#request.add_header("Content-Type", b'application/x-www-form-urlencoded;charset=UTF-8')
#request.add_data(b'grant_type=client_credentials')

#resp = urllib2.urlopen(request)
#data = json.load(resp)
#if data['token_type'] != 'bearer':
#    throw("Bad token_type: " + data['token_type'])
#access_token = data['access_token']
access_token = "AAAAAAAAAAAAAAAAAAAAAJuFTAAAAAAA3nIjLnjxjYNYr5RCVhdaUYy4hXA%3DAmwn37LankzEFzpIErizOl6oNk6Azyc2sc3CSHy6kM"
#print("access_token: " + access_token)
#print("AAAAAAAAAAAAAAAAAAAAAJuFTAAAAAAA3nIjLnjxjYNYr5RCVhdaUYy4hXA%3DAmwn37LankzEFzpIErizOl6oNk6Azyc2sc3CSHy6kM")
#print('')

# Auxiliary functions
def shortTweet(status):
    ''' Here, status is a full json object from twitter
    '''
    st = {}
    st["created_at"]=status["created_at"]
    st["lang"]=status["lang"]
    st["retweet_count"]=status["retweet_count"]
    st["text"]=status["text"]
    st["screen_name"]=status["user"]["screen_name"]
    return st


def searchGeo(longitude,latitude,radius,limit=15):
    ll=",".join([longitude,latitude,radius])
    param="geocode=%s&count=%d"%(ll,limit)
    search_url_geo="https://api.twitter.com/1.1/search/tweets.json?%s"
    return _query(search_url_geo,param)


def searchPlace(place_id,limit=15):
    par = "q=place%3A"+place_id+"&count=%s"%str(limit)
    search_url ="https://api.twitter.com/1.1/search/tweets.json?%s"
    return _query(search_url,par)


def trendingGeo(ywoe_id,limit=15):
    param="id=%s"%ywoe_id
    trends_url = "https://api.twitter.com/1.1/trends/place.json?%s"
    return _query(trends_url,param)
    

def search(query):
    url = "https://api.twitter.com/1.1/search/tweets.json?%s"
    param = "q=%s&count=%d"%(query,limit)
    return _query(url,param)


def _query(url,param):
    request = urllib2.Request(
        url%param
    )
    #
    # Step 3: Authenticate API requests with the bearer token
    #
    request.add_header('Authorization', b'Bearer ' + access_token)
    resp = urllib2.urlopen(request)
    data = json.load(resp)
    return data
    

if __name__=="__main__":
    prog,completos,cortos,trends = sys.argv
    # Note on geolocation: Check: https://scholar.google.com/scholar?oe=utf-8&um=1&ie=UTF-8&lr&cites=17986691942471982298
    # and http://betanews.com/2012/07/31/twitter-500-million-accounts-billions-of-tweets-and-less-than-one-percent-use-their-location/
    # and http://dfreelon.org/2013/05/12/twitter-geolocation-and-its-limitations/

    # search
    longlat_arica="-70.298767,-18.482214,10mi"
    longlat_iquique="-70.117493,-20.249314,60mi"
    longlat_anotfa="-70.399017,-23.691062,200mi"
    longlat_copiapo="-70.320740,-27.393717,120mi"
    longlat_serena="-71.253204,-29.941845,60mi"
    longlat_illapel="-71.133728,-31.641691,40mi"
    longlat_stgo="-70.666122,-33.458370,50mi"
    longlat_valpo="-71.589661,-33.070829,50mi"
    longlat_ranc="-70.716248,-34.200445,60mi"
    longlat_talca="-71.644592,-35.453958,60mi"
    longlat_conce="-73.009644,-36.857648,100mi"
    longlat_temuco="-72.432861,-38.848264,120mi"
    longlat_valdivia="-73.185425,-39.854938,60mi"
    longlat_osorno="-73.004150,-40.605612,60mi"
    longlat_ptomontt="-73.267822,-41.795888,60mi"
    longlat_coyhaique="-72.301025,-45.790509,60mi"
    longlat_ptarenas="-70.900269,-53.202742,60mi"

    # parameters for querying
    q="michellebachellet"
    ywoeid="23424782"
    place="Chile"
    place_id_cl="47a3cf27863714de" #chile
    q_place_id = "place%3A"+place_id_cl
    chile_bounding_box = "-109.4791708,-56.5573577,-66.15203,-17.497384"


    streaming_search ="https://stream.twitter.com/1.1/statuses/filter.json?locations=%s"%chile_bounding_box

    data = searchPlace(place_id_cl,100)
    open(completos,"a").write("BEGIN-T-RESULT"+str(data))
    with open(cortos,"a") as f:
        for s in data["statuses"]:
            f.write(str(shortTweet(s)))
            
    open(trends,"a").write("BEGIN-TRENDS-QUERY"+str(trendingGeo(ywoeid)))
