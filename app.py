import streamlit as st
import jaconv

GRADE = {"AA":4.0,"A":3.0,"B":2.0,"C":1.0,"D":0.0}

def home():

    st.write("# 東北大生用 GPA Calculator (β版)")
    lines = st.text_area("""学務情報システムから，成績をコピーしてそのままペーストしてください．""",height=300).split("\n")
    
    grades = []
    for line in lines:
        splited = line.split()
        try:
            grades.append([splited[-3],splited[-4]])
        except:
            pass
    
    raw_gpa = 0.0 
    weighted_gpa = 0.0
    cred = 0.0

    for grade in grades:
        grade[0] = jaconv.z2h(grade[0], kana=False, digit=True, ascii=True)
        grade[1] = jaconv.z2h(grade[1], kana=False, digit=True, ascii=True)
        if grade[0] in GRADE.keys():
            raw_gpa += GRADE[grade[0]]
            weighted_gpa += GRADE[grade[0]]*float(grade[1])
            cred += float(grade[1])

    operation = st.button("GPAを計算")

    if not operation:
        st.stop()

    if not cred:
        st.write("取得された単位数が0のため，GPAを計算することができません．")
        st.stop()
    
    st.write(f"総取得単位数：{cred}")
    st.write(f"GPA：{weighted_gpa/cred}")

#deploy sever
if __name__ == "__main__":
    home()