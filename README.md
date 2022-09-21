# 유저 투자 계좌 및 자산 내역 조회, 투자금 입금 API
원티드 프리온보딩 백엔드 기업 과제

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [과제 요구사항 분석](#과제-요구사항-분석)
3. [프로젝트 기술 스택](#프로젝트-기술-스택)
4. [개발 기간](#개발-기간)
5. [ERD](#ERD)
6. [API 목록](#API-목록)
7. [프로젝트 시작 방법](#프로젝트-시작-방법)


<br>


## 프로젝트 개요
Django Rest Framework 를 이용한 REST API 서버로

- 투자 내역 조회 (계좌명, 증권사, 계좌번호, 총 자산)
- 투자 상세 내역 조회 (계좌명, 증권사, 계좌번호, 총 자산, 투자 원금, 수익금, 총 수익률)
- 보유 종목 내역 조회 (보유 종목명, 종목 자산군, 평가 금액(수량 * 현재가), ISIN)
- 투자금 입금 
- 배치 스케쥴링

위 기능을 제공합니다.


<br>

## 과제 요구사항 분석
- ✅ 모든 기능은 로그인한 유저만 이용 가능
- ✅ 유저는 1인 1 계좌를 가질 수 있다는 가정 하에 기능 구현

### 1. 투자 내역 조회
- Authorization : `Bearer {token}`
- url: `GET /api/v1/accounts/`
- 인증된 유저의 투자 계좌 내역 조회 (계좌명, 증권사, 계좌번호, 총 자산)

    - `get_queryset`을 override 하여 해당 유저의 계좌를 조회
    - django ORM의 `annotate`를 이용하여 계좌를 외래키로 가지고 있는 보유 종목의 평가 금액 총합을 조회



### 2. 투자 상세 내역 조회
- Authorization : `Bearer {token}`
- url: `GET /api/v1/accounts/:id/`
- 인증된 유저의 투자 계좌 상세 내역 조회 (계좌명, 증권사, 계좌번호, 총 자산, 투자 원금, 수익금, 총 수익률)

    - `get_queryset`을 override 하여 해당 유저의 계좌를 조회
    - django ORM의 `annotate`를 이용하여 계좌를 외래키로 가지고 있는 보유 종목의 평가 금액 총합(총 자산)을 조회
    - `rest_framework.serailizers.SerializerMethodField` 를 이용하여 수익금과 수익률을 계산해서 반환


### 3. 보유 종목 내역 조회
- Authorization : `Bearer {token}`
- url: `GET /api/v1/assets/`
- 인증된 유저의 보유 종목 내역 조회 (보유 종목명, 종목 자산군, 평가 금액(수량 * 현재가), ISIN)

    - `get_queryset`을 override 하여 해당 유저의 계좌를 조회
    - django ORM의 `annotate`를 이용하여 계좌를 외래키로 가지고 있는 보유 종목의 평가 금액을 조회
    - 현재는 유저 당 1계좌를 가지고 있다고 가정했으므로 보유 종목 api를 나눴으나 여러 계좌 보유가 가능할 경우 <br>
      `accounts/:id/assets`로 변경 예정

### 4. 투자금 입금

- 투자금 입금은 2 phase 로 진행

#### 4-1. 거래 내역 유효성 검증 (phase 1)
- Authorization : `Bearer {token}`
- url: `POST /api/v1/transactions/validation/`
- 거래 내역 유효성 검증
- serializer의 `validate` 함수를 이용하여 입력 데이터의 'account_number'(계좌번호), 'user_name'(유저 이름)이 유효한지 확인
  - 해당 계좌가 존재하는지
  - 계좌의 소유주와 입력 데이터의 유저명이 같은지

- transaction info 데이터로 저장 후 생성된 identifier 반환

#### 4-2. 거래 내역 저장 (phase 2)
- Authorization : `Bearer {token}`
- url: `POST /api/v1/transactions/`
- 자산 업데이트 및 거래 내역 저장
1) serializer의 `validate` 함수를 이용하여 유효성 검증
  - 입력 데이터인 identifier에 일치하는 transaction info가 있는지 확인
  - 입력 데이터인 signature와 암호화한 transaction info가 같은지 확인

2) 자산 업데이트 및 거래 내역 저장
  - 유효성 검증에 통과하면 유저의 자산(투자원금)을 업데이트 하고 거래 내역은 transaction 데이터로 저장

- 암호화 방법 : `bcrypt` (추후 변경 예정)

### 5. 배치 스케쥴링
- 매일 오전 4시에 데이터 갱신 및 생성을 위한 배치 기능 구현
  - `apscheduler` 의 `BackgroundScheduler` 를 이용하여 배치 및 스케쥴링 기능 구현
  - 주어진 데이터는 ORM의 `update_or_create`를 이용하여 없는 데이터의 경우 생성, 있으면 갱신

### 기능 목록

| 버전   | 기능            | 세부 기능 | 설명                     | 상태  |
|------|---------------|-------|------------------------|-----|
| v1   | 투자 내역         | 조회    | 인증된 유저의 투자 계좌 내역 조회    | ✅   |
| -    | 투자 상세 내역      | 조회    | 인증된 유저의 투자 계좌 상세 내역 조회 | ✅   |
| -    | 보유 종목 내역      | 조회    | 인증된 유저의 보유 종목 내역 조회    | ✅   |
| -    | 투자금 입금(phase 1) | 생성    | 거래 내역 유효성 검증           | ✅   | 
| -    | 투자금 입금(phase 2) | 생성    | 유저 자산 업데이트 및 거래 내역 저장  | ✅   |
| -    | 배치 스케쥴링       | -     | 데이터 동기화를 위한 배치 스케쥴링    | ✅   |
| -    | 테스트           | 테스트   | 기능, 전체 테스트             | ✅   |

🔥 추가 기능 구현시 업데이트 예정

<br>


## 프로젝트 기술 스택

### Backend
<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB
<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools
<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord-5865F2?logo=Discord&logoColor=white">
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>



<br>


## 개발 기간
- 2022/09/16 - 2022/09/21 (4일)


<br>


## ERD
ERD 


<br>


## API 목록
API 명세 주소

<br>


## 프로젝트 시작 방법
1. 로컬에서 실행할 경우
```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b develop --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt
# 실행
python manage.py runserver
```

<br>
