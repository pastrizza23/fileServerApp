import datetime
import psycopg2
import jwt
import uuid

from utils.config_parser import config


def create(email, hashed_secret):
    conn = None
    query = "insert into clients (\"email\", \"password\", \"uuid\") values(%s,%s,%s)"

    try:
        conn = psycopg2.connect(dbname=config()["auth"]["dbname"],
                                user=config()["auth"]["dbuser"],
                                password=config()["auth"]["dbpassword"],
                                host='localhost',
                                port=54320)
        cur = conn.cursor()
        cur.execute(query, (email, hashed_secret, str(uuid.uuid4())))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def delete(user_uuid):
    conn = None
    query = f"DELETE FROM clients WHERE uuid='{user_uuid}'"

    try:
        conn = psycopg2.connect(dbname=config()["auth"]["dbname"],
                                user=config()["auth"]["dbuser"],
                                password=config()["auth"]["dbpassword"],
                                host='localhost',
                                port=54320)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def authenticate(user_email, hashed_secret):
    conn = None
    query = f"SELECT * FROM clients WHERE email=\'{user_email}\' AND password='{hashed_secret}'"

    try:
        conn = psycopg2.connect(dbname=config()["auth"]["dbname"],
                                user=config()["auth"]["dbuser"],
                                password=config()["auth"]["dbpassword"],
                                host='localhost',
                                port=54320)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchone()

        if cur.rowcount == 1:
            payload = {
                "id": rows[0],
                "user_email": rows[1],
                "uuid": rows[3],
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }

            encoded_jwt = jwt.encode(payload, config()['auth']['secret_key'], algorithm='HS256')

            return {"token": encoded_jwt}
        else:
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def get_user(email):
    conn = None
    query = f"SELECT * FROM clients WHERE email=\'{email}\'"

    try:
        conn = psycopg2.connect(dbname=config()["auth"]["dbname"],
                                user=config()["auth"]["dbuser"],
                                password=config()["auth"]["dbpassword"],
                                host='localhost',
                                port=54320)
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return []
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def verify(token):
    try:
        blacklisted = check_blacklist(token)
        if blacklisted:
            return {"success": False}
        else:
            decoded = jwt.decode(token, config()["auth"]["secret_key"], algorithms=['HS256'])
            return decoded
    except Exception as error:
        print(error)
        return {"success": False}


def blacklist(token):
    conn = None
    query = "insert into blacklist (\"token\") values(\'" + token + "\')"
    try:
        conn = psycopg2.connect(dbname=config()["auth"]["dbname"],
                                user=config()["auth"]["dbuser"],
                                password=config()["auth"]["dbpassword"],
                                host='localhost',
                                port=54320)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def check_blacklist(token):
    conn = None
    query = "select count(*) from blacklist where token=\'" + token + "\'"
    try:
        conn = psycopg2.connect(dbname=config()["auth"]["dbname"],
                                user=config()["auth"]["dbuser"],
                                password=config()["auth"]["dbpassword"],
                                host='localhost',
                                port=54320)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()