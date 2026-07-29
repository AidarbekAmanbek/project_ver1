import streamlit as st

from data.concrete import CONCRETE_CLASSES_PRECISE, CONCRETE_CLASSES
from data.creep_shrinkage import CEMENT_CLASS
from calculations.calc_creep_coef import (
    calc_autogenous_shrinkage,
    calc_kh,
    calc_epsilon_cd0,
    calc_drying_shrinkage,
    calc_total_shrinkage,
    calc_creep_coefficient,
)


st.title("Ползучесть и усадка бетона")
st.caption("п.3.1.4 СП РК EN 1992-1-1:2004/2011")

concrete_list = list(CONCRETE_CLASSES)
cement_list = list(CEMENT_CLASS)

concrete = st.selectbox("Класс бетона", concrete_list, index=2)
concrete_table = CONCRETE_CLASSES
area = st.number_input("Площадь поперечного сечения Aс, мм", value=126000, min_value=0)
perimetr = st.number_input("Периметр сечения u, мм", value=2360, min_value=0)
relative_humidity = st.number_input("Относительная влажность бетона RH, %", value=80, min_value=0, max_value=100)

t0 = st.number_input("Возраст бетона при приложении нагрузки t0, суток", value=30, min_value=0)
ts = st.number_input("Возраст бетона к моменту окончания влажного хранения (начала высыхания) ts, суток", value=3, min_value=0)
t = st.number_input("Возраст бетона на момент, для которого выполняется расчёт t, суток", value=18250, min_value=0)

cement = st.selectbox("Класс цемента:", cement_list, index=1)

f_ck = concrete_table[concrete]["fck"]
f_cm = concrete_table[concrete]["fcm"]
epsilon_sa, betta_as, epsilon_sat, h0 = calc_autogenous_shrinkage(f_ck, t, area, perimetr)

epsilon_sa_e6 = epsilon_sa * 1e6
epsilon_sat_e6 = epsilon_sat * 1e6

if st.button("Выполнить расчет"):
    st.write("Предельная величина усадки от аутогенного эффекта (3.11):")
    st.latex(fr"\varepsilon_{{ca}}(\infty) = 2.5\cdot(f_{{ck}} - 10)\cdot 10^{{-6}} = 2.5\cdot({f_ck} - 10)\cdot 10^{{-6}} = {epsilon_sa_e6:g}\cdot 10^{{-6}}")

    st.write(f"Коэффициент развития во времени, t = {t} суток (3.13):")
    st.latex(fr"\beta_{{as}}(t) = 1 - \exp(-0.2\cdot t^{{0.5}}) = 1 - \exp(-0.2\cdot {t}^{{0.5}}) = {betta_as}")

    st.write(f"Усадка от аутогенного эффекта на момент времени t (3.12):")
    st.latex(fr"\varepsilon_{{ca}}(t) = \beta_{{as}}(t)\cdot \varepsilon_{{ca}}(\infty) = {betta_as}\cdot {epsilon_sa_e6:g}\cdot 10^{{-6}} = {epsilon_sat_e6:g}\cdot 10^{{-6}}")

    st.write("Приведённый размер поперечного сечения h0:")
    st.latex(fr"h_0 = \dfrac{{2\cdot A_c}}{{u}} = \dfrac{{2\cdot {area}}}{{{perimetr}}} = {h0}\ \mathrm{{мм}}")

    kh = calc_kh(h0)
    epsilon_cd0 = calc_epsilon_cd0(f_cm, relative_humidity, cement)
    betta_ds, epsilon_cd = calc_drying_shrinkage(t, ts, h0, kh, epsilon_cd0)
    epsilon_cs = calc_total_shrinkage(epsilon_cd, epsilon_sat)

    epsilon_cd_e6 = epsilon_cd * 1e6
    epsilon_cs_e6 = epsilon_cs * 1e6

    st.write(f"Коэффициент kh по таблице 3.3 (интерполяция по h0 = {h0} мм):")
    st.latex(fr"k_h = {kh}")

    ads1 = CEMENT_CLASS[cement]["ads1"]
    ads2 = CEMENT_CLASS[cement]["ads2"]
    betta_rh = 1.55 * (1 - (relative_humidity / 100) ** 3)
    epsilon_cd0_e6 = epsilon_cd0 * 1e6

    st.write(f"Коэффициент βRH, RH = {relative_humidity}% (B.12):")
    st.latex(fr"\beta_{{RH}} = 1.55\left[1 - \left(\dfrac{{RH}}{{100}}\right)^3\right] = 1.55\left[1 - \left(\dfrac{{{relative_humidity}}}{{100}}\right)^3\right] = {betta_rh:.4f}")

    st.write(f"Номинальное значение εcd,0, цемент класса {cement} (αds1={ads1}, αds2={ads2}), f_cm = {f_cm} МПа (B.11):")
    st.latex(fr"\varepsilon_{{cd,0}} = 0.85\left[(220 + 110\cdot\alpha_{{ds1}})\cdot\exp\left(-\alpha_{{ds2}}\cdot\dfrac{{f_{{cm}}}}{{f_{{cmo}}}}\right)\right]\cdot 10^{{-6}}\cdot\beta_{{RH}} = 0.85\left[(220 + 110\cdot{ads1})\cdot\exp\left(-{ads2}\cdot\dfrac{{{f_cm}}}{{10}}\right)\right]\cdot 10^{{-6}}\cdot {betta_rh:.4f} = {epsilon_cd0_e6:g}\cdot 10^{{-6}}")

    st.write(f"Коэффициент развития усадки при высыхании во времени, t = {t} суток, ts = {ts} суток (3.10):")
    st.latex(fr"\beta_{{ds}}(t,t_s) = \dfrac{{t - t_s}}{{(t-t_s) + 0.04\sqrt{{h_0^3}}}} = \dfrac{{{t} - {ts}}}{{({t}-{ts}) + 0.04\sqrt{{{h0}^3}}}} = {betta_ds}")

    st.write("Усадка при высыхании на момент времени t (3.9):")
    st.latex(fr"\varepsilon_{{cd}}(t) = \beta_{{ds}}(t,t_s)\cdot k_h\cdot \varepsilon_{{cd,0}} = {betta_ds}\cdot {kh}\cdot {epsilon_cd0_e6:g}\cdot 10^{{-6}} = {epsilon_cd_e6:g}\cdot 10^{{-6}}")

    st.write(f"Полная усадка бетона на момент времени t = {t} суток (3.8):")
    st.latex(fr"\varepsilon_{{cs}}(t) = \varepsilon_{{cd}}(t) + \varepsilon_{{ca}}(t) = {epsilon_cd_e6:g}\cdot 10^{{-6}} + {epsilon_sat_e6:g}\cdot 10^{{-6}} = {epsilon_cs_e6:g}\cdot 10^{{-6}}")

    epsilon_cd_inf = kh * epsilon_cd0
    epsilon_cs_inf = calc_total_shrinkage(epsilon_cd_inf, epsilon_sa)

    epsilon_cd_inf_e6 = epsilon_cd_inf * 1e6
    epsilon_cs_inf_e6 = epsilon_cs_inf * 1e6

    st.write("Предельная усадка при высыхании, t → ∞ (β_ds → 1):")
    st.latex(fr"\varepsilon_{{cd}}(\infty) = k_h\cdot \varepsilon_{{cd,0}} = {kh}\cdot {epsilon_cd0_e6:g}\cdot 10^{{-6}} = {epsilon_cd_inf_e6:g}\cdot 10^{{-6}}")

    st.write("Окончательная (предельная) усадка бетона, εcs(∞,ts) (3.8):")
    st.latex(fr"\varepsilon_{{cs}}(\infty) = \varepsilon_{{cd}}(\infty) + \varepsilon_{{ca}}(\infty) = {epsilon_cd_inf_e6:g}\cdot 10^{{-6}} + {epsilon_sa_e6:g}\cdot 10^{{-6}} = {epsilon_cs_inf_e6:g}\cdot 10^{{-6}}")


    phi_0, alpha_1, alpha_2, h0_b, betta_fcm, betta_t0, phi_RH = calc_creep_coefficient(f_cm, t0, t, relative_humidity, area, perimetr)

    st.write("Коэффициент ползучести (Приложение В. СП РК EN 1992-1-1:2004/2011)")

    st.write(f"Коэффициенты α1, α2, учитывающие влияние прочности бетона (B.8c):")
    st.latex(fr"\alpha_1 = \left(\dfrac{{35}}{{f_{{cm}}}}\right)^{{0.7}} = \left(\dfrac{{35}}{{{f_cm}}}\right)^{{0.7}} = {alpha_1}")
    st.latex(fr"\alpha_2 = \left(\dfrac{{35}}{{f_{{cm}}}}\right)^{{0.2}} = \left(\dfrac{{35}}{{{f_cm}}}\right)^{{0.2}} = {alpha_2}")

    st.write(f"Коэффициент β(fcm), учитывающий влияние прочности бетона на сжатие (B.4):")
    st.latex(fr"\beta(f_{{cm}}) = \dfrac{{16.8}}{{\sqrt{{f_{{cm}}}}}} = \dfrac{{16.8}}{{\sqrt{{{f_cm}}}}} = {betta_fcm}")

    st.write(f"Коэффициент β(t0), учитывающий влияние возраста бетона при загружении, t0 = {t0} суток (B.5):")
    st.latex(fr"\beta(t_0) = \dfrac{{1}}{{0.1 + t_0^{{0.2}}}} = \dfrac{{1}}{{0.1 + {t0}^{{0.2}}}} = {betta_t0}")

    st.write(f"Коэффициент φRH, учитывающий влияние относительной влажности воздуха, RH = {relative_humidity}% (B.2):")
    if f_cm <= 35:
        st.latex(fr"\varphi_{{RH}} = 1 + \dfrac{{1 - RH/100}}{{0.1\cdot\sqrt[3]{{h_0}}}} = 1 + \dfrac{{1 - {relative_humidity}/100}}{{0.1\cdot\sqrt[3]{{{h0_b}}}}} = {phi_RH}")
    else:
        st.latex(fr"\varphi_{{RH}} = \left(1 + \dfrac{{1 - RH/100}}{{0.1\cdot\sqrt[3]{{h_0}}}}\cdot \alpha_1\right)\cdot \alpha_2 = \left(1 + \dfrac{{1 - {relative_humidity}/100}}{{0.1\cdot\sqrt[3]{{{h0_b}}}}}\cdot {alpha_1}\right)\cdot {alpha_2} = {phi_RH}")

    st.write("Окончательный коэффициент ползучести φ0 (B.1):")
    st.latex(fr"\varphi_0 = \varphi_{{RH}}\cdot \beta(f_{{cm}})\cdot \beta(t_0) = {phi_RH}\cdot {betta_fcm}\cdot {betta_t0} = {phi_0}")
