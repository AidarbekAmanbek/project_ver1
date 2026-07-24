LENGTH_TO_MM = {
    "мм": 1,
    "см": 10,
    "м": 1000,
    "км": 1_000_000,
    "дюйм (in)": 25.4,
    "фут (ft)": 304.8,
}

AREA_TO_MM2 = {
    "мм²": 1,
    "см²": 100,
    "м²": 1_000_000,
    "дюйм² (in²)": 645.16,
}

FORCE_TO_N = {
    "Н": 1,
    "кН": 1_000,
    "кгс (kgf)": 9.80665,
    "тс (tf)": 9_806.65,
    "фунт-сила (lbf)": 4.4482216153,
}

PRESSURE_TO_PA = {
    "Па": 1,
    "кПа": 1_000,
    "МПа": 1_000_000,
    "бар": 100_000,
    "кгс/см²": 98_066.5,
    "кгс/мм²": 9_806_650,
    "psi": 6_894.757293168,
}

MASS_TO_KG = {
    "г": 0.001,
    "кг": 1,
    "т": 1_000,
    "фунт (lb)": 0.45359237,
}

CATEGORIES = {
    "Длина": LENGTH_TO_MM,
    "Площадь": AREA_TO_MM2,
    "Сила": FORCE_TO_N,
    "Напряжение/давление": PRESSURE_TO_PA,
    "Масса": MASS_TO_KG,
}


def convert(value, from_unit, to_unit, table, digits=6):
    base = value * table[from_unit]
    result = base / table[to_unit]
    return round(result, digits)
