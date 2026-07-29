from data.rebar import REBAR_TABLE


def calc_effective_depth(thickness, cover, diametr, spacing, digits=3):
    As = REBAR_TABLE[diametr]["area_cm2"]
    ax = cover + diametr/2
    ay = cover + diametr + diametr/2

    dx = thickness - ax
    dy = thickness - ay

    d_eff = (dx + dy) / 2


    p_txy = (As * 0.001) / (spacing * d_eff) 
    p1 = (p_txy) ** 0.5

    return (
        round(d_eff, digits),
        round(ax, digits),
        round(ay, digits),
        round(dx, digits),
        round(dy, digits),
        round(p_txy, 10000),
        round(p1, 10000),
    )



# def calc_punching_shear_column(height, weight, betta, d, digits=4):

#     C_Rdc = 0.18 / y_c
#     k1 = 0.1
    

#     k = 1 + (200 / d) ** 0.5
#     p_l = (p_ly * p_lz) ** 0.5


#     v_new = betta * ((V_ed) / (ui *d))
#     V_Rdc = C_Rdc * k *(100 * p_l * f_ck) + k1 * sigma_cp

#     return (
#         round(V_Rdc, digits),
#         round(k, digits),
    