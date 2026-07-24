from math import exp

from calculations.calc_units import interpolate, interpolate_table
from data.creep_shrinkage import SHRINKAGE_CD0_TABLE, KH_TABLE


def calc_kh(h0, digits=3):
    return interpolate_table(h0, KH_TABLE, digits)


def calc_epsilon_cd0(fck, rh, digits=3):
    fck_keys = sorted(SHRINKAGE_CD0_TABLE)

    if fck <= fck_keys[0]:
        return interpolate_table(rh, SHRINKAGE_CD0_TABLE[fck_keys[0]], digits)
    if fck >= fck_keys[-1]:
        return interpolate_table(rh, SHRINKAGE_CD0_TABLE[fck_keys[-1]], digits)

    for f1, f2 in zip(fck_keys, fck_keys[1:]):
        if f1 <= fck <= f2:
            break

    eps_f1 = interpolate_table(rh, SHRINKAGE_CD0_TABLE[f1], digits)
    eps_f2 = interpolate_table(rh, SHRINKAGE_CD0_TABLE[f2], digits)
    return interpolate(fck, f1, eps_f1, f2, eps_f2, digits)


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
# epsilon_cd0 берётся в промилле (как в таблице 3.2), внутри переводится в абсолютные единицы
def calc_drying_shrinkage(t, ts, h0, kh, epsilon_cd0, digits=9):
    betta_ds = (t - ts) / ((t - ts) + 0.04 * (h0 ** 3) ** 0.5)
    epsilon_cd = betta_ds * kh * (epsilon_cd0 * 1e-3)

    return round(betta_ds, 4), round(epsilon_cd, digits)


# окончательная (полная) усадка бетона epsilon_cs по (3.8)
def calc_total_shrinkage(epsilon_cd, epsilon_ca, digits=9):
    epsilon_cs = epsilon_cd + epsilon_ca
    return round(epsilon_cs, digits)


