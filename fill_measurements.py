#!/usr/bin/python3
# -*- coding: utf-8 -*-
import postgresql.exceptions
import postgresql.driver as pg_driver
import numpy as np

user = 'postgres'
password = 'postgres'
host = 'localhost'
db_family = 'family'
db_measurements = 'measurements'
table_name = 'n0007'

try:
    db = pg_driver.connect(user=user, password=password, host=host, port=5432, database=db_measurements)
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)

try:
    inputFile = open("input.csv")
except IOError:
    print("file not found")
n = int(inputFile.readline())
tmp = np.zeros(2, dtype=float)
for i in range(n):
    tmp = inputFile.readline().split(",")
    ps = db.prepare('insert into ' + table_name + '(time, temperature) values (\'' \
                    + str(tmp[0]) + '\',\'' + str(tmp[1]) + '\');')
    print(ps())
inputFile.close()
