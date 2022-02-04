from typing import AbstractSet
import streamlit as st
import streamlit.components.v1 as components
import webbrowser
import jaconv

GRADE = {"AA": 4.0, "A": 3.0, "B": 2.0, "C": 1.0, "D": 0.0}

st.set_page_config(
    page_title="Tohoku GPA Calculator",
    layout="wide",
)


def home():
    st.write("# 東北大生用 GPA Calculator (β版)")
    st.markdown(
        """<small>App Developer:
    <a href="https://github.com/kuriyan1204"
    target="_blank">
    @kuriyan1204
    </a></small>
    """,
        unsafe_allow_html=True,
    )
    lines = st.text_area("""学務情報システムから，成績をコピーしてそのままペーストしてください．""", height=300).split(
        "\n"
    )

    grades = []
    for line in lines:
        splited = line.split()
        try:
            # credit, grade, year, semester
            grades.append((splited[-4], splited[-3], splited[-2], splited[-1]))
        except:
            pass

    raw_gpa = 0.0
    weighted_gpa = 0.0
    cred = 0.0
    semester_gpa = {}
    semester_cred = {}

    creds = {"AA": 0.0, "A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0}

    for credit, grade, year, semester in grades:
        credit = jaconv.z2h(credit, kana=False, digit=True, ascii=True)
        grade = jaconv.z2h(grade, kana=False, digit=True, ascii=True)

        # If numerical grades
        if grade.isdecimal():
            int_grade = int(grade)
            if 90 <= int_grade <= 100:
                grade = "AA"
            elif 80 <= int_grade < 90:
                grade = "A"
            elif 70 <= int_grade < 80:
                grade = "B"
            elif 60 <= int_grade < 70:
                grade = "C"
            else:
                grade = "D"

        if grade not in GRADE:
            continue

        if semester.startswith("前期"):
            semester = "前期"
        elif semester.startswith("後期"):
            semester = "後期"
        else:  # e.g. 通年
            semester = "他"

        sem = year + " " + semester
        if sem not in semester_gpa:
            semester_gpa[sem] = semester_cred[sem] = 0

        credit = float(credit)
        raw_gpa += GRADE[grade]
        weighted_gpa += GRADE[grade] * credit
        semester_gpa[sem] += GRADE[grade] * credit
        cred += credit
        semester_cred[sem] += credit
        creds[grade] += credit

    operation = st.button("GPAを計算")

    if not operation:
        st.stop()

    if not cred:
        st.write("取得された単位数が0のため，GPAを計算することができません．")
        st.stop()

    st.write(f"総取得単位数：{cred}")
    st.write(f"GPA：{weighted_gpa/cred:.3f}")

    with st.expander("セメスターごとの成績", expanded=False):
        for sem in semester_gpa:
            st.write(f"{sem}：{semester_gpa[sem]/semester_cred[sem]:.3f}")

    with st.expander("取得単位の詳細", expanded=False):
        for grade in creds:
            st.write(f"{grade}：{creds[grade]}単位")

    cur_sem = list(semester_cred)[-1]

    tweet_text = f"""
    今季の取得単位数は{semester_cred[cur_sem]}で，GPAは{semester_gpa[cur_sem]/semester_cred[cur_sem]:.3f}でした！
    累積のGPAは{weighted_gpa/cred:.3f}です．
    """

    tweet_button = f"""
    <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" 
    data-text = "{tweet_text}"
    data-show-count="false" 
    data-size='large' 
    data-related='kuriyan1204' >
    tweet</a>
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    components.html(tweet_button)


# deploy sever
if __name__ == "__main__":
    home()
