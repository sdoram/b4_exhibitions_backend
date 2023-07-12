import psycopg2, os
import pandas as pd
import numpy as np
import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 특정 정보와 서비스명 유사도가 높은 서비스 정보를 얻기 위한 함수
def recommendation(id, top_n=5):
    # 데이터베이스 연결
    con = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT"),
    )
    cur = con.cursor()
    cur.execute(
        "SELECT id, info_name, location, category, start_date, end_date, svstatus From exhibitions_exhibition"
    )
    cols = [column[0] for column in cur.description]
    exhibition_df = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)
    con.close()  # 데이터베이스 연결 종료

    # info_name별 유사도 측정
    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
    info_name_mat = count_vect.fit_transform(exhibition_df["info_name"])

    # 유사도 행렬 생성
    info_name_sim = cosine_similarity(info_name_mat, info_name_mat)

    # 입력한 정보의 index
    target_info_name = exhibition_df[exhibition_df["id"] == id]
    target_index = target_info_name.index.values

    # 입력한 정보의 유사도 데이터 프레임 추가
    exhibition_df["similarity"] = info_name_sim[target_index, :].reshape(-1, 1)

    # start_date가 오늘 날짜 이전이거나 오늘이고, end_date가 오늘 날짜거나 오늘 날짜 이후인 데이터만 추출하기
    today = datetime.date.today()
    period = (exhibition_df["start_date"] <= today) & (
        exhibition_df["end_date"] >= today
    )
    filterd_exhibition_df = exhibition_df.loc[period].sort_values(
        by=["end_date"], ascending=True
    )

    # 필터링 된 데이터프레임의 유사도 내림차순 정렬 후 상위 index 추출
    temp = filterd_exhibition_df.sort_values(by=["similarity"], ascending=False)
    temp = temp[temp.index.values != target_index]  # 자기 자신 제거
    temp = temp[temp["svstatus"] == "접수중"]  # svstatus가 접수중인 데이터만 추출하기

    final_index = temp.index.values[:top_n]
    raw_exhibitions = filterd_exhibition_df.loc[final_index]
    ml_recommend_exhibitions_id_list = list(
        np.array(raw_exhibitions[["id"]]["id"].tolist())
    )

    return ml_recommend_exhibitions_id_list
