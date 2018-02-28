import os
import random
import time

import telegram

import db_utils
import utils

TOKEN = utils.read_token()
BOT = telegram.Bot(token=TOKEN)


def send_to_channel(photo_id, chat_id='-1001189643268'):
    fn = db_utils.get_fn(photo_id)
    try:
        with open(fn, 'rb') as f:
            BOT.send_photo(chat_id=chat_id, photo=f)
        db_utils.set_used(photo_id)
    except:
        print('Cannot send file')
        return False

    return True




chat_id='-1001189643268'
for id in db_utils.get_not_used_photo():
    send_to_channel(id)
    print('I post new photo')
    time.sleep(2)