# Net 챌린지 시즌 7 - Hierarchical X
### Air network 기반 모바일 VR/AR 서비스 프로젝트
<br>
이 프로젝트는 Net 챌린지 시즌7 공모전에 참여하기위해 진행한 프로젝트 입니다. <br>User device - drone - air balloon - AR/VR server의 통신망을 구축하하여 사용자에게 장소의 제약 없이 초저지연 VR/AR 서비스를 제공해주도록 했습니다.
<br><br>
본 repo는 해당 프로젝트에서 사용자의 위치 정보를 사용해 VR/AR 서비스를 중계해줄 드론의 최적 위치 판별 알고리즘을 작성한 repo입니다.<br>python 언어를 사용해 개발을 진행했으며, 이 과정에서 k-means clustering 알고리즘을 활용해 사용자의 위치신호를 군집화하고, 그 군집의 중심 좌표를 구해 위도/경도값으로 환산했습니다. 
<br>사용자의 위치 신호는 직접 구현한 멀티스레드 서버로 수집했으며, 위치 신호를 대체하기 위해 라즈베리파이에 gps 센서를 부착하고 gps signal을 서버로 지속 송신하는 스크립트를 구동시켰습니다. 이 때, 서버와 라즈베리파이는 소켓통신을 통해 데이터를 주고받습니다.
<br><br>

#### 소스코드 구성
1. gps_client.py : 라즈베리파이에서 서버로 위치정보를 전송하기 위한 스크립트
2. k_means_clustering.py : 라즈베리파이에서 수집한 위치정보를 이용하여 위치정보를 군집화. VR/AR 서비스 중계 드론의 최적 위치 도추 ㄹ
3. real_multi_server.py : 라즈베리파이의 위치정보를 수집하고 k_means_clustering 모듈을 호출
