import streamlit as st

st.title("Анкеровка продольной арматуры")
st.caption("Расчёт по EN 1992-1-1:2004/2011 (СП РК)")

fyk = st.number_input(
    "Характеристический предел текучести арматуры, fyk (МПа)",
    min_value=0.0,
    value=500.0,
    step=10.0,
)

field2 = st.number_input("Поле 2 (пока не используется)", value=0.0)
field3 = st.number_input("Поле 3 (пока не используется)", value=0.0)
field4 = st.number_input("Поле 4 (пока не используется)", value=0.0)

if st.button("Рассчитать"):
    st.write(f"fyk = {fyk} МПа")
