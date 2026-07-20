import streamlit as st
from calculations.calc_overlap import (
    calc_f_bd,
    calc_f_ctd,
    calc_l_bqrd,
    calc_cd,
    calc_alph_12_tension,
    calc_alph_3_tension,
    calc_alph_5_tension,
    calc_alpha_123_compression,
    calc_alph_6,
    calc_l0_min,
    calc_l0_overlap,
    calc_A_st,
)
from data.concrete import CONCRETE_CLASSES


st.title("Соединения внахлестку")
st.caption("СП РК EN 1992-1-1:2004/2011")

concrete_classes = list(CONCRETE_CLASSES)
concrete = st.selectbox("Класс прочности бетона:", concrete_classes, index=2)

f_yk = st.number_input(
    "Характеристический предел текучести арматуры, fyk (МПа):",
    min_value=0,
    max_value=1000,
    value=500,
    step=10,
)


diameter = st.number_input(
    "Диаметр стержня Ø, мм",
    value=12,
    min_value=0,
    max_value=40,
    key="diameter_c"
)
if diameter >= 40:
    st.warning("Арматура диаметром более 40 мм, в данном расчете не рассматривается")
elif diameter <0:
    st.warning("Диаметр не мржет быть отрицательным")

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
                f_ctk_005 = CONCRETE_CLASSES[concrete]["fctk_005"]
                f_ctd = calc_f_ctd(a_ct, f_ctk_005, y_c)
                f_bd, n1, n2 = calc_f_bd(f_ctd, bond_condition, diameter)
                f_yd = f_yk / y_s
                l_brqd = calc_l_bqrd(diameter, f_yd, f_bd)

                st.write("Расчетное сопротивление бетона на растяжение по (3.16):")
                st.latex(fr"f_{{ctd}} = \dfrac{{\alpha_{{ct}}\cdot f_{{ctk,0.05}}}}{{\gamma_c}} = \dfrac{{{a_ct}\cdot {f_ctk_005}}}{{{y_c}}} = {f_ctd}\ \mathrm{{МПа}}")

                st.write("Предельные напряжения сцепления по (8.2):")
                st.latex(fr"f_{{bd}} = 2.25\cdot n_1\cdot n_2\cdot f_{{ctd}} = 2.25\cdot {n1}\cdot {n2}\cdot {f_ctd} = {f_bd}\ \mathrm{{МПа}}")

                st.write("Расчетное сопротивление арматуры по (3.15):")
                st.latex(fr"f_{{yd}} = \dfrac{{f_{{yk}}}}{{\gamma_s}} = \dfrac{{{f_yk:.0f}}}{{{y_s}}} = {f_yd:.1f}\ \mathrm{{МПа}}")

                st.write("Базовая длина анкеровки по (8.3):")
                st.latex(fr"l_{{b,rqd}} = \dfrac{{\varnothing}}{{4}}\cdot \dfrac{{\sigma_{{sd}}}}{{f_{{bd}}}} = \dfrac{{{diameter:.0f}}}{{4}}\cdot \dfrac{{{f_yd:.1f}}}{{{f_bd}}} = {l_brqd}\ \mathrm{{мм}}")

                st.write(f"Значения коэффициентов α1, α2, α3, α5, α6 по таблице 8.2")
                st.write("Форма стержня и защитный слой бетона (влияют на α1, α2 по таблице 8.2):")
                bars_type_select = st.selectbox(
                    "Форма стержня", ("прямой", "с загибом/крюком", "петля"), key="bars_type_t"
                )
                if bars_type_select == "прямой":
                    bars_type = "straight"
                elif bars_type_select == "с загибом/крюком":
                    bars_type = "hooked"
                elif bars_type_select == "петля":
                    bars_type = "looped"

                c_t = st.number_input("Защитный слой бетона c, мм", value=25, key="c_t", disabled=bars_type == "hooked")
                c1_t = st.number_input("Расстояние в свету между стержнями c1, мм", value=25, key="c1_t", disabled=bars_type == "looped")
                a_min_t = st.number_input("Расстояние между осями стержней a, мм", value=200, key="a_min_t", disabled=bars_type == "looped")

                cd_t = calc_cd(bars_type, a_min_t, c_t, c1_t)


                alpha_1, alpha_2, alpha_2_raw = calc_alph_12_tension(bars_type, diameter, cd_t)

                st.write(f"Значения cd для по рисунку 8.3:")
                if bars_type == "straight":
                    st.latex(fr"c_d = \min\left(\dfrac{{a}}{{2}}, c, c_1\right) = \min\left(\dfrac{{{a_min_t}}}{{2}}, {c_t}, {c1_t}\right) = {cd_t}\ \mathrm{{мм}}")
                elif bars_type == "hooked":
                    st.latex(fr"c_d = \min\left(\dfrac{{a}}{{2}}, c_1\right) = \min\left(\dfrac{{{a_min_t}}}{{2}}, {c1_t}\right) = {cd_t}\ \mathrm{{мм}}")
                elif bars_type == "looped":
                    st.latex(fr"c_d = c = {cd_t}\ \mathrm{{мм}}")

                st.write(f"Форма стержней ({bars_type_select}):")
                if bars_type == "straight":
                    st.latex(fr"\alpha_1 = {alpha_1}")
                else:
                    diam_3d = 3 * diameter
                    if cd_t > 3 * diameter:
                        st.latex(fr"cd = {cd_t} > 3 \cdot {diameter:.0f} = {diam_3d} \mathrm{{мм}}")
                        st.latex(fr"\alpha_1 = {alpha_1}")
                    else:
                        st.latex(fr"cd = {cd_t} \leq 3 \cdot {diameter:.0f} = {diam_3d}\ \mathrm{{мм}}")
                        st.latex(fr"\alpha_1 = {alpha_1}")

                st.write(f"Защитный слой бетона ({bars_type_select}):")
                if bars_type == "straight":
                    st.latex(
                        fr"\alpha_2 = 1 - 0.15\cdot\left(\dfrac{{c_d-\varnothing}}{{\varnothing}}\right) = 1 - 0.15\cdot\dfrac{{{cd_t}-{diameter}}}{{{diameter}}} = {alpha_2_raw}"
                    )
                else:
                    st.latex(
                        fr"\alpha_2 = 1 - 0.15\cdot\left(\dfrac{{c_d-3\cdot\varnothing}}{{\varnothing}}\right) = 1 - 0.15\cdot\dfrac{{{cd_t}-3\cdot{diameter}}}{{{diameter}}} = {alpha_2_raw}"
                    )
                st.write("c учётом ограничения 0.7 ≤ α2 ≤ 1.0:")
                st.latex(fr" \alpha_2 = {alpha_2}")


                st.write("Наличие поперечной арматуры, не приваренной к главной арматуре:")
                k_select = st.selectbox(
                    "Коэффициент k", (0, 0.05, 0.1), key="factor_k"
                )
                if k_select == 0:
                    alpha_3 = 1.0
                else:
                    sigma_sd_t = st.number_input(
                        "Расчетное напряжение в стержне на длине нахлеста σsd, МПа",
                        value=f_yd,
                        key="sigma_sd_t",
                    )
                    
                    A_st_alter = st.text_input(
                        "Площадь сечения поперечной арматуры на расчетной длине нахлеста l0 (кол-во х диаметр)",
                        value="3x12",
                        key="A_st_alter",
                        help="Укажите количество и диаметр стержней. Пример: 4х20",
                    )

                    try:
                        A_st = calc_A_st(A_st_alter)
                        st.caption(f"A_st = {A_st} мм²")
                    except ValueError as e:
                        st.error(f"Некорректный ввод: {e}")
                        A_st = 0.0

                    alpha_3 = calc_alph_3_tension(k_select, diameter, A_st, sigma_sd_t, f_yd)


                st.write("c учётом ограничения 0.7 ≤ α3 ≤ 1.0:")
                st.latex(fr" \alpha_3 = {alpha_3}")

                st.write("Наличие поперечного сжатия:")
                p = st.number_input("поперечное давление на длине l0, МПа", value=0, min_value=0, max_value=100)
                alpha_5 = calc_alph_5_tension(p)
                if p == 0:
                    st.latex(fr" \alpha_5 = 1 - 0.04\cdot p = {alpha_5}")
                else:
                    st.latex(fr" \alpha_5 = 1 - 0.04\cdot p = 1 - 0.04 \cdot {p} = {alpha_5}")
                st.latex(fr" \alpha_5 = {alpha_5}")

                st.write("Процент стержней, соединяемых внахлестку в одном сечении:")
                p1 = st.number_input("Процент соединяемых внахлестку стержней:", value=50, min_value=0, max_value=100, key="p1_t")
                alpha_6 = calc_alph_6(p1)
                st.latex(fr"\alpha_6 = \sqrt{{p_1/25}} = {alpha_6}")

                st.write("Минимальная длина нахлеста по (8.10):")
                l0_min = calc_l0_min(alpha_6, diameter, l_brqd)
                st.latex(
                    fr"l_{{0,min}} = \max\left(0.3\,\alpha_6\,l_{{b,rqd}},\;15\varnothing,\;200\right) = \max\left(0.3\cdot {alpha_6}\cdot {l_brqd:.1f},\;15\cdot {diameter:.0f},\;200\right) = {l0_min:.0f}\ \mathrm{{мм}}"
                )

                l0 = calc_l0_overlap(alpha_1, alpha_2, alpha_3, alpha_5, alpha_6, l_brqd, l0_min)

                st.write(f"α1 = {alpha_1}")
                st.write(f"α2 = {alpha_2}")
                st.write(f"α3 = {alpha_3}")
                st.write(f"α5 = {alpha_5}")
                st.write(f"α6 = {alpha_6}")

                st.write("Длина нахлеста по (8.10):")
                st.latex(
                    fr"l_{{0}} = \alpha_1\cdot\alpha_2\cdot\alpha_3\cdot\alpha_5\cdot\alpha_6\cdot l_{{b,rqd}}"
                    fr" = {alpha_1}\cdot {alpha_2}\cdot {alpha_3}\cdot {alpha_5}\cdot {alpha_6}\cdot {l_brqd}\ \mathrm{{мм}}"
                    fr" \geq l_{{0,min}} = {l0_min:.0f}\ \mathrm{{мм}}"
                )
                st.latex(fr"l_{{0}} = {l0} \geq {l0_min:.0f}")

                st.write(f"Расчетная длина нахлеста для арматуры диаметром Ø{diameter:.0f} и классом бетона {concrete}:")
                st.write(f"**{l0} мм** или **{l0:.0f} мм**")

    with compression_col:
        compression_active = st.toggle("Стержни сжатые", value=False, key="compression_active")
        if compression_active:
            with st.expander("Расчет для сжатых стержней", expanded=True):

                f_ctk_005 = CONCRETE_CLASSES[concrete]["fctk_005"]
                f_ctd = calc_f_ctd(a_ct, f_ctk_005, y_c)
                f_bd, n1, n2 = calc_f_bd(f_ctd, bond_condition, diameter)
                f_yd = f_yk / y_s
                l_brqd = calc_l_bqrd(diameter, f_yd, f_bd)

                alpha_1, alpha_2, alpha_3 = calc_alpha_123_compression()

                st.write("Расчетное сопротивление бетона на растяжение по (3.16):")
                st.latex(fr"f_{{ctd}} = \dfrac{{\alpha_{{ct}}\cdot f_{{ctk,0.05}}}}{{\gamma_c}} = \dfrac{{{a_ct}\cdot {f_ctk_005}}}{{{y_c}}} = {f_ctd}\ \mathrm{{МПа}}")

                st.write("Предельные напряжения сцепления по (8.2):")
                st.latex(fr"f_{{bd}} = 2.25\cdot n_1\cdot n_2\cdot f_{{ctd}} = 2.25\cdot {n1}\cdot {n2}\cdot {f_ctd} = {f_bd}\ \mathrm{{МПа}}")

                st.write("Расчетное сопротивление арматуры по (3.15):")
                st.latex(fr"f_{{yd}} = \dfrac{{f_{{yk}}}}{{\gamma_s}} = \dfrac{{{f_yk:.0f}}}{{{y_s}}} = {f_yd:.1f}\ \mathrm{{МПа}}")

                st.write("Базовая длина анкеровки по (8.3):")
                st.latex(fr"l_{{b,rqd}} = \dfrac{{\varnothing}}{{4}}\cdot \dfrac{{\sigma_{{sd}}}}{{f_{{bd}}}} = \dfrac{{{diameter:.0f}}}{{4}}\cdot \dfrac{{{f_yd:.1f}}}{{{f_bd}}} = {l_brqd}\ \mathrm{{мм}}")

                st.write("Значения коэффициентов α1, α2, α3 по таблице 8.2 (для сжатых стержней принимаются равными 1.0):")
                st.latex(fr"\alpha_1 = \alpha_2 = \alpha_3 = 1.0")

                st.write("Процент стержней, соединяемых внахлестку в одном сечении:")
                p1_c = st.number_input("Процент соединяемых внахлестку стержней:", value=50, min_value=0, max_value=100, key="p1_c")
                alpha_6 = calc_alph_6(p1_c)
                st.latex(fr"\alpha_6 = \sqrt{{p_1/25}} = {alpha_6}")

                st.write("Минимальная длина нахлеста по (8.10):")
                l0_min = calc_l0_min(alpha_6, diameter, l_brqd)
                st.latex(
                    fr"l_{{0,min}} = \max\left(0.3\,\alpha_6\,l_{{b,rqd}},\;15\varnothing,\;200\right) = \max\left(0.3\cdot {alpha_6}\cdot {l_brqd:.1f},\;15\cdot {diameter:.0f},\;200\right) = {l0_min:.0f}\ \mathrm{{мм}}"
                )

                l0 = calc_l0_overlap(alpha_1, alpha_2, alpha_3, 1.0, alpha_6, l_brqd, l0_min)

                st.write("Длина нахлеста для сжатых стержней по (8.10):")
                st.latex(
                    fr"l_{{0}} = \alpha_1\cdot\alpha_2\cdot\alpha_3\cdot\alpha_6\cdot l_{{b,rqd}}"
                    fr" = {alpha_1}\cdot {alpha_2}\cdot {alpha_3}\cdot {alpha_6}\cdot {l_brqd}\ \mathrm{{мм}}"
                    fr" \geq l_{{0,min}} = {l0_min:.0f}\ \mathrm{{мм}}"
                )
                st.latex(fr"l_{{0}} = {l0} \geq {l0_min:.0f}")

                st.write(f"Расчетная длина нахлеста для арматуры диаметром Ø{diameter:.0f} и классом бетона {concrete}:")
                st.write(f"**{l0} мм** или **{l0:.0f} мм**")



if st.button("Выполнить рассчитать в табличной форме"):
    st.write(f"Скоро все будет")
