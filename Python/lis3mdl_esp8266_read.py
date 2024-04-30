import socket
import numpy as np
import time
import matplotlib.pyplot as plt


# def read_wifi_data():
# 这里放置读取WiFi数据的代码，具体取决于你要获取的数据类型

# ESP8266的IP地址和端口号
HOST = "192.168.4.1"  # ESP8266的默认AP IP
PORT = 333  # 端口号，需要与ESP8266上的服务器端口匹配


def esp_connected():
    try:
        n = 300
        data1 = np.zeros(n * 6)
        data2 = np.zeros(n * 6)
        data3 = np.zeros(n * 6)
        Bx1 = np.zeros(n)
        By1 = np.zeros(n)
        Bz1 = np.zeros(n)
        Bx2 = np.zeros(n)
        By2 = np.zeros(n)
        Bz2 = np.zeros(n)
        Bx3 = np.zeros(n)
        By3 = np.zeros(n)
        Bz3 = np.zeros(n)
        while True:
            # 创建一个socket连接
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                # if not s.recv(1) == b"0x19":
                #     continue
                data1 = s.recv(n * 6)
                data2 = s.recv(n * 6)
                data3 = s.recv(n * 6)
            #     arr = s.recv(10)
            # for i in range(10):
            #     print(f"arr[{i}]: {arr[i]}\n")

            for i in range(n):
                Bx1[i] = data1[0 + 6 * i] << 8 | data1[1 + 6 * i]
                By1[i] = data1[2 + 6 * i] << 8 | data1[3 + 6 * i]
                Bz1[i] = data1[4 + 6 * i] << 8 | data1[5 + 6 * i]
                if Bx1[i] > 32767:
                    Bx1[i] -= 65536
                if By1[i] > 32767:
                    By1[i] -= 65536
                if Bz1[i] > 32767:
                    Bz1[i] -= 65536
                Bx1[i] = Bx1[i] / 6842
                By1[i] = By1[i] / 6842
                Bz1[i] = Bz1[i] / 6842

                # print(f"Bx1: {Bx1[i]}, By1: {By1[i]}, Bz1: {Bz1[i]}\n")

                Bx2[i] = data2[0 + i * 6] << 8 | data2[1 + i * 6]
                By2[i] = data2[2 + i * 6] << 8 | data2[3 + i * 6]
                Bz2[i] = data2[4 + i * 6] << 8 | data2[5 + i * 6]
                if Bx2[i] > 32767:
                    Bx2[i] -= 65536
                if By2[i] > 32767:
                    By2[i] -= 65536
                if Bz2[i] > 32767:
                    Bz2[i] -= 65536
                Bx2[i] = Bx2[i] / 6842
                By2[i] = By2[i] / 6842
                Bz2[i] = Bz2[i] / 6842

                Bx3[i] = data3[0 + i * 6] << 8 | data3[1 + i * 6]
                By3[i] = data3[2 + i * 6] << 8 | data3[3 + i * 6]
                Bz3[i] = data3[4 + i * 6] << 8 | data3[5 + i * 6]
                if Bx3[i] > 32767:
                    Bx3[i] -= 65536
                if By3[i] > 32767:
                    By3[i] -= 65536
                if Bz3[i] > 32767:
                    Bz3[i] -= 65536
                Bx3[i] = Bx3[i] / 6842
                By3[i] = By3[i] / 6842
                Bz3[i] = Bz3[i] / 6842
            break

        Bx = np.concatenate((Bx1, Bx2, Bx3))
        By = np.concatenate((By1, By2, By3))
        Bz = np.concatenate((Bz1, Bz2, Bz3))
        plt.plot(Bx, label="Bx")
        plt.plot(By, label="By")
        plt.plot(Bz, label="Bz")
        plt.legend()
        plt.show()
        # print(f"Bx: {Bx}, By: {By}, Bz: {Bz}\n")
        print(f"length of data1: {len(Bx)}, length of data2: {len(data2)}\n")
    except KeyboardInterrupt:
        print("Program stopped by user")


def esp_connected1():
    try:
        group = 3
        n = 300  # data[group][n]
        data = np.zeros((group, n * 6), dtype=np.uint8)
        Bx = np.zeros((group, n))
        By = np.zeros((group, n))
        Bz = np.zeros((group, n))

        while True:
            # 创建一个socket连接
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))

                data1 = s.recv(n * 6)
                data2 = s.recv(n * 6)
                data3 = s.recv(n * 6)
                print(f"data1: {data1}\n")
                # for i in range(group):
                #     data1 = s.recv(n*6)
                #     data[i] = data1
                # # data[0] = s.recv(n*6)
                # # data[1] = s.recv(n*6)
                # # data[2] = s.recv(n*6)
                # print(f"data[0]: {data[0]}\n")

        #     for i in range(group):
        #         for j in range(n):
        #             Bx[i][j] = data[i][0 + 6*j] << 8 | data[i][1 + 6*j]
        #             By[i][j] = data[i][2 + 6*j] << 8 | data[i][3 + 6*j]
        #             Bz[i][j] = data[i][4 + 6*j] << 8 | data[i][5 + 6*j]

        #             Bx[i][j] = Bx[i][j] if Bx[i][j] <= 32767 else Bx[i][j] - 65536
        #             By[i][j] = By[i][j] if By[i][j] <= 32767 else By[i][j] - 65536
        #             Bz[i][j] = Bz[i][j] if Bz[i][j] <= 32767 else Bz[i][j] - 65536

        #             Bx[i][j] = Bx[i][j] / 6842
        #             By[i][j] = By[i][j] / 6842
        #             Bz[i][j] = Bz[i][j] / 6842

        #     break

        # Bx = np.concatenate((Bx[0], Bx[1], Bx[2]), axis=1)
        # By = np.concatenate((By[0], By[1], By[2]), axis=1)
        # Bz = np.concatenate((Bz[0], Bz[1], Bz[2]), axis=1)
        # plt.plot(Bx)
        # plt.show()
        # print(f"Bx: {Bx}, By: {By}, Bz: {Bz}\n")
        # print(f"length of data1: {len(Bx)}, length of data2: {len(data)}\n")
    except KeyboardInterrupt:
        print("Program stopped by user")


def esp8266_read():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    n = 10
    rxFlag = s.recv(1)
    rxFlag = int.from_bytes(rxFlag, byteorder="big")

    data = s.recv(n)
    print(f"rxFlag: {rxFlag}\n")
    for i in range(n):
        print(f"data[{i}]: {data[i]}\n")


if __name__ == "__main__":
    esp_connected()
