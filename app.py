import streamlit as st
import jaconv


GRADE = {"AA":4.0,"A":3.0,"B":2.0,"C":1.0,"D":0.0}

def home():
    st.write("# GPA Calculator for Tohoku University Students (ver.β)")

    lines = st.text_area("Copy & Paste your grades").split("\n")
    
    new = []
    for line in lines:
        separated = line.split()
        try:
            new.append([separated[-3],separated[-4]])
        except:
            pass
    
    raw_gpa = 0.0 
    cred = 0.0

    for gr in new:
        gr[0] = jaconv.z2h(gr[0], kana=False, digit=True, ascii=True)
        gr[1] = jaconv.z2h(gr[1], kana=False, digit=True, ascii=True)
        if gr[0] in GRADE.keys():
            raw_gpa += GRADE[gr[0]]*float(gr[1])
            cred += float(gr[1])

    try:
        st.write(raw_gpa/cred)
    except:
        pass

    st.write(raw_gpa)
    st.write(cred)
    st.write(lines)
    st.write(new)
    return None

#deploy sever
if __name__ == "__main__":
    home()