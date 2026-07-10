import streamlit as st

pages = [
    st.Page("views/anchorage.py", title="Анкеровка продольной арматуры"),
    st.Page("views/cover.py", title="Защитный слой бетона"),
]

st.navigation(pages).run()
