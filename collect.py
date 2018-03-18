# -*- coding: utf-8 -*-
import traceback
from datetime import datetime
import time
import requests
#
# pip install git+https://git@github.com/ping/instagram_private_api.git@1.4.0
from instagram_private_api import Client, ClientCompatPatch
#
import db_utils
import utils

class Instagram:
    """ Class for collect photo from instagram """

    def __init__(self, login, password):
        self.Source = "Instagram"
        self.API = Client(login, password)

    def get_user_video(self, user_id):
        _first = True
        count_of_loaded_photo = 0
        next_max_id = None
        while next_max_id or _first:
            try:
                _first = False
                results = self.API.user_feed(user_id=user_id, max_id=next_max_id)
                for item in results.get('items', []):
                    try:
                        id = item["id"]
                        date = item["caption"]["created_at"]
                        photo_url = item['video_versions'][0]['url']
                        print('I find video))')
                    except:
                        continue
                    if self._save_photo(photo_url, id, date, extension='mp4'):
                        print('I load video))')
                        db_utils.insert_photo({"source_id": id, "source": self.Source, "date": date})
                        count_of_loaded_photo += 1
                        if count_of_loaded_photo % db_utils.COMMIT_COUNT == 0:
                            db_utils.commit()
                next_max_id = results.get('next_max_id')
            except:
                utils.print_message(traceback.format_exc())
        db_utils.commit()
        return count_of_loaded_photo



    def get_user_photo(self, user_id):
        """
        Get all user photo

        :param
            - user_id: Account id in instagram
        """
        _first = True
        count_of_loaded_photo = 0
        next_max_id = None
        while next_max_id or _first:
            try:
                _first = False
                results = self.API.user_feed(user_id=user_id, max_id=next_max_id)
                for item in results.get('items', []):
                    try:
                        id = item["id"]
                        date = item["caption"]["created_at"]
                        photo_url = item["image_versions2"]["candidates"][0]["url"]
                    except:
                            continue
                    if self._save_photo(photo_url, id, date):
                        db_utils.insert_photo({"source_id" : id, "source" : self.Source, "date" : date})
                        count_of_loaded_photo += 1
                        if count_of_loaded_photo % db_utils.COMMIT_COUNT == 0:
                            db_utils.commit()
                next_max_id = results.get('next_max_id')
            except:
                utils.print_message(traceback.format_exc())
        db_utils.commit()
        return count_of_loaded_photo


    def get_timeline(self, K):
        """
        Get K photo from feed timeline

        :param
            - K: Count of post in timeline
        """
        result = []
        _first = True
        count_of_loaded_photo = 0
        next_max_id = None
        counter = K
        while (next_max_id or _first) and counter > 0:
            try:
                _first = False
                results = self.API.feed_timeline(max_id=next_max_id)
                for item in results.get('feed_items', []):
                    try:
                        id = item["media_or_ad"]["id"]
                        date = item["media_or_ad"]["caption"]["created_at"]
                        photo_url = item["media_or_ad"]["image_versions2"]["candidates"][0]["url"]
                    except:
                        continue
                    if counter <= 0: return
                    counter -= 1
                    if self._save_photo(photo_url, id, date):
                        db_utils.insert_photo({"source_id" : id, "source" : self.Source, "date" : date})
                        count_of_loaded_photo += 1
                        if count_of_loaded_photo % db_utils.COMMIT_COUNT == 0:
                            db_utils.commit()
                next_max_id = results.get('next_max_id')
            except:
                utils.print_message(traceback.format_exc())
        db_utils.commit()
        return count_of_loaded_photo

    def get_followings_accounts(self):
        """ Get followings accounts from current user """
        return self.API.user_following(self.API.authenticated_user_id).get('users')


    def load_all_following_photo(self):
        """ Download all photo from each following account """
        count_of_loaded_photo = 0
        for account in self.get_followings_accounts():
            count_of_loaded_photo += self.get_user_photo(account['pk'])
        return count_of_loaded_photo
 

    def _save_photo(self, url, source_id, source_time, extension='jpg'):
        TRY_COUNTS = 3
        try_counter = TRY_COUNTS
        result = False
        while(try_counter > 0):
            try:
                if db_utils.check_exists(source_id, self.Source):
                    break
                filename = r".\{}\{}.{}".format(self.Source, source_id, extension)
                p = requests.get(url)
                if p.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(p.content)
                        result = True
                        break
            except:
                utils.print_message(traceback.format_exc())
            try_counter -= 1
        return result