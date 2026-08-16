import signal
import sys
import time

def graceful_shutdown(signum, frame):
    global portHandler

    print(f"\n[!] Signal {signum} received. Cleaning up resources...", flush=True)
    if portHandler.is_open:
        print("Closing port...", flush=True)
        portHandler.closePort()
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)

from dynamixel_sdk import *

PROTOCOL_VERSION        = 2.0

BAUDRATE                = 57600
DEVICENAME              = '/dev/tty.usbserial-FTBINA6H'

portHandler = PortHandler(DEVICENAME)

packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    sys.exit()


if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    sys.exit()

print("\n\n")

while True:
    dxl_data_list, dxl_comm_result = packetHandler.broadcastPing(portHandler)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    print("Detected Dynamixel :")
    for dxl_id in dxl_data_list:
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list.get(dxl_id)[0], dxl_data_list.get(dxl_id)[1]))

    time.sleep(1)
