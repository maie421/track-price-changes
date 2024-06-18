# track-price-changes
쿠팡 밀키트 가격 변동 추적 사이트

## 프로젝트 목적
쿠팡 파트너스 활동을 위해 해당 사이트 개발을 진행하였습니다.<br>
쿠팡 로켓프레시에 있는 상품 가격 변화를 알 수 있도록 하는 것을 목표로 합니다.

## cypress
https://github.com/maie421/track-price-cypress

## 프로젝트 기간
2023.12.02 ~ 2024.01.12

### Server
ubuntu 22.04<br>
Core : 1vCore<br>
Memory : 1GB<br>
Storage : SSD 25GB<br>

### 스펙
- flask : 3.0.0 <br>
평균가, 역대최고가, 역대최저가를 계산해야 하기 때문에 통계 라이브러리가 많은 파이썬 언어로 선택을 했고 <br>
장고, flask , fast api 중 flask 가 웹애플리케이션 개발과 학습 곡선이 낮고 타 프레임워크 보다 가벼워 선택하게 되었습니다. <br>
- mysql8 <br>
- ngnix
- ChatGPT3.5

로켓프레시에 있는 상품들을 크롤링하여 데이터를 저장을 할려고 하였지만
1. 해당 데이터들을 크롤링 하는데 오래 걸리지 않을까?
2. 처음 부터 많은 데이터들을 서버가 버틸 수 있을까?

에 대한 의문점이 생겨 시장이 커지고 있는 밀키트 제품을 선택하여 데이터 수집하기로 결정하였습니다.<br>
#### 참조 
- https://mobile.newsis.com/view.html?ar_id=NISX20230106_0002150006#_PA

## 1차 프로토타입 배포 
2023.12.02 ~ 2023.12.13<br>

### 배포 구조
<img width="698" alt="image" src="https://github.com/maie421/track-price-changes/assets/35258834/4f3cf9b2-db79-41aa-8445-1a37e647c4d1">

### 기능
1. 로켓프레시 밀키트 제품 크롤링 (2시간 마다 수집)
2. 메인페이지
   - 할인율이 높은 제품
   - 검색
3. 상세페이지
   - 평균가, 역대 최고가, 역대 최저가, 현재 가격
   - 일별로 최저가, 최고가를 보여주는 그래프
4. 카테고리별 제품
   
### UI
### 메인 페이지
<img width="600" alt="image" src="https://github.com/maie421/track-price-changes/assets/35258834/e89e3d2e-e7eb-4f30-95b3-d2977e44a264">

### 상세 페이지
<img width="600" alt="image" src="https://github.com/maie421/track-price-changes/assets/35258834/3518e7b2-7473-4b15-a894-91c92eb88dd7">

## 2차 프로토타입 배포 
1. ngnix
2. 이 상품과 비슷한 상품
3. 챗봇
  - 대화중 사이트에 해당 상품이 있다면 상품 알려줌

<img width="500" alt="스크린샷 2024-01-21 오후 11 22 21" src="https://github.com/maie421/track-price-changes/assets/35258834/2f672c20-1612-4b7f-aa38-c0bb91084869">
<img width="500" alt="스크린샷 2024-01-21 오후 11 25 28" src="https://github.com/maie421/track-price-changes/assets/35258834/825198be-e4c6-4997-9399-7e35b9ade833">




