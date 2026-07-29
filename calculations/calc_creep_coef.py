from math import exp

from calculations.calc_units import interpolate_table
from data.creep_shrinkage import KH_TABLE, CEMENT_CLASS


def calc_kh(h0, digits=3):
    return interpolate_table(h0, KH_TABLE, digits)


# номинальное значение усадки при высыхании epsilon_cd,0 по (B.11), betta_RH по (B.12)
def calc_epsilon_cd0(fcm, rh, cement_class, digits=9):
    ads1 = CEMENT_CLASS[cement_class]["ads1"]
    ads2 = CEMENT_CLASS[cement_class]["ads2"]
    fcmo = 10

    betta_rh = 1.55 * (1 - (rh / 100) ** 3)
    epsilon_cd0 = 0.85 * ((220 + 110 * ads1) * exp(-ads2 * fcm / fcmo)) * 1e-6 * betta_rh

    return round(epsilon_cd0, digits)


def calc_autogenous_shrinkage(f_ck, t, area, perimetr, digits=9):
    epsilon_sa = (2.5 * (f_ck - 10)) * (10 ** (-6))
    betta_t = 1 - exp(-0.2 * t ** 0.5)

    epsilon_sat = betta_t * epsilon_sa
    h0 = 2 * (area / perimetr)

    return (
        round(epsilon_sa, digits),
        round(betta_t, 4),
        round(epsilon_sat, digits),
        round(h0, 2),
    )


# развитие усадки при высыхании во времени, betta_ds по (3.10), epsilon_cd(t) по (3.9)
def calc_drying_shrinkage(t, ts, h0, kh, epsilon_cd0, digits=9):
    betta_ds = (t - ts) / ((t - ts) + 0.04 * (h0 ** 3) ** 0.5)
    epsilon_cd = betta_ds * kh * epsilon_cd0

    return round(betta_ds, 4), round(epsilon_cd, digits)


# окончательная (полная) усадка бетона epsilon_cs по (3.8)
def calc_total_shrinkage(epsilon_cd, epsilon_ca, digits=9):
    epsilon_cs = epsilon_cd + epsilon_ca
    return round(epsilon_cs, digits)


# Коэффициента ползучести по (В.1)
def calc_creep_coefficient(f_cm, t0, t, RH, area, perimetr, digits=4):
    # α1/2/3 - коэффициенты, учитывающие влияние прочности бетона (B.8c):
    alpha_1 = (35/f_cm) ** 0.7
    alpha_2 = (35/f_cm) ** 0.2
    alpha_3 = (35/f_cm) ** 0.5

    # h0 - условный приведенный размер элемента, мм (B.6)
    h0 = 2 * (area / perimetr)

    # φRH - коэффициент, учитывающий влияние относительной влажности воздуха на коэффициент ползучести (B.2)
    if f_cm <= 35:
        phi_RH = 1 + (1 - (RH / 100)) / (0.1 * h0 ** (1/3))
        betta_H = 1.5 * (1 + (0.012 * RH)**18) * h0 + 250
        if betta_H >= 1500:
            betta_H = 1500
    elif f_cm > 35:
        phi_RH = (1 + (1 - (RH / 100)) / (0.1 * h0 ** (1/3)) * alpha_1) * alpha_2
        betta_H = 1.5 * (1 + (0.012 * RH)**18) * h0 + 250 * alpha_3
        if betta_H >= 1500 * alpha_3:
            betta_H = 1500 * alpha_3
    
    # β(fcm) - коэффициент, учитывающий влияние предела прочности при сжатии бетона на коэффициент ползучести (B.4)
    betta_fcm = 16.8 / (f_cm ** 0.5)

    # β (t0) - коэффициент, учитывающий влияние возраста бетона при начале нагружения на коэффициент ползучести (B.5):
    betta_t0 = 1 / (0.1 + t0 ** 0.20)

 

    # βc(t, t0) - коэффициент, описывающий развитие ползучести после приложения нагрузки (B.7)
    betta_c = ((t- t0) / (betta_H + t- t0)) ** 0.3


    # φ0 - коэффициент ползучести (B.1)
    phi_0 = phi_RH * betta_fcm * betta_t0
    return (
        round(phi_0, digits),
        round(alpha_1, digits),
        round(alpha_2, digits),
        round(h0, digits),
        round(betta_fcm, digits),
        round(betta_t0, digits),
        round(phi_RH, digits),
    )
