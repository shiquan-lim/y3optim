import StringIO
import json
import logging
import random
import urllib
import urllib2
import os

# from urllib.parse import urlparse
from time import gmtime, strftime
from datetime import datetime
from firebase import firebase

# for sending images
# from PIL import Image
# import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

# SQListBot Token
# TOKEN = '134200866:AAGSqcPJVNtMruJBGpFX-1PEGBwA6KYxfKs'
# Quantum Token
TOKEN = '279379002:AAGRWKf3V3mUtTt9Lg-t9OSSu7kp2mGdESE'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

def listToString(invitees):
    listString = ""
    for invitee in invitees:
        listString=listString+"\n"+invitee+" has been invited"
    return listString

def createEvent():
    db = firebase.FirebaseApplication('https://telegram-list-bot.firebaseio.com', None)
    db.put('/events', 'TESTEVENT', {'key1': 'value1'}, {'key2': 'value2'})

# ================================

#Variables for list functionality
invitees=[]
isEventCreated=False
eventName="Test Event"

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(30)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(30)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(30)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(30)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        text = text.lower()

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            # elif text == '/image':
            #     img = Image.new('RGB', (512, 512))
            #     base = random.randint(0, 16777216)
            #     pixels = [base+i*j for i in range(512) for j in range(512)]
            #     img.putdata(pixels)
            #     output = StringIO.StringIO()
            #     img.save(output, 'JPEG')
            #     reply(img=output.getvalue())
            elif text == '/version':
                reply('Version 3.0: Last updated 25.01.17')
            elif text == '/createevent':
                createEvent()
                reply('Event Created!')
            elif text == 'shiquan':
                reply('DAS ME!')
            elif '/generatelist' in text:
                reply('Please set the event name:'
                    +'\nType /rsvp to respond to this event.'
                    +'\nType /viewresponses to view current event status.'
                    +'\nType /destroylist to terminate the existing event.')
                isEventCreated=True
            elif '/rsvp' in text:
                if isEventCreated:
                    invitee = str(fr.get('first_name'))
                    invitees.append(invitee)
                    reply(invitee+' is going!')
                else:
                    reply('There is no active event to rsvp to!')
            elif '/viewresponses' in text:
                if isEventCreated:
                    reply(listToString(invitees))
                else:
                    reply('There is no active event to view!')
            elif '/destroylist' in text:
                if isEventCreated:
                    isEventCreated=False
                    reply(eventName+' terminated.')
                else:
                    reply("There is no existing event to terminate!")
            else:
                reply('What command?')

        elif 'who are you' in text:
            reply('I am QUANTUM, created by Master Shi Quan.')
        elif 'what time' in text:
            now = datetime.now()
            reply("It is "+str((now.hour+8)%24)+":"+str(now.minute))
        else:
            if getEnabled(chat_id):
                try:
                    resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                    back = resp1.get('res').get('msg')
                except urllib2.HTTPError, err:
                    logging.error(err)
                    back = str(err)
                if not back:
                    reply('okay...')
                elif 'I HAVE NO RESPONSE' in back:
                    reply('you said something with no meaning')
                else:
                    reply(back)
                # reply("No Meaning")
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
