import time
import csv
from robomaster import robot
import pandas as pd
import matplotlib.pyplot as plt

axis_x = []
axis_y = []
time_all = []
target = []

#ค่าเป้าหมาย เริ่มต้น
global expect
expect = 1

def subposition_handler(position_info):
    x, y, z = position_info
    axis_x.append(x)
    axis_y.append(y)
    end_time = time.time() - start_time
    final_endtime= '{:.05f}'.format(end_time)
    time_all.append(final_endtime)
    target.append(expect)

#ฟังชั่นสลับ ค่าเป้าหมาย 
def toggle_target(expect):
    if expect == 1:
        return 0
    elif expect == 0:
        return 1

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis
    ep_chassis.sub_position(freq=50, callback=subposition_handler)

    speed = 100
    #PID
    p = 155.00
    #เริ่มจับเวลา
    start_time = time.time()
    #รอบ
    times = 0

    try:
    #ลูปทำงานไปกลับ 2 รอบ
        while True:
#เริมทำงานตอนมีทั้งเวลา และรู้จุดรถ
            if axis_x and time_all:
                #รู้จุด x ของรถตอนนี้
                now_x = axis_x[-1]
                #รู้เวลารถตอนนี้
                now_time = float(time_all[-1])
                #ค่าระยะห่างระหว่างรถกับเป้าหมาย
                err = expect - now_x
                #ค่าคงที่ที่เหมาะสม * ระยะห่างของรถกับเป้าหมาย
                speed = err * p
                #ค่าที่ห่างกันของรถ โดยกันไม่ให้ติดลบด้วย Absolute
                err_abs = abs(err)
                #ค่ารถกับเป้าหมายใกล้เคียงกัน หยุดได้
                if err_abs < 0.001:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    time.sleep(2)
                    expect = toggle_target(expect)
                    # รอบ
                    times += 1
                    #รถห่างกับเป้าหมาย 0.2 ให้ 2.5 เพราะ ค่า err น้อยจนล้อไม่ขยับ
                elif err_abs < 0.2 :
                    speed = (err*p) * 2.90
                #ให้รถขยับ ไปตามค่า speed ที่ได้จาก err
                ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
    except KeyboardInterrupt:
        print('Something went wrong')

    ep_robot.close()

    with open('POS.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Target", "X Position"])
        writer.writerows(zip(time_all, target, axis_x))

    df = pd.read_csv('POS.csv')
    plt.figure(figsize=(6, 6))
    plt.plot(time_all, target)
    plt.plot(time_all, axis_x)
    plt.title('Robot MAP')
    plt.ylabel('X position')
    plt.xlabel('Time')
    plt.tight_layout()
    plt.show()

# import robomaster
# import time
# import csv
# from robomaster import robot
# import pandas
# import matplotlib.pyplot as plt

# axis_x = []
# axis_y = []
# time_all = []
# target = []

# #ค่าเป้าหมาย เริ่มต้น
# global expect
# expect = 1

# def sub_position_handler(position_info):
#     x, y, z = position_info
#     axis_x.append(x)
#     axis_y.append(y)
#     end_time = time.time()-start_time
#     final_endtime= '{:.05f}'.format(end_time)
#     time_all.append(final_endtime)
#     target.append(expect)

# #ฟังชั่นสลับ ค่าเป้าหมาย 
# def toggle_target(expect):
#     if expect == 1:
#         return 0
#     elif expect == 0:
#         return 1

# if __name__ == '__main__':
#     ep_robot = robot.Robot()
#     ep_robot.initialize(conn_type="ap")
#     ep_chassis = ep_robot.chassis
#     ep_chassis.sub_position(freq=50, callback=sub_position_handler)

#     speed = 100
#     #PID
#     p = 150.00
#     #เริ่มจับเวลา
#     start_time = time.time()
#     #รอบ
#     times = 0

#     #ลูปทำงานไปกลับ 2 รอบ
#     while times < 4:

#         #เริมทำงานตอนมีทั้งเวลา และรู้จุดรถ
#         if axis_x and time_all:
#             #รู้จุด x ของรถตอนนี้
#             now_x = axis_x[-1]
#             #รู้เวลารถตอนนี้
#             now_time = float(time_all[-1])
#             #ค่าระยะห่างระหว่างรถกับเป้าหมาย
#             err = expect - now_x
#             #ค่าคงที่ที่เหมาะสม * ระยะห่างของรถกับเป้าหมาย
#             speed = err*p 
#             #ค่าที่ห่างกันของรถ โดยกันไม่ให้ติดลบด้วย Absolute
#             err_abs = abs(err)
#             #ค่ารถกับเป้าหมายใกล้เคียงกัน หยุดได้
#             if err_abs < 0.001:
#                 ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)   
#                 time.sleep(2)  
#                 # สลับค่าเป้าหมาย จาก 1 เป็น 0 หรือ 0 เป็น 1
#                 expect = toggle_target(expect)
#                 # รอบ
#                 times += 1
#                 #รถห่างกับเป้าหมาย 0.2 ให้ * 2.5 เพราะ ค่า err น้อยจนล้อไม่ขยับ
#             elif err_abs < 0.2 :
#                 speed = (err*p)*3
#             #ให้รถขยับ ไปตามค่า speed ที่ได้จาก err           
#             ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
            
#     ep_robot.close()
#     plt.figure(figsize=(6, 6))
#     plt.plot(time_all, target)
#     plt.plot(time_all, axis_x)
#     plt.title('Robot MAP')
#     plt.ylabel('X position')
#     plt.xlabel('Time')
#     plt.tight_layout()
#     plt.show()