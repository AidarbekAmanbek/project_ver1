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

pages = {
        "Утилиты": [
        st.Page("views/units.py", title="Единицы измерений"),
    ],
    
    "СП РК EN 1992-1-1": [
        st.Page("views/anchorage.py", title="Анкеровка продольной арматуры"),
        st.Page("views/overlap.py", title="Нахлест арматуры"),
        st.Page("views/cover.py", title="Защитный слой бетона"),
        st.Page("views/beam_rebar.py", title="Минимальная и максимальная площади арматуры в балке"),
        st.Page("views/creep_coefficient.py", title="Ползучесть и усадка бетона"),
        st.Page("views/punching_shear.py", title="Продавливание"),
        st.Page("views/sample.py", title="Продавливание +"),

    ],

}

st.navigation(pages).run()
