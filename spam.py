import random
import time

import vk

import utils

token = utils.read_token('vk')
session = vk.AuthSession(access_token=token)
API = vk.API(session)
IDS = ['-35807284']

# TODO в комменты фотки
def send_comment_to_video(msg, ids, count=20):
    for id in ids:
        # TODO переделай count
        try:
            t = random.randint(1)
            time.sleep()
            videos_info = API.video.get(owner_id=id, count=count)[1:]
        except:
            print('нет доступа к видео {}'.format(id))
            continue
        for i, video in enumerate(videos_info):
            try:
                API.video.createComment(owner_id=id, video_id=video['vid'], message=msg)
                print('послал коммент')
            except:
                print('для группы {} комменты на стене заблокированы'.format(id))
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

def send_comment_to_wall_post(msg, ids, count=20):
    for id in ids:
        try:
            posts_info = API.wall.get(owner_id=id, count=count)[1:]
        except:
            print('нет доступа к постам {}'.format(id))
            continue
        for i, post in enumerate(posts_info):
            try:
                API.wall.createComment(owner_id=id, post_id=post['id'], message=msg)
                print('послал коммент на стену')
            except:
                print('для группы {} комменты на стене заблокированы'.format(id))
            if i == count:
                break
        return 0

def send_post_on_wall(msg, id):
    try:
        API.wall.post(owner_id=id, message=msg)
        print('постнул на стену {}'.format(id))
    except:
        print('не постнул на стену((( {}'.format(id))
    return 0


def send_comment_to_photo(msg, ids, count=20, limit_al=2):
    for id in ids:
        try:
            albums = API.photos.getAlbums(owner_id=id)
            if not albums:
                print('Для Группы {0} нет фото'.format(id))
                return False
        except Exception as e:
            print(e)
            print('Для Группы {0} недоступны фото'.format(id))
            return False

        print('Всего альбомов {}'.format(len(albums)))
        for i_alb, album in enumerate(albums):
            if i_alb == limit_al:
                break
            print('Текущий альбом {}'.format(i_alb))
            photos = API.photos.get(owner_id=id, count=count, album_id=album['aid'])  #  Получаем список фото

            for photo in photos:
                photo_id = photo['pid']  #  Получаем адрес изображения
                try:
                    API.photos.createComment(owner_id=id, photo_id=photo_id, message=msg)
                    print('добавил коммент под фотку')
                except:
                    print("не смог закоментить фото в группе {}".format(id))
    return 0


def get_gid_for_query(q):
    groups = API.groups.search(q=q, count=1000)
    print(len(groups))
    gid = ['-' + str(g['gid']) for g in groups[1:]]
    return gid

ids = get_gid_for_query(q='эротика')

msg = 'Лайк за дружбу'

send_comment_to_photo(msg, ids, count=100)
send_comment_to_video(msg, ids, count=100)
send_comment_to_wall_post(msg, ids, count=100)
for id in ids:
    send_post_on_wall(msg, id)
