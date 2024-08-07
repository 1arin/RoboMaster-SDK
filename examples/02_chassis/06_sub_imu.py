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

imu_data = []

def sub_imu_info_handler(imu_info):
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_info
    print("chassis imu: acc_x:{0}, acc_y:{1}, acc_z:{2}, gyro_x:{3}, gyro_y:{4}, gyro_z:{5}".format(
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))
    imu_data.append((acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    
    x_val = 0.6
    y_val = 0.6
    z_val = 90

    # 订阅底盘姿态信息
    for i in range(3):
    # 订阅底盘IMU信息
        ep_chassis.sub_imu(freq=1, callback=sub_imu_info_handler)
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

        ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
        
        ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

        ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.unsub_imu()

    ep_robot.close()

    with open('sub_imu_s1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Acc_X", "Acc_Y", "Acc_Z","Gyro_X","Gyro_Y","Gyro_Z"])
        writer.writerows(imu_data)


