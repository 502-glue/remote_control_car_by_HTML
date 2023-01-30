from machine import Pin, SoftI2C, PWM, Timer
import socket
import time
import network
import machine
import re
import _thread


fl_pwm = PWM(Pin(13))
fr_pwm = PWM(Pin(25))
bl_pwm = PWM(Pin(32))
br_pwm = PWM(Pin(33))

fl_pwm.freq(1000)
fr_pwm.freq(900)
bl_pwm.freq(800)
br_pwm.freq(700)

f_in1 = Pin(26, Pin.OUT)
f_in2 = Pin(27, Pin.OUT)
f_in3 = Pin(14, Pin.OUT)
f_in4 = Pin(12, Pin.OUT)

b_in1 = Pin(22, Pin.OUT)
b_in2 = Pin(21, Pin.OUT)
b_in3 = Pin(23, Pin.OUT)
b_in4 = Pin(19, Pin.OUT)

f_in1.value(0)
f_in2.value(0)
f_in3.value(0)
f_in4.value(0)
b_in1.value(0)
b_in2.value(0)
b_in3.value(0)
b_in4.value(0)


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('正在连接网络...')
        wlan.connect('wifi名', '密码')
        print("正在连接...", end='')
        while not wlan.isconnected():
            print('.', end='')
            time.sleep(1)
        print('\n连接成功!')
    print('network config:', wlan.ifconfig())
    return wlan.ifconfig()[0]


def move(cmd):
    if cmd == "forward":
        f_in1.value(0)
        f_in2.value(1)
        f_in3.value(0)
        f_in4.value(1)
        b_in1.value(0)
        b_in2.value(1)
        b_in3.value(0)
        b_in4.value(1)
    elif cmd == "back":
        f_in1.value(1)
        f_in2.value(0)
        f_in3.value(1)
        f_in4.value(0)
        b_in1.value(1)
        b_in2.value(0)
        b_in3.value(1)
        b_in4.value(0)
    elif cmd == "left":
        f_in1.value(0)
        f_in2.value(1)
        f_in3.value(1)
        f_in4.value(0)
        b_in1.value(1)
        b_in2.value(0)
        b_in3.value(0)
        b_in4.value(1)
    elif cmd == "right":
        f_in1.value(1)
        f_in2.value(0)
        f_in3.value(0)
        f_in4.value(1)
        b_in1.value(0)
        b_in2.value(1)
        b_in3.value(1)
        b_in4.value(0)
    elif cmd == "stop":
        f_in1.value(0)
        f_in2.value(0)
        f_in3.value(0)
        f_in4.value(0)
        b_in1.value(0)
        b_in2.value(0)
        b_in3.value(0)
        b_in4.value(0)


def link_server():
    while True:
        client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_s.connect(("服务器ip", 5001))

        timer = Timer(1)
        timer.init(period=2000, mode=Timer.PERIODIC, callback=lambda t: client_s.send("hey".encode("utf-8")))

        while True:
            try:
                recv_content = client_s.recv(1024).decode('utf-8')
                print(recv_content)
                move(recv_content)

            except Exception as ret:
                print("ERROR:", ret)

        client_s.close()
        print("关闭套接字")


def main():
    fl_pwm.duty(512)
    fr_pwm.duty(512)
    bl_pwm.duty(512)
    br_pwm.duty(512)
    ip = do_connect()
    print("ip地址是：", ip)
    link_server()


if __name__ == "__main__":
    main()

