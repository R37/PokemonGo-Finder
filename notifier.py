import json
import tweepy
from pushbullet import Pushbullet
from geopy.geocoders import Nominatim
from datetime import datetime

pushbullet_client = None
wanted_pokemon = None

auth = tweepy.OAuthHandler("consumer key here", "consumer secret key here")
auth.set_access_token("access key here", "access secure key here")

api = tweepy.API(auth)

# Initialize object
def init():
    global pushbullet_client, wanted_pokemon
    # load pushbullet key
    with open('config.json') as data_file:
        data = json.load(data_file)
        # get list of pokemon to send notifications for
        wanted_pokemon = _str( data["notify"] ) . split(",")
        # transform to lowercase
        wanted_pokemon = [a.lower() for a in wanted_pokemon]
        # get api key
        api_key = _str( data["pushbullet"] )
        if api_key:
            pushbullet_client = Pushbullet(api_key)


# Safely parse incoming strings to unicode
def _str(s):
  return s.encode('utf-8').strip()

# Notify user for discovered Pokemon
def pokemon_found(pokemon):
    # get name
    pokename = _str(pokemon["name"]).lower()
    # check array
    if not pushbullet_client or not pokename in wanted_pokemon: return
    # notify
    print "[+] Notifier found pokemon:", pokename
    address = Nominatim().reverse(str(pokemon["lat"])+", "+str(pokemon["lng"])).address
    # Locate pokemon on GMAPS
    gMaps = "http://maps.google.com/maps?q=" + str(pokemon["lat"]) + "," + str(pokemon["lng"]) + "&24z"
    notification_text = "Pokemon Finder found " + _str(pokemon["name"]) + "!"
    disappear_time = str(datetime.fromtimestamp(pokemon["disappear_time"]).strftime("%I:%M%p").lstrip('0'))+")"
    location_text = _str(pokemon["name"]) + " Found at " + gMaps + " available until " + disappear_time + "."
    push = pushbullet_client.push_link(notification_text, location_text)
    api.update_status(location_text)




init()
