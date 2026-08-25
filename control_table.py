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
    # MAX_VOLTAGE_LIMIT = 32        # [추천] 최대 인가 전압 한계 (단위: 0.1V)
    # MIN_VOLTAGE_LIMIT = 34        # [추천] 최소 인가 전압 한계 (단위: 0.1V)
    PWM_LIMIT = 36
    VELOCITY_LIMIT = 44
    MAX_POSITION_LIMIT = 48
    MIN_POSITION_LIMIT = 52
    # SHUTDOWN = 63                 # [추천] 하드웨어 에러 발생 시 토크 자동 차단 조건 설정

    # --- RAM Area (volatile, resets on power-cycle) ---
    TORQUE_ENABLE = 64
    LED = 65
    HARDWARE_ERROR_STATUS = 70

    # [추천] 게인 튜닝 레지스터 (Phase 4 PID 튜닝 및 진동 억제용)
    # VELOCITY_I_GAIN = 76          # 속도 I 게인
    # VELOCITY_P_GAIN = 78          # 속도 P 게인
    # POSITION_D_GAIN = 80          # 위치 D 게인 (손가락 관절 떨림/오버슈트 억제)
    # POSITION_I_GAIN = 82          # 위치 I 게인 (정상상태 오차 보정)
    POSITION_P_GAIN = 84          # 위치 P 게인
    # FEEDFORWARD_2ND_GAIN = 88     # 2차 피드포워드 게인 (가속도 보상)
    # FEEDFORWARD_1ST_GAIN = 90     # 1차 피드포워드 게인 (속도 보상)

    # [추천] 통신 안전 레지스터
    # BUS_WATCHDOG = 98             # 버스 워치독 타이머 (통신 단절 시 자동 토크 차단, 단위: 20ms)

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

    # --- EEPROM Area ---
    ID = 1
    BAUD_RATE = 1
    DRIVE_MODE = 1
    OPERATING_MODE = 1
    HOMING_OFFSET = 4
    TEMPERATURE_LIMIT = 1
    # MAX_VOLTAGE_LIMIT = 2
    # MIN_VOLTAGE_LIMIT = 2
    PWM_LIMIT = 2
    VELOCITY_LIMIT = 4
    MAX_POSITION_LIMIT = 4
    MIN_POSITION_LIMIT = 4
    # SHUTDOWN = 1

    # --- RAM Area ---
    TORQUE_ENABLE = 1
    LED = 1
    HARDWARE_ERROR_STATUS = 1

    # VELOCITY_I_GAIN = 2
    # VELOCITY_P_GAIN = 2
    # POSITION_D_GAIN = 2
    # POSITION_I_GAIN = 2
    POSITION_P_GAIN = 2
    # FEEDFORWARD_2ND_GAIN = 2
    # FEEDFORWARD_1ST_GAIN = 2

    # BUS_WATCHDOG = 1

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
