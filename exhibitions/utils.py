import os
import sys
import django
import schedule
import time
import requests
from datetime import datetime
from dotenv import load_dotenv


"""
- openAPI를 통해 전시 정보를 가져와서 DB에 저장하는 코드 입니다.
- 지금 장고 ORM을 이용해서 DB에 저장하고 있기 때문에 settings에서 postgresql을 자동으로 불러옵니다.
- 그래서 load_dotev를 통해서 secret key를 불러오고, sys.path.append를 통해서 프로젝트 디렉터리를 지정합니다.
- 그리고 os.environ.setdefault를 통해서 장고 프로젝트의 settings.py 파일을 설정합니다.
- 마지막으로 django.setup()을 통해서 장고 프로젝트를 환경에 맞게 설정합니다.
"""


def update_exhibition():
    load_dotenv(verbose=True)  # .env 파일로부터 환경변수를 읽어온다.

    # 프로젝트 디렉터리를 지정하기
    PJ_DIR = os.environ.get("PJ_DIR")
    project_root_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        PJ_DIR,
    )
    sys.path.append(project_root_directory)

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "b4_drf_project.settings"  # 장고 프로젝트의 settings.py 파일을 설정한다.
    )

    django.setup()  # 장고 프로젝트를 환경에 맞게 설정한다.

    from exhibitions.models import Exhibition  # Exhibition 모델 import

    UTILS_API_KEY = os.environ.get("UTILS_API_KEY")
    ENDPOINT = (
        f"http://openAPI.seoul.go.kr:8088/{UTILS_API_KEY}/json/ListPublicReservationCulture/1/1000/"
    )
    headers = {"Authorization": UTILS_API_KEY}
    response = requests.get(ENDPOINT, headers=headers)

    # 응답 데이터 확인해보기
    if response.status_code != 200:
        print(f"API를 불러오지 못 함: {response.status_code}")
    else:
        utils = response.json()

    # 필요한 데이터만 가져오기
    new_list = []

    # 데이터 파싱하기
    for data in utils["ListPublicReservationCulture"]["row"]:  # openAPI 형식에 맞게 필드명들을 가져와야합니다.
        new_data = {"model": "exhibitions.exhibition"}
        new_data["fields"] = {}
        new_data["fields"]["user_id"] = 1  # 관리자 user_id = 1
        new_data["fields"]["info_name"] = data["SVCNM"]
        new_data["fields"]["category"] = data["MINCLASSNM"]
        new_data["fields"]["image"] = data["IMGURL"]
        new_data["fields"]["location"] = data["PLACENM"]
        new_data["fields"]["content"] = data["DTLCONT"]
        new_data["fields"]["created_at"] = datetime.now().isoformat()
        new_data["fields"]["updated_at"] = datetime.now().isoformat()
        new_data["fields"]["direct_url"] = data["SVCURL"]
        new_data["fields"]["longitude"] = float(data["X"]) if data.get("X") else None
        new_data["fields"]["latitude"] = float(data["Y"]) if data.get("Y") else None
        new_data["fields"]["svstatus"] = data["SVCSTATNM"]

        if data["SVCOPNBGNDT"]:
            new_data["fields"]["start_date"] = (
                datetime.strptime(data["SVCOPNBGNDT"], "%Y-%m-%d %H:%M:%S.%f").date().isoformat()
            )
        else:
            new_data["fields"]["start_date"] = None

        if data["SVCOPNENDDT"]:
            new_data["fields"]["end_date"] = (
                datetime.strptime(data["SVCOPNENDDT"], "%Y-%m-%d %H:%M:%S.%f").date().isoformat()
            )
        else:
            new_data["fields"]["end_date"] = None

        new_list.append(new_data)

    # DB에 저장된 전시가 중복되는지 확인하기
    def is_duplicate(new_fields):
        duplicated_exhibition = (
            Exhibition.objects.filter(  # odjects.all() 전체를 가져오면 중복된 데이터를 못 찾아 fllter를 사용
                info_name=new_fields["info_name"],
                start_date=new_fields["start_date"],
                end_date=new_fields["end_date"],
                direct_url=new_fields["direct_url"],
            )
        )

        return duplicated_exhibition.exists()

    # DB에 저장하고 새로운 전시가 추가되었는지 확인하기
    for new_data in new_list:
        if not is_duplicate(new_data["fields"]):
            exhibition = Exhibition(**new_data["fields"])
            exhibition.save()
            print("새 전시 추가:", new_data["fields"]["info_name"])
        else:
            print("중복된 전시:", new_data["fields"]["info_name"])


schedule.every().saturday.at("12:00").do(update_exhibition)  # 매주 토요일 12시에 실행됩니다.

while True:
    schedule.run_pending()
    time.sleep(60)  # 1분마다 실행되는 작업을 확인합니다.
