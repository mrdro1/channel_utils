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

# CONSOLE LOG
cfromat = "[{0}] {1}{2}"
def print_message(message, level=0):
    level_indent = " " * level
    print(cfromat.format(datetime.now(), level_indent, message))
#

class Instagram:
    """ Class for collect photo from instagram """

    def __init__(self, login, password):
        self.Source = "Instagram"
        self.API = Client(login, password)


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
                print_message(traceback.format_exc())
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
                print_message(traceback.format_exc())
        db_utils.commit()
        return count_of_loaded_photo

    def get_followings_accounts(self):
        """ Get followings accounts from current user """
        return self.API.user_following(self.API.authenticated_user_id).get('users')


    def load_all_following_photo(self):
        """ Download all photo from each following account """
        for account in self.get_followings_accounts():
            self.get_user_photo(account['pk'])
 

    def _save_photo(self, url, source_id, source_time):
        TRY_COUNTS = 3
        try_counter = TRY_COUNTS
        result = False
        while(try_counter > 0):
            try:
                if db_utils.check_exists(source_id, self.Source):
                    break
                filename = r".\{}\{}.jpg".format(self.Source, source_id)
                p = requests.get(url)
                if p.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(p.content)
                        result = True
                        break
            except:
                print_message(traceback.format_exc())
            try_counter -= 1
        return result


#def main():
#    start_time = datetime.now()
#    login, password = utils.read_login_pwd()
#    insta = Instagram(login, password)
#    insta.load_all_following_photo()
#    end_time = datetime.now()
#    print_message("Run began on {0}".format(start_time))
#    print_message("Run ended on {0}".format(end_time))
#    print_message("Elapsed time was: {0}".format(end_time - start_time))

#if __name__ == "__main__":
#    main()
