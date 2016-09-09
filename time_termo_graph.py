#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime

import numpy as np
import postgresql.exceptions
import postgresql.driver as pg_driver
from matplotlib.dates import HourLocator, DateFormatter
from scipy import interpolate
import matplotlib.pyplot as plt
import const

user = const.user
password = const.password
host = const.host
db_family = const.db_family
db_measurements = const.db_measurements


def draw_through_points(x_plt, x0_plt, y_plt, plt_def, n):
    plt_def.figure()
    tck, u = interpolate.splprep({x_plt, y_plt}, k=3, s=0)
    u = np.linspace(0, 1, num=n, endpoint=True)
    out = interpolate.splev(u, tck)
    plt_def.plot(x_plt, y_plt, 'ro', out[0], out[1], 'b')
    plt_def.legend(['Points', 'Interpolated B-spline', 'True'], loc='best')
    plt_def.axis([min(x_plt) - 1, max(x_plt) + 1, min(y_plt) - 1, max(y_plt) + 1])
    plt_def.title('Temperature in object')
    plt_def.grid(True)
    plt_def.show()


def draw_beautiful(x_plt, x0_plt, y_plt, plt_def):
    l = len(x_plt)
    t = np.linspace(0, 1, l - 2, endpoint=True)
    t = np.append([0, 0, 0], t)
    t = np.append(t, [1, 1, 1])
    tck = [t, [x_plt, y_plt], 3]
    u3 = np.linspace(0, 1, (max(l * 2, 100)), endpoint=True)
    out = interpolate.splev(u3, tck)
    out[0] = np.array([datetime.datetime.fromtimestamp(out[0][i]) for i in range(len(out[0]))])
    fig, ax = plt_def.subplots()
    ax.plot_date(x0_plt, y_plt, 'ro', label='Measured points', marker='o', markerfacecolor='green')
    ax.plot_date(out[0], out[1], 'b', linewidth=2.0, label='B-spline curve')
    ax.set_xlim(x0_plt[0], x0_plt[-1])
    ax.xaxis.set_major_locator(HourLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate()
    plt_def.legend(loc='best')
    plt_def.xlabel('Time (s)')
    plt_def.ylabel('Temperature (ºC)')
    plt_def.title('Temperature in object')
    plt_def.grid(True)
    plt_def.show()

#################################################
table_name = 'n0007'        # Target table      #
start_time = 1473331438     # Target start time #
#################################################

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
print(datetime.datetime.now())
x0 = np.array([datetime.datetime.fromtimestamp(x[i]) for i in range(len(x))])
y = draw_data[:, 1]
print(x0[0])
# draw_through_points(x, x0, y, plt, n=len(x))
draw_beautiful(x, x0, y, plt)
