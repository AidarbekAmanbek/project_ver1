import streamlit as st
from calculations.anchorage import (
    calc_f_bd,
    calc_f_ctd,
    calc_l_bqrd,
    calc_alphas_compression,
    calc_lb_min,
    calc_lbd,
)
from data.concrete import CONCRETE_CLASSES

st.title("Анкеровка продольной арматуры")
st.caption("Расчёт по EN 1992-1-1:2004/2011 (СП РК)")

concrete_classes = list(CONCRETE_CLASSES)
concrete = st.selectbox("Класс прочности бетона:", concrete_classes, index=2)

f_yk = st.number_input(
    "Характеристический предел текучести арматуры, fyk (МПа):",
    min_value=0.0,
    value=500.0,
    step=10.0,
)

diameter = st.number_input("Диаметр стержня Ø, мм", value=20.0, key="diameter_c")

a_ct = st.number_input(
    "αct - коэффициент, учитывающий влияние длительных процессов на прочность бетона при растяжении",
    value=1.0,
    key="a_ct",
)
y_c = st.number_input("γc - частный коэффициент безопасности для бетона", value=1.5, key="y_c")
y_s = st.number_input("γs - частный коэффициент безопасности для арматуры", value=1.15, key="y_s")


radio_button = st.radio(
    "Условий сцепления:",
    ("хорошое", "умеренное(плохое)"),
    index=0,
    horizontal=True,
)
bond_condition = "good" if radio_button == "хорошое" else "poor"

with st.expander("Показать схему условий сцепления (рисунок 8.2)"):
    st.image("assets/anchorage/bond_conditions.png")
    st.caption(
        "a) и b) хорошие условия сцепления для всех стержней; "
        "c) и d) незаштрихованная зона — хорошие условия сцепления, "
        "заштрихованная зона — умеренные условия сцепления"
    )

with st.container(border=True):
    tension_col, compression_col = st.columns(2)

    with tension_col:
        tension_active = st.toggle("Стержни растянуты", value=False, key="tension_active")
        if tension_active:
            with st.expander("Расчет для растянутых стержней", expanded=True):
                st.write("Поля появятся здесь")

    with compression_col:
        compression_active = st.toggle("Стержни сжатые", value=True, key="compression_active")
        if compression_active:
            with st.expander("Расчет для сжатых стержней", expanded=True):
                
                f_ctk_005 = CONCRETE_CLASSES[concrete]["fctk_005"]
                f_ctd = calc_f_ctd(a_ct, f_ctk_005, y_c)
                f_bd, n1, n2 = calc_f_bd(f_ctd, bond_condition, diameter)
                f_yd = f_yk / y_s
                l_brqd = calc_l_bqrd(diameter, f_yd, f_bd)

                alpha_1, alpha_2, alpha_3, alpha_4 = calc_alphas_compression()
                lb_min = calc_lb_min("compression", diameter, l_brqd)
                l_bd = calc_lbd(alpha_1, alpha_2, alpha_3, alpha_4, 1.0, l_brqd, lb_min)

                st.write("Расчетное сопротивление бетона на растяжение по (3.16):")
                st.latex(fr"f_{{ctd}} = \dfrac{{\alpha_{{ct}}\cdot f_{{ctk,0.05}}}}{{\gamma_c}} = \dfrac{{{a_ct}\cdot {f_ctk_005}}}{{{y_c}}} = {f_ctd}\ \mathrm{{МПа}}")

                st.write("Предельные напряжения сцепления по (8.2):")
                st.latex(fr"f_{{bd}} = 2.25\cdot n_1\cdot n_2\cdot f_{{ctd}} = 2.25\cdot {n1}\cdot {n2}\cdot {f_ctd} = {f_bd}\ \mathrm{{МПа}}")

                st.write("Расчетное сопротивление арматуры по (3.15):")
                st.latex(fr"f_{{yd}} = \dfrac{{f_{{yk}}}}{{\gamma_s}} = \dfrac{{{f_yk:.0f}}}{{{y_s}}} = {f_yd:.1f}\ \mathrm{{МПа}}")

                st.write("Базовая длина анкеровки по (8.3):")
                st.latex(fr"l_{{b,rqd}} = \dfrac{{\varnothing}}{{4}}\cdot \dfrac{{\sigma_{{sd}}}}{{f_{{bd}}}} = \dfrac{{{diameter:.0f}}}{{4}}\cdot \dfrac{{{f_yd:.1f}}}{{{f_bd}}} = {l_brqd}\ \mathrm{{мм}}")

                st.write("Минимальная длина анкеровки для сжатых стержней по (8.7):")
                st.latex(
                    fr"l_{{b,min}} = \max\left(0.3\,l_{{b,rqd}},\;10\varnothing,\;100\right) = \max\left(0.3\cdot {l_brqd:.1f},\;10\cdot {diameter:.0f},\;100\right) = {lb_min:.0f}\ \mathrm{{мм}}"
                )

                st.write("Расчетная длина анкеровки для сжатых стержней по (8.4)-(8.7):")
                st.latex(
                    fr"l_{{bd}} = \alpha_1\cdot\alpha_2\cdot\alpha_3\cdot\alpha_4\cdot l_{{b,rqd}}"
                    fr" = {alpha_1}\cdot {alpha_2}\cdot {alpha_3}\cdot {alpha_4}\cdot {l_brqd}\ \mathrm{{мм}}"
                    fr" \geq l_{{b,min}} = {lb_min:.0f}\ \mathrm{{мм}}"
                )
                st.write(f"Расчетная длина анкеровки для арматуры диаметром Ø{diameter:.0f} и классом бетона {concrete}: **{l_bd} мм** или **{l_bd:.0f} м**")










if st.button("Выполнить рассчитать в табличной форме"):
    st.write(f"fyk =  МПа")
