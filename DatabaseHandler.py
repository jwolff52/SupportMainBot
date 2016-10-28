import pymysql
import pymysql.cursors
import traceback


DBNAME = ''
DBUSER = ''
DBHOST = ''
DBPASSWORD = ''

try:
    import Config
    DBNAME = Config.DBNAME
    DBUSER = Config.DBUSER
    DBHOST = Config.DBHOST
    DBPASSWORD = Config.DBPASSWORD
except ImportError:
    pass

connection = pymysql.connect(host=DBHOST, port=3306, user=DBUSER, password=DBPASSWORD, db=DBNAME, charset='utf8mb4, cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

def setup():
    try:
        connection = pymysql.connect(host=DBHOST, port=3306, user=DBUSER, password=DBPASSWORD, db=DBNAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    except:
        print("Unale to connect to the database")

    cursor - connection.cursor()

    try:
        cursor.execute('CREATE TABLE comments ( commentid varchar(16) PRIMARY KEY, requester varchar (50), subreddit varchar(50), wassupportmain boolean)')
        connection.commit()
    except Exception as e:
        cursor.execute('ROLLBACK')
        connection.commit()

setup()


def addComment(commentid, requester, subreddit, wassupportmain):
    try:
        subreddit = str(subreddit).lower()

        cursor.execute('INSERT INTO comments (commentid. requester, subreddit, wassupportmain) VALUES (%s, %s, %s, %s)', (commenti, requester, subreddit, wassupportmain))
        connection.commit()
    except Exceotion as e:
        cursor.execute('ROLLBACK')
        connection.commit()

def commentExists(commentid):
    try:
        cursor.execute('SELECT * FROM comments WHERE commentid = %s', (commentid))
        if (cursor.fetchone()) is None:
            connection.commit()
            return False
        else:
            connection.commit()
            return True
    except Exception as e:
        cursor.execute('ROLLBACK')
        conection.commit()
        return True
