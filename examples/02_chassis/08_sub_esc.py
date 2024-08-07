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


import time
import robomaster
from robomaster import robot
import csv

esc_data = []

def sub_esc_info_handler(esc_info):
    speed, angle, timestamp, state = esc_info
    print("chassis esc: speed:{0}, angle:{1}, timestamp:{2}, state:{3}".format(speed, angle, timestamp, state))
    esc_data.append((speed, angle, timestamp, state))

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis

    x_val = 0.6
    y_val = 0.6
    z_val = 90

    for i in range(3):
    # 订阅底盘电调信息
        ep_chassis.sub_esc(freq=1, callback=sub_esc_info_handler)
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

        ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
        
        ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

        ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.unsub_esc()

    ep_robot.close()

    with open('sub_esc_s1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Speed", "Angel", "Timestamp","State"])
        writer.writerows(esc_data)

