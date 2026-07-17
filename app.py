import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1160px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pages = [
    st.Page("views/anchorage.py", title="Анкеровка продольной арматуры"),
    st.Page("views/cover.py", title="Защитный слой бетона"),
]

st.navigation(pages).run()
