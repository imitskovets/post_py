import postgresql.exceptions
import postgresql.driver as pg_driver
import const

user = const.user
password = const.password
host = const.host
db_family = const.db_family
db_measurements = const.db_measurements

try:
    db = pg_driver.connect(user=user, password=password, host=host, port=5432, database=db_measurements)
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)
for i in range(8):
    psdrop = db.prepare('drop table n000' + str(i) + ';')
    print(psdrop())
    pscreate = db.prepare('create table n000' + str(i) + '(time integer,temperature float);')
    print(pscreate())
