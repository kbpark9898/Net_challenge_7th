import socket 
from _thread import *
import k_means_clustering as KMC
import copy
# 쓰레드에서 실행되는 코드입니다. 
count =0
cordinates=[]
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다. 
def threaded(client_socket, addr): 
    global count
    global cordinates
    print('Connected by :', addr[0], ':', addr[1]) 



    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break

            print('Received from ' + addr[0],':',addr[1] , data.decode())

            client_socket.send(data) 
            if (data.decode() != "GPS is not working")and(data.decode()!=","):
                current_cordinate = (data.decode()).split(',')
                cordinates.append(current_cordinate)
                count+=1
            if count>1000:
                sum_x=0
                sum_y=0
                for i in cordinates:
                    before_lat = float(i[0])
                    before_lon = float(i[1])
                    after_latdeg = before_lat//100
                    after_latmin = ((before_lat-after_latdeg*100)*100000)//60
                    after_lat = after_latdeg + after_latmin/100000
                    i[0]=copy.deepcopy(after_lat)
                
                    before_lon = float(i[1])
                    after_londeg = before_lon//100
                    after_lonmin = ((before_lon-after_londeg*100)*100000)//60
                    after_lon = after_londeg + after_lonmin/100000
                    i[1]=copy.deepcopy(after_lon)
                result = KMC.cluster(cordinates)
                count = 0
                cordinates=[]
                print(result) 

        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0],':',addr[1])
            break
             
    client_socket.close() 

#'117.123.90.209'
HOST =''
PORT =34190

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')


# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True: 

    print('wait')


    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close() 

