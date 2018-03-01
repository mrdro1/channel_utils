import random
import time
import traceback

import vk

import utils
import telegram

TOKEN = utils.read_token('tlg')
BOT = telegram.Bot(token=TOKEN)

token = utils.read_token('vk')
session = vk.AuthSession(access_token=token)
API = vk.API(session)
IDS = ['-35807284']

SUCCESS_POST = 0

# TODO в комменты фотки
def send_comment_to_video(msg, ids, count=20):
    for id in ids:
        # TODO переделай count
        try:
            t = random.randint(10, 11)
            time.sleep(t)
            videos_info = API.video.get(owner_id=id, count=count)[1:]
        except:
            #print('нет доступа к видео {}'.format(id))
            continue
        for i, video in enumerate(videos_info):
            try:
                API.video.createComment(owner_id=id, video_id=video['vid'], message=msg)
                print('послал коммент')
                global SUCCESS_POST
                SUCCESS_POST += 1
            except:
                #print('для группы {} комменты на стене заблокированы'.format(id))
                pass
            if i == count:
                break
    return 0

def like_to_friend():
    """ Accept friend and set like to avatar """
    for user_id in API.friends.getRequests(need_viewed=1):
        try:
            photo_id = API.users.get(user_ids=user_id, fields="photo_id")[0].get("photo_id")
            if photo_id:
                photo_id = photo_id.split('_')[1]
                if API.likes.isLiked(type="photo", owner_id=user_id, item_id=photo_id) == 0:
                    API.likes.add(type="photo", owner_id=user_id, item_id=photo_id)
            API.friends.add(user_id=user_id, follow=0)
            API.messages.send(user_id=user_id, message="Привет ;-)")
            time.sleep(5)
        except:
            print("Не удалось добавить {} в друзья.".format(user_id))
            print(traceback.format_exc())

def kill_badman():
    """ Kill badman whois del me from friends! """
    for bad_user_id in API.friends.getRequests(out=1, need_viewed=1):
        try:
            user_info = API.users.get(user_ids=bad_user_id, fields="photo_id, can_write_private_message")[0]
            photo_id = user_info.get("photo_id")
            if photo_id:
                photo_id = photo_id.split('_')[1]
                if API.likes.isLiked(type="photo", owner_id=bad_user_id, item_id=photo_id) == 1:
                    API.likes.delete(type="photo", owner_id=bad_user_id, item_id=photo_id)
            if user_info.get("can_write_private_message") == 1:
                API.messages.send(user_id=bad_user_id, message="Пока, BADMAN!!! :-(")
            API.friends.delete(user_id=bad_user_id)
            time.sleep(5)
        except:
            print("Не удалось исключить {} из друзей.".format(bad_user_id))
            print(traceback.format_exc())
            
            
def send_comment_to_wall_post(msg, ids, count=20):
    for id in ids:
        try:
            t = random.randint(10, 11)
            time.sleep(t)
            posts_info = API.wall.get(owner_id=id, count=count)[1:]
        except:
            print(traceback.format_exc())
            #print('нет доступа к постам {}'.format(id))
            continue
        for i, post in enumerate(posts_info):
            try:
                API.wall.createComment(owner_id=id, post_id=post['id'], message=msg)
                print('послал коммент на стену')
                global SUCCESS_POST
                SUCCESS_POST += 1
            except:
                print(traceback.format_exc())
                #print('для группы {} комменты на стене заблокированы'.format(id))
            if i == count:
                break
        return 0

def send_post_on_wall(msg, id):
    try:
        API.wall.post(owner_id=id, message=msg)
        print('постнул на стену {}'.format(id))
        global SUCCESS_POST
        SUCCESS_POST += 1
    except:
        print(traceback.format_exc())
        #print('не постнул на стену((( {}'.format(id))
        pass
    return 0


def send_comment_to_photo(msg, ids, count=20, limit_al=2):
    for id in ids:
        try:
            t = random.randint(10, 11)
            time.sleep(t)
            albums = API.photos.getAlbums(owner_id=id)
            if not albums:
                #print('Для Группы {0} нет фото'.format(id))
                continue
        except Exception as e:
            #print(e)
            #print('Для Группы {0} недоступны фото'.format(id))
            continue

        #print('Всего альбомов {}'.format(len(albums)))
        for i_alb, album in enumerate(albums):
            if i_alb == limit_al:
                break
            #print('Текущий альбом {}'.format(i_alb))
            t = random.randint(10, 11)
            time.sleep(t)
            photos = API.photos.get(owner_id=id, count=count, album_id=album['aid'])  #  Получаем список фото

            for photo in photos:
                photo_id = photo['pid']  #  Получаем адрес изображения
                try:
                    API.photos.createComment(owner_id=id, photo_id=photo_id, message=msg)
                    print('добавил коммент под фотку')
                    global SUCCESS_POST
                    SUCCESS_POST += 1
                except:
                    print(traceback.format_exc())
                    #print("не смог закоментить фото в группе {}".format(id))
                    pass
    return 0


def get_gid_for_query(q, offset=20):
    groups = API.groups.search(q=q, count=1000, offset=offset)
    print(len(groups))
    gid = ['-' + str(g['gid']) for g in groups[1:]]
    return gid

def send_message_to_telegram_chats():
    from telethon import TelegramClient
    from telethon.utils import get_display_name
    from telethon.tl.types import InputPeerChat

    api_id = 165394
    api_hash = '42193b1c6ff424bf14a3e852bea3b8b0'
    phone = '+79035350898'
    #phone = '+79998022698'

    client = TelegramClient('@Sess81', api_id, api_hash)
    client.connect()
    client.sign_in(phone=phone)
    #code = 74352
    #me = client.sign_in(code=code)
    me = client.sign_in(code=input('введи код из сообщения от телеги: '))
    print(client.is_user_authorized())

    chat_user_name = 'or_dg'
    chats = [
        "@atypical_chat",
        "@PrTalk2",
        "@chat30",
        "@bezdna42",
        "@odeepwebchat",
        "@findkievchat",
        "@ru2chhw",
        "@govorismari",
        "@littlepkbspb",
        "@TGPR_RealType",
        "@zayavi_o_sebe",
        "@ru2chkz",
        "@d4rkchat",
        "@trollchat"
        ]
    message = r"Ребят, смотрите классный канал нашёл недавно https://t.me/join_relaxxx"  
    for chat in chats:
        channel = client.get_entity(chat)
        client.send_message(channel, "")
        time.sleep(2)
    pass

if __name__ == '__main__':
    #send_message_to_telegram_chats()
    while(True):
        #like_to_friend()
        #time.sleep(60 * 1)
        kill_badman()
        time.sleep(60 * 1)
    ids = get_gid_for_query(q='спортивные девушки', offset=2)[:10]
    #ids = ['-465675969']

    msg = 'Лайк за дружбу'

    send_comment_to_photo(msg, ids, count=100)
    send_comment_to_video(msg, ids, count=100)
    send_comment_to_wall_post(msg, ids, count=100)
    for id in ids:
        send_post_on_wall(msg, id)

    print('#'*100)
    print('успешных постов = {}'.format(SUCCESS_POST))