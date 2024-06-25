import math
import streamlit as st


def show_sidebar():
    with st.sidebar:
        if not st.session_state['main']:
            st.button("На главный экран", on_click=change_version, kwargs={"obj": 'main.txt'})
        st.write('Какой то текст')


def calculate_doza():
    if 'V1' in st.session_state:
        dose_ng = int(st.session_state['V1']) * 0.25
        dose_ml = round((int(st.session_state['V1']) * 0.25) / 50, 2)
        st.session_state["calculate_dose"] = f"{dose_ml} ml"
        st.success(f"Доза кетамина: 5% - {dose_ml} ml, {dose_ng} mg")
    else:
        st.error(f"Заполните все формы")


def calculate_ketamin():
    show_sidebar()
    st.title("Рассчет дозы кетамина")
    with st.form("CALCULATE_DOSE"):
        st.info("Рассчитать дозировку кетамина")
        number1 = st.number_input(placeholder="Введите вес пациента", label='Вес пациента', key="V1", step=1)
        st.form_submit_button('Рассчитать дозу', on_click=calculate_doza)


def calculate_osh():
    if 'R1' in st.session_state and "R2" in st.session_state:
        dicti1 = {"R1": {"больше 15 усл.ед.": 0, "меньше или равно 15 усл.ед.": 1},
                  "R2": {"меньше 5 баллов ЦРШ": 0, "больше или равно 5 баллов ЦРШ": 1}}
        osh = math.exp(-3.96 + 1.97 * dicti1['R1'][st.session_state["R1"]] + 1.81 * dicti1['R2'][st.session_state["R2"]])
        st.session_state["calculate_num"] = osh
        p = osh/(1 + osh)
        if p > 0.44:
            st.session_state['flag'] = True
            st.error(f'''У пациентки имеется риск возникновения высокоинтенсивной боли, рекомендовано интраоперационное введение кетамина в дозе 0,25 мг/кг
            однократно болюсно сразу после извлечения плода.''')
        else:
            st.success(f"У вашей пациентки низкая вероятность появления высокоинтенсивной послеоперационной боли")
    else:
        st.info(f"Заполните все формы")

    if st.session_state['flag']:
        st.button("Рассчитать дозу", on_click=change_version, kwargs={"obj": "ketamin"})


def calculate_osh_main():
    show_sidebar()
    if "flag" not in st.session_state:
        st.session_state['flag'] = None

    if not st.session_state['flag']:
        with st.form("CALCULATE"):
            st.info("Рассчитать вероятность высокоинтенсивной послеоперационной боли")
            radio1 = ["больше 15 усл.ед.", "меньше или равно 15 усл.ед."]
            radio2 = ["меньше 5 баллов ЦРШ", "больше или равно 5 баллов ЦРШ"]
            number1 = st.radio(label="Терпимость боли при давлении", options=radio1, index=1, key="R1")
            number2 = st.radio(label="Интенсивность боли при выполнении инъекции лидокаина", options=radio2, index=1,
                               key="R2")
            st.form_submit_button('Рассчитать', on_click=calculate_osh)


def change_version(obj):
    lst = ["main", "veroyatnost", "ketamin"]
    for item in lst:
        if item == obj:
            st.session_state[item] = True
        else:
            st.session_state[item] = False


def main_page():
    show_sidebar()
    st.title("🩺 Главная страница")
    with open('texts/main.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    st.write(f'🚑🚑🚑 {text} ⬇️⬇️⬇️')
    expand = st.expander("1️⃣ Оценке порога боли при давлении (подробнее)")
    with open("texts/file1.txt", mode='r', encoding="utf-8") as file:
        txt1 = file.read()
    expand.write(txt1)
    expand = st.expander("2️⃣ Оценке интенсивности боли при выполнении инфильтрационной анестезии лидокаином (подробнее)")
    with open("texts/file2.txt", mode='r', encoding="utf-8") as file:
        txt2 = file.read()
    expand.write(txt2)
    st.write("Выполните тестирование порога боли и рассчитайте риск высокоинтенсивной послеоперационной боли.")
    st.button("❓ Рассчитать", on_click=change_version, kwargs={"obj": "veroyatnost"})


def settings():
    if 'main' not in st.session_state:
        st.session_state['main'] = True
    if 'veroyatnost' not in st.session_state:
        st.session_state['veroyatnost'] = False
    if 'ketamin' not in st.session_state:
        st.session_state['ketamin'] = False


def router():
    if st.session_state['main']:
        main_page()
    if st.session_state['veroyatnost']:
        calculate_osh_main()
    if st.session_state['ketamin']:
        calculate_ketamin()


if __name__ == '__main__':
    settings()
    router()
