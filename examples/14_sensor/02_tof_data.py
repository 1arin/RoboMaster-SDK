# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import robomaster
from robomaster import robot
import time 
import csv
import pandas as pd
import matplotlib.pyplot as plt


sub_data = []

def sub_data_handler(sub_info):
    distance = sub_info
    print("tof1:{0}  tof2:{1}  tof3:{2}  tof4:{3}".format(distance[0], distance[1], distance[2], distance[3]))
    sub_data.append((distance[0], distance[1], distance[2], distance[3]))


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    x_val = 0.6
    y_val = 0.6
    z_val = 90

    for i in range(3):
        ep_sensor.sub_distance(freq=1, callback=sub_data_handler)
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

        ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
        
        ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

        ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
        ep_sensor.unsub_distance()
    ep_robot.close()

    with open('sub_tof_s2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["tof0","tof1", "tof2", "tof3"])
        writer.writerows(sub_data)

df = pd.read_csv('sub_tof_s2.csv')
plt.plot(df['tof0'])
plt.xlabel('TIME')
plt.ylabel('Value')
plt.title('TOF')
plt.show()