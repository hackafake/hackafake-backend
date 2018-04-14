import sys
import time
import telepot
from telepot.loop import MessageLoop
import requests
import re

from config import TOKEN
"""
$ python2.7 skeleton.py <token>
A skeleton for your telepot programs.
"""

def handle(msg):
    flavor = telepot.flavor(msg)

    content_type, chat_type, chat_id = telepot.glance(msg)
    summary = telepot.glance(msg, flavor=flavor)

    if content_type == 'text':
        urls =re.findall('https?:\/\/[^\s]+', msg['text'])
        if len(urls) > 0:
            for url in urls:
                r = requests.get('https://api.fakenewsdetector.org/votes?url={}&title='.format(url))
                for data in r.json()['content']['robot']:
                    if data['category_id'] == 2 and data['chance'] > 0.5:
                        bot.sendMessage(chat_id, 'Attenzione: %s e\' una fake news!\nprobabilita\': %s'%(url, data['chance']))
                        requests.post("http://52.212.172.20:8080/fakenews", json={
                            'url': url,
                            'user': ''
                        })
            print(urls)



    print (flavor, summary)



bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
