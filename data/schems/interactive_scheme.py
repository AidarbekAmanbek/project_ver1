import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.widgets import TextBox, Button


def horizontal_dimension(ax, x1, x2, y, text, extension_y):
    """Горизонтальная размерная линия."""
    ax.annotate(
        "",
        xy=(x2, y),
        xytext=(x1, y),
        arrowprops={"arrowstyle": "<->", "lw": 1.2, "color": "black"},
    )
    ax.plot([x1, x1], [extension_y, y], color="0.5", lw=0.8)
    ax.plot([x2, x2], [extension_y, y], color="0.5", lw=0.8)
    ax.text((x1 + x2) / 2, y + 0.08, text, ha="center", va="bottom")


def vertical_dimension(ax, x, y1, y2, text, extension_x):
    """Вертикальная размерная линия."""
    ax.annotate(
        "",
        xy=(x, y2),
        xytext=(x, y1),
        arrowprops={"arrowstyle": "<->", "lw": 1.2, "color": "black"},
    )
    ax.plot([extension_x, x], [y1, y1], color="0.5", lw=0.8)
    ax.plot([extension_x, x], [y2, y2], color="0.5", lw=0.8)
    ax.text(x + 0.12, (y1 + y2) / 2, text, ha="left", va="center")


def draw_scheme(ax, d, h, c):
    """
    d — расстояние от площадки до верхней линии;
    h — полная высота от верхней линии до низа стенок;
    c — ширина проёма между стенками.
    """
    if d <= 0 or h <= 0 or c <= 0:
        raise ValueError("Все размеры должны быть больше нуля.")
    if h <= d:
        raise ValueError("Для этой схемы требуется h > d.")

    ax.clear()

    theta = np.degrees(np.arctan2(d, 2 * d))

    x_left = -c / 2
    x_right = c / 2
    y_platform = 0.0
    y_top = d
    y_bottom = d - h

    x_left_top = x_left - 2 * d
    x_right_top = x_right + 2 * d
    x_min = x_left_top - 1.2 * d
    x_max = x_right_top + 1.2 * d
    slab_thickness = 0.10 * d

    # Верхнее перекрытие.
    ax.plot([x_min, x_max], [y_top, y_top], color="black", lw=2.2)
    ax.plot(
        [x_min, x_max],
        [y_top + slab_thickness, y_top + slab_thickness],
        color="0.25",
        lw=1.2,
    )

    # Условные крепления.
    dots = np.linspace(x_min + 0.4 * d, x_max - 0.4 * d, 8)
    ax.scatter(
        dots,
        np.full_like(dots, y_top - 0.10 * d),
        s=14,
        color="black",
        zorder=4,
    )

    # Площадки и вертикальные стенки.
    ax.plot([x_min, x_left], [0, 0], color="black", lw=1.8)
    ax.plot([x_right, x_max], [0, 0], color="black", lw=1.8)
    ax.plot([x_left, x_left], [0, y_bottom], color="black", lw=1.8)
    ax.plot([x_right, x_right], [0, y_bottom], color="black", lw=1.8)

    # Наклонные линии.
    ax.plot([x_left_top, x_left], [y_top, 0], color="0.35", lw=1.8)
    ax.plot([x_right, x_right_top], [0, y_top], color="0.35", lw=1.8)

    # Вспомогательные линии.
    ax.plot(
        [x_left_top, x_left_top],
        [0, y_top + slab_thickness],
        "--",
        color="0.65",
        lw=0.8,
    )
    ax.plot(
        [0, 0],
        [y_bottom - 0.5 * d, y_top + slab_thickness],
        "--",
        color="0.75",
        lw=0.8,
    )

    # Углы theta.
    radius = 0.60 * d
    ax.add_patch(
        Arc(
            (x_left, 0),
            2 * radius,
            2 * radius,
            theta1=180 - theta,
            theta2=180,
            lw=1.1,
        )
    )
    ax.add_patch(
        Arc(
            (x_right, 0),
            2 * radius,
            2 * radius,
            theta1=0,
            theta2=theta,
            lw=1.1,
        )
    )

    ax.text(
        x_left - 0.52 * d,
        0.28 * d,
        rf"$\theta={theta:.1f}^\circ$",
        ha="right",
        va="center",
    )
    ax.text(
        x_right + 0.52 * d,
        0.28 * d,
        rf"$\theta={theta:.1f}^\circ$",
        ha="left",
        va="center",
    )

    # Размерные линии.
    horizontal_dimension(
        ax,
        x_left_top,
        x_left,
        -0.58 * d,
        r"$2d$",
        extension_y=0,
    )
    horizontal_dimension(
        ax,
        x_left,
        x_right,
        y_bottom - 0.45 * d,
        r"$c$",
        extension_y=y_bottom,
    )
    vertical_dimension(
        ax,
        x_max + 0.60 * d,
        0,
        y_top,
        r"$d$",
        extension_x=x_max,
    )
    vertical_dimension(
        ax,
        x_max + 1.35 * d,
        y_bottom,
        y_top,
        r"$h$",
        extension_x=x_max,
    )

    # Выноска A.
    target = ((x_right + x_right_top) / 2, y_top / 2)
    ax.annotate(
        "A",
        xy=target,
        xytext=(target[0] + 0.70 * d, target[1] - 0.90 * d),
        bbox={"boxstyle": "square,pad=0.25", "fc": "white", "ec": "0.4"},
        arrowprops={"arrowstyle": "->", "lw": 1.0, "color": "0.35"},
        ha="center",
        va="center",
    )

    ax.text(
        x_min,
        y_bottom - 0.95 * d,
        rf"$\theta=\arctan(d/(2d))=\arctan(1/2)={theta:.1f}^\circ$",
        ha="left",
        va="top",
    )

    ax.set_xlim(x_min - 0.35 * d, x_max + 1.8 * d)
    ax.set_ylim(y_bottom - 1.25 * d, y_top + 0.55 * d)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title(
        f"Параметрическая схема: d={d:g}, h={h:g}, c={c:g}",
        pad=12,
    )


def parse_number(text):
    """Поддерживает и точку, и запятую как десятичный разделитель."""
    return float(text.strip().replace(",", "."))


fig, ax = plt.subplots(figsize=(11, 6))
fig.subplots_adjust(bottom=0.22)

draw_scheme(ax, d=1.0, h=3.0, c=1.2)

# Поля ввода.
box_d = TextBox(
    plt.axes([0.10, 0.075, 0.13, 0.055]),
    "d = ",
    initial="1.0",
)
box_h = TextBox(
    plt.axes([0.33, 0.075, 0.13, 0.055]),
    "h = ",
    initial="3.0",
)
box_c = TextBox(
    plt.axes([0.56, 0.075, 0.13, 0.055]),
    "c = ",
    initial="1.2",
)

button = Button(
    plt.axes([0.76, 0.068, 0.15, 0.065]),
    "Обновить",
)

status = fig.text(
    0.10,
    0.025,
    "",
    ha="left",
    va="center",
)


def update(_=None):
    try:
        d = parse_number(box_d.text)
        h = parse_number(box_h.text)
        c = parse_number(box_c.text)
        draw_scheme(ax, d=d, h=h, c=c)
        status.set_text("")
    except ValueError as error:
        status.set_text(f"Ошибка: {error}")

    fig.canvas.draw_idle()


# Обновление по кнопке или по Enter в любом поле.
button.on_clicked(update)
box_d.on_submit(update)
box_h.on_submit(update)
box_c.on_submit(update)

plt.show()
