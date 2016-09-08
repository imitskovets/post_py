#!/usr/bin/python3
# -*- coding: utf-8 -*-
import postgresql.exceptions
import postgresql.driver as pg_driver
import matplotlib.pyplot as plt


user = 'postgres'
password = 'postgres'
host = 'localhost'
db_family = 'family'
db_measurements = 'measurements'
table_name = 'n0007'
start_time = 1473331438

try:
    db = pg_driver.connect(user=user, password=password, host=host, port=5432, database=db_measurements)
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)

ps = db.prepare('select * from ' + table_name + ' where time > ' + str(start_time) + ' ;')
points = ps()
print(points)
#plt.plot(points)
#plt.grid(True)
#plt.show()