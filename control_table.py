from enum import IntEnum


class ControlTable(IntEnum):
    """XL430-W250 Control Table addresses (Protocol 2.0)."""

    # --- EEPROM Area (Torque Enable must be 0 to write) ---
    ID = 7
    BAUD_RATE = 8
    DRIVE_MODE = 10
    OPERATING_MODE = 11
    HOMING_OFFSET = 20
    TEMPERATURE_LIMIT = 31
    PWM_LIMIT = 36
    VELOCITY_LIMIT = 44
    MAX_POSITION_LIMIT = 48
    MIN_POSITION_LIMIT = 52

    # --- RAM Area (volatile, resets on power-cycle) ---
    TORQUE_ENABLE = 64
    LED = 65
    HARDWARE_ERROR_STATUS = 70
    POSITION_P_GAIN = 84
    GOAL_PWM = 100
    GOAL_VELOCITY = 104
    PROFILE_ACCELERATION = 108
    PROFILE_VELOCITY = 112
    GOAL_POSITION = 116
    MOVING = 122
    PRESENT_LOAD = 126
    PRESENT_VELOCITY = 128
    PRESENT_POSITION = 132
    PRESENT_INPUT_VOLTAGE = 144
    PRESENT_TEMPERATURE = 146


class DataLength(IntEnum):
    """Byte length for each ControlTable entry."""

    ID = 1
    BAUD_RATE = 1
    DRIVE_MODE = 1
    OPERATING_MODE = 1
    HOMING_OFFSET = 4
    TEMPERATURE_LIMIT = 1
    PWM_LIMIT = 2
    VELOCITY_LIMIT = 4
    MAX_POSITION_LIMIT = 4
    MIN_POSITION_LIMIT = 4

    TORQUE_ENABLE = 1
    LED = 1
    HARDWARE_ERROR_STATUS = 1
    POSITION_P_GAIN = 2
    GOAL_PWM = 2
    GOAL_VELOCITY = 4
    PROFILE_ACCELERATION = 4
    PROFILE_VELOCITY = 4
    GOAL_POSITION = 4
    MOVING = 1
    PRESENT_LOAD = 2
    PRESENT_VELOCITY = 4
    PRESENT_POSITION = 4
    PRESENT_INPUT_VOLTAGE = 2
    PRESENT_TEMPERATURE = 1


class OperatingMode(IntEnum):
    """Values for ControlTable.OPERATING_MODE."""

    VELOCITY = 1
    POSITION = 3
    EXTENDED_POSITION = 4
    PWM = 16
