import streamlit as st
import pandas as pd

# 제목과 간단한 설명 표시
st.title("시약 LOT 관리 프로그램")
st.write("엑셀 파일을 업로드하여 LOT 정보를 불러오고, 장비별 on/off 상태를 확인해보세요.")

# 파일 업로드 버튼: 확장자가 xlsx 혹은 csv 파일을 업로드할 수 있도록 함
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # 업로드한 파일을 판다스를 이용하여 데이터프레임으로 읽음
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error("엑셀 파일을 읽는 데에 문제가 발생했습니다.")
        st.error(e)
    else:
        st.subheader("업로드한 파일 미리보기")
        st.dataframe(df)

        st.subheader("장비별 LOT on/off 상태 조절")
        # 예제에서는 장비를 고정된 3대(장비1, 장비2, 장비3)로 가정
        equipments = ["장비1", "장비2", "장비3"]

        # 각 행(예: 검사 항목)마다 장비의 on/off 체크박스 생성
        # 엑셀 파일에 '검사 항목'이라는 컬럼이 있다고 가정(컬럼 이름은 여러분의 파일에 맞게 수정)
        if '검사 항목' not in df.columns:
            st.info("엑셀 파일에 '검사 항목' 컬럼이 없으므로 인덱스 번호로 대체합니다.")
            df['검사 항목'] = df.index.astype(str)

        # 각 검사 항목에 대해 체크박스로 상태 표시
        for index, row in df.iterrows():
            st.markdown(f"### 검사 항목: {row['검사 항목']}")
            for equip in equipments:
                # 체크박스 키 값은 고유해야 하므로 row index와 장비명을 함께 사용
                status = st.checkbox(f"{equip} 사용 상태", key=f"{equip}_{index}")
                # 상태에 따라 화면에 ON/OFF 표시
                st.write(f"{equip} 상태: **{'ON' if status else 'OFF'}**")
            st.markdown("---")
