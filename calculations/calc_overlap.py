from data.rebar import REBAR_TABLE
from math import sqrt
import re

def calc_l_bqrd(diameter, sigma_sd, f_bd, digits=2):
    l_brqd = (diameter / 4) * (sigma_sd / f_bd) 
    return round(l_brqd, digits)


def calc_f_ctd(a_ct, f_ctk_005, yc, digits=2):
    f_ctd = (a_ct * f_ctk_005) / yc

    return round(f_ctd, digits)

#--------Расчетное значение предельных напряжений сцепления fbd п.8.4.2(2) --------
def calc_f_bd(f_ctd, bond_condition, diameter, digits=2):
    n1 = 1.0 if bond_condition == "good" else 0.7
    n2 = 1.0 if diameter <= 32 else (132 - diameter) / 100
    f_bd = 2.25 * n1 * n2 * f_ctd

    return round(f_bd, digits), n1, n2


def calc_cd(bars_type, a_min=None, c=None, c1=None, digits=2):
    if bars_type == "straight":
        cd = min(a_min/2, c, c1)
    elif bars_type == "hooked":
        cd = min(a_min/2, c1)
    elif bars_type == "looped":
        cd = c
    return round(cd, digits)


# минимальная длина нахлеста 
def calc_l0_min(alpha_6, diameter, l_brqd, digits=0):
    lb_min = max(0.3*alpha_6*l_brqd, 15*diameter, 200)

    return round(lb_min, digits)

# Значения коэффициентов α1, α2, α3 таблица 8.2 (для сжатых стержней - константы)
def calc_alpha_123_compression():
    alpha_1, alpha_2, alpha_3 = 1.0, 1.0, 1.0
    return alpha_1, alpha_2, alpha_3


# расчетная длина анкеровки lbd по (8.4), с учетом минимальной lb,min по (8.6)/(8.7)
def calc_l0_overlap(alpha_1, alpha_2, alpha_3, alpha_5, alpha_6, l_brqd, l0_min, digits=2):
    l_bd = alpha_1 * alpha_2 * alpha_3 * alpha_5 * alpha_6 * l_brqd
    l_bd = max(l_bd, l0_min)
    return round(l_bd, digits)


# Значения коэффициентов α1, α2 таблица 8.2 для растянутых стержней.
def calc_alph_12_tension(bars_type, diameter, cd, digits=3):
    if bars_type == "straight":
        alpha_1 = 1.0
        alpha_2_raw = 1.0 - 0.15 * (cd - diameter) / diameter
    else:
        alpha_1 = 0.7 if cd > 3 * diameter else 1.0
        alpha_2_raw = 1.0 - 0.15 * (cd - 3 * diameter) / diameter

    alpha_2 = min(max(alpha_2_raw, 0.7), 1.0)

    return (
        round(alpha_1, digits),
        round(alpha_2, digits),
        round(alpha_2_raw, digits),
    )

# Значения коэффициентов α3 таблица 8.2 для растянутых стержней.
def calc_alph_3_tension(factor_k, diameter, A_st, sigma_s, f_yd, digits=3):
    k = factor_k
    As = REBAR_TABLE[diameter]["area_mm2"]
    A_st_min = round(1.0 * As * (sigma_s / f_yd), digits)

    lambda_1 = (A_st - A_st_min)/As 

    alpha_3 = 1 - k * lambda_1
    alpha_3 = min(max(alpha_3, 0.7), 1.0)
    return round(alpha_3, digits)

# Значения коэффициентов α5 таблица 8.2 для растянутых стержней.
def calc_alph_5_tension(p, digits=3):
    if p == 0:
        alpha_5 = 1.0
    else:
        alpha_5 = 1 - 0.04 * p

    alpha_5 = min(max(alpha_5, 0.7), 1.0)
    return round(alpha_5, digits)

# Значения коэффициентов α6 таблица 8.2 для растянутых стержней.
def calc_alph_6(p1, digits=3):
    alpha_6 = round(sqrt(p1 / 25), digits)

    if alpha_6 <= 1.0:
        alpha_6 = 1.0
    elif alpha_6 >= 1.5:
        alpha_6 = 1.5

    return round(alpha_6, digits)


def calc_A_st(rebar_text, digits=3):
    parts = re.split(r"\s*[хx×]\s*", rebar_text.strip())
    if len(parts) != 2:
        raise ValueError("используйте формат 'количество x диаметр', например 4x20")

    try:
        count, diameter = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError("количество и диаметр должны быть целыми числами")

    if count <= 0:
        raise ValueError("количество стержней должно быть больше 0")

    if diameter not in REBAR_TABLE:
        raise ValueError(f"диаметр {diameter} мм отсутствует в таблице арматуры")

    A_st = count * REBAR_TABLE[diameter]["area_mm2"]

    return round(A_st, digits)