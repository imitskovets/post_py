import postgresql.driver as pg_driver

db = pg_driver.connect(user='postgres', password='postgres', host='localhost', port=5432, database='family')
ps = db.prepare("SELECT now()")
print(ps())
