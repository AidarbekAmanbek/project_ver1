import streamlit as st

st.title("Анкеровка продольной арматуры")
st.caption("Расчёт по EN 1992-1-1:2004/2011 (СП РК)")

fyk = st.number_input(
    "Характеристический предел текучести арматуры, fyk (МПа)",
    min_value=0.0,
    value=500.0,
    step=10.0,
)



def new_func():
    a_ct = st.number_input("Поле 2 (пока не используется)", value=1.0)
    ys = st.number_input("Поле 3 (пока не используется)", value=1.15)
    yc = st.number_input("Поле 3 (пока не используется)", value=1.5)
    concrete_classes = [
    "C12/15",
    "C16/20",
    "C20/25",
    "C25/30",
    "C30/37",
    "C35/45",
    "C40/50",
]
    concrete = st.selectbox("Прочность бетона (класс C)", concrete_classes, index=2)

new_func()

if st.button("Рассчитать"):
    st.write(f"fyk = {fyk} МПа")
