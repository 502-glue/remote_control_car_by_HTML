## RC_car_by_HTML
### 使用网页控制的无限距离小车
___
#### 一、概述:
&emsp;&emsp;网页点击按钮发出请求，经服务器处理转发给esp32控制小车，理论有网就可无限距离控制。
<img src="https://s2.loli.net/2023/01/30/lb37zghxHYVAKry.jpg" width="70%">
<img src="https://s2.loli.net/2023/01/30/TAeFhxrpDgqVa7y.jpg" width="70%">
<img src="https://s2.loli.net/2023/01/30/Ih8RYxKZtg1kDTC.png" width="70%">
___
#### 二、实现:
##### &emsp;1.网页端
&emsp;&emsp;网页通过AJAX发起GET请求，通过在请求连接中带的参数发出指令(如?move=left就是向左旋转)，后台用正则读取即可。

```
//javascript
var ajax = new XMLHttpRequest();
ajax.open('GET','http://localhost:端口号?move=left',true);
ajax.send();
```

&emsp;&emsp;实操时发现的问题：服务器设置为https协议，试图给服务器发送http协议浏览器会因为安全机制报错而发送失败（http基于UDP协议，只管发送，不管结果；https是http的安全版本，基于TCP，数据发送要经过三次握手保证连接安全可靠）如果改为发送https请求，后端则因为数据加密而读取到乱码。

&emsp;&emsp;解决方法：通过服务器设置nginx代理，将https请求代理到http即可。
在nginx.conf中server{}里添加：
```
# /usr/local/nginx/conf/nginx.conf
# car可以随便改名，保持网页js请求里一致即可
location /car {
            proxy_pass http://127.0.0.1:5000;
            index  index.html index.htm index.jsp;
}
```
&emsp;&emsp;设置后重启nginx
```
$ cd /usr/local/nginx/sbin
$ ./nginx -s reload
```
&emsp;&emsp;网页中改为:
```
ajax.open('GET','/car?move=left',true);
```
##### &emsp;2.服务端
&emsp;&emsp;服务端用socket接收来自网页的请求，处理后发送给小车。测试环境为python3.8，使用的都是原生的库，没有的话pip install安装即可，然后直接运行python文件。
```
$ python server.py
```
##### &emsp;3.小车端
&emsp;&emsp;单片机采用的是esp32DevKitC ，MicroPython编程，用两个L298N驱动四个电机，对于这个项目其实用一个驱动带两个电机就足够了，但手头没有多余的材料，就把以前做的拆了改做此项目了，引脚可以自定义，修改程序即可，注意部分引脚不支持PWM输出如34、35引脚。
![esp32-devkitC-v4-pinout.png](https://s2.loli.net/2023/01/30/2RIfSgJNwUuvkdV.png)
&emsp;&emsp;3节16850约12V，除直接给驱动供电外，还分出一路经降压为5V给esp32供电，但本人不建议这样做，当电机功率过大导致电池供电不足时可能导致单片机发生重启之类的问题，有条件可以单独再加个电源给IC供电，要注意共地。
&emsp;&emsp;单片机与服务端同样采用socket通信。遇到了个问题，就是服务端怎么知道单片机已经断开连接了，经网上查询得知单片机关闭套接口后服务端尝试从该端口读取数据会读到空白数据，只要判断收到数据长度为0时就可知小车已经断开连接了。
```
while True:
    recv_message = socket.recv(1024)
    if len(recv_message == 0):
        socket.close()
```
&emsp;&emsp;但脱离调试实装小车时发现给单片机直接断电后服务端接收不到任何信息，尝试发送也成功了，过了很久才报错，最后采用了时间戳判断，每隔两秒单片机给服务器发送一个信息，服务器接受消息后记录当前时间戳，服务器同样每两秒给单片机发送消息，每次发送比对当前时间与上次记录的时间戳，如果大于5秒就认为单片机已经断开了。
___
#### 三、体验:
&emsp;&emsp;服务器是位于广州的腾讯云，本人在北方，实际延迟大约一秒，速度还可以接受，但是点击过快似乎会出现丢包，车收不到停止指令，这时随便点击一个键可恢复。
##### ps
后续尝试做视频转发，可以在网页实时观看小车画面
