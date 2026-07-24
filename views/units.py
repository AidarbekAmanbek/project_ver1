import streamlit as st
from calculations.calc_units import CATEGORIES, convert

st.title("Преобразование единиц измерений")

category_name = st.segmented_control(
    "Величина", list(CATEGORIES), default=list(CATEGORIES)[0], required=True
)
table = CATEGORIES[category_name]
units = list(table)

from_unit = units[0]

col1, col2 = st.columns(2)
with col1:
    value = st.number_input(f"Значение, {from_unit}", value=1.0)
with col2:
    st.write("")

col1b, col2b = st.columns(2)
with col1b:
    to_unit = st.selectbox(
        "В", units, index=min(1, len(units) - 1), key="to_unit", label_visibility="collapsed"
    )

result = convert(value, from_unit, to_unit, table)

st.subheader("Преобразование во все единицы:")
conversion_results = {}
for unit in units:
    conversion_results[unit] = convert(value, from_unit, unit, table)

# display the conversion table aligned to the left
left, mid, right = st.columns([2, 1, 1])
with left:
    st.table({"Единица": list(conversion_results.keys()), "Значение": list(conversion_results.values())})

with st.expander("Таблица коэффициентов (относительно базовой единицы)"):
    st.table({"Единица": list(table.keys()), "1 ед. = ... базовой": list(table.values())})
