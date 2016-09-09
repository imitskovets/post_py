#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import postgresql.exceptions
import postgresql.driver as pg_driver
from scipy import interpolate
import matplotlib.pyplot as plt


def draw_through_points(x_plt, y_plt, plt_def, n):
    plt_def.figure()
    tck, u = interpolate.splprep([x_plt, y_plt], k=3, s=0)
    u = np.linspace(0, 1, num=n, endpoint=True)
    out = interpolate.splev(u, tck)
    plt_def.plot(x_plt, y_plt, 'ro', out[0], out[1], 'b')
    plt_def.legend(['Points', 'Interpolated B-spline', 'True'], loc='best')
    plt_def.axis([min(x_plt) - 1, max(x_plt) + 1, min(y_plt) - 1, max(y_plt) + 1])
    plt_def.title('Temperature in object')
    plt_def.grid(True)
    plt_def.show()


def draw_beautiful(x_plt, y_plt, plt_def):
    plt_def.figure()
    l = len(x_plt)
    t = np.linspace(0, 1, l - 2, endpoint=True)
    t = np.append([0, 0, 0], t)
    t = np.append(t, [1, 1, 1])
    tck = [t, [x_plt, y_plt], 3]
    u3 = np.linspace(0, 1, (max(l * 2, 100)), endpoint=True)
    out = interpolate.splev(u3, tck)
    plt_def.plot(x_plt, y_plt, 'ro', label='Measured points', marker='o', markerfacecolor='green')
    plt_def.plot(out[0], out[1], 'b', linewidth=2.0, label='B-spline curve')
    plt_def.legend(loc='best')
    plt_def.xlabel('Time (s)')
    plt_def.ylabel('Temperature (ºC)')
    plt_def.axis([min(x_plt) - 1, max(x_plt) + 1, min(y_plt) - 1, max(y_plt) + 1])
    plt_def.title('Temperature in object')
    plt_def.grid(True)
    plt_def.show()


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
draw_data = np.array(points)
x = draw_data[:, 0]
y = draw_data[:, 1]
# draw_through_points(x, y, plt, n=len(x))
draw_beautiful(x, y, plt)
