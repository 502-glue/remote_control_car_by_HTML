import re
import socket
import threading
import time
import inspect
import ctypes

HOST = '127.0.0.1'
PORT = 5000        # 网页要绑定的端口
ESP32_PORT = 5001  # esp32要绑定的端口

esp32IsLink = False


def _async_raise(tid, exctype):

    tid = ctypes.c_long(tid)

    if not inspect.isclass(exctype):
        exctype = type(exctype)

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

    if res == 0:

        raise ValueError("invalid thread id")

    elif res != 1:

        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class socketRecv(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        global timeStamp
        while True:
            recv_mess = self.socket.recv(1024)
            timeStamp = int(time.time())
            # print(recv_mess)


class esp32Link(threading.Thread):
    def __init__(self):
        super().__init__()
        self.esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.esp32.bind(("", ESP32_PORT))
        self.esp32.listen(5)

    def run(self):
        global esp32socket
        global esp32IsLink
        global timeStamp

        def keep32Link(thread):
            global esp32IsLink
            nonlocal timer
            global timeStamp
            try:
                if (int(time.time()) - timeStamp) < 5:
                    esp32socket.send("you".encode("utf-8"))
                    timer = threading.Timer(2, keep32Link, args=[thread])
                    timer.start()
                else:
                    esp32IsLink = False
                    if thread.is_alive():
                        stop_thread(thread)
                    print("连接超时")
            except:
                esp32IsLink = False
                if thread.is_alive():
                    stop_thread(thread)
                print("连接超时")

        while True:
            esp32socket, client_info32 = self.esp32.accept()
            timeStamp = int(time.time())
            print(client_info32)
            esp32IsLink = True
            recvThread = socketRecv(esp32socket)
            recvThread.start()
            timer = threading.Timer(2, keep32Link, args=[recvThread])
            timer.start()

    def __del__(self):
        print("关闭套接字")
        self.esp32.shutdown(socket.SHUT_RDWR)
        self.esp32.close()


class webListen(threading.Thread):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(128)

    def run(self):
        global esp32socket
        global esp32IsLink
        while True:
            conn, addr = self.sock.accept()
            request = conn.recv(1024).decode("utf-8")
            conn.send(b'HTTP1.1 200 OK\r\nContent-Type: text/html;charset=utf8\r\n\r\n')
            cmd = re.search(r"car\?move=.+? ", request)
            if cmd is not None:
                cmd = cmd.group()
                if (len(cmd) > 13):
                    cmd = cmd[13:len(cmd) - 1]
                    if cmd == "state":
                        if esp32IsLink:
                            conn.send(b'esp_true')
                        else:
                            conn.send(b'esp_false')
                    else:
                        print('Connect by: ', addr)
                        print('cmd is', cmd)
                        if (esp32IsLink):
                            try:
                                esp32socket.send(cmd.encode("utf-8"))
                            except (TimeoutError, OSError):
                                print("连接超时")
                                esp32IsLink = False
                                conn.close()
                                continue
                        else:
                            print("esp32未连接")
                else:
                    conn.send(b'done')
            else:
                conn.send(b'done')

            conn.close()

    def __del__(self):
        print("关闭网页监听")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


esp32_linker = esp32Link()
esp32_linker.start()
web_listenr = webListen()
web_listenr.start()


