import asyncio
from robomaster import robot

async def main():
    # Initialize the robot with USB connection
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")

    # Start camera stream
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream()

    # Wait for 5 seconds without blocking the event loop
    await asyncio.sleep(5)

    # Stop camera stream
    ep_camera.stop_video_stream()

    # Close connection
    ep_robot.close()

if __name__ == "__main__":
    asyncio.run(main())
