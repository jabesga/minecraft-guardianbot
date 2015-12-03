import web
import requests
import sqlite3 as lite
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('settings.ini')
BOT_TOKEN = config.get('Bot', 'token')

def sendMessage(chat_id, text):
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(BOT_TOKEN, 'sendMessage'), data={'chat_id': chat_id, 'text': text}).json()

class index:
    def POST(self):
        data = web.input()

        con = lite.connect('data.db')
        with con:
            cur = con.cursor()    
            cur.execute("SELECT * FROM Users WHERE username=?", (data.username,))
            user_data = cur.fetchone()
            if user_data:
                if data.north != '0':
                    sendMessage(user_data[1], "Se ha detectado un intruso por la entrada norte")
                if data.east != '0':
                    sendMessage(user_data[1], "Se ha detectado un intruso por la entrada este")
                if data.west != '0':
                    sendMessage(user_data[1], "Se ha detectado un intruso por la entrada oeste")
                if data.south != '0':
                    sendMessage(user_data[1], "Se ha detectado un intruso por la entrada sur")
            else:
                print "There's not user in DB"

urls = (
  '/', 'index'
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

# REQUESTS SAMPLE
# requests.post("http://localhost:8080", data={'username': "USERNAME", 'north': 0, 'east': 0, 'west': 0, 'south': 0})