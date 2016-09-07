#!/usr/bin/python3
# -*- coding: utf-8 -*-
import postgresql.exceptions
import postgresql.driver as pg_driver

try:
    db = pg_driver.connect(user='postgres', password='postgres', host='localhost', port=5432, database='family')
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)

ps = db.prepare("SELECT now()")
print(ps())
