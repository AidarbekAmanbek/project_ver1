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


def calc_cd(bars_type, a_min=200, c=25, c1=25, digits=2):
    if bars_type == "straight":
        cd = min(a_min/2, c, c1)
    elif bars_type == "hooked":
        cd = min(a_min/2, c1)
    elif bars_type == "looped":
        cd = c
    return round(cd, digits)


#-------- базовая длины анкеровки lb,rqd п.8.4.3 --------



# минимальная длина анкеровки 
def calc_lb_min(bars, diameter, l_brqd, digits=0):
    if bars == "tension":
        lb_min = max(0.3*l_brqd, 10*diameter, 100)
    elif bars == "compression":
        lb_min = max(0.6*l_brqd, 10*diameter, 100)

    return round(lb_min, digits)

# Значения коэффициентов α1, α2, α3, α4 таблица 8.2 (для сжатых стержней - константы)
def calc_alphas_compression():
    alpha_1, alpha_2, alpha_3, alpha_4 = 1.0, 1.0, 1.0, 0.7
    return alpha_1, alpha_2, alpha_3, alpha_4


# расчетная длина анкеровки lbd по (8.4), с учетом минимальной lb,min по (8.6)/(8.7)
def calc_lbd(alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, l_brqd, lb_min, digits=2):
    l_bd = alpha_1 * alpha_2 * alpha_3 * alpha_4 * alpha_5 * l_brqd
    l_bd = max(l_bd, lb_min)
    return round(l_bd, digits)


# def calc_alphas_tension(bars, bars_type, diameter, cd, A_st, A_stmin, As, type_const, digits=2):

#     if type_const == "beam":
#         A_stmin = 0.25 * As

#     lamda = 1.0
#     k = 0.0

#     if bars == "tension":
#         if bars_type == "straight":
#             alpha_1 = 1.0
#             alpha_2 = 1.0 - 0.15 * (cd - diameter) / diameter
#             if alpha_2 < 0.7:
#                 alpha_2 = 0.7
#             elif alpha_2 > 1.0:
#                 alpha_2 = 1.0
#             alpha_3 = 1.0 - k * lamda
#         else:
#             alpha_1 = 0.7 if cd > 3 * diameter else 1.0
#             alpha_2 = 1.0
#             alpha_3 = 1.0

#         alpha_4 = 0.7
#         alpha_5 = 1.0

#     elif bars == "compression":
#         alpha_1, alpha_2, alpha_3, alpha_4, alpha_5 = 1.0, 1.0, 1.0, 0.7, 1.0
#     else:
#         raise ValueError("bars must be 'tension' or 'compression'")

#     return (
#         round(alpha_1, digits),
#         round(alpha_2, digits),
#         round(alpha_3, digits),
#         round(alpha_4, digits),
#         round(alpha_5, digits),
#     )