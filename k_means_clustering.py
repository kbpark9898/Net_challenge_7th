# 드론의 최적 위치를 결정하기 위한 k-means clustering 알고리즘 모듈입니다.
# 멀티쓰레드 서버로부터 넘겨받은 위치정보를 3개의 집단으로 군집화하고, 군집의 중심을 도출합니다.
# 3개의 군집의 중심을 다시 평균내어 VR/AR 서비스를 위한 드론의 최적 위치를 결정합니다.

import numpy as np
import copy

def cluster(cordinates_Data):        
    geo = np.array(cordinates_Data)
    x=np.asmatrix(geo)
    print(x)
    k=3
    m=x.shape[0]

    mu = x[np.random.randint(0, m, k), :]
    print(mu)
  
    samecount = 0
    y = np.empty([m,1])
    for j in range(100):    
        for i in range(m):
            d0=np.linalg.norm(x[i,:]-mu[0,:],2)
            d1=np.linalg.norm(x[i,:]-mu[1,:],2)
            d2=np.linalg.norm(x[i,:]-mu[2,:],2)
            y[i]=np.argmin([d0, d1, d2])
        for i in range(k):
            mu[i, :] = np.mean(x[np.where(y==i)[0]], axis = 0)
        print("current step is... ", j)
        print(mu)

    x0 = x[np.where(y==0)[0]]
    x1=x[np.where(y==1)[0]]
    x2=x[np.where(y==2)[0]]
  
    print(mu)
    final_x = 0
    final_y =0
    for i in mu:
        final_x += i[:, 0]
        final_y += i[:, 1]

    print(final_x[0]/3, final_y[0]/3)
    return [final_x[0]/3, final_y[0]/3]
 