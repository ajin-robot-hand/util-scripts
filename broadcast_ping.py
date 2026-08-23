from dynamixel_sdk import *
import argparse
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

def get_default_port() -> str:
    if sys.platform.startswith('win'):
        return 'COM3'  # Windows 환경 기본값
    elif sys.platform.startswith('darwin'):
        return '/dev/tty.usbserial-FTBINA6H'  # Mac 환경 기본값 (기존 하드코딩 설정)
    else:
        return '/dev/ttyUSB0'  # Linux / WSL 환경 기본값


parser = argparse.ArgumentParser(description="Broadcast Ping Dynamixel Servos.")
parser.add_argument(
    "-p", "--port",
    default=get_default_port(),
    help="Serial port device name (e.g., /dev/ttyUSB0 for WSL/Linux, COM3 for Windows, /dev/tty.usbserial-* for Mac)"
)
parser.add_argument(
    "-b", "--baudrate",
    type=int,
    default=57600,
    help="Baud rate (default: 57600)"
)
args = parser.parse_args()

PROTOCOL_VERSION        = 2.0
BAUDRATE                = args.baudrate
DEVICENAME              = args.port

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
