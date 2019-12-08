"""
任务：写一个web服务器
1、导入模块socket\threading\sys
2、建立套接字对象
3、地址重写
3、绑定端口号
4、设置监听，套接字由主动变被动
5、接受浏览器的链接accept
6、接收浏览器的请求  第三次修改....
8、查找请求目录
9、发送响应报文 第二次修改....
10、结束与浏览器的链接 第一次修改...
"""
import socket
import threading
import sys
from application import app

class HttpServer(object):
    """服务器类"""

    def __init__(self):

        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        self.tcp_server_socket.bind(("", 8080))

        self.tcp_server_socket.listen(128)

    def request_client(self, new_client_socket, ip_port):
        print("浏览器上线：", ip_port)
        request_data = new_client_socket.recv(1024)
        # print(request_data)

        if not request_data:
            print("浏览器下线", ip_port)
            new_client_socket.close()
            return

        response_data = app.application("./static", request_data, ip_port)

        new_client_socket.send(response_data)

        new_client_socket.close()


    def start(self):

        while True:
            new_client_socket, ip_port = self.tcp_server_socket.accept()

            thread_client = threading.Thread(target=self.request_client, args=(new_client_socket, ip_port))

            thread_client.setDaemon(True)

            thread_client.start()


if __name__ == '__main__':
    """启动"""

    http_server_socket = HttpServer()

    http_server_socket.start()

