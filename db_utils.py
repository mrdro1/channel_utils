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

