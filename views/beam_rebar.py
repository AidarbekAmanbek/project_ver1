import streamlit as st
from data.concrete import CONCRETE_CLASSES

st.title("Минимальная и максимальная площади арматуры")
st.caption("п.9.2.1.1 СП РК EN 1992-1-1:2004/2011")

concrete_classes = list(CONCRETE_CLASSES)
concrete = st.selectbox("Класс прочности бетона:", concrete_classes)
width = st.number_input("средняя ширина растянутой зоны")
caption = st.caption("для тавровых балок со сжатой полкой для расчета bt нужно принимать в расчет только ширину ребра;")


st.latex