# -*- coding: utf-8 -*-
import traceback
from datetime import datetime
import time
#
#pip install git+https://git@github.com/ping/instagram_private_api.git@1.4.0
from instagram_private_api import Client, ClientCompatPatch
#


# CONSOLE LOG
cfromat = "[{0}] {1}{2}"
def print_message(message, level=0):
    level_indent = " " * level
    print(cfromat.format(datetime.now(), level_indent, message))
#

class Instagram:
    """ Class for collect photo from instagram """

    def __init__(self, login, password):
        self.API = Client(login, password)


    def get_user_photo(self, user_id):
        """
        Get all user photo

        :param
            - user_id: Account id in instagram
        """
        result = []
        _first = True
        next_max_id = None
        while next_max_id or _first:
            try:
                _first = False
                results = self.API.user_feed(user_id=user_id, max_id=next_max_id)
                result.extend([item for item in results.get('items', []) if item.get('image_versions2').get('candidates')])
                next_max_id = results.get('next_max_id')
            except:
                print_message(traceback.format_exc())
        return result


    def get_timeline(self, K):
        """
        Get K photo from feed timeline

        :param
            - K: Count of post in timeline
        """
        result = []
        _first = True
        next_max_id = None
        while next_max_id or _first:
            try:
                _first = False
                results = self.API.feed_timeline(max_id=next_max_id)
                result.extend([item for item in results.get('feed_items', []) if item.get('media_or_ad')])
                next_max_id = results.get('next_max_id')
                if len(result) >= K: break
            except:
                print_message(traceback.format_exc())
        return result[:K]

    def get_followings_accounts(self):
        """
        Get followings accounts from current user

        """
        return self.API.user_following(self.API.authenticated_user_id).get('users')


    def _save_photo():
        pass
        print_message("Save photos...")
        for i, item in enumerate(items):
            try:
                print_message("Process photo #{} (total {})".format(i, len(items)), 1)
                ClientCompatPatch.media(item['media_or_ad'])
                filename = "{}_{}.jpg".format(item['media_or_ad']['id'], item['media_or_ad']['created_time'])
                if os.path.exists("{}{}".format(PATH, filename)): 
                    print_message("Photo {} already exists, skip".format(filename), 2)
                    continue
                print_message("Get photo by url {}".format(item['media_or_ad']['images']['standard_resolution']['url']), 2)
                p = requests.get(item['media_or_ad']['images']['standard_resolution']['url'])
                if p.status_code == 200:
                    print_message("Save photo {}".format(filename), 2)
                    with open(r"D:\girls\{}".format(filename), "wb") as f:
                        f.write(p.content)
            except:
                print_message(traceback.format_exc())

def main():
    start_time = datetime.now()
    login = "opora2017"
    password = "girls_scrapper"
    insta = Instagram(login, password)
    print_message(len(insta.get_timeline(1000)))
    print_message(len(insta.get_followings_accounts()))
    print_message(len(insta.get_user_photo(r[0]['pk'])))
    end_time = datetime.now()
    print_message("Run began on {0}".format(start_time))
    print_message("Run ended on {0}".format(end_time))
    print_message("Elapsed time was: {0}".format(end_time - start_time))

if __name__ == "__main__":
    main()