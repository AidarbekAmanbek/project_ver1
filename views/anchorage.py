import streamlit as st
from calculations.anchorage import (
    calc_f_bd,
    calc_f_ctd,
    calc_l_bqrd,
    calc_cd,
    calc_alph_12_tension,
    calc_alph_3_tension,
    calc_alph_5_tension,
    calc_alpha_123_compression,
    calc_alpha_4_compression,
    calc_lb_min,
    calc_lbd,
)
from data.concrete import CONCRETE_CLASSES
from data.rebar import REBAR_TABLE

st.title("Анкеровка продольной арматуры")
st.caption("Расчёт по EN 1992-1-1:2004/2011 (СП РК)")

concrete_classes = list(CONCRETE_CLASSES)
concrete = st.selectbox("Класс прочности бетона:", concrete_classes, index=2)

f_yk = st.number_input(
    "Характеристический предел текучести арматуры, fyk (МПа):",
    min_value=0,
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
        tension_active = st.toggle("Стержни растянуты", value=True, key="tension_active")
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

                st.write("Минимальная длина анкеровки для растянутых стержней по (8.6):")
                lb_min = calc_lb_min("tension", diameter, l_brqd)
                st.latex(
                    fr"l_{{b,min}} = \max\left(0.3\,l_{{b,rqd}},\;10\varnothing,\;100\right) = \max\left(0.3\cdot {l_brqd:.1f},\;10\cdot {diameter:.0f},\;100\right) = {lb_min:.0f}\ \mathrm{{мм}}"
                )

                st.write(f"Значения коэффициентов α1, α2, α3, α4, α5 по таблице 8.2")
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
                    select_constraction = st.selectbox(
                        "Тип конструкции:", ("балка", "плита"), key="construction_type"
                    )
                    construction_type = "beam" if select_constraction == "балка" else "slab"
                    A_st = st.number_input("Площадь сечения поперечной арматуры на расчетной длине анкеровки lbd, мм²", value=339.3, key="A_st")
                    alpha_3 = calc_alph_3_tension(k_select, diameter, A_st, construction_type)


                st.write("c учётом ограничения 0.7 ≤ α3 ≤ 1.0:")
                st.latex(fr" \alpha_3 = {alpha_3}")

                st.write("Наличие приваренной поперечной арматуры:")
                tension_welded_radio = st.radio(
                    "Наличие приваренной поперечной арматуры:",
                    ("да", "нет"),
                    index=1,
                    horizontal=True,
                    key="tension_welded_radio",
                    label_visibility="collapsed"
                )
                
                alpha_4 = calc_alpha_4_compression(tension_welded_radio == "да")
                if tension_welded_radio == "да":
                    st.latex(fr" \alpha_4 = {alpha_4}")
                else:
                    st.latex(fr" \alpha_4 - \text{{не учитывается}}")

                st.write("Наличие поперечного сжатия:")
                p = st.number_input("поперечное давление на длине lbd, МПа", value=0, min_value=0, max_value=10)
                alpha_5 = calc_alph_5_tension(p)
                if p == 0:
                    st.latex(fr" \alpha_5 = 1 - 0.04\cdot p = {alpha_5}")
                else:
                    st.latex(fr" \alpha_5 = 1 - 0.04\cdot p = 1 - 0.04 \cdot {p} = {alpha_5}")
                st.latex(fr" \alpha_5 = {alpha_5}")

                l_bd = calc_lbd(alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, l_brqd, lb_min)

                st.write(f"α1 = {alpha_1}")
                st.write(f"α2 = {alpha_2}")
                st.write(f"α3 = {alpha_3}")
                st.write(f"α4 = {alpha_4}")
                st.write(f"α5 = {alpha_5}")

                st.write("Расчетная длина анкеровки для растянутых стержней по (8.4):")
                if tension_welded_radio == "да":
                    st.latex(
                        fr"l_{{bd}} = \alpha_1\cdot\alpha_2\cdot\alpha_3\cdot\alpha_4\cdot\alpha_5\cdot l_{{b,rqd}}"
                        fr" = {alpha_1}\cdot {alpha_2}\cdot {alpha_3}\cdot {alpha_4}\cdot {alpha_5}\cdot {l_brqd}\ \mathrm{{мм}}"
                        fr" \geq l_{{b,min}} = {lb_min:.0f}\ \mathrm{{мм}}"
                    )
                else:
                    st.latex(
                        fr"l_{{bd}} = \alpha_1\cdot\alpha_2\cdot\alpha_3\cdot\alpha_5\cdot l_{{b,rqd}}"
                        fr" = {alpha_1}\cdot {alpha_2}\cdot {alpha_3}\cdot {alpha_5}\cdot {l_brqd}\ \mathrm{{мм}}"
                        fr" \geq l_{{b,min}} = {lb_min:.0f}\ \mathrm{{мм}}"
                    )
                    st.latex(fr"l_{{bd}} = {l_bd} \geq {lb_min:.0f}")

                st.write(f"Расчетная длина анкеровки для арматуры диаметром Ø{diameter:.0f} и классом бетона {concrete}:")
                st.write(f"**{l_bd} мм** или **{l_bd:.0f} мм**")
                
    with compression_col:
        compression_active = st.toggle("Стержни сжатые", value=True, key="compression_active")
        if compression_active:
            with st.expander("Расчет для сжатых стержней", expanded=True):
                
                f_ctk_005 = CONCRETE_CLASSES[concrete]["fctk_005"]
                f_ctd = calc_f_ctd(a_ct, f_ctk_005, y_c)
                f_bd, n1, n2 = calc_f_bd(f_ctd, bond_condition, diameter)
                f_yd = f_yk / y_s
                l_brqd = calc_l_bqrd(diameter, f_yd, f_bd)

                alpha_1, alpha_2, alpha_3 = calc_alpha_123_compression()
                lb_min = calc_lb_min("compression", diameter, l_brqd)
                

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
                    fr"l_{{b,min}} = \max\left(0.6\,l_{{b,rqd}},\;10\varnothing,\;100\right) = \max\left(0.6\cdot {l_brqd:.1f},\;10\cdot {diameter:.0f},\;100\right) = {lb_min:.0f}\ \mathrm{{мм}}"
                )

                st.write(f"Значения коэффициентов α1, α2, α3, α4 по таблице 8.2")
                st.write("Форма стержней:")
                st.write(f"α1 = {alpha_1}")
                st.write("Защитный слой бетона:")
                st.write(f"α2 = {alpha_2}")
                st.write("Наличие поперечной арматуры, не приваренной к главной арматуре:")
                st.write(f"α3 = {alpha_3}")
                st.write("Наличие приваренной поперечной арматуры:")
                compression_welded_radio = st.radio(
                    "Наличие приваренной поперечной арматуры:",
                    ("да", "нет"),
                    index=1,
                    horizontal=True,
                    key="compression_welded_radio",
                    label_visibility="collapsed"
                )
                alpha_4 = calc_alpha_4_compression(compression_welded_radio == "да")

                st.write(f"α4 = {alpha_4}")
                

                st.write("Расчетная длина анкеровки для сжатых стержней по (8.4)-(8.7):")
                l_bd = calc_lbd(alpha_1, alpha_2, alpha_3, alpha_4, 1.0, l_brqd, lb_min)
                st.latex(
                    fr"l_{{bd}} = \alpha_1\cdot\alpha_2\cdot\alpha_3\cdot\alpha_4\cdot l_{{b,rqd}}"
                    fr" = {alpha_1}\cdot {alpha_2}\cdot {alpha_3}\cdot {alpha_4}\cdot {l_brqd}\ \mathrm{{мм}}"
                    fr" \geq l_{{b,min}} = {lb_min:.0f}\ \mathrm{{мм}}"
                )
                st.write(f"Расчетная длина анкеровки для арматуры диаметром Ø{diameter:.0f} и классом бетона {concrete}:")
                st.write(f"**{l_bd} мм** или **{l_bd:.0f} мм**")









if st.button("Выполнить рассчитать в табличной форме"):
    st.write(f"fyk =  МПа")
