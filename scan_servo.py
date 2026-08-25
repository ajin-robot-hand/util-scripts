from dynamixel_sdk import *

import sys, signal

from control_table import ControlTable, DataLength


def graceful_shutdown(signum, frame):
    global portHandler

    print(f"\n[!] Signal {signum} received. Cleaning up resources...", flush=True)
    if portHandler.is_open:
        print("Closing port...", flush=True)
        portHandler.closePort()
    sys.exit(0)

def sendTxRx(packet:Protocol2PacketHandler, port:PortHandler, nByte:int, dxl_id:int, addr:int) -> tuple[bool, int]:
    status: bool = False

    if nByte == 1:
        data, result, err = packet.read1ByteTxRx(port, dxl_id, addr)
    elif nByte == 2:
        data, result, err = packet.read2ByteTxRx(port, dxl_id, addr)
    elif nByte == 4:
        data, result, err = packet.read4ByteTxRx(port, dxl_id, addr)
    else:
        raise ValueError(f"Unsupported number of byte {nByte}")

    if err != 0:
        raise Exception(packet.getRxPacketError(err))
    elif result != COMM_SUCCESS:
        raise Exception(packet.getTxRxResult(result))
    else:
        status = True

    return status, data
    

signal.signal(signal.SIGINT, graceful_shutdown)

import argparse

def get_default_port() -> str:
    if sys.platform.startswith('win'):
        return 'COM3'  # Windows 환경 기본값
    elif sys.platform.startswith('darwin'):
        return '/dev/tty.usbserial-FTBINA6H'  # Mac 환경 기본값 (기존 하드코딩 설정)
    else:
        return '/dev/ttyUSB0'  # Linux / WSL 환경 기본값


parser = argparse.ArgumentParser(description="Scan Dynamixel Servos across baudrates and IDs.")
parser.add_argument(
    "-p", "--port",
    default=get_default_port(),
    help="Serial port device name (e.g., /dev/ttyUSB0 for WSL/Linux, COM3 for Windows, /dev/tty.usbserial-* for Mac)"
)
parser.add_argument(
    "--max-id",
    type=int,
    default=10,
    help="Maximum Dynamixel ID to scan (default: 10)"
)
args = parser.parse_args()

PROTOCOL_VERSION = 2.0
BAUDRATES = [57600, 115200, 230400, 500000, 576000, 921600, 1000000, 1152000]
DEVICENAME = args.port
ID = args.max_id

# name -> [address, nByte, print formatter]
STATUS_FIELDS = {
    "Position": [ControlTable.PRESENT_POSITION, DataLength.PRESENT_POSITION, lambda v: f"  Position: {v}"],
    "Velocity": [ControlTable.PRESENT_VELOCITY, DataLength.PRESENT_VELOCITY, lambda v: f"  Velocity: {v}"],
    "Voltage": [ControlTable.PRESENT_INPUT_VOLTAGE, DataLength.PRESENT_INPUT_VOLTAGE, lambda v: f"  Voltage: {v / 10.0} V"],
    "Temperature": [ControlTable.PRESENT_TEMPERATURE, DataLength.PRESENT_TEMPERATURE, lambda v: f"  Temperature: {v} C"],
    "Moving": [ControlTable.MOVING, DataLength.MOVING, lambda v: f"  Moving: {bool(v)}"],
    "Hardware Error Status": [ControlTable.HARDWARE_ERROR_STATUS, DataLength.HARDWARE_ERROR_STATUS, lambda v: f"  Hardware Error Status: {v}"],
}

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if not portHandler.openPort():
    print("Could not opening a port")
    sys.exit()

for b in BAUDRATES:
    if not portHandler.setBaudRate(b):
        print(f"Could not set a baudrate to {b}")
    for i in range(ID + 1):
        model_number, result, error = packetHandler.ping(portHandler, i)

        if error != 0:
            print(packetHandler.getRxPacketError(error))
        elif result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(result))
            pass
        else:
            print(f"[ID:{i:03d}] model number: {model_number} at baudrate {b}")

            try:
                for addr, n_byte, fmt in STATUS_FIELDS.values():
                    _, value = sendTxRx(packetHandler, portHandler, n_byte, i, addr)
                    print(fmt(value))
            except:
                portHandler.closePort()
                sys.exit()

portHandler.closePort()
