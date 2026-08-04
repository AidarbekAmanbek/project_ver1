import streamlit as st

st.title("Демо: возможности Streamlit")

# --- текст ---
st.write("st.write — универсальный вывод (текст, число, список, DataFrame)")
st.markdown("**st.markdown** — рендерит *markdown*-разметку")
st.caption("st.caption — мелкий серый текст")
st.latex(r"st.latex \Rightarrow v_{Ed} = \dfrac{\beta V_{Ed}}{u_1 d}")
st.divider()

# --- статус-баннеры ---
st.info("st.info — нейтральная информация")
st.warning("st.warning — предупреждение")
st.success("st.success — всё хорошо")
st.error("st.error — ошибка / не проходит")
st.divider()

# --- колонки ---
col1, col2, col3 = st.columns([1, 0.2, 1])
with col1:
    st.markdown("st.columns — слева")
with col3:
    n_ed = st.number_input("Расчетная нагрузка", min_value=0.0, key="n_ed", label_visibility="collapsed")
st.divider()

# --- метрики ---
v_ed, v_rdc = 0.65, 0.80
margin = v_rdc - v_ed
m1, m2, m3 = st.columns(3)
m1.metric("v_Ed", f"{v_ed} МПа")
m2.metric("V_Rd,c", f"{v_rdc} МПа")
m3.metric("Запас", f"{margin:+.2f} МПа", delta=f"{margin:+.2f} МПа")
st.divider()

# --- container (просто группировка, опционально с рамкой) ---
with st.container(border=True):
    st.write("st.container(border=True) — блок с рамкой, без сворачивания (в отличие от expander)")
    st.write("Можно класть сколько угодно элементов подряд")
st.divider()

# --- help= — значок "?" с подсказкой при наведении (почти у любого виджета) ---
with st.container(border=True):
    st.number_input(
        "Полезная высота d", value=200,
        help="Расстояние от центра тяжести арматуры до сжатой грани сечения.",
    )
    st.metric(
        "v_Ed", "0.65 МПа",
        help="Максимальное напряжение среза по формуле (6.38).",
    )
    st.markdown(
        "ρ_l — коэффициент армирования",
        help="ρ_l = √(ρ_lx · ρ_ly), ограничивается сверху значением 0.02.",
    )
st.divider()

# --- expander / popover ---
with st.expander("st.expander — разворачиваемый блок"):
    st.write("Содержимое внутри expander")

with st.popover("st.popover — всплывающая панель по клику"):
    st.write("Содержимое внутри popover")
    st.latex(r"\rho_l = \sqrt{\rho_{lx}\cdot\rho_{ly}}")
st.divider()

# --- вкладки ---
tab1, tab2 = st.tabs(["Расчёт", "Справка"])
with tab1:
    st.write("st.tabs — содержимое первой вкладки")
with tab2:
    st.write("st.tabs — содержимое второй вкладки")
st.divider()

# --- session_state (сохраняется между перезапусками скрипта) ---
if "clicks" not in st.session_state:
    st.session_state.clicks = 0
if st.button("st.session_state — нажми меня"):
    st.session_state.clicks += 1
st.write(f"Нажатий: {st.session_state.clicks}")
st.divider()

# --- форма (не перезапускает скрипт на каждое поле, только по кнопке) ---
with st.form("demo_form"):
    st.number_input("Поле внутри st.form", key="form_val")
    submitted = st.form_submit_button("Отправить форму")
if submitted:
    st.write("Форма отправлена")
st.divider()

# --- таблица и скачивание ---
st.dataframe({"Ø, мм": [12, 14, 16], "As, мм²": [113.1, 153.9, 201.1]})
st.download_button("st.download_button — скачать CSV", data="a,b\n1,2", file_name="demo.csv")
st.divider()

# --- разное ---
if st.button("st.toast — показать уведомление"):
    st.toast("Готово!")

with st.spinner("st.spinner — идёт расчёт..."):
    import time
    time.sleep(1)
