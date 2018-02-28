import vk

import utils

token = utils.read_token()
session = vk.AuthSession(access_token=token)
API = vk.API(session)
IDS = ['-35807284']

# TODO в комменты фотки
def send_comment_to_video(msg, ids, count=20):
    for id in ids:
        # TODO переделай count
        videos_info = API.video.get(owner_id=id, count=4)[1:]
        for i, video in enumerate(videos_info):
            try:
                API.video.createComment(owner_id=id, video_id=video['vid'], message=msg)
                print('послал коммент')
            except:
                print('для группы {} комменты заблокированы'.format(id))
            if i == count:
                break
    return 0


def like_to_friend():
    """ Accept friend and set like to avatar """
    for user_id in API.friends.getRequests(need_viewed=1):
        try:
            photo_id = API.users.get(user_ids=user_id, fields="photo_id")[0].get("photo_id").split('_')[1]
            if API.likes.isLiked(type="photo", owner_id=user_id, item_id=photo_id) == 0:
                API.likes.add(type="photo", owner_id=user_id, item_id=photo_id)
            API.friends.add(user_id=user_id, follow=0)
            API.messages.send(user_id=user_id, message="Привет ;-)")
        except:
            print("Не удалось добавить {} в друзья.".format(bad_user_id))


def kill_badman():
    """ Kill badman whois del me from friends! """
    for bad_user_id in API.friends.getRequests(out=1, need_viewed=1):
        try:
            photo_id = API.users.get(user_ids=bad_user_id, fields="photo_id")[0].get("photo_id").split('_')[1]
            API.messages.send(user_id=bad_user_id, message="Пока, BADMAN!!! :-(")
            if API.likes.isLiked(type="photo", owner_id=bad_user_id, item_id=photo_id) == 1:
                API.likes.delete(type="photo", owner_id=bad_user_id, item_id=photo_id)
            API.friends.delete(user_id=bad_user_id)
        except:
            print("Не удалось исключить {} из друзей.".format(bad_user_id))