# -*- coding: utf-8 -*-
import collections
from datetime import datetime
import argparse
import json
import time
#
#
import utils
import db_utils
import post
import spam
import collect

PARAMS = {}
# COMMAND:
# 1. post
#   timeout - post interval (sec.)
#   count - count photo
# 2. spam
#   count - count posts
#   text - text of comment
#   ids - ids from accounts (groups) 
#   query - search query
# 3. collect
#   source - resource from collect photo
#   count - count photo
#   mode - Mode of collect
#          For example: source - istagramm,
#                       mode - (all|feed_timeline|from_id)
#   content_type - (video|photo)
#   [id] - for instagram account id from download photo
# 4. friends
CONTROL_KEYS = [
    "command",
    "count",
    "source",
    "timeout",
    "mode",
    "id",
    "ids",
    "query",
    "text",
    "content_type"
    ]

CONTROL_DEFAULT_VALUES = collections.defaultdict(lambda: str())
CONTROL_DEFAULT_VALUES = \
    {
        "command" : None,
        "timeout" : 2,
        "count" : 2
    }


def parser_init():
    # Command line parser
    _parser = argparse.ArgumentParser()
    requiredNamed = _parser.add_argument_group('Required arguments')
    requiredNamed.add_argument("-c", "--control", action="store", dest="CONTROL_FILE_NAME", help="Control file", type=str, required=True)
    try:
        with open(_parser.parse_args().CONTROL_FILE_NAME, "r", encoding='UTF-8') as data_file:
            PARAMS.update(json.load(data_file))
        for key in PARAMS.keys():
            if not key in CONTROL_KEYS:
                raise Exception("Unknown parameter: {0}".format(key))
        # check all params, if null then set default
        for key in CONTROL_DEFAULT_VALUES.keys():
            PARAMS.setdefault(key, CONTROL_DEFAULT_VALUES[key]) 
    except Exception as error:
        utils.print_message("Invalid file control. Check the syntax.")
        utils.print_message(error.args[0])
        exit()
    utils.print_message("Parameters:")
    for key in PARAMS.keys():
        param_str = "  {0} = '{1}'".format(key, PARAMS[key])
        utils.print_message(param_str)
    _SUCCESSFUL_START_FLAG = True

def main():
    if PARAMS['command'] is None:
        utils.print_message("Error: Empty command. Exit.")
        return
    #utils.print_message("Command: '{}'".format(PARAMS['command']))
    if PARAMS['command'].lower() == "post":
        chat_id='-1001189643268'
        utils.print_message("Processing...", 2)
        for i, id in enumerate(db_utils.get_not_used_photo()):
            post.send_to_channel(id)
            utils.print_message('I post new photo', 3)
            time.sleep(PARAMS['timeout'])
            if i == PARAMS['count']:
                break
    elif PARAMS['command'].lower() == "spam":
        ids = []
        if "query" in PARAMS:
            ids.extend(spam.get_gid_for_query(q=PARAMS["query"])[:10])
        if "ids" in PARAMS:
            ids.extend(PARAMS["ids"])
        msg = PARAMS["text"]
        #spam.send_comment_to_photo(msg, ids, count=PARAMS["count"])
        #spam.send_comment_to_video(msg, ids, count=PARAMS["count"])
        spam.send_comment_to_wall_post(msg, ids, count=PARAMS["count"])
        for id in ids:
            spam.send_post_on_wall(msg, id)
        utils.print_message('успешных постов = {}'.format(spam.SUCCESS_POST), 2)
    elif PARAMS['command'].lower() == "collect":
        if PARAMS['source'].lower() == "instagram":
            login, password = utils.read_login_pwd()
            insta = collect.Instagram(login, password)
            utils.print_message("Processing...", 2)
            if PARAMS['mode'].lower() == "all":
                count = insta.load_all_following_photo()
            elif PARAMS['mode'].lower() == "feed_timeline":
                count = insta.get_timeline(PARAMS['count'])
            elif PARAMS['mode'].lower() == "from_id":
                if PARAMS['content_type'].lower() == "video":
                    count = insta.get_user_video(PARAMS['id'])
                elif PARAMS['content_type'].lower() == "photo":
                    count = insta.get_user_photo(PARAMS['id'])
            utils.print_message("Download photo: {}".format(count), 2)
    elif PARAMS['command'].lower() == "friends":
        utils.print_message("Processing...", 2)
        #while(True):
        spam.like_to_friend()
        time.sleep(60 * 1)
        spam.kill_badman()
        time.sleep(60 * 1)
    utils.print_message("End processing", 2)


if __name__ == '__main__':
    start_time = datetime.now()
    parser_init()
    main() 
    end_time = datetime.now()
    utils.print_message("Run began on {0}".format(start_time))
    utils.print_message("Run ended on {0}".format(end_time))
    utils.print_message("Elapsed time was: {0}".format(end_time - start_time))