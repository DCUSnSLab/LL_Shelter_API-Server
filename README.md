# TODO

기존 Livinglab Main-Shelter 간 구성의 경우 localhost에서의 동작을 전제로 만들어졌습니다.
따라서 아래 명시된 파일들에 대한 코드 수정 및 Main - Shelter 간 관계를 명시하기 위한 다른 방안이 필요하빈다.

local_shelter_server/static/assets/app.js:  // let response = await fetch('http://localhost:8000/image', {
local_shelter_server/ShelterLogin/views.py:# db = pymysql.connect(host='localhost', # DB 주소
local_shelter_server/ShelterLogin/views.py:    CheckShelter = pymysql.connect(host='localhost',  # DB 주소
local_shelter_server/local_shelter_server/settings.py:                         ,'http://localhost:3000'
local_shelter_server/local_shelter_server/settings.py:                         ,'http://localhost:3001']
local_shelter_server/Updator/ShelterUpdator.py:CMS_MAIN_SERVER_DB = pymysql.connect(host='localhost',  # DB 주소
local_shelter_server/Updator/ShelterUpdator.py:LOCAL_SHELTER_SERVER_DB = pymysql.connect(host='localhost',  # DB 주소
