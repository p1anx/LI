import numpy as np
import binascii
import time
import matplotlib.pyplot as plt
import serial
from tqdm import trange


def lis3mdl_setup(port, baudrate):
    fs_4gauss = b"\x00"
    fs_8gauss = b"\x20"
    fs_12gauss = b"\x40"
    fs_16gauss = b"\x60"

    fs_setup = fs_16gauss  # 8 Gauss full scale

    ser = serial.Serial(port, baudrate)
    if not ser.is_open:
        print("Serial port is not open.")
        ser.open()
    try:
        while True:
            ser.write(fs_setup)
            if ser.in_waiting > 0:
                if ser.read(1) == b"\x12":
                    print("Full scale Setup success.\n")
                    break
        if fs_setup == fs_4gauss:
            return 6842
        elif fs_setup == fs_8gauss:
            return 3421
        elif fs_setup == fs_12gauss:
            return 2281
        elif fs_setup == fs_16gauss:
            return 1711
        else:
            return 6842
    except KeyboardInterrupt:
        ser.close()
        print("Serial port closed.")


def lis3mdl_period_read():
    start_time = time.time()
    txData = b"\xff"
    s_start = b"\x00"
    s_end = b"\x01"
    Bx_start = b"\x10"
    Bx_end = b"\x11"
    By_start = b"\x20"
    By_end = b"\x21"
    Bz_start = b"\x30"
    Bz_end = b"\x31"
    size = 1000  # 10 samples
    rxData = np.zeros(8, dtype=np.uint8)
    port = "COM9"
    baudrate = 115200
    ser = serial.Serial(port, baudrate)
    if not ser.is_open:
        print("Serial port is not open.")
        ser.open()
    try:
        BxBuf, ByBuf, BzBuf = [], [], []  # Buffer for Bx, By, Bz
        Bx, By, Bz = [], [], []  # Bx, By, Bz
        s = np.zeros(1, dtype=np.uint8)
        for i in trange(0, size):
            # rxData = b"\x00"
            time.sleep(0.001)
            # uart_time = time.time()
            ser.write(txData)
            while True:
                if ser.in_waiting > 0:
                    if not ser.read(1) == s_start:
                        pass
                    else:
                        rxData = ser.read(8)
                        break
            # uart_end = time.time()
            # print(uart_end - uart_time, end="\n")
            s = rxData[1] | rxData[0] << 8
            BxBuf = rxData[3] | rxData[2] << 8
            ByBuf = rxData[5] | rxData[4] << 8
            BzBuf = rxData[7] | rxData[6] << 8
            Bx.append(BxBuf)
            By.append(ByBuf)
            Bz.append(BzBuf)

        Bx = np.array(Bx)
        By = np.array(By)
        Bz = np.array(Bz)
        for i in trange(0, size):
            if Bx[i] > 32767:
                Bx[i] = Bx[i] - 65536  # Convert to signed 16-bit
            if By[i] > 32767:
                By[i] = By[i] - 65536
            if Bz[i] > 32767:
                Bz[i] = Bz[i] - 65536

        Bx = Bx / s  # Convert to Gauss
        By = By / s
        Bz = Bz / s

        x = range(0, size)
        plt.figure(1)
        plt.plot(x, Bx, label="Bx")
        plt.plot(x, By, label="By")
        plt.plot(x, Bz, label="Bz")

        plt.xlabel("x/Time")
        plt.ylabel("y/Gauss")
        plt.legend()
        # for i in range(0, size):
        #     print(Bx[i], end="\r", flush=True)
        #     time.sleep(0.1)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Run time: {run_time}s\n")
        print(f"Full scale: {s}")
        plt.show()

    except KeyboardInterrupt:
        ser.close()
        print("Serial port closed.")


# python setup the fullscale of lis3mdl
def lis3mdl_period_pysetup_fs():
    start_time = time.time()
    txData = b"\xff"
    s_start = b"\x00"
    s_end = b"\x01"
    Bx_start = b"\x10"
    Bx_end = b"\x11"
    By_start = b"\x20"
    By_end = b"\x21"
    Bz_start = b"\x30"
    Bz_end = b"\x31"
    size = 100  # 10 samples
    rxData = np.zeros(6, dtype=np.uint8)
    port = "COM9"
    baudrate = 115200
    # ***************************************
    s = lis3mdl_setup(port, baudrate)  # Full scale setup
    # ***************************************
    ser = serial.Serial(port, baudrate)
    if not ser.is_open:
        print("Serial port is not open.")
        ser.open()
    try:
        BxBuf, ByBuf, BzBuf = [], [], []  # Buffer for Bx, By, Bz
        Bx, By, Bz = [], [], []  # Bx, By, Bz
        for i in trange(0, size):
            # rxData = b"\x00"
            time.sleep(0.0001)
            ser.write(txData)
            while True:
                if ser.in_waiting > 0:
                    if not ser.read(1) == s_start:
                        pass
                    else:
                        rxData = ser.read(6)
                        break
            # s = rxData[1] | rxData[0] << 8
            BxBuf = rxData[1] | rxData[0] << 8
            ByBuf = rxData[3] | rxData[2] << 8
            BzBuf = rxData[5] | rxData[4] << 8
            Bx.append(BxBuf)
            By.append(ByBuf)
            Bz.append(BzBuf)

        Bx = np.array(Bx)
        By = np.array(By)
        Bz = np.array(Bz)
        for i in trange(0, size):
            if Bx[i] > 32767:
                Bx[i] = Bx[i] - 65536  # Convert to signed 16-bit
            if By[i] > 32767:
                By[i] = By[i] - 65536
            if Bz[i] > 32767:
                Bz[i] = Bz[i] - 65536

        Bx = Bx / s  # Convert to Gauss
        By = By / s
        Bz = Bz / s

        x = range(0, size)
        plt.figure(1)
        plt.plot(x, Bx, label="Bx")
        plt.plot(x, By, label="By")
        plt.plot(x, Bz, label="Bz")

        plt.xlabel("x/Time")
        plt.ylabel("y/Gauss")
        plt.legend()
        # for i in range(0, size):
        #     print(Bx[i], end="\r", flush=True)
        #     time.sleep(0.1)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Run time: {run_time}s\n")
        plt.show()

    except KeyboardInterrupt:
        ser.close()
        print("Serial port closed.")


def printf_test():
    ser = serial.Serial("COM9", 115200)
    if not ser.is_open:
        print("Serial port is not open.")
        ser.open()
    while True:
        if ser.in_waiting > 0:
            for i in trange(0, 9):
                print(ser.read(1), end="")
            break
    ser.close()


if __name__ == "__main__":
    print("hello\n")
    lis3mdl_period_read()
