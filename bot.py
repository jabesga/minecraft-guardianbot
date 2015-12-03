#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sqlite3 as lite
import signal
import sys
import ConfigParser

class Bot(object):
    
    token = None
    my_username = None
    update_id = None
        
    def __init__(self, token):
        print 'Bot initialized!'
        self.token = str(token)
        response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'getMe')).json()
        self.my_username = response['result']['username']
        
    def sendMessage(self, chat_id, text):
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'sendMessage'), data={'chat_id': chat_id, 'text': text}).json()

    def checkUpdates(self):
            response = requests.post(
                url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'getUpdates'), data={'offset': self.update_id}).json()
            
            if response['ok'] == True:
                if response['result']:
                    if self.update_id == None:
                        self.update_id = response['result'][0]['update_id']
                        print 'Update_id updated! (%s)' % str(self.update_id)
                    
                    if response['result'][0]['update_id'] == self.update_id:
                        message = response['result'][0]['message']
                        self.update_id += 1
                        print message
                        return message
            else:
                print 'Unsuccessful request. Error code: %s. %s' % (response['error_code'], response['description'])        
                
    

    def run(self):
        while True:
            message = self.checkUpdates()

            if message:
                if 'text' in message:
                    if message['text'] in ['/vigilar', '/vigilar@MinecraftGuardianBot']:
                        if 'username' in message['from']:
                            USERNAME = message['from']['username']
                            USER_ID = message['from']['id']
                            con = lite.connect('data.db')
                            with con:
                                cur = con.cursor()    
                                cur.execute("SELECT * FROM Users WHERE username=?", (USERNAME,))
                                user_data = cur.fetchone()
                                if user_data == None:
                                    cur.execute("INSERT INTO Users VALUES(?,?)", (USERNAME, USER_ID))
                                    print "Usuario aniadido (%s, %s)" % (USERNAME, USER_ID)
                                    self.sendMessage(message['from']['id'], 'Vigilancia activada! Ahora vigilare tus construcciones.')
                                else:
                                    self.sendMessage(message['from']['id'], 'Ya estás en mi lista de vigilancia!')
                        else:
                            self.sendMessage(message['chat']['id'], 'Necesitas tener un nombre de usuario de Telegram para suscribirme a las alertas')

  
def signal_handler(signal, frame):
    print('Bot stopped. Ctrl+C pressed!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

config = ConfigParser.RawConfigParser()
config.read('settings.ini')
token = config.get('Bot', 'token')

b = Bot(token)
b.run()
