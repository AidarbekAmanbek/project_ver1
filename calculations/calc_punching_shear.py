import math
from math import pi, sin

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D

from data.rebar import REBAR_TABLE



def input_row(description, value, **kwargs):
    desc_col, select_col = st.columns([1, 1], vertical_alignment="center")
    with desc_col:
        st.markdown(description)
    with select_col:
        kwargs.setdefault("min_value", type(value)(0))
        return st.number_input(description, value=value, label_visibility="collapsed", **kwargs)


def select_row(description, options, **kwargs):
    desc_col, select_col = st.columns([1, 1], vertical_alignment="center")
    with desc_col:
        st.markdown(description)
    with select_col:
        return st.selectbox(description, options, label_visibility="collapsed", **kwargs)


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
        c1,
        c2,
        d_eff,
        digits=3
    ):

    As_x = REBAR_TABLE[diametr_x]["area_mm2"]
    As_y = REBAR_TABLE[diametr_y]["area_mm2"]

    b_x = c1 + 6 * d_eff
    b_y = c2 + 6 * d_eff

    rebar_x = b_x // spacing_x
    rebar_y = b_y // spacing_y

    p_lx = rebar_x * As_x / (b_x * d_eff)
    p_ly = rebar_y * As_y / (b_y * d_eff)

    p_l = min((p_lx * p_ly) ** 0.5, 0.02)

    return (
        round(As_x, digits),
        round(As_y, digits),
        round(b_x),
        round(b_y),
        round(rebar_x),
        round(rebar_y),
        round(p_lx, 5),
        round(p_ly, 5),
        round(p_l, 5),
    )


# контрольный периметр u1 и расчетное значение
def calc_control_perimeter_u1(c, d_eff, column_type, digits=3):
    if column_type == "rectangular":
        u1 = 2 * c[0] + 2 * c[1] + 2 * pi * 2 * d_eff
    elif column_type == "circular":
        u1 = 2 * pi * (c / 2 + 2 * d_eff)

    return (round(u1, digits), round(pi, digits),)

# максимального напряжения срезающего усилия по (6.33)
def calc_punching_shear_stress(u1, betta, force, d_eff, digits=3):
    v_Ed = (betta * force * 1000) / (u1 * d_eff)

    return round(v_Ed, digits)


# расчетное значение сопротивления продавливанию по (6.47)
def calc_punching_shear_resistance(d_eff, p_l, f_ck, y_c, c_rdc_coef, k1, sigma_cp=0, digits=3):
    C_Rdc = (c_rdc_coef / 100) / y_c
    k = 1 + (200 / d_eff) ** 0.5
    if k > 2.0:
        k_fact = 2.0
    else:
        k_fact = k

    V_Rdc = C_Rdc * k_fact * (100 * p_l * f_ck) ** (1 / 3) + k1 * sigma_cp
    V_Rdc_min = 0.035 * k_fact ** (3 / 2) * f_ck ** (1 / 2) + k1 * sigma_cp

    return (
        round(C_Rdc, digits),
        round(k, digits),
        round(V_Rdc, digits),
        round(V_Rdc_min, digits),
        round(max(V_Rdc, V_Rdc_min), digits),
    )


# площадь внутри контрольного периметра u1 (прямоугольник со скруглёнными углами радиусом 2d)
def calc_area_within_u1(c1, c2, d_eff, digits=3):
    t = 2 * d_eff
    area = c1 * c2 + 2 * t * (c1 + c2) + math.pi * t ** 2

    return round(area, digits)


# снижение продавливающего усилия за счёт реактивного давления грунта по 6.4.4(2)
def calc_delta_v_ed(area_u1, soil_pressure, digits=3):
    delta_v_ed = soil_pressure * (area_u1 / 1e6)

    return round(delta_v_ed, digits)



def capture_punchin_shear_column_circle(c, d_eff):
    fig, ax = plt.subplots(figsize=(3, 3))

    radius_c = c / 2
    radius_u1 = radius_c + 2 * d_eff

    column = plt.Circle(
        (0, 0),
        radius=radius_c,
        facecolor="lightgray",
        edgecolor="black",
        linewidth=1
    )

    u1 = plt.Circle(
        (0, 0),
        radius=radius_u1,
        fill=False,
        edgecolor="black",
        linewidth=0.5,
        linestyle="--"
    )

    ax.add_patch(column)
    ax.add_patch(u1)

    margin = 0.3 * radius_u1

    # размерная линия диаметра колонны c (снизу)
    dim_y = -(radius_u1 + margin * 0.6)
    ax.plot([-radius_c, -radius_c], [0, dim_y], color="gray", linewidth=0.5)
    ax.plot([radius_c, radius_c], [0, dim_y], color="gray", linewidth=0.5)
    ax.annotate(
        "", xy=(radius_c, dim_y), xytext=(-radius_c, dim_y),
        arrowprops=dict(arrowstyle="<->", color="black", linewidth=0.8),
    )
    ax.text(0, dim_y, "c", ha="center", va="top", fontsize=9)

    # размерная линия 2d (от края колонны до края u1, справа по горизонтали)
    ax.annotate(
        "", xy=(radius_u1, 0), xytext=(radius_c, 0),
        arrowprops=dict(arrowstyle="<->", color="black", linewidth=0.8),
    )
    ax.text(
        (radius_c + radius_u1) / 2, 0,
        "2d", ha="center", va="bottom", fontsize=9,
    )

    # обозначение периметра u1 (выноска от окружности под 45°)
    angle = math.radians(45)
    u1_point = (radius_u1 * math.cos(angle), radius_u1 * math.sin(angle))
    u1_label = (u1_point[0] + 0.2 * radius_u1, u1_point[1] + 0.2 * radius_u1)
    ax.annotate(
        "$u_1$",
        xy=u1_point,
        xytext=u1_label,
        fontsize=9,
        ha="left",
        va="bottom",
        arrowprops=dict(arrowstyle="-", color="black", linewidth=0.6),
    )

    ax.set_xlim(-radius_u1 - margin, radius_u1 + margin)
    ax.set_ylim(dim_y - margin, radius_u1 + margin)
    ax.set_aspect("equal")
    ax.axis("off")

    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor="lightgray", edgecolor="black", label="Колонна"),
        Line2D([0], [0], color="black", linestyle="--", linewidth=0.5, label="Контрольный периметр $u_1$"),
        Line2D([0], [0], color="black", linewidth=0.8, label="c — диаметр колонны"),
        Line2D([0], [0], color="black", linewidth=0.8, label="2d — расстояние от грани\nколонны до периметра $u_1$"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=7,
        frameon=False,
    )

    st.pyplot(fig, width=600)

# Сопротивление продавливанию плит или фундаментов колонн, имеющих поперечную арматуру
def calc_punching_shear_resistance_with_rebar(V_Rdc, u1, d_eff, diametr, f_ywd, Sr, alpha, digits=3):
    Asw = REBAR_TABLE[diametr]["area_mm2"]

    f_ywd_ef = 250 + 0.25 * d_eff
    if f_ywd_ef > f_ywd:
        f_ywd_ef = f_ywd

    V_Rdcs = 0.75 * V_Rdc + 1.5 * (d_eff / Sr) * Asw * f_ywd_ef * (1 / (u1 * d_eff)) * sin(math.radians(alpha))
    return (
        round(V_Rdcs, digits),
        round(f_ywd_ef, digits),
        round(Asw, digits),
    )

def control_perimert_uout():
    pass