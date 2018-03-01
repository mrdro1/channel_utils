import os
import random

from twython import Twython

import post
import utils

APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET = utils.read_token_twitter()
TWITTER = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def send_post(fn, msg, hash_tags=post.tags):
    photo = open(fn, 'rb')
    response = TWITTER.upload_media(media=photo)
    TWITTER.update_status(status=msg + ' ' + ' '.join(hash_tags), media_ids=[response['media_id']])

def chose_random_fn(dir='Instagram'):
    fns = os.listdir(dir)
    fn = random.choice(fns)
    fn = dir + '//' + fn
    return fn

fn = chose_random_fn()
send_post(fn, 'Very pretty girl!!!')
