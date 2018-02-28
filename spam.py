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
