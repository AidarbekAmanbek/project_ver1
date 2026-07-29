import streamlit as st

from data.concrete import CONCRETE_CLASSES
from calculations.calc_punching_shear import calc_effective_depth


st.title("Продавливание")
st.caption("п.4.1 СП РК EN 1992-1-1:2004/2011")

st.subheader("Геометрия колонны")
column_type = st.selectbox("Форма колонны:", ("Прямоугольная", "Круглая", "Сложная"))

if column_type == "Прямоугольная":
    height = st.number_input("Высота c1, мм:", value=400, disabled=column_type == "Круглая")
    weight = st.number_input("Ширина c2, мм:", value=400, disabled=column_type == "Круглая")
elif column_type == "Круглая":
    radius = st.number_input("Радиус, мм:", value=250, disabled=column_type == "Прямоугольная")
else:
    dimension = st.number_input("Контрольный периметр ui, мм:", value=300)


plate_thickness = st.number_input("Толщина плиты перекрытия/покрытия, мм", min_value=0, value=250)
concrete_classes = list(CONCRETE_CLASSES)
concrete = st.selectbox("Класс прочности бетона:", concrete_classes, index=3)
rebar_y = st.number_input("Диаметр арматуры, мм", min_value=0, value=14)
# rebar_z = st.number_input("Диаметр арматуры, мм", min_value=0)
rebar_spacing = st.number_input("Шаг арматуры, мм", min_value=0, value=100)
cover = st.number_input("Защитный слой бетона, мм", min_value=0, value=25)


st.subheader("Коэффициент β")
betta_check = st.checkbox("Принимать значения коэффициента β, приведенные на рисунке 6.21N", value=True)

if betta_check == True:
    column_position = st.selectbox(
        "Расположение колонны:",
        ("Внутренняя (β = 1.15)", "Крайняя (β = 1.4)", "Угловая (β = 1.5)"),
    )

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


st.subheader("Нагрузки")
vertical_shear_force = st.number_input("Расчетное значение поперечного усилия VEd, кН", min_value=0, value=500)


st.subheader("Параметры установленные в национальном приложений")
a_cc = st.number_input(
    "αcc - коэффициент, учитывающий влияние длительных процессов на прочность при сжатии",
    value=0.85,
    key="a_cc",
)
y_c = st.number_input("γc - частный коэффициент безопасности для бетона", value=1.5, key="y_c")
y_s = st.number_input("γs - частный коэффициент безопасности для арматуры", value=1.15, key="y_s")


if st.button("Расчет"):
    st.write("Результат")


    st.write("Определяем расстояния от верха плиты до центров тяжести арматуры каждого направления")
    a = calc_effective_depth(plate_thickness, cover, rebar_y, rebar_spacing)
    st.write(f"{a}")


# core_dy = st.number_input("Полезная высота для арматуры в направлении y, dy, мм", min_value=0)
# core_dz = st.number_input("Полезная высота для арматуры в направлении z, dz, мм", min_value=0)

# vertical_shear_force = st.number_input("Расчетное значение поперечного усилия VEd, кН", min_value=0)



# st.subheader("Материалы и армирование")



# y_c = st.number_input("γc - частный коэффициент безопасности для бетона", value=1.5)

# rho_y = st.number_input(
#     "Коэффициент армирования продольной арматурой в направлении y, ρy, %",
#     min_value=0.0,
#     max_value=2.0,
#     value=0.5,
#     step=0.05,
# )
# rho_z = st.number_input(
#     "Коэффициент армирования продольной арматурой в направлении z, ρz, %",
#     min_value=0.0,
#     max_value=2.0,
#     value=0.5,
#     step=0.05,
# )

# st.subheader("Параметры национального приложения:")