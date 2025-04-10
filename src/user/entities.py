from src.database import get_db_connection


def query_blog_author(title):
    db = get_db_connection()

    try:
        with db.cursor() as cursor:
            query = "SELECT Author FROM articles WHERE Title = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()

            if result:
                query = "SELECT id FROM users WHERE username = %s"
                cursor.execute(query, (result[0],))
                author_uid = cursor.fetchone()
                return result[0], author_uid[0]
            else:
                return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
    finally:
        try:
            cursor.close()
        except NameError:
            pass
        db.close()


def authorize_by_aid(article_id, user_name):
    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                query = "SELECT 1 FROM articles WHERE ArticleID = %s AND `Status` != 'Deleted' AND Author = %s"
                cursor.execute(query, (article_id, user_name))
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def get_user_id(user_name):
    db = get_db_connection()
    user_id = 0
    try:
        with db.cursor() as cursor:
            query = "SELECT `id` FROM `users` WHERE `username` = %s;"
            cursor.execute(query, (user_name,))
            user_id = cursor.fetchone()[0]
            if user_id:
                return user_id
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

    return user_id


def get_user_sub_info(query, user_id):
    db = None
    user_sub_info = []
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute(query, (int(user_id),))
            user_sub = cursor.fetchall()
            subscribe_ids = [sub[0] for sub in user_sub]
            if subscribe_ids:
                placeholders = ', '.join(['%s'] * len(subscribe_ids))
                query = f"SELECT `id`, `username` FROM `users` WHERE `id` IN ({placeholders});"
                cursor.execute(query, tuple(subscribe_ids))
                user_sub_info = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if db is not None:
            db.close()
    return user_sub_info


def check_user_conflict(zone, value):
    if zone == 'username':
        query = "SELECT username FROM users"
    elif zone == 'email':
        query = "SELECT email FROM users"
    else:
        return False
    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                cursor.execute(query)
                if value not in [row[0] for row in cursor.fetchall()]:
                    return False
        return False
    except Exception as e:
        print(f"Error getting user list: {e}")
        return False


def db_save_avatar(user_id, avatar_uuid):
    db = None
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            query = "UPDATE users SET profile_picture = %s WHERE id = %s"
            cursor.execute(query, (avatar_uuid, user_id))
            db.commit()
    except Exception as e:
        print(f"Error saving avatar: {e} by user {user_id} avatar uuid: {avatar_uuid}")
    finally:
        if db is not None:
            db.close()


def db_save_bio(user_id, bio):
    db = None
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            query = "UPDATE users SET bio = %s WHERE id = %s"
            cursor.execute(query, (bio, user_id))
            db.commit()
    except Exception as e:
        print(f"Error saving bio: {e} by user {user_id} bio: {bio}")
    finally:
        if db is not None:
            db.close()


def db_change_username(user_id, new_username):
    # 修改用户名将可能导致资料被意外删除,建议先导出您的资料再进行下一步操作
    # 导出资料: 点击右上角头像 -> 点击设置 -> 点击导出资料
    db = None
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            query = "UPDATE users SET username = %s WHERE id = %s"
            cursor.execute(query, (new_username, user_id))
            db.commit()
    except Exception as e:
        print(f"Error changing username: {e} by user {user_id} new username: {new_username}")
    finally:
        if db is not None:
            db.close()


def db_bind_email(user_id, param):
    pass
