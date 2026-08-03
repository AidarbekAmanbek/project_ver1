import streamlit as st

from data.concrete import CONCRETE_CLASSES
from calculations.calc_punching_shear import (
    calc_effective_depth,
    calc_reinforcement_ratio,
    calc_punching_shear_stress,
    calc_punching_shear_resistance,
)


BETA_VALUES = {
    "Внутренняя (β = 1.15)": 1.15,
    "Крайняя (β = 1.4)": 1.4,
    "Угловая (β = 1.5)": 1.5,
}


st.title("Продавливание")
st.caption("п.4.1 СП РК EN 1992-1-1:2004/2011")

st.subheader("Геометрия колонны")
column_type = st.selectbox("Форма колонны:", ("Прямоугольная", "Круглая", "Сложная"))

if column_type == "Прямоугольная":
    height = st.number_input("Высота c1, мм:", value=400, disabled=column_type == "Круглая")
    width = st.number_input("Ширина c2, мм:", value=400, disabled=column_type == "Круглая")
elif column_type == "Круглая":
    radius = st.number_input("Радиус, мм:", value=250, disabled=column_type == "Прямоугольная")
else:
    dimension = st.number_input("Контрольный периметр ui, мм:", value=300)


plate_thickness = st.number_input("Толщина плиты перекрытия/покрытия, мм", min_value=0, value=250)
concrete_classes = list(CONCRETE_CLASSES)
concrete = st.selectbox("Класс прочности бетона:", concrete_classes, index=3)
rebar_x = st.number_input("Диаметр арматуры в направлении x, мм", min_value=0, value=14)
rebar_x_spacing = st.number_input("Шаг арматуры в направлении x, мм", min_value=0, value=100)
rebar_y = st.number_input("Диаметр арматуры в направлении y, мм", min_value=0, value=14)
rebar_y_spacing = st.number_input("Шаг арматуры в направлении y, мм", min_value=0, value=100)
cover = st.number_input("Защитный слой бетона, мм", min_value=0, value=25)


st.subheader("Коэффициент β")
betta_check = st.checkbox("Принимать значения коэффициента β, приведенные на рисунке 6.21N", value=True)

if betta_check == True:
    column_position = st.selectbox(
        "Расположение колонны:",
        list(BETA_VALUES),
    )
    betta = BETA_VALUES[column_position]

    with st.expander("Рисунок 6.21N - Рекомендуемые значения β"):
        st.image("assets/punching_sheap/coef_betta.png", width=350)
        st.caption(
            "A - средняя колонна"
            "B - крайняя колонна"
            "C - угловая колонна"
        )
else:
    med_y = st.number_input("Расчетный изгибающий момент MEd,y, кН·м", min_value=0.0)
    med_z = st.number_input("Расчетный изгибающий момент MEd,z, кН·м", min_value=0.0)
    betta = None


st.write("Нагрузки")
vertical_shear_force = st.number_input("Расчетное значение поперечного усилия VEd, кН", min_value=0, value=500)


st.write("Параметры установленные в национальном приложений")
a_cc = st.number_input(
    "αcc - коэффициент, учитывающий влияние длительных процессов на прочность при сжатии",
    value=0.85,
    key="a_cc",
)
y_c = st.number_input("γc - частный коэффициент безопасности для бетона", value=1.5, key="y_c")
y_s = st.number_input("γs - частный коэффициент безопасности для арматуры", value=1.15, key="y_s")
С_Rdc = st.number_input("СRdc - частный коэффициент (по 6.4.4(1))", value=18, key="СRdc")
k1 = st.number_input("k1 - частный коэффициент (по 6.4.4(1)", value=0.1, key="k1")


if st.button("Расчет", key="calculate"):
    st.write("Результат")

    d_eff, ax, ay, dx, dy = calc_effective_depth(plate_thickness, cover, rebar_x, rebar_y)

    st.write("Расстояние от верха плиты до оси арматуры в направлении x:")
    st.latex(
        fr"a_x = c + \dfrac{{\varnothing_x}}{{2}} = {cover} + \dfrac{{{rebar_x}}}{{2}} = {ax}\ \mathrm{{мм}}"
    )

    st.write("Расстояние от верха плиты до оси арматуры в направлении y:")
    st.latex(
        fr"a_y = c + \varnothing_x + \dfrac{{\varnothing_y}}{{2}} = {cover} + {rebar_x} + \dfrac{{{rebar_y}}}{{2}} = {ay}\ \mathrm{{мм}}"
    )

    st.write("Полезная высота сечения в направлении x:")
    st.latex(fr"d_x = h - a_x = {plate_thickness} - {ax} = {dx}\ \mathrm{{мм}}")

    st.write("Полезная высота сечения в направлении y:")
    st.latex(fr"d_y = h - a_y = {plate_thickness} - {ay} = {dy}\ \mathrm{{мм}}")

    st.write("Средняя полезная высота сечения по (6.32):")
    st.latex(fr"d = \dfrac{{d_x + d_y}}{{2}} = \dfrac{{{dx} + {dy}}}{{2}} = {d_eff}\ \mathrm{{мм}}")

    As_x, As_y, p_lx, p_ly, p_l = calc_reinforcement_ratio(
        rebar_x, rebar_y, rebar_x_spacing, rebar_y_spacing, d_eff
    )

    st.write(f"Площадь сечения стержня Ø{rebar_x:.0f} (направление x) и Ø{rebar_y:.0f} (направление y):")
    st.latex(fr"A_{{s,x}} = {As_x}\ \mathrm{{мм^2}}, \quad A_{{s,y}} = {As_y}\ \mathrm{{мм^2}}")

    st.write("Коэффициент армирования в направлении x по (6.32):")
    st.latex(
        fr"\rho_{{lx}} = \dfrac{{A_{{s,x}}}}{{s_x\cdot d}} = \dfrac{{{As_x}}}{{{rebar_x_spacing}\cdot {d_eff}}} = {p_lx}"
    )

    st.write("Коэффициент армирования в направлении y по (6.32):")
    st.latex(
        fr"\rho_{{ly}} = \dfrac{{A_{{s,y}}}}{{s_y\cdot d}} = \dfrac{{{As_y}}}{{{rebar_y_spacing}\cdot {d_eff}}} = {p_ly}"
    )

    st.write("Комбинированный коэффициент армирования по (6.32):")
    st.latex(
        fr"\rho_{{l}} = \sqrt{{\rho_{{lx}}\cdot\rho_{{ly}}}} = \sqrt{{{p_lx}\cdot {p_ly}}} = {p_l}"
    )

    if column_type != "Прямоугольная":
        st.info("Расчёт напряжения продавливания пока реализован только для прямоугольных колонн.")
    elif betta is None:
        st.warning("Расчёт коэффициента β по изгибающим моментам ещё не реализован. Включите использование рисунка 6.21N.")
    else:
        v_ed, v_ed_ts, u1, pi_val = calc_punching_shear_stress(width, height, betta, vertical_shear_force, d_eff)

        st.write("Контрольный периметр u1 (на расстоянии 2d от грани колонны):")
        st.latex(
            fr"u_1 = 2\cdot c_2 + 2\cdot c_1 + 2\cdot\pi\cdot 2d = 2\cdot {width} + 2\cdot {height} + 2\cdot {pi_val}\cdot 2\cdot {d_eff} = {u1}\ \mathrm{{мм}}"
        )

        st.write("Максимальное напряжение среза, вызванное местной сосредоточенной нагрузкой, по (6.38):")
        st.latex(
            fr"v_{{Ed}} = \dfrac{{\beta\cdot V_{{Ed}}}}{{u_1\cdot d}} = \dfrac{{{betta}\cdot {vertical_shear_force}\cdot 10^3}}{{{u1}\cdot {d_eff}}} = {v_ed}\ \mathrm{{МПа}} = {v_ed_ts}\ \mathrm{{тс/м2}}"
        )

        f_ck = CONCRETE_CLASSES[concrete]["fck"]
        c_rdc, k, v_rdc, v_rdc_min, v_rdc_design = calc_punching_shear_resistance(d_eff, p_l, f_ck, y_c)

        st.write("Расчётное сопротивление бетона продавливанию без поперечной арматуры:")
        st.latex(fr"C_{{Rd,c}} = \dfrac{{0.18}}{{\gamma_c}} = \dfrac{{0.18}}{{{y_c}}} = {c_rdc}")

        # Ограничение k не должно превышать 2.0
        st.write("Коэффициент k:")
        k_limited = min(k, 2.0)
        note = " (ограничено до 2.0)" if k > 2.0 else ""
        st.latex(
            fr"k = 1 + \sqrt{{\dfrac{{200}}{{d}}}} = 1 + \sqrt{{\dfrac{{200}}{{{d_eff}}}}} = {k}{note} \Rightarrow k_{{принят}} = {k_limited}"
        )

        st.write("Расчётное сопротивление продавливанию по (6.47):")
        st.latex(
            fr"V_{{Rd,c}} = C_{{Rd,c}}\cdot k\cdot\left(100\cdot\rho_l\cdot f_{{ck}}\right)^{{1/3}}"
            fr" = {c_rdc}\cdot {k}\cdot\left(100\cdot {p_l}\cdot {f_ck}\right)^{{1/3}} = {v_rdc}\ \mathrm{{МПа}}"
        )

        st.write("Минимальное сопротивление продавливанию по (6.3N):")
        st.latex(
            fr"v_{{min}} = 0.035\cdot k^{{3/2}}\cdot f_{{ck}}^{{1/2}}"
            fr" = 0.035\cdot {k}^{{3/2}}\cdot {f_ck}^{{1/2}} = {v_rdc_min}\ \mathrm{{МПа}}"
        )

        st.write("Расчётное значение сопротивления продавливанию:")
        st.latex(
            fr"V_{{Rd,c}} = \max\left(V_{{Rd,c}},\ v_{{min}}\right) = \max\left({v_rdc},\ {v_rdc_min}\right) = {v_rdc_design}\ \mathrm{{МПа}}"
        )

        st.write("Проверка условия по (6.4.3(2)):")
        if v_ed <= v_rdc_design:
            st.latex(fr"v_{{Ed}} = {v_ed}\ \mathrm{{МПа}} \leq V_{{Rd,c}} = {v_rdc_design}\ \mathrm{{МПа}}")
            st.success("Условие выполняется — поперечная арматура на продавливание не требуется.")
        else:
            st.latex(fr"v_{{Ed}} = {v_ed}\ \mathrm{{МПа}} > V_{{Rd,c}} = {v_rdc_design}\ \mathrm{{МПа}}")
            st.error("Условие не выполняется — требуется поперечная арматура на продавливание (расчёт по 6.4.5).")

            if st.button("Расчёт поперечной арматуры на продавливание (по 6.4.5)", key="calc_shear_rebar"):
                st.write("Расчёт поперечной арматуры на продавливание (по 6.4.5) пока не реализован.")