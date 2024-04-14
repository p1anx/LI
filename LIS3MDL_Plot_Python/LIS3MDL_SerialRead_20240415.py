import numpy as np
import serial
import time
import matplotlib.pyplot as plt
from tqdm import trange

port = "COM20"
baudrate = 115200
def rxTest():

    start_time = time.time()
    ser = serial.Serial(port, baudrate)
    
    try:
        rxFlag = b"\x19"
        dataSize = 1000
        Bx = np.zeros(dataSize)
        By = np.zeros(dataSize)
        Bz = np.zeros(dataSize)
        while True:
            if not ser.read(1) == rxFlag:
                continue
            rxdata = ser.read(dataSize*6)
            for i in trange(dataSize):
                Bx[i] = rxdata[i*6+0] << 8 | rxdata[i*6+1]
                By[i] = rxdata[i*6+2] << 8 | rxdata[i*6+3]
                Bz[i] = rxdata[i*6+4] << 8 | rxdata[i*6+5]
                if Bx[i] > 32767:
                    Bx[i] = Bx[i] - 65536
                if By[i] > 32767:
                    By[i] = By[i] - 65536
                if Bz[i] > 32767:
                    Bz[i] = Bz[i] - 65536
                Bx[i] = Bx[i]/6842
                By[i] = By[i]/6842
                Bz[i] = Bz[i]/6842
            break
            # print(f"Received: {rxdata.hex()}", end = "\n", flush = True)

        # plot Bx, By, Bz
        x = range(0, dataSize)
        plt.plot(x, Bx, label = "Bx")
        plt.plot(x, By, label = "By")
        plt.plot(x, Bz, label = "Bz")
        plt.legend()
        end_time = time.time()
        print(f"Time taken: {end_time - start_time}")
        plt.show()

    except KeyboardInterrupt:   
        ser.close()
        print("Serial port closed")
def test():
    ser = serial.Serial(port, baudrate)
    try:
        while True:
            if not ser.read(1) == b'\x12':
                continue
            rxdata = ser.read(36)
            time.sleep(1)
            for i in range(6):
                print(f"a[0][{i}] = {rxdata[i*6+0]}\n")
                print(f"a[1][{i}] = {rxdata[i*6+1]}\n")
                print(f"a[2][{i}] = {rxdata[i*6+2]}\n")
                print(f"a[3][{i}] = {rxdata[i*6+3]}\n")
                print(f"a[4][{i}] = {rxdata[i*6+4]}\n")
                print(f"a[5][{i}] = {rxdata[i*6+5]}\n")
    except KeyboardInterrupt:
        ser.close()
        print("Serial port closed")
if __name__ == "__main__":
    rxTest()
    # test()
    print("Hello, World!")