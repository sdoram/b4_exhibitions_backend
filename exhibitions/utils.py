import json
from datetime import datetime

# 파일 읽어오기
with open("exhibitions/utils.json", "r", encoding="UTF-8") as f:
    utils = json.load(f)

# 선택한 필드만 가져오기
selected_fields = [
    "svcnm",
    "category",
    "minclassnm",
    "imgurl",
    "placenm",
    "dtlcont",
    "svcopnbgndt",
    "svcopnenddt",
]

# 필요한 데이터만 가져오기
new_list = []

for data in utils["DATA"]:
    new_data = {"model": "exhibitions.exhibition"}
    new_data["fields"] = {}
    new_data["fields"]["user_id"] = 1  # 관리자 user_id = 1
    new_data["fields"]["info_name"] = data["svcnm"]
    new_data["fields"]["category"] = data["minclassnm"]
    new_data["fields"]["image"] = data["imgurl"]
    new_data["fields"]["location"] = data["placenm"]
    new_data["fields"]["content"] = data["dtlcont"]
    new_data["fields"]["created_at"] = datetime.now().isoformat()
    new_data["fields"]["updated_at"] = datetime.now().isoformat()
    if data[
        "svcopnbgndt"
    ]:  # "svcopnbgndt":1676300400000 시작일이 이렇게 불러와져서 데이터에 저장이 안됨 -> 1000으로 나눠주고 datetime으로 변환
        new_data["fields"]["start_date"] = (
            datetime.fromtimestamp(data["svcopnbgndt"] // 1000).date().isoformat()
        )
    else:
        new_data["fields"]["start_date"] = None

    if data[
        "svcopnenddt"
    ]:  # "svcopnenddt":1676300400000 종료일이 이렇게 불러와져서 데이터에 저장이 안됨 -> 1000으로 나눠주고 datetime으로 변환
        new_data["fields"]["end_date"] = (
            datetime.fromtimestamp(data["svcopnenddt"] // 1000).date().isoformat()
        )
    else:
        new_data["fields"]["end_date"] = None
    new_list.append(new_data)

# 파싱된 데이터가 exhibitions/utils_data.json 으로 저장
with open("exhibitions/utils_data.json", "w", encoding="UTF-8") as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)
