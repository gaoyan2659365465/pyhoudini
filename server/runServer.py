#服务器

import socket
import threading

BUF_SIZE = 16384
ip_port = (r"127.0.0.1", 11552)
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 先拿到套接字,指定个ipv4以及流式数据包
my_socket.bind(ip_port) # 绑定
my_socket.listen(10)
conn_list = []
conn_dt = {}

def tcplink(sock,addr):
    while True:
        try:
            recvdata=sock.recv(BUF_SIZE).decode('utf-8')
            if not recvdata:
                break
            try:
              exec(recvdata)
            except Exception as ex:
              print("出现如下异常%s"%ex)
              sock.send(bytes("出现如下异常%s"%ex, encoding="utf-8"))
              continue
            #sock.send(bytes("我是服务器你好", encoding="utf-8"))
        except:
            sock.close()
            print(addr,'offline')
            _index = conn_list.index(addr)
            conn_dt.pop(addr)
            conn_list.pop(_index)
            break

def recs():
    while True:
        print("等待客户端连接..")
        conn, address = my_socket.accept()
        print("连接到 .." + str(address))
        if address not in conn_list:
            conn_list.append(address)
            conn_dt[address] = conn
        #在这里创建线程，就可以每次都将socket进行保持
        t=threading.Thread(target=tcplink,args=(conn,address))
        t.start()

if __name__ == '__main__':
    t1 = threading.Thread(target=recs, args=(), name='rec')
    t1.start()