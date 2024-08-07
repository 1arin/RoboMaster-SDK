# # # -*-coding:utf-8-*-
# # # Copyright (c) 2020 DJI.
# # #
# # # Licensed under the Apache License, Version 2.0 (the "License");
# # # you may not use this file except in compliance with the License.
# # # You may obtain a copy of the License in the file LICENSE.txt or at
# # #
# # #     http://www.apache.org/licenses/LICENSE-2.0
# # #
# # # Unless required by applicable law or agreed to in writing, software
# # # distributed under the License is distributed on an "AS IS" BASIS,
# # # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # # See the License for the specific language governing permissions and
# # # limitations under the License.


# # import robomaster
# # from robomaster import robot
# # import csv

# # attitude_info = []


# # def sub_attitude_info_handler(attitude_info):
# #     yaw, pitch, roll = attitude_info
# #     print("chassis attitude: yaw:{0}, pitch:{1}, roll:{2} ".format(yaw, pitch, roll))



# # if __name__ == '__main__':
# #     ep_robot = robot.Robot()
# #     ep_robot.initialize(conn_type="ap")

# #     ep_chassis = ep_robot.chassis
# #     x_val = 0.6
# #     y_val = 0.6
# #     z_val = 90


# #     # 订阅底盘姿态信息
# #     ep_chassis.sub_attitude(freq=10, callback=sub_attitude_info_handler)
# #     # ep_chassis.move(x=0, y=0, z=90).wait_for_completed()
# #     # ep_chassis.move(x=0, y=0, z=-90).wait_for_completed()
# #     ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

# #     # # 后退 0.5米
# #     ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()

    
# #     ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

# #     # # 左移 0.6米
# #     # ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()

# #     # # 右移 0.6米
# #     ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
# #     ep_chassis.unsub_attitude()

# #     ep_robot.close()

# #     with open('sub_attitude.csv', 'w', newline='') as file:
# #         writer = csv.writer(file)
# #         # writer.writerow(["Time", "Target", "X Position"])
# #         writer.writerow(["Yaw", "Pitch", "Roll"])

# #         writer.writerows(attitude_info)

# import robomaster
# from robomaster import robot
# import csv

# attitude_data = []

# def sub_attitude_info_handler(attitude_info):
#     yaw, pitch, roll = attitude_info
#     attitude_data.append((yaw, pitch, roll))

# if __name__ == '__main__':
#     ep_robot = robot.Robot()
#     ep_robot.initialize(conn_type="ap")

#     ep_chassis = ep_robot.chassis
#     x_val = 0.6
#     y_val = 0.6
#     z_val = 90

#     # 订阅底盘姿态信息
#     for i in range(3):
#         ep_chassis.sub_attitude(freq=10, callback=sub_attitude_info_handler)
#         ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

#         ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
        
#         ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()

#         ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
#         ep_chassis.unsub_attitude()

#     ep_robot.close()

#     with open('sub_attitude_1.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Yaw", "Pitch", "Roll"])
#         writer.writerows(attitude_data)
import robomaster
from robomaster import robot
import csv
import time

attitude_data = []

def sub_attitude_info_handler(attitude_info):
    yaw, pitch, roll = attitude_info
    attitude_data.append((yaw, pitch, roll))

if __name__ == '__main__':
    start_time = time.time()  # Record start time
    
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    x_val = 0.6
    y_val = 0.6
    z_val = 90

    # Perform movements and subscribe to attitude info multiple times
    for i in range(3):
        ep_chassis.sub_attitude(freq=1, callback=sub_attitude_info_handler)
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.unsub_attitude()

    ep_robot.close()

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
    elapsed_minutes = elapsed_time / 60  # Convert elapsed time to minutes
    
    with open('sub_attitude_addtime_s1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Yaw", "Pitch", "Roll"])
        writer.writerows(attitude_data)

    print(f"Total elapsed time: {elapsed_time} seconds or {elapsed_minutes} minutes")