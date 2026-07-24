import streamlit as st

from data.concrete import CONCRETE_CLASSES_PRECISE, CONCRETE_CLASSES
from calculations.calc_creep_coef import (
    calc_autogenous_shrinkage,
    calc_kh,
    calc_epsilon_cd0,
    calc_drying_shrinkage,
    calc_total_shrinkage,
)


st.title("Ползучесть и усадка бетона")
st.caption("п.3.1.4 СП РК EN 1992-1-1:2004/2011")
# st.write("P Ползучесть и усадка бетона зависят, в основном, от относительной влажности окружающей среды, геометрических размеров конструктивного элемента и состава бетона. На ползучесть бетона также оказывает влияние степень зрелости бетона (начальная прочность) при первоначальном приложении нагрузки, а также продолжительность нагружения и величина нагрузки")


concrete_list = list(CONCRETE_CLASSES)




concrete = st.selectbox("Класс бетона", concrete_list)
concrete_table = CONCRETE_CLASSES
area = st.number_input("Площадь поперечного сечения Aс, мм", value=126000, min_value=0)
perimetr = st.number_input("Периметр сечения u, мм", value=2360, min_value=0)
relative_humidity = st.number_input("Относительная влажность бетона RH, %", value=80, min_value=0, max_value=100)

t = st.number_input("Возраст бетона на рассматриваемый период, суток", value=30, min_value=0)
ts = st.number_input("возраст бетона к моменту окончания влажного хранения бетона, суток", value=3, min_value=0)


f_ck = concrete_table[concrete]["fck"]
epsilon_sa, betta_as, epsilon_sat, h0 = calc_autogenous_shrinkage(f_ck, t, area, perimetr)

epsilon_sa_e6 = epsilon_sa * 1e6
epsilon_sat_e6 = epsilon_sat * 1e6

st.write("Предельная величина усадки от аутогенного эффекта (3.11):")
st.latex(fr"\varepsilon_{{ca}}(\infty) = 2.5\cdot(f_{{ck}} - 10)\cdot 10^{{-6}} = 2.5\cdot({f_ck} - 10)\cdot 10^{{-6}} = {epsilon_sa_e6:g}\cdot 10^{{-6}}")

st.write(f"Коэффициент развития во времени, t = {t} суток (3.13):")
st.latex(fr"\beta_{{as}}(t) = 1 - \exp(-0.2\cdot t^{{0.5}}) = 1 - \exp(-0.2\cdot {t}^{{0.5}}) = {betta_as}")

st.write(f"Усадка от аутогенного эффекта на момент времени t (3.12):")
st.latex(fr"\varepsilon_{{ca}}(t) = \beta_{{as}}(t)\cdot \varepsilon_{{ca}}(\infty) = {betta_as}\cdot {epsilon_sa_e6:g}\cdot 10^{{-6}} = {epsilon_sat_e6:g}\cdot 10^{{-6}}")

st.write("Приведённый размер поперечного сечения h0:")
st.latex(fr"h_0 = \dfrac{{2\cdot A_c}}{{u}} = \dfrac{{2\cdot {area}}}{{{perimetr}}} = {h0}\ \mathrm{{мм}}")

kh = calc_kh(h0)
epsilon_cd0 = calc_epsilon_cd0(f_ck, relative_humidity)
betta_ds, epsilon_cd = calc_drying_shrinkage(t, ts, h0, kh, epsilon_cd0)
epsilon_cs = calc_total_shrinkage(epsilon_cd, epsilon_sat)

epsilon_cd_e6 = epsilon_cd * 1e6
epsilon_cs_e6 = epsilon_cs * 1e6

st.write(f"Коэффициент kh по таблице 3.3 (интерполяция по h0 = {h0} мм):")
st.latex(fr"k_h = {kh}")

st.write(f"Номинальное значение εcd,0 по таблице 3.2 (интерполяция по f_ck = {f_ck} МПа, RH = {relative_humidity}%):")
st.latex(fr"\varepsilon_{{cd,0}} = {epsilon_cd0}\cdot 10^{{-3}}")

st.write(f"Коэффициент развития усадки при высыхании во времени, ts = {ts} суток (3.10):")
st.latex(fr"\beta_{{ds}}(t,t_s) = \dfrac{{t - t_s}}{{(t-t_s) + 0.04\sqrt{{h_0^3}}}} = \dfrac{{{t} - {ts}}}{{({t}-{ts}) + 0.04\sqrt{{{h0}^3}}}} = {betta_ds}")

st.write("Усадка при высыхании на момент времени t (3.9):")
st.latex(fr"\varepsilon_{{cd}}(t) = \beta_{{ds}}(t,t_s)\cdot k_h\cdot \varepsilon_{{cd,0}} = {betta_ds}\cdot {kh}\cdot {epsilon_cd0}\cdot 10^{{-3}} = {epsilon_cd_e6:g}\cdot 10^{{-6}}")

st.write("Окончательная (полная) усадка бетона (3.8):")
st.latex(fr"\varepsilon_{{cs}} = \varepsilon_{{cd}}(t) + \varepsilon_{{ca}}(t) = {epsilon_cd_e6:g}\cdot 10^{{-6}} + {epsilon_sat_e6:g}\cdot 10^{{-6}} = {epsilon_cs_e6:g}\cdot 10^{{-6}}")
