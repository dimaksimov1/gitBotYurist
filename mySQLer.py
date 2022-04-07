import config
from mysql.connector import MySQLConnection, Error


def parseDictionary(dictionaryArgs):
    k, v = [], []
    for el in dictionaryArgs:
        k.append(el)
        v.append(dictionaryArgs[el])
    return k, v

def db_connect():
    try:
        conn = MySQLConnection(host=config.dbhost,
                               database=config.database,
                               user=config.dbuser,
                               password=config.dbpassword)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
        else:
            print('Connected failed')
            return False

    except Error as e:
        print(e)

def connectBd(db):
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {db}')

        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def insertBdActionNew(dictArgs):  # Добавление новой / изменение строки в dbAction
    args = list(dictArgs.values())
    args.extend(list(dictArgs.values()))
    strValues = ' = %s, '.join(list(dictArgs.keys())) + ' = %s'

    query = f'INSERT INTO dbAction SET {strValues} ON DUPLICATE KEY UPDATE {strValues}'

    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def updateBdAction(dictArgs):  # изменение строки в dbAction
    args = list(dictArgs.values())
    strValues = ' = %s, '.join(list(dictArgs.keys())) + ' = %s'

    userId = dictArgs['userId']
    query = f'UPDATE dbAction SET {strValues} WHERE userId = {userId}'

    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def deleteBd(db, id):  # Удаление строки по id
    query = f'DELETE FROM {db} WHERE id = %s'
    args = (id,)
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def deleteBdAll(db):
    query = f'TRUNCATE TABLE {db}'
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def selectBd(db, quest):  # запрос строки по quest - кортеж (где искать = что искать)
    query = f'SELECT * FROM {db} WHERE {quest[0]} = %s'
    args = (quest[1],)
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        print(cursor.fetchall())
        return cursor.fetchall()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def selectBdPeriod(perodStart, periodEnd):  # запрос строки по perod - кортеж (Дата начала, дата конца)
    query = 'SELECT start, step1, step2, step3, step4, step5, step6 ' \
            'FROM dbAction ' \
            'WHERE dataStart > %s and dataLast < %s'
    args = (perodStart.strftime('%Y-%m-%d %H:%M:%S'), periodEnd.strftime('%Y-%m-%d %H:%M:%S'))

    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        answer = cursor.fetchall()
        print(answer)
        return answer
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def selectBdLast(count):
    query = f'SELECT * FROM dbAction ORDER BY dataStart DESC LIMIT {count}'
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(query)
        answer = cursor.fetchall()
        print(answer)
        return answer
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()