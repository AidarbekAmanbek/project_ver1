def calculate_f_ctd(a_ct, f_ctk_005, yc, digits=3):
    f_ctd = (a_ct * f_ctk_005) / yc

    return round(f_ctd, digits)


def calculate_f_bd(f_ctd, bond_condition, diameter, digits=3):
    n1 = 1.0 if bond_condition == "good" else 0.7
    n2 = 1.0 if diameter <= 32 else (132 - diameter) / 100
    f_bd = 2.25 * n1 * n2 * f_ctd

    return round(f_bd, digits), n1, n2


def calculate_cd(bars_type, a_min=200, c=25, c1=25, digits=3):
    if bars_type == "straight":
        cd = min(a_min/2, c, c1)
    elif bars_type == "hooked":
        cd = min(a_min/2, c1)
    elif bars_type == "looped":
        cd = c
    return round(cd, digits)


def calculate_base_anchorage_length(diameter, sigma_sd, f_bd, digits=3):
    l_brqd = (diameter / 4) * (sigma_sd / f_bd) 
    return round(l_brqd, digits)

