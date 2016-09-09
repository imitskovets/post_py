#!/usr/bin/python3
# -*- coding: utf-8 -*-
import postgresql.exceptions
import postgresql.driver as pg_driver

user = 'postgres'
password = 'postgres'
host = 'localhost'
db_family = 'family'
db_measurements = 'measurements'


def fill_from_childer(db_fam, db_mea, parent):
    ps = db_f.prepare('SELECT id,child,capacity from ' + parent + ';')
    children_list = ps()
    print(children_list)
    if children_list[0][1] is None:
        ps = db_m.prepare('SELECT max(time) from ' + parent + ';')
        max_time = ps()[0][0]
        ps = db_m.prepare('SELECT time,temperature from ' + parent + ' where time=' + str(max_time) + ';')
        pss = ps()
        # print('then no child return :' + str(pss[0]))
        return (pss[0])
    else:
        sum_capacity = 0.
        sum_energy = 0.
        for_av_time = 0
        for i in range(len(children_list)):
            sum_capacity += children_list[i][2]
            # print('go to ' + str(children_list[i][1]))
            child_data = fill_from_childer(db_fam, db_mea, children_list[i][1])
            sum_energy += children_list[i][2] * child_data[1]
            for_av_time += child_data[0]
        # print(str(sum_capacity))
        # print(str(sum_energy))
        # print('set temperature in ' + str(parent) + ' = ' + str(sum_energy/sum_capacity))
        ps_temp = db_m.prepare('INSERT INTO ' + str(parent) + ' (time, temperature) VALUES (' + str(
            int(for_av_time / len(children_list))) + ' , ' + str(sum_energy / sum_capacity) + ' ) ;')
        ps_temp()
        # print('with time = ' + str(int(for_av_time/len(children_list))))
        rez = (int(for_av_time / len(children_list)), sum_energy / sum_capacity)
        return rez


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
print(str(fill_from_childer(db_f, db_m, 'n0000')))
