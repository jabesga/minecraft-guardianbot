#!/usr/bin/env python

"""Server that manages the HTTP requests sent with the computers made with the Minecraft OpenComputers Mod"""

import web
import requests
import sqlite3 as lite
import ConfigParser

__author__ = "Jon Ander Besga"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jon Ander Besga"
__email__ = "jonan.bsg@gmail.com"

# Get BOT_TOKEN from the settings.ini file
config = ConfigParser.RawConfigParser()
config.read('settings.ini')
BOT_TOKEN = config.get('Bot', 'token')

def sendMessage(chat_id, text):
    """Bot sends a message to provided chat_id with the provided text"""

    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(BOT_TOKEN, 'sendMessage'),
        data={'chat_id': chat_id, 'text': text}
    ).json()


class index:
    def POST(self):
        """
        REQUESTS SAMPLE: requests.post("http://localhost:8080", data={'username': "USERNAME", 'north': 0, 'east': 0, 'west': 0, 'south': 0})
        Data has the followings parameters: username, north, east, west, south.
        """

        data = web.input() 

        con = lite.connect('data.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Users WHERE username=?", (data.username,))
            user_exists = cur.fetchone() # Get user data if exists
            username_id = user_exists[1] # Get username id

            if user_exists:
                if data.north != '0':
                    sendMessage(username_id, config.get('Messages', 'north'))
                if data.east != '0':
                    sendMessage(username_id, config.get('Messages', 'east'))
                if data.west != '0':
                    sendMessage(username_id, config.get('Messages', 'west'))
                if data.south != '0':
                    sendMessage(username_id, config.get('Messages', 'south'))
            else:
                print "This user is not in the DB"

urls = (
  '/', 'index'
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()