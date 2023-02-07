from django.shortcuts import render, redirect
import pymysql, psycopg2, json, os
from pathlib import Path

# 일단 같은 로컬 서버 내에서 DB 연결 수행
# 하지만 외부 쉘터 DB에서 접근해야함으로 이렇게하면 안됨
# db = pymysql.connect(host='localhost', # DB 주소
#                      port=3306,         # DB port
#                      user='master600', # DB 관리자 계정
#                      passwd='0110',     # DB 접속 비밀번호
#                      db='cms_main_server_06', # DB 명
#                      charset='utf8',
#                      cursorclass=pymysql.cursors.DictCursor)



def CheckShelter(name, number):

    # 메인서버 DB접속, 보안문제가 있음
    '''
    CheckShelter = pymysql.connect(host='localhost',  # DB 주소
                                   port=3306,  # DB port
                                   user='main01',  # DB 관리자 계정
                                   passwd='main01',  # DB 접속 비밀번호
                                   db='cms_main',  # DB 명
                                   charset='utf8', )
    '''
    cms_main_ip = os.environ['CMS_MAIN_IP']
    cms_main_dbpw = None # 

    CheckShelter = psycopg2.connect(host=cms_main_ip,  # DB 주소
                                   port=5432,  # DB port
                                   user='main',  # DB 관리자 계정
                                   password='20121208',  # DB 접속 비밀번호
                                   dbname='cms_main_server',  # DB 명
                                   )
    # print("db conn Check")
    # print(CheckShelter)
    cursor = CheckShelter.cursor()  # control structure of database(연결 객체로 봐도 무방)
    # print(cursor)

    # sql = "SELECT id FROM Management_shelter WHERE title = %s AND access_number = %s"
    sql = "SELECT id FROM \"Management_shelter\" WHERE title = '{title}' AND access_number = '{access_number}'".format(title=name, access_number=number)

    print("name and num")

    print(name, number)

    values = (name, number)

    try:
        cursor.execute(sql)

        result = cursor.fetchall()
        CheckShelter.close()
        return result[0][0]     # tuple 리턴

    except Exception as e:
        print(e)
        print("조회한 쿼리가 없음")
        return None

def Login(request):

    print("사이니지 로그 뷰")

    if request.method == 'POST':

        shelter = request.POST['shelter_name']
        access = request.POST['access_number']

        # print(type(shelter), type(access))

        accessVal = CheckShelter(shelter, access)
        # print(accessVal)

        if accessVal is not None:

            # json 파일 생성
            shelter_info = {
                "shelter_name": shelter,
                "access_number": access,
                "shelter_id": accessVal
            }
            BASE_DIR = Path(__file__).resolve().parent.parent
            Shelter_info_DIR = str(BASE_DIR)+"/ShelterInfo/shelter_info.json"

            file_exist = os.path.exists(Shelter_info_DIR)

            if not file_exist:
                with open(Shelter_info_DIR, 'w', encoding='utf-8') as file:
                    json.dump(shelter_info, file)

            else:
                pass

            # return redirect('Idle', accessVal)
            return redirect('Idle')
            #return render(request, 'Service/Idle.html')
        else:
            return redirect('Login')
    else:
        return render(request, 'ShelterLogin/Login.html')
