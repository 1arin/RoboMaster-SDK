import robomaster
import time
import math
from robomaster import robot
import matplotlib.pyplot as plt
import itertools

position_data = []  # Lists สำหรับเก็บข้อมูลตำแหน่งของหุ่นยนต์ที่ได้จาก sub_position
actual_distance = []  # Lists สำหรับเก็บระยะทางที่หุ่นยนต์เคลื่อนที่ไปได้


def sub_position_handler(position_info):
    global x  # ประกาศเป็น global เพื่อใช้นอกฟังก์ชัน
    x, y, z = position_info
    print(f"chassis position: x:{x}, y:{y}, z:{z}")
    position_data.append((x, y, z))
    actual_distance.append(abs(x) * 100)  # เก็บระยะทางเป็นหน่วยเซนติเมตร


if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis

    ep_chassis.sub_position(freq=10, callback=sub_position_handler)

    distance = 120  # กำหนดระยะทางเป็น 120 cm
    diameter = (5 * (2 * math.pi)) / 60  # คำนวณเส้นผ่านศูนย์กลางของล้อ
    slp = 2.5
    speed = distance / (diameter * slp)  # คำนวณความเร็ว

    direction = [1, -1]  # 1 for forward , -1 for backward
    diff = [0, 0]  # Lists สำหรับเก็บ index ของข้อมูลเพื่อคำนวณความต่าง
    total = []  # Lists สำหรับเก็บระยะทางที่ควรจะได้

    try:
        round = -1
        while True:  # กำหนดให้หุนยนต์ทำงานไปเรื่อยๆ
            round += 1
            sw = True if round % 2 == 0 else False  # เพื่อเช็คว่าเดินหน้าหรือถอยหลัง
            speed_multiple = direction[0] if sw else direction[-1]  # กำหนดทิศทาง
            print(f"direction round {round+1} = {speed_multiple}")
            ep_chassis.drive_wheels(
                w1=speed * speed_multiple,
                w2=speed * speed_multiple,
                w3=speed * speed_multiple,
                w4=speed * speed_multiple,
            )  # สั่งให้หุ่นยนต์เคลื่อนที่ตามความเร็วและทิศทางที่กำหนด

            time.sleep(slp)
            ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)  # หยุดการเคลื่อนที่ของหุ่นยนต์
            time.sleep(slp)

            # ปรับให้หุ่นยนต์กลับไปตำแหน่งเดิมถ้าเคลื่อนที่เกิน 1.2 m หรือ 120 cm
            if sw == True and x > 1.2:
                ep_chassis.move(x=x - 1.2, y=0, z=0, xy_speed=1).wait_for_completed()
            elif sw == False:
                ep_chassis.move(x=x - 0, y=0, z=0, xy_speed=1).wait_for_completed()

            diff.pop(0)
            diff.append(len(position_data))  # อัปเดตจำนวนความยาวล่าสุดใน position_data
            len_distance = diff[-1] - diff[0]  # คำนวณค่าผลต่าง
            val = distance if sw else 0
            total.append(
                [val for _ in range(len_distance)]
            )  # เพิ่มระยะทางที่คาดหวังลงไปใน Lists

            print("----------------------------------------------------------")

    except KeyboardInterrupt:  # หยุดการทำงานของลูป while เมื่อกด Ctrl C
        print("Exiting program")  # แสดงข้อความเมื่อโปรแกรมหยุดทำงาน

    ep_chassis.unsub_position()
    ep_robot.close()

    expected_distance = list(
        itertools.chain(*total)
    )  # รวมระยะทางที่คาดหวังทั้งหมดที่เก็บไว้ใน total ให้เหลือมิติเดียว
    print("expected_distance = {}".format(expected_distance))
    print("actual_distance = {}".format(actual_distance))

    print("#######################")

    # สร้างกราฟเปรียบเทียบระหว่างระยะทางที่คาดหวังและระยะทางที่ได้จริง
    plt.plot(expected_distance, label="Expected Distance")
    plt.plot(actual_distance, label="Actual Distance")
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("Distance (cm)")
    plt.title("Robot Position vs. Distance")
    plt.show()
