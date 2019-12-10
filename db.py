from config import DB_NAME, DB_USER, DB_PWD, DB_HOST
import pymysql

def dbskiutc_con():
    con = pymysql.connect(
        host=DB_HOST,
        db=DB_NAME,
        user=DB_USER,
        password=DB_PWD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    return con

if __name__ == '__main__':
    _main(sys.argv)
