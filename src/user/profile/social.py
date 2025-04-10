from src.database import get_db_connection


def get_subscriber_ids(uid):
    db = get_db_connection()
    cursor = db.cursor()

    try:
        # 查询用户的订阅信息和对应的用户名，合并两个查询
        query = """
                SELECT u.id, u.username
                FROM subscriptions s
                         JOIN users u ON s.subscribe_to_id = u.id
                WHERE s.subscriber_id = %s
                  AND s.subscribe_type = 'User'; \
                """
        cursor.execute(query, (uid,))
        subscribers = cursor.fetchall()

        # 如果没有找到订阅者，返回空列表
        if not subscribers:
            return []

        # 创建（ID, 用户名）元组列表
        subscriber_ids_list = [(sub[0], sub[1]) for sub in subscribers]
        print(subscriber_ids_list)
        return subscriber_ids_list

    except Exception as e:
        return f"未知错误{e}", False, False

    finally:
        cursor.close()
        db.close()


def get_following_count(user_id, subscribe_type='User'):
    db = get_db_connection()
    count = 0
    try:
        with db.cursor() as cursor:
            if subscribe_type == 'User':
                query = "SELECT COUNT(*) FROM subscriptions WHERE `subscriber_id` = %s AND `subscribe_type` = 'User';"
                cursor.execute(query, (int(user_id),))
            else:
                query = ("SELECT COUNT(*) FROM subscriptions WHERE `subscriber_id` = %s AND `subscribe_type` = "
                         "'Category';")
                cursor.execute(query, (int(user_id),))

            # 读取查询结果
            count = cursor.fetchone()[0]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

    return count


def get_follower_count(user_id, subscribe_type='User'):
    db = get_db_connection()
    count = 0
    try:
        with db.cursor() as cursor:
            if subscribe_type == 'User':
                query = "SELECT COUNT(*) FROM subscriptions WHERE `subscribe_to_id` = %s AND `subscribe_type` = 'User';"
                cursor.execute(query, (int(user_id),))
            else:
                query = ("SELECT COUNT(*) FROM subscriptions WHERE `subscribe_to_id` = %s AND `subscribe_type` = "
                         "'Category';")
                cursor.execute(query, (int(user_id),))

            count = cursor.fetchone()[0]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

    return count


def get_can_followed(user_id, target_id):
    db = get_db_connection()
    can_follow = 1
    try:
        with db.cursor() as cursor:
            query = "SELECT COUNT(*) FROM `subscriptions` WHERE `subscriber_id` = %s AND `subscribe_to_id` = %s;"
            cursor.execute(query, (int(user_id), int(target_id)))
            count = cursor.fetchone()[0]
            if count:
                can_follow = 0
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

    return can_follow
