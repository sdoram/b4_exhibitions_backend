# Project-Exhibition-Backend - <a href="https://github.com/sdoram/b4_exhibitions_frontend">Frontend 바로가기!</a>
DRF를 기반으로 Machine Learning 기능을 추가한 각종 전시 및 체험활동 예약 및 추천 커뮤니티 사이트
<br>
<br>

## 🖥️ 프로젝트 소개 - <a href="https://www.notion.so/S-A-d04b7899646e45e59da17fbec7cdacfb">S.A. 바로가기!</a>
지금은 전시상황! 프로젝트는 서울 공공서비스 체험, 전시, 그리고 다양한 활동들을 한 눈에 볼 수 있는 웹사이트입니다. 추천 기능을 통해 현재 보고 있는 활동과 비슷한 활동을 추천 받을 수 있고, 해당 활동에 대한 후기를 확인할 수 있습니다. 또한 댓글을 통해 다양한 활동을 함께 할 친구를 구할 수 있는 공간이 마련되어 있습니다.
<br>
<br>

## 🕰️ 개발 기간
* 23.06.05 - 23.06.30
<br>
<br>

## 🧑‍🤝‍🧑 팀원 구성 및 역할 분담
- 팀장😄 <a href="https://github.com/sdoram">김세만</a><br>
[BE] 페이지네이션(전시 전체, 리뷰, 동행구하기), 검색 기능   
[FE] js 연결(메인, 백오피스 메인, 로그인, 회원가입, 회원정보 조회 및 수정, 회원탈퇴)
- 팀원😄 <a href="https://github.com/goodminjeong">구민정</a><br> 
[BE] 동행 구하기/신청하기 CRUD, 전시 추천 기능  
[FE] js 연결(전시 상세페이지, 추천바, 리뷰 CRUD, 동행 구하기 CRUD)
- 팀원😄 <a href="https://github.com/OCmonet">이동현</a><br>
[BE] 회원가입, 로그인, 유저 정보 조회 및 수정, 회원 탈퇴   
[FE] html, css 전체 담당
- 팀원😄 <a href="https://github.com/mijinleee">이미진</a><br>
[BE] 리뷰 CRUD, 배포  
- 팀원😄 <a href="https://github.com/banghyunjae">방현재</a><br>
[BE] 전시 CRUD, 오픈API 활용하여 전시 데이터 DB에 담기 
<br>
<br>

## ⚙️ 개발 환경 (Tech Stack)
- **Language** : `Python 3.8.10`
- **IDE** : `Visual Studio Code`
- **Framework** : `Django-Rest-Framework 3.14.0`
- **Database** : `PostgreSQL 15`
- **Packaging-tool** : `requirements.txt`
- **FRONTEND** : <a href="https://github.com/sdoram/b4_exhibitions_frontend">b4_exhibitions_frontend</a>

### <b>🦊 BE 😼</b>

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"> <img src="https://img.shields.io/badge/dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=white"> <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<br>
<br>

### <b>😈 FE 👽</b>

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
<br>
<br>

### <b>🦝ETC🦄</b>

<img src="https://img.shields.io/badge/visualstudiocode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"/> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white"> <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white"/> <img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white"/> <img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=white"/>
<br>
<br>

## 🔑 프로젝트 설치 및 실행 방법
#### 깃허브 클론하기
```bash
$ git init
$ git clone <레파지토리 주소>
```
#### 패키지 밎 라이브러리 설치
```bash
$ pip install -r requirements.txt
```
#### .env에 추가(DB 연동을 위한 작업)
```.env
$ DB_ENGINE="django.db.backends.postgresql"
$ DB_NAME="데이터베이스 이름"
$ DB_USER="유저 이름"
$ DB_PASSWORD="비밀번호"
$ DB_HOST="호스트 주소 또는 localhost"
$ DB_PORT=포트번호
```
#### DB 연동
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
#### 관리자 계정 생성
```bash
$ python manage.py createsuperuser
```
#### 필드 최대 길이 조정
```sql
$ ALTER TABLE exhibitions_exhibition ALTER COLUMN content TYPE VARCHAR (30000);
$ ALTER TABLE exhibitions_exhibition ALTER COLUMN image TYPE VARCHAR (200);
$ ALTER TABLE exhibitions_exhibition ALTER COLUMN direct_url TYPE VARCHAR (200);
```
#### 전시 데이터 DB에 저장
```bash
$ python manage.py loaddata exhibitions/utils_data.json
```
#### 백엔드 서버 실행
```bash
$ python manage.py runserver
```
#### 프론트엔드 라이브서버 실행
```
$ vscode 확장팩 <Live Server> 설치
$ index.html에서 마우스 우클릭 후 Open with Live Server 클릭(단축키 Alt+L+O)
```
<br>
<br>

## 📌 주요 기능
#### 로그인 
- DB값 검증
- 로그인 시 JWT Token 생성
- 소셜 로그인(구글)

#### 회원가입 
- Email, nickname 중복방지

#### 회원탈퇴
- 회원탈퇴 시 is_active 상태가 true에서 false로 전환

#### 마이페이지
- 프로필 정보 수정(프로필 사진, 비밀번호, 닉네임, 성별, 자기소개)
- 좋아요 누른 전시 조회
- 사용자 본인의 프로필만 수정, 회원탈퇴 버튼이 보임

#### 좋아요 기능
- 메인페이지 또는 상세페이지에서 좋아요 클릭 가능
- 좋아요 누른 게시글은 마이페이지에서 확인 가능함
- 비로그인 사용자는 좋아요 누를 수 없음

#### 메인 페이지 
- 검색 기능 : 게시글의 제목, 내용, 장소를 기준으로 검색할 수 있음
- 전시 종료 날짜가 빠른순으로 정렬되어 있음
- 종료된 전시는 메인페이지에서 확인할 수 없지만 검색 또는 좋아요 누른 게시글 확인 가능
- 상세보기 클릭 시 상세페이지로 이동
- 예약하기 클릭 시 예약페이지로 이동

#### 백오피스 메인 페이지 
- is_admin = True인 사용자가 로그인 시 백오피스 메인페이지로 연결됨
- 수정, 삭제 가능하며 이미지 클릭 시 상세페이지로 이동함
- 전시 등록 가능함

#### 전시 등록, 수정 및 삭제
- 게시글 수정 시 원래 내용 불러오는 기능
- 수정하지 않은 내용은 그대로 다시 DB에 저장됨
- 관자리자만 등록, 수정, 삭제 가능

#### 상세 페이지
- 전시 제목, 장소, 날짜, 내용, 이미지 확인 가능
- 우측에 해당 전시와 비슷한 전시를 추천하는 추천 바가 있음
- 이용후기 버튼 클릭 시 후기 작성하기 버튼과 이용후기 목록 뜸
- 동행 구해요! 버튼 클릭 시 동행구하기 버튼과 동행 구하는 글 목록이 뜸
- 예약하기 버튼 클릭 시 예약페이지로 이동함

#### 추천바
- 현재 보고 있는 전시와 비슷한 키워드를 가진 5개의 전시를 추천함
- 클릭 시 해당 전시의 상세페이지로 이동함
- 제목 부분 부터 예약하기 버튼 사이에 추천바가 뜨고 스크롤이 맨 위나 예약하기 버튼 아래에 위치할 땐 추천바가 사라짐

#### 이용후기
- 이미지, 별점, 내용 작성 가능
- 수정 시 원래 데이터를 확인할 수 있음
- 삭제 시 "정말 삭제하시겠습니까?" 확인 창이 뜨고 확인 누르면 삭제, 취소 누르면 삭제되지 않음

#### 동행 구해요!
- 목표인원, 동행시간, 내용 작성 가능
- 수정 시 원래 데이터를 확인할 수 있음
- 삭제 시 "정말 삭제하시겠습니까?" 확인 창이 뜨고 확인 누르면 삭제, 취소 누르면 삭제되지 않음


***
💜 [ERD](https://www.erdcloud.com/d/ftoBoJc3WCLvnTqca)
------
자세한 내용은 ERD를 클릭해 주세요!
![image](https://github.com/sdoram/b4_exhibitions_frontend/assets/125722304/cca145f2-88af-4a2b-bc30-5205965c768d)

***
💚 [API 명세](https://www.notion.so/S-A-d04b7899646e45e59da17fbec7cdacfb?pvs=4#1d8b724ee81745669e6042a4c6076517)
------
API 명세를 클릭해 주세요!