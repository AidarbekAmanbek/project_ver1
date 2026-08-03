import math

from data.rebar import REBAR_TABLE

# Средняя полезная высота сечения по (6.32)
def calc_effective_depth(
        thickness,
        cover,
        diametr_x,
        diametr_y,
    ):

    ax = cover + diametr_x/2
    ay = cover + diametr_x + diametr_y/2

    dx = thickness - ax
    dy = thickness - ay

    d_eff = (dx + dy) / 2

    return (
        round(d_eff),
        round(ax),
        round(ay),
        round(dx),
        round(dy),

    )

# коэффициент армирования в обоих направлениях
def calc_reinforcement_ratio(
        diametr_x, 
        diametr_y, 
        spacing_x, 
        spacing_y,
        d_eff,
        digits=3
    ):

    As_x = REBAR_TABLE[diametr_x]["area_mm2"]
    As_y = REBAR_TABLE[diametr_y]["area_mm2"]

    p_lx = As_x / (spacing_x * d_eff)
    p_ly = As_y / (spacing_y * d_eff)
    p_l = min((p_lx * p_ly) ** 0.5, 0.02)

    return (
        round(As_x, digits),
        round(As_y, digits),
        round(p_lx, 5),
        round(p_ly, 5),
        round(p_l, 5),
    )

# максимального напряжения срезающего усилия по (6.33)
def calc_punching_shear_stress(
        widght,
        height,
        betta,
        force,
        d_eff,
        digits=3
    ):

    g = 9.81
    pi = math.pi
    u1 = (2 * widght + 2 * height) + (2 * pi * 2 * d_eff)
    v_Ed = (betta * force * 1000) / (u1 * d_eff)
    v_Ed_ts = (v_Ed * 1000) / g

    return (
        round(v_Ed, digits),
        round(v_Ed_ts, digits),
        round(u1),
        round(pi, digits),
        )


# расчетное значение сопротивления продавливанию по (6.47)
def calc_punching_shear_resistance(d_eff, p_l, f_ck, y_c, digits=3):
    C_Rdc = 0.18 / y_c
    k = min(1 + (200 / d_eff) ** 0.5, 2.0)

    V_Rdc = C_Rdc * k * (100 * p_l * f_ck) ** (1 / 3)
    V_Rdc_min = 0.035 * k ** (3 / 2) * f_ck ** (1 / 2)

    return (
        round(C_Rdc, digits),
        round(k, digits),
        round(V_Rdc, digits),
        round(V_Rdc_min, digits),
        round(max(V_Rdc, V_Rdc_min), digits),
    )