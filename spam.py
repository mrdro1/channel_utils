import random
import time
import traceback
import os
import requests
import json
#
import vk
import telegram
from telethon import TelegramClient
from telethon.utils import get_display_name
from telethon.tl.types import InputPeerChat
from telethon.tl.types import InputChannel
from telethon.tl.functions.channels import JoinChannelRequest
#
import utils
import db_utils

TOKEN = utils.read_token('tlg')
BOT = telegram.Bot(token=TOKEN)

token = utils.read_token('vk')
session = vk.AuthSession(access_token=token)
API = vk.API(session)
IDS = ['-35807284']
TMP_ALBUM = '253436161'
SUCCESS_POST = 0


def get_rand_photo():
    TRY_COUNT = 5
    photo = None
    for counter in range(TRY_COUNT):
        photo_id = db_utils.get_random_photo(k=1)[0]
        fn = db_utils.get_fn(photo_id)
        if os.path.exists(fn):
            photo = open(fn, 'rb')
            break
    if photo is None: return None
    return photo


def upload_photo_to_album(album_id):
    try:
        upload_info = API.photos.getUploadServer(album_id=album_id)
        photo = get_rand_photo()
        if photo is None: return None
        resp = json.loads(requests.post(upload_info["upload_url"], files={"file1":photo}).content)
        return API.photos.save(album_id=album_id, server=resp["server"], photos_list=resp["photos_list"], hash=resp["hash"])
    except:
        utils.print_message("Не удалось загрузить фотографию в альбом {}.".format(album_id))
        utils.print_message(traceback.format_exc())
    return None


def upload_photo_to_message(peer_id):
    try:
        upload_info = API.photos.getMessagesUploadServer(peer_id=peer_id)
        photo = get_rand_photo()
        if photo is None: return None
        resp = json.loads(requests.post(upload_info["upload_url"], files={"file1":photo}).content)
        return API.photos.saveMessagesPhoto(server=resp["server"], photo=resp["photo"], hash=resp["hash"])
    except:
        utils.print_message("Не удалось загрузить фотографию в диалог {}.".format(peer_id))
        utils.print_message(traceback.format_exc())
    return None


def upload_photo_to_wall(group_id):
    try:
        group_id = abs(int(group_id))
        upload_info = API.photos.getWallUploadServer(group_id=group_id)
        photo = get_rand_photo()
        if photo is None: return None
        resp = json.loads(requests.post(upload_info["upload_url"], files={"file1":photo}).content)
        return API.photos.saveWallPhoto(group_id=group_id, server=resp["server"], photo=resp["photo"], hash=resp["hash"])
    except:
        utils.print_message("Не удалось загрузить фотографию на стену {}.".format(group_id))
        utils.print_message(traceback.format_exc())
    return None


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
            utils.print_message("{} добавлен в друзья.".format(user_id))
            API.messages.send(user_id=user_id, message="Привет ;-)")
            time.sleep(5)
        except:
            utils.print_message("Не удалось добавить {} в друзья.".format(user_id))
            utils.print_message(traceback.format_exc())


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
            utils.print_message("{} удалён из друзей.".format(bad_user_id))
            time.sleep(5)
        except:
            utils.print_message("Не удалось исключить {} из друзей.".format(bad_user_id))
            utils.print_message(traceback.format_exc())
            
            
def send_comment_to_wall_post(msg, ids, count=20, use_random_photo=False):
    for id in ids:
        try:
            t = random.randint(10, 11)
            time.sleep(t)
            posts_info = API.wall.get(owner_id=id, count=count)[1:]
        except:
            utils.print_message(traceback.format_exc())
            #utils.print_message('нет доступа к постам {}'.format(id))
            continue
        for i, post in enumerate(posts_info):
            try:
                t = random.randint(5, 6)
                time.sleep(t)
                att = upload_photo_to_wall(id)[0]["id"] if use_random_photo else None
                API.wall.createComment(owner_id=id, post_id=post['id'], message=msg, attachments=att)
                utils.print_message('послал коммент на стену. id сообщества: {}'.format(id))
                global SUCCESS_POST
                SUCCESS_POST += 1
            except vk.exceptions.VkAPIError as e:
                if e.code == 14:
                    input("Введите капчу. Нажмите Enter для продолжения.")
                elif e.code == 213:
                    utils.print_message('для группы {} комменты на стене заблокированы'.format(id))
                    break
                else:
                    utils.print_message(traceback.format_exc())
            except:
                utils.print_message(traceback.format_exc())
                #
            if i == count:
                break
    return 0


def send_post_to_wall(msg, ids, use_random_photo=False):
    for id in [ group["id"] for group in API.groups.getById(group_ids=[abs(int(id)) for id in ids], fields="can_post") if group["can_post"] == 1]:
        try:
            t = random.randint(5, 6)
            time.sleep(t)
            att = upload_photo_to_wall(id)[0]["id"] if use_random_photo else None
            API.wall.post(owner_id=id, message=msg, attachments=att)
            utils.print_message('постнул на стену, owner={}'.format(id))
            global SUCCESS_POST
            SUCCESS_POST += 1
        except:
            utils.print_message(traceback.format_exc())
            #utils.print_message('не постнул на стену((( {}'.format(id))
            pass
    return 0


def send_comment_to_photo(msg, ids, count=20, limit_al=2, use_random_photo=False):
    for id in ids:
        try:
            t = random.randint(10, 11)
            time.sleep(t)
            albums = API.photos.getAlbums(owner_id=id)
            if not albums:
                #utils.print_message('Для Группы {0} нет фото'.format(id))
                continue
        except Exception as e:
            #utils.print_message(e)
            #utils.print_message('Для Группы {0} недоступны фото'.format(id))
            continue

        #utils.print_message('Всего альбомов {}'.format(len(albums)))
        for i_alb, album in enumerate(albums):
            if i_alb == limit_al:
                break
            #utils.print_message('Текущий альбом {}'.format(i_alb))
            t = random.randint(5, 6)
            time.sleep(t)
            photos = API.photos.get(owner_id=id, count=count, album_id=album['aid'])  #  Получаем список фото

            for photo in photos:
                photo_id = photo['pid']  #  Получаем адрес изображения
                try:
                    t = random.randint(5, 6)
                    time.sleep(t)
                    att = upload_photo_to_wall(id)[0]["id"] if use_random_photo else None
                    API.photos.createComment(owner_id=id, photo_id=photo_id, message=msg, attachments=att)
                    utils.print_message('добавил коммент под фотку, owner={}'.format(id))
                    global SUCCESS_POST
                    SUCCESS_POST += 1
                except vk.exceptions.VkAPIError as e:
                    if e.code == 14:
                        input("Введите капчу. Нажмите Enter для продолжения.")
                    elif e.code == 213:
                        utils.print_message('для группы {} комменты к фото заблокированы'.format(id))
                        break
                    else:
                        utils.print_message(traceback.format_exc())
                except:
                    utils.print_message(traceback.format_exc())
                    #utils.print_message("не смог закоментить фото в группе {}".format(id))
                    pass
    return 0


<<<<<<< HEAD
def get_gid_for_query(q, offset=0):
=======
def send_comment_to_video(msg, ids, count=20, use_random_photo=False):
    for id in ids:
        # TODO переделай count
        try:
            t = random.randint(10, 11)
            time.sleep(t)
            videos_info = API.video.get(owner_id=id, count=count)[1:]
        except:
            #utils.print_message('нет доступа к видео {}'.format(id))
            continue
        for i, video in enumerate(videos_info):
            try:
                t = random.randint(5, 6)
                time.sleep(t)
                att = upload_photo_to_wall(id)[0]["id"] if use_random_photo else None
                API.video.createComment(owner_id=id, video_id=video['vid'], message=msg, attachments=att)
                utils.print_message('послал коммент, owner={}'.format(id))
                global SUCCESS_POST
                SUCCESS_POST += 1
            except vk.exceptions.VkAPIError as e:
                if e.code == 14:
                    input("Введите капчу. Нажмите Enter для продолжения.")
                elif e.code == 801:
                    utils.print_message('для группы {} комменты к видео заблокированы'.format(id))
                    break
                else:
                    utils.print_message(traceback.format_exc())
            except:
                #utils.print_message('для группы {} комменты на стене заблокированы'.format(id))
                pass
            if i == count:
                break
    return 0


def get_gid_for_query(q, offset=20):
>>>>>>> d025259baaf59dc42bfae83442538a7cc9d86639
    groups = API.groups.search(q=q, count=1000, offset=offset)
    utils.print_message(len(groups))
    gid = ['-' + str(g['gid']) for g in groups[1:]]
    return gid

tlg_chats = \
    ['PRTalk',
     'ipiar',
     'FreeVPP',
     'bezdna42',
     'tgplug',
     'piarzero',
     'kingtelegrams',
     'bestprchat',
     'piardublechat',
     'AdToChat',
     'zayavi_o_sebe',
     'PrTalk2',
     'pr_vse',
     'megi_VP',
     'besplatnyipiar',
     'piars',
     'piar_podpiska',
     'piarGo',
     'prfree',
     'TGPR_RealType']
def send_message_to_telegram_chats(bot, msg=r"Ребят, смотрите классный канал нашёл недавно @join_relaxxx" , list_chat=tlg_chats):
    """ """
    success_msg = 0
    list_chat = list(set(list_chat))
    print('всего каналов для рассылки {}'.format(len(list_chat)))
    for chat in list_chat:

        try:
            channel = bot.get_entity(chat)
            bot.send_message(channel, msg)
            print('Отправил в {}'.format(chat))
            success_msg += 1
        except:

            #s = traceback.format_exc()
            print("Не смог отправить {}".format(chat))
            list_chat.remove(chat)


        time.sleep(1)
    return success_msg, list_chat


def create_tlg_client():
    api_id, api_hash, phone = utils.read_tlg_token()

    client = TelegramClient('@Sess81', api_id, api_hash)
    client.connect()
    client.sign_in(phone=phone)
    me = client.sign_in(code=input('введи код из сообщения от телеги: '))
    utils.print_message(client.is_user_authorized())
    return client

def join_to_channel(bot, list_ids=tlg_chats):
    success_rate = 0
    for id in list_ids:
        try:
            i = InputChannel(bot.get_entity(id).id, bot.get_entity(id).access_hash)
            bot.invoke(JoinChannelRequest(i))
            success_rate += 1
            print("присоединился к {}".format(id))
            time.sleep(5)
        except:
            print('не могу присоединиться к {}'.format(id))
            list_ids.remove(id)
    return success_rate/len(list_ids), list_ids