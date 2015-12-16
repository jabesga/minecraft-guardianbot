#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Telegram bot"""

import requests
import sqlite3 as lite
import signal
import sys
import ConfigParser
import os

__author__ = "Jon Ander Besga"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jon Ander Besga"
__email__ = "jonan.bsg@gmail.com"


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
        """Bot sends a message to provided chat_id with the provided text"""

        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'sendMessage'),
            data={'chat_id': chat_id, 'text': text}
        ).json()

    def checkUpdates(self):
        """Check new messages received by the bot"""

        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'getUpdates'),
            data={'offset': self.update_id}
        ).json()
        
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
                            USERNAME_ID = message['from']['id']

                            con = lite.connect('data.db')
                            with con:
                                cur = con.cursor()    
                                cur.execute("SELECT * FROM Users WHERE username=?", (USERNAME,))
                                user_data = cur.fetchone()
                                if user_data == None:
                                    cur.execute("INSERT INTO Users VALUES(?,?)", (USERNAME, USERNAME_ID))
                                    print "\tUsuario aniadido (%s, %s)" % (USERNAME, USERNAME_ID)
                                    self.sendMessage(message['from']['id'], 'Vigilancia activada! Ahora vigilare tus construcciones.')
                                else:
                                    self.sendMessage(message['from']['id'], 'Ya estas en mi lista de vigilancia!')
                        else:
                            self.sendMessage(message['chat']['id'], 'Necesitas tener un nombre de usuario de Telegram para suscribirte a las alertas')

  
def signal_handler(signal, frame):
    print('Bot stopped. Ctrl+C pressed!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Get BOT_TOKEN from the settings.ini file
config = ConfigParser.RawConfigParser()
config.read('settings.ini')
BOT_TOKEN = config.get('Bot', 'token')

b = Bot(BOT_TOKEN)
b.run()
