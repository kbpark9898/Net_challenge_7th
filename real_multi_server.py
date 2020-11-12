# 서버컴퓨터에서 실행되는 멀티쓰레드 서버 코드입니다.
# 라즈베리파이로부터 지속적으로 GPS 신호를 수신합니다. 이때 GPS 신호는 NMEA GPGGA signal 로 넘어오게 되며, 이를 위도 및 경도 값으로 환산합니다.
# 위도 경도값으로 환산하여 저장한 위치 정보가 1000개 이상 모이면, 해당 위치 데이터를 k-means clustering 모듈로 넘겨 군집화하고 드론의 최적 위치를 계산합니다.
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
    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 
        try:
            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)
            if not data: 
                print('machine disconnected!')
                break
            client_socket.send(data) 
            if (data.decode() != "GPS is not working")and(data.decode()!=","):
                current_cordinate = (data.decode()).split(',')
                before_lat = float(current_cordinate[0])
                after_latdeg = before_lat//100
                after_latmin = ((before_lat-after_latdeg*100)*100000)//60
                after_lat = after_latdeg + after_latmin/100000
                current_cordinate[0]=copy.deepcopy(after_lat)
                before_lon = float(current_cordinate[1])
                after_londeg = before_lon//100
                after_lonmin = ((before_lon-after_londeg*100)*100000)//60
                after_lon = after_londeg + after_lonmin/100000
                current_cordinate[1]=copy.deepcopy(after_lon)
                print("Received data : ", str(current_cordinate[0])+','+str(current_cordinate[1]))
                cordinates.append(current_cordinate)
                count+=1
            if count>1000:
                result = KMC.cluster(cordinates)
                count = 0
                cordinates=[]
                print(result) 

        except ConnectionResetError as e:

            print('machine disconnected!')
            break
             
    client_socket.close() 

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

