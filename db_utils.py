import sqlite3

CONN = sqlite3.connect('default_files//photo.db')
CURSOR = CONN.cursor()

def set_used(id, is_used=1):
    UPDATE_IS_USED_PHOTO_BY_ID = 'update photo set is_used == {} where id == {}'
    ans = CURSOR.execute(UPDATE_IS_USED_PHOTO_BY_ID.format(is_used, id))
    return ans

def insert_photo(dict_data):
    INSERT_PHOTO = 'insert into photo values(null,:source_id,:source,:date,0)'
    ans = CURSOR.execute(INSERT_PHOTO, dict_data)

def check_exists(source_id, source):
    SELECT_BY_SOURCE_AND_SID = 'select id from photo where source_id == {} and source == {}'
    ans = CURSOR.execute(SELECT_BY_SOURCE_AND_SID.format(source_id, source)).fetchone()
    exists = ans is not None
    return exists

def get_fn(id):
    SELECT_SOURCE_AND_SID = 'select source, source_id from photo where id == {}'
    ans = CURSOR.execute(SELECT_SOURCE_AND_SID.format(id)).fetchone()
    fn = '//'.join(ans) + '.jpg'
    return fn

def get_not_used_photo(k=None):
    SELECT_NOT_USED_PHOTO = 'select id from photo where is_used == 0'
    SELECT_NOT_USED_PHOTO_WITH_LIMIT = 'select id from photo where is_used == 0 limit {}'
    if k:
        query = SELECT_NOT_USED_PHOTO_WITH_LIMIT.format(k)
    else:
        query = SELECT_NOT_USED_PHOTO
    # TODO мб сделать генератор
    ans = CURSOR.execute(query).fetchall()
    ans = [row[0] for row in ans]
    return ans

