import os
import random
import time

import telegram

import db_utils
import utils

TOKEN = utils.read_token('tlg')
BOT = telegram.Bot(token=TOKEN)

tags = [
        '#sexy', '#body', '#beautiful', '#girl', '#girls', 
        '#perfect', '#supergirls', '#model', '#beauty', '#glamour',
        '#lingerie', '#sensual', '#fitnessmodel', '#bestgirl', 
        '#sport', '#fitnessgirl', '#hot', '#hotgirl', '#beautifulbody',
        '#FitnessCure', '#Fitlife', '#Gethealthy', '#Healthylife',
        '#Delhi', '#SlimmingWorld', '#HealthBenefits', '#Results',
        '#Magic', '#Workout', '#Reviews', '#fitbody', '#Shape',
        '#InspirationalQuotes', '#Throwback', '#Nature', '#BestoftheDay',
        '#gorgeous', '#beautiful', '#fitchick', '#bikinibody',
        '#bikinimodel', '#fitnessmodel', '#bikinigoddess', '#sexy',
        '#abs', '#sexyabs', '#abgoals', '#abcheck', '#fitnessgirl',
        '#model', '#swimsuitmodel', '#dreamgirl', '#goddess', '#skinny',
        '#sexystomach', '#fitnessmotivation', '#beachbabe', '#bodygoals',
        '#perfectbody', '#bikini', '#bikinibody', '#bikiniphoto', '#Baler'
       ]
       
def send_to_channel(photo_id, chat_id='-1001189643268'):
    fn = db_utils.get_fn(photo_id)
    try:
        with open(fn, 'rb') as f:
            caption = ' '.join(random.sample(tags, 2))
            BOT.send_photo(chat_id=chat_id, photo=f, caption=caption)
        db_utils.set_used(photo_id)
        db_utils.commit()
    except:
        utils.print_message('Cannot send file')
        return False
    return True


# 510929420