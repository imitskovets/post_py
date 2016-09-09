#!/usr/bin/python3
# -*- coding: utf-8 -*-
import postgresql.exceptions
import postgresql.driver as pg_driver
import numpy as np
import const
#import temperature_surf

user = const.user
password = const.password
host = const.host
db_family = const.db_family
db_measurements = const.db_measurements

def insert_last_row(db_f, db_m, parent):
    ps = db_f.prepare('SELECT id,child FROM ' + parent + ';')
    children_list = ps()
    if children_list[0][1] is None:
        try:
            inputFile = open('update_' + parent + '.csv')
        except IOError:
            print("file not found")
        n = int(inputFile.readline())
        tmp = np.zeros(2, dtype=float)
        # TODO skip lines
        for i in range(n):
            tmp = inputFile.readline().split(",")
        ps2 = db_m.prepare('insert into ' + parent + ' (time, temperature) values ( ' \
                         + str(tmp[0]) + ',' + str(tmp[1]) + ' );')
        ps2()
        inputFile.close()
        return 0
    else:
        for i in range(len(children_list)):
            insert_last_row(db_f, db_m, children_list[i][1])
        return 0

def insert_all_rows(db_f, db_m, parent):
    ps = db_f.prepare('SELECT id,child FROM ' + parent + ';')
    children_list = ps()
    if children_list[0][1] is None:
        try:
            inputFile = open('update_' + parent + '.csv')
        except IOError:
            print("file not found")
        n = int(inputFile.readline())
        tmp = np.zeros(2, dtype=float)
        for i in range(n):
            tmp = inputFile.readline().split(",")
            ps2 = db_m.prepare('insert into ' + parent + '( time, temperature) values ( ' \
                             + str(tmp[0]) + ',' + str(tmp[1]) + ' );')
            #print('insert into ' + str(parent) + '(time, temperature) values ( ' \
            #      + str(tmp[0]) + ',' + str(tmp[1]) + ' );')
            ps2()
        inputFile.close()
        return 0
    else:
        for i in range(len(children_list)):
            insert_all_rows(db_f, db_m, children_list[i][1])
        return 0

try:
    db_f = pg_driver.connect(user=user, password=password, host=host, port=5432, database=db_family)
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)
try:
    db_m = pg_driver.connect(user=user, password=password, host=host, port=5432, database=db_measurements)
    print("Connect to postgres successfully!")
except postgresql.exceptions.ClientCannotConnectError:
    print('Cannot connect! Check your internet connection and psql server status.')
    exit(-1)
# fill n row in objects are wich childless
insert_all_rows(db_f, db_m, 'n0000')
# add just row number n in objects are wich childless
#insert_last_row(db_f, db_m, 'n0000')
# calculate and fill one row objects with children
#temperature_surf.fill_from_children(db_f, db_m, 'n0000')

