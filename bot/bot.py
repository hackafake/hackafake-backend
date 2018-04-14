import sys
import time
import telepot
from telepot.loop import MessageLoop
import requests
import re

from config import TOKEN

def handle(msg):
    flavor = telepot.flavor(msg)

    content_type, chat_type, chat_id = telepot.glance(msg)
    summary = telepot.glance(msg, flavor=flavor)

    if content_type == 'text':
        urls =re.findall('https?:\/\/[^\s]+', msg['text'])
        if len(urls) > 0:
            for url in urls:
                res = requests.post("http://52.212.172.20:8080/fakenews", json={
                    'url': url,
                    'username': msg["from"].get('username') or (msg["from"].get("first_name") + ' ' + msg["from"].get("last_name"))
                })
                if res.json()['is_fake'] == True:
                    bot.sendMessage(chat_id, 'Attenzione: %s e\' una fake news!'%(url))

    print (flavor, summary)



bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
