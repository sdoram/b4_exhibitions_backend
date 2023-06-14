import json
from datetime import datetime

# 파일 읽어오기
with open("exhibitions/utils.json", "r", encoding="UTF-8") as f:
    utils = json.load(f)

# print(utils)

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

# print(selected_fields)

new_list = []
for data in utils["DATA"]:
    new_data = {"model": "exhibitions.exhibition"}
    new_data["fields"] = {}
    new_data["fields"]["user_id"] = 1
    new_data["fields"]["info_name"] = data["svcnm"]
    new_data["fields"]["category"] = data["minclassnm"]
    new_data["fields"]["image"] = data["imgurl"]
    new_data["fields"]["location"] = data["placenm"]
    new_data["fields"]["content"] = data["dtlcont"]
    new_data["fields"]["created_at"] = datetime.now().isoformat()
    new_data["fields"]["updated_at"] = datetime.now().isoformat()
    if data["svcopnbgndt"]:
        new_data["fields"]["start_date"] = (
            datetime.fromtimestamp(data["svcopnbgndt"] // 1000).date().isoformat()
        )
    else:
        new_data["fields"]["start_date"] = None

    if data["svcopnenddt"]:
        new_data["fields"]["end_date"] = (
            datetime.fromtimestamp(data["svcopnenddt"] // 1000).date().isoformat()
        )
    else:
        new_data["fields"]["end_date"] = None
    new_list.append(new_data)


with open("exhibitions/utils_data.json", "w", encoding="UTF-8") as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)


# from exhibitions.models import ExhibitionOpenAPI

# for data in data_list["DATA"]:
#     fields = {k: v for k, v in data.items() if k in selected_fields}
#     if all(v is not None for v in fields.values()):
#         exhibition = ExhibitionOpenAPI(**fields)
#         exhibition.save()

# for data in utils["DATA"]:
#     new_fields = {k: v for k, v in data.items() if k in selected_fields}
#     # print(new_fields)

#     # 필드값이 비어있지 않은 경우에만 추가
#     if all(v is not None for v in new_fields.values()):
#         new_data = {"model": "exhibitions.exhibition", "fields": new_fields}
#         new_list.append(new_data)

# print(new_list)
