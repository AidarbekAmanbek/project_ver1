import streamlit as st

from data.concrete import CONCRETE_CLASSES
from data.punching_shear import (
    BETA_VALUES,
    CONSTRUCTION_TYPES,
    COLUMN_TYPES,
    BETTA_CHECK_TYPES,
    REBAR_INCLUDE_TYPES,
)
from calculations.calc_punching_shear import (
    calc_effective_depth,
    calc_reinforcement_ratio,
    calc_punching_shear_stress,
    calc_punching_shear_resistance,
    calc_punching_shear_resistance_with_rebar,
    calc_control_perimeter_u1,
    capture_punchin_shear_column_circle,
    input_row,
    select_row,
)


st.title("Расчет на продавливание")
st.caption("п.6.4.1 СП РК EN 1992-1-1:2004/2011")


with st.container(border=True):
    concrete_classes = list(CONCRETE_CLASSES)
    concrete = select_row("Класс бетона, $f_{ck}$ (МПа):", concrete_classes, index=2)
    construction_types = select_row(
        "Место приложение нагрузки:",
        list(CONSTRUCTION_TYPES),
        format_func=lambda key: CONSTRUCTION_TYPES[key],
    )
    column_types = select_row(
        "Форма колонны:",
        list(COLUMN_TYPES),
        index=0,
        format_func=lambda key: COLUMN_TYPES[key],
    )


with st.container(border=True):
    if construction_types == "floor_slab":
        plate_thickness = input_row("Толщина плиты перекрытия/покрытия, $h$ (мм)", value=200)
        cover = input_row("Защитный слой бетона, по нижней грани (мм)", value=35)
        vertical_shear_force = input_row("Расчетное значение поперечного усилия, $V_{Ed}$ (кН)", value=500)

    elif construction_types == "foundation_slab":
        plate_thickness = input_row("Толщина фундаментной плиты, $h$ (мм)", value=500)
        cover = input_row("Защитный слой бетона, по нижней грани (мм)", value=50)
        vertical_shear_force = input_row("Расчетное значение поперечного усилия, $V_{Ed}$ (кН)", value=500)
        upward_pressure_soil = input_row("Давление, направленное вверх от грунта, за исключением собственного веса плиты, $p_{Ed}$ (кПа)", value=0)


with st.container(border=True):
    if column_types == "rectangular":
        c1 = input_row("Высота колонны, $c_{1}$ (мм)", value=400)
        c2 = input_row("Ширина колонны, $c_{2}$ (мм)", value=400)
    elif column_types == "circular":
        diametr = input_row("Диаметр колонны, $c$ (мм)", value=300)
    else:
        dimension = input_row("Контрольный периметр, $u_{1}$ (мм)", value=2340)


st.write("Расположение колонны:") 
with st.container(border=True):
    betta_check = select_row(
        "Значения коэффициента $β$:",
        list(BETTA_CHECK_TYPES),
        index=0,
        format_func=lambda key: BETTA_CHECK_TYPES[key],
    )

    if betta_check == "figure":
        column_position = select_row("Расположение колонны:", list(BETA_VALUES), index=0)
        betta = BETA_VALUES[column_position]
        col1, col2 = st.columns([1, 1])
        with col2:
            st.popover("Показать Рисунок 6.21N").image(
                "assets/punching_sheap/coef_betta.png", width=350)

    elif betta_check == "formula":
        M_ed_y = input_row("Расчетный изгибающий момент, $M_{Ed,y}$ (кН·м)", value=0.0)
        M_ed_z = input_row("Расчетный изгибающий момент, $M_{Ed,z}$ (кН·м)", value=0.0)

    elif betta_check == "manual":
        betta = input_row("Коэффициент β:", value=1.15)

st.write("Параметры армирования плиты:") 
with st.container(border=True):
    rebar_x = input_row("Диаметр арматуры в направлении x, (мм)", value=12)
    rebar_x_spacing = input_row("Шаг арматуры в направлении x, (мм)", value=200)
    rebar_y = input_row("Диаметр арматуры в направлении y, (мм)", value=12)
    rebar_y_spacing = input_row("Шаг арматуры в направлении y, (мм)", value=200)

 
with st.container(border=True):
    rebar_include = select_row(
        "Вид расчета",
        list(REBAR_INCLUDE_TYPES),
        index=0,
        format_func=lambda key: REBAR_INCLUDE_TYPES[key],
    )
    if rebar_include == "with_shear_rebar":
        sw_diametr = input_row("Диаметр поперечной арматуры, $A_{sw}$ (мм)", value=8)
        f_ywd = input_row("Расчетный предел текучести поперечной арматуры;, $f _{ywd}$ (мм)", value=500)
        s_r = input_row("Шаг поперечной арматуры, $s_{r}$ (мм)", value=200)
        alpha = input_row("Угол наклона поперечной арматуры, $\\alpha$ (°)", value=90)


with st.expander("Параметры установленные в национальном приложении"):
    a_cc = input_row(
        "Коэффициент, учитывающий влияние длительных процессов на прочность при сжатии, $\\alpha_{cc}$",
        value=0.85)
    y_c = input_row("Частный коэффициент безопасности для бетона, $\\gamma_c$:", value=1.5)
    y_s = input_row("Частный коэффициент безопасности для арматуры, $\\gamma_s$:", value=1.15)
    c_rdc_coef = input_row("Частный коэффициент, $C_{Rd,c}$", value=18)
    k1 = input_row("Частный коэффициент, $k_1$", value=0.1)



# if st.button("Расчет", key="calculate"):
with st.container(border=True):
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



    if betta_check == "formula":
        st.warning(
            "Расчёт коэффициента β по изгибающим моментам (6.42, 6.43) ещё не реализован. "
            "Выберите другой способ определения β."
        )
    else:
        if column_types == "rectangular":
            u1, pi_val = calc_control_perimeter_u1([c1, c2], d_eff, column_types)
            st.write("Контрольный периметр $u_1$ (на расстоянии $2d$ от грани прямоугольной колонны):")
            st.latex(
                fr"u_1 = 2\cdot c_1 + 2\cdot c_2 + 2\cdot\pi\cdot 2d"
                fr" = 2\cdot {c1} + 2\cdot {c2} + 2\cdot {pi_val}\cdot 2\cdot {d_eff} = {u1}\ \mathrm{{мм}}"
            )
        elif column_types == "circular":
            u1, pi_val = calc_control_perimeter_u1(diametr, d_eff, column_types)
            st.write("Контрольный периметр $u_1$ (окружность на расстоянии $2d$ от грани круглой колонны):")
            st.latex(
                fr"u_1 = 2\pi\left(\dfrac{{c}}{{2}} + 2d\right)"
                fr" = 2\cdot {pi_val}\cdot\left(\dfrac{{{diametr}}}{{2}} + 2\cdot {d_eff}\right) = {u1}\ \mathrm{{мм}}"
            )
        else:
            u1 = dimension
            st.write("Контрольный периметр $u_1$ задан вручную:")
            st.latex(fr"u_1 = {u1}\ \mathrm{{мм}}")

    # if column_types == "circular":
    #     capture_punchin_shear_column_circle(diametr, d_eff)
    #     st.caption("Рисунок 6.20N. Контрольный периметр для круглой колонны")


        v_Ed = calc_punching_shear_stress(u1, betta, vertical_shear_force, d_eff)
        st.write("Максимальное напряжение среза, вызванное местной сосредоточенной нагрузкой, по (6.33):")
        st.latex(
            fr"v_{{Ed}} = \dfrac{{\beta\cdot V_{{Ed}}}}{{u_1\cdot d}}"
            fr" = \dfrac{{{betta}\cdot {vertical_shear_force}\cdot 10^3}}{{{u1}\cdot {d_eff}}} = {v_Ed}\ \mathrm{{МПа}}"
        )
    if column_types == "rectangular":
        As_x, As_y, b_x, b_y, n_x, n_y, p_lx, p_ly, p_l = calc_reinforcement_ratio(
            rebar_x, rebar_y, rebar_x_spacing, rebar_y_spacing, c2, c1, d_eff
        )

        st.write(f"Площадь сечения стержня Ø{rebar_x:.0f} (направление x) и Ø{rebar_y:.0f} (направление y):")
        st.latex(fr"A_{{s,x}} = {As_x}\ \mathrm{{мм^2}}, \quad A_{{s,y}} = {As_y}\ \mathrm{{мм^2}}")

        st.write("Ширина расчётной полосы (колонна + 3d в каждую сторону):")
        st.latex(
            fr"b_x = c_2 + 6d = {c2} + 6\cdot {d_eff} = {b_x}\ \mathrm{{мм}}, \quad"
            fr" b_y = c_1 + 6d = {c1} + 6\cdot {d_eff} = {b_y}\ \mathrm{{мм}}"
        )

        st.write("Число стержней в пределах расчётной полосы:")
        st.latex(
            fr"n_x = \left\lfloor \dfrac{{b_x}}{{s_x}} \right\rfloor = \left\lfloor \dfrac{{{b_x}}}{{{rebar_x_spacing}}} \right\rfloor = {n_x},"
            fr" \quad n_y = \left\lfloor \dfrac{{b_y}}{{s_y}} \right\rfloor = \left\lfloor \dfrac{{{b_y}}}{{{rebar_y_spacing}}} \right\rfloor = {n_y}"
        )

        st.write("Коэффициент армирования в направлении x по (6.32):")
        st.latex(
            fr"\rho_{{lx}} = \dfrac{{n_x\cdot A_{{s,x}}}}{{b_x\cdot d}} = \dfrac{{{n_x}\cdot {As_x}}}{{{b_x}\cdot {d_eff}}} = {p_lx}"
        )

        st.write("Коэффициент армирования в направлении y по (6.32):")
        st.latex(
            fr"\rho_{{ly}} = \dfrac{{n_y\cdot A_{{s,y}}}}{{b_y\cdot d}} = \dfrac{{{n_y}\cdot {As_y}}}{{{b_y}\cdot {d_eff}}} = {p_ly}"
        )

        st.write("Комбинированный коэффициент армирования по (6.32):")
        st.latex(
            fr"\rho_{{l}} = \sqrt{{\rho_{{lx}}\cdot\rho_{{ly}}}} = \sqrt{{{p_lx}\cdot {p_ly}}} = {p_l}"
        )

        f_ck = CONCRETE_CLASSES[concrete]["fck"]
        C_Rdc, k, V_Rdc, V_Rdc_min, V_Rdc_design = calc_punching_shear_resistance(
            d_eff, p_l, f_ck, y_c, c_rdc_coef, k1
        )

        st.write("Расчётное сопротивление бетона продавливанию без поперечной арматуры:")
        st.latex(
            fr"C_{{Rd,c}} = \dfrac{{C_{{Rd,c}}}}{{\gamma_c}} = \dfrac{{{c_rdc_coef}/100}}{{{y_c}}} = {C_Rdc}"
        )

        st.write("Коэффициент k:")
        st.latex(
            fr"k = 1 + \sqrt{{\dfrac{{200}}{{d}}}} = 1 + \sqrt{{\dfrac{{200}}{{{d_eff}}}}} = {k}"
        )

        st.write("Расчётное сопротивление продавливанию по (6.47):")
        st.latex(
            fr"V_{{Rd,c}} = C_{{Rd,c}}\cdot k\cdot\left(100\cdot\rho_l\cdot f_{{ck}}\right)^{{1/3}}"
            fr" = {C_Rdc}\cdot {k}\cdot\left(100\cdot {p_l}\cdot {f_ck}\right)^{{1/3}} = {V_Rdc}\ \mathrm{{МПа}}"
        )

        st.write("Минимальное сопротивление продавливанию по (6.3N):")
        st.latex(
            fr"v_{{min}} = 0.035\cdot k^{{3/2}}\cdot f_{{ck}}^{{1/2}}"
            fr" = 0.035\cdot {k}^{{3/2}}\cdot {f_ck}^{{1/2}} = {V_Rdc_min}\ \mathrm{{МПа}}"
        )

        st.write("Расчётное значение сопротивления продавливанию:")
        st.latex(
            fr"V_{{Rd,c}} = \max\left(V_{{Rd,c}},\ v_{{min}}\right) = \max\left({V_Rdc},\ {V_Rdc_min}\right) = {V_Rdc_design}\ \mathrm{{МПа}}"
        )

        if betta_check != "formula":
            st.write("Проверка условия по (6.4.3(2)):")
            if v_Ed <= V_Rdc_design:
                st.latex(fr"v_{{Ed}} = {v_Ed}\ \mathrm{{МПа}} \leq V_{{Rd,c}} = {V_Rdc_design}\ \mathrm{{МПа}}")
                st.success("Условие выполняется — поперечная арматура на продавливание не требуется.")
            else:
                st.latex(fr"v_{{Ed}} = {v_Ed}\ \mathrm{{МПа}} > V_{{Rd,c}} = {V_Rdc_design}\ \mathrm{{МПа}}")
                st.error("Условие не выполняется — требуется поперечная арматура на продавливание (расчёт по 6.4.5).")

            if rebar_include == "with_shear_rebar":
                V_Rdcs, f_ywd_ef, Asw = calc_punching_shear_resistance_with_rebar(
                    V_Rdc_design, u1, d_eff, sw_diametr, f_ywd, s_r, alpha
                )

                st.write("Расчётный предел текучести поперечной арматуры с учётом эффективности:")
                st.latex(
                    fr"f_{{ywd,ef}} = \min\left(250 + 0.25d,\ f_{{ywd}}\right)"
                    fr" = \min\left(250 + 0.25\cdot {d_eff},\ {f_ywd}\right) = {f_ywd_ef}\ \mathrm{{МПа}}"
                )

                st.write(f"Площадь сечения одного стержня поперечной арматуры Ø{sw_diametr:.0f}:")
                st.latex(fr"A_{{sw}} = {Asw}\ \mathrm{{мм^2}}")

                st.write("Сопротивление продавливанию с учётом поперечной арматуры по (6.4.5):")
                st.latex(
                    fr"V_{{Rd,cs}} = 0.75\cdot V_{{Rd,c}} + 1.5\cdot\dfrac{{d}}{{s_r}}\cdot A_{{sw}}\cdot f_{{ywd,ef}}\cdot\dfrac{{1}}{{u_1\cdot d}}\cdot\sin\alpha"
                    fr" = 0.75\cdot {V_Rdc_design} + 1.5\cdot\dfrac{{{d_eff}}}{{{s_r}}}\cdot {Asw}\cdot {f_ywd_ef}\cdot\dfrac{{1}}{{{u1}\cdot {d_eff}}}\cdot\sin({alpha}^\circ) = {V_Rdcs}\ \mathrm{{МПа}}"
                )

                st.write("Проверка условия по (6.4.5):")
                if v_Ed <= V_Rdcs:
                    st.latex(fr"v_{{Ed}} = {v_Ed}\ \mathrm{{МПа}} \leq V_{{Rd,cs}} = {V_Rdcs}\ \mathrm{{МПа}}")
                    st.success("Условие выполняется — принятой поперечной арматуры достаточно.")
                else:
                    st.latex(fr"v_{{Ed}} = {v_Ed}\ \mathrm{{МПа}} > V_{{Rd,cs}} = {V_Rdcs}\ \mathrm{{МПа}}")
                    st.error("Условие не выполняется — необходимо увеличить количество поперечной арматуры (уменьшить шаг $s_r$ или увеличить $\\varnothing_{sw}$).")

    else:
        st.info("Расчет коэффициента армирования ещё не реализован. Выберите прямоугольную колонну.")