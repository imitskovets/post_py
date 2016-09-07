#!/usr/bin/python3
# -*- coding: utf-8 -*-
import postgresql.exceptions
import postgresql.driver as pg_driver
user = 'postgres'
password = 'postgres'
host = 'localhost'
db_family = 'family'
db_measurements = 'measurements'

try:
    db = pg_driver.connect(user=user, password=password, host=host, port=5432, database=db_family)
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)

ps = db.prepare("SELECT now()")
print(ps())
