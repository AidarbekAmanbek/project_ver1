import streamlit as st

from data.concrete import CONCRETE_CLASSES
from data.punching_shear import BETA_VALUES
from calculations.calc_punching_shear import (
    calc_effective_depth,
    calc_reinforcement_ratio,
    calc_punching_shear_stress,
    calc_punching_shear_resistance,
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
        "Место приложение нагрузки:", ("Плита перекрытия/покрытия", "Фундаментная плита")
    )
    column_types = select_row("Форма колонны:", ("Прямоугольная", "Круглая", "Сложная"), index=1)

with st.container(border=True):
    if construction_types == "Плита перекрытия/покрытия":
        plate_thickness = input_row("Толщина плиты перекрытия/покрытия, $h$ (мм)", value=200)
        cover = input_row("Защитный слой бетона, по нижней грани (мм)", value=35)
        vertical_shear_force = input_row("Расчетное значение поперечного усилия, $V_{Ed}$ (кН)", value=500)
        
    elif construction_types == "Фундаментная плита":
        plate_thickness = input_row("Толщина фундаментной плиты, $h$ (мм)", value=500)
        cover = input_row("Защитный слой бетона, по нижней грани (мм)", value=50)
        vertical_shear_force = input_row("Расчетное значение поперечного усилия, $V_{Ed}$ (кН)", value=500)
        upward_pressure_soil = input_row("Давление, направленное вверх от грунта, за исключением собственного веса плиты, $p_{Ed}$ (кПа)", value=0)
        
    

with st.container(border=True):
    if column_types == "Прямоугольная":
        c1 = input_row("Высота колонны, $c_{1}$ (мм)", value=400)
        c2 = input_row("Ширина колонны, $c_{2}$ (мм)", value=400)
    elif column_types == "Круглая":
        diametr = input_row("Диаметр колонны, $c$ (мм)", value=300)
    else:
        dimension = input_row("Контрольный периметр, $u_{1}$ (мм)", value=2340)
    
with st.container(border=True):
    rebar_include = select_row("Вид расчета", ("без поперечной арматуры", "с поперечной арматурой"), index=0)
    if rebar_include == "с поперечной арматурой":
        s_r = input_row("Шаг поперечной арматуры, $s_{r}$ (мм)", value=200)
        alpha = input_row("Угол наклона поперечной арматуры, $\\alpha$ (°)", value=90)

with st.container(border=True):
    betta_check = select_row("Значения коэффициента $β$:", 
        ("определить по рисунку 6.21N", "определить по формуле 6.42 и 6.43", "прописать вручную"), index=0)

    if betta_check == "определить по рисунку 6.21N":
        column_position = select_row("Расположение колонны:", list(BETA_VALUES), index=0)
        betta = BETA_VALUES[column_position]
        col1, col2 = st.columns([1, 1])
        with col2:
            st.popover("Показать Рисунок 6.21N").image(
                "assets/punching_sheap/coef_betta.png", width=350)
            
    elif betta_check == "определить по формуле 6.42 и 6.43":
        M_ed_y = input_row("Расчетный изгибающий момент, $M_{Ed,y}$ (кН·м)", value=0.0)
        M_ed_z = input_row("Расчетный изгибающий момент, $M_{Ed,z}$ (кН·м)", value=0.0)

    elif betta_check == "прописать вручную":
        betta = input_row("Коэффициент β:", value=1.15)

with st.container(border=True):
    rebar_x = input_row("Диаметр арматуры в направлении x, (мм)", value=12)
    rebar_x_spacing = input_row("Шаг арматуры в направлении x, (мм)", value=200)
    rebar_y = input_row("Диаметр арматуры в направлении y, (мм)", value=12)
    rebar_y_spacing = input_row("Шаг арматуры в направлении y, (мм)", value=200)



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

    if column_types == "Круглая":
        capture_punchin_shear_column_circle(diametr, d_eff)
        st.caption("Рисунок 6.20N. Контрольный периметр для круглой колонны")

        