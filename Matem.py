import streamlit as st
import pandas as pd
import random

# Sahifa sozlamalari
st.set_page_config(
    page_title="Matematika Trenajori",
    page_icon="📐",
    layout="centered"
)

# Oq, yashil va sariq ranglar uyg'unligidagi CSS dizayn
st.markdown("""
    <style>
        /* Asosiy fon */
        .stApp {
            background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 50%, #fefce8 100%);
            color: #1e293b;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Yuqori sarlavha paneli */
        .header-card {
            background-color: #ffffff;
            border-left: 6px solid #15803d;
            border-top: 1px solid #dcfce7;
            border-right: 1px solid #dcfce7;
            border-bottom: 1px solid #dcfce7;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(21, 128, 61, 0.08);
            margin-bottom: 25px;
            text-align: center;
        }
        .header-title {
            color: #15803d;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .author-badge {
            background-color: #fef08a;
            color: #854d0e;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            display: inline-block;
            border: 1px solid #fde047;
        }

        /* Misol ko'rsatiladigan panel */
        .math-box {
            background-color: #fef9c3;
            border: 2px dashed #ca8a04;
            border-radius: 15px;
            padding: 24px;
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            color: #713f12;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }

        /* Tugmalar dizayni */
        div.stButton > button:first-child {
            background-color: #15803d !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 24px !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:first-child:hover {
            background-color: #166534 !important;
            transform: scale(1.02);
        }

        /* Jadvallar chegarasini aniq qilib ko'rsatish */
        table {
            border: 2px solid #334155 !important;
            width: 100% !important;
        }
        th {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
            border: 1.5px solid #334155 !important;
            text-align: center !important;
            padding: 10px !important;
        }
        td {
            border: 1.5px solid #64748b !important;
            text-align: center !important;
            padding: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sarlavha qismi
st.markdown("""
    <div class="header-card">
        <div class="header-title">Matematika: Ko'paytirish va Bo'lish Trenajori</div>
        <div class="author-badge">Tuzuvchi: Quljanova Shukurjon Zaribovna</div>
    </div>
""", unsafe_allow_html=True)

def generate_questions(op_choice):
    q_list = []
    for _ in range(15):
        if op_choice == "Ko'paytirish (×)":
            is_mult = True
        elif op_choice == "Bo'lish (÷)":
            is_mult = False
        else:
            is_mult = random.choice([True, False])

        if is_mult:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            q_list.append({
                "problem": f"{a} × {b}",
                "correct": a * b
            })
        else:
            b = random.randint(2, 9)
            ans = random.randint(2, 9)
            a = b * ans
            q_list.append({
                "problem": f"{a} ÷ {b}",
                "correct": ans
            })
    return q_list

# Dastur holatini saqlash (Session State)
if "started" not in st.session_state:
    st.session_state.started = False
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "finished" not in st.session_state:
    st.session_state.finished = False

# 1-BOSQICH: O'quvchi ma'lumotlarini kiritish
if not st.session_state.started and not st.session_state.finished:
    with st.container():
        st.subheader("O'quvchi ma'lumotlari")
        student_name = st.text_input("O'quvchining ismi va familiyasi:", placeholder="Masalan: Azizbek Karimov")
        op_type = st.selectbox(
            "Amal turini tanlang:",
            ["Aralash (× va ÷)", "Ko'paytirish (×)", "Bo'lish (÷)"]
        )

        if st.button("Mashqni boshlash"):
            if student_name.strip():
                st.session_state.student_name = student_name.strip()
                st.session_state.questions = generate_questions(op_type)
                st.session_state.current_index = 0
                st.session_state.answers = []
                st.session_state.started = True
                st.rerun()
            else:
                st.warning("Iltimos, ism va familiyangizni kiriting!")

# 2-BOSQICH: 15 ta misolni navbatma-navbat ishlash
elif st.session_state.started and not st.session_state.finished:
    idx = st.session_state.current_index
    total = len(st.session_state.questions)
    curr_q = st.session_state.questions[idx]

    # Holat satri
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"👤 **O'quvchi:** {st.session_state.student_name}")
    with col2:
        st.write(f"📊 **Misol:** {idx + 1} / {total}")

    st.progress((idx) / total)

    # Misol oynasi
    st.markdown(f"""
        <div class="math-box">
            {curr_q['problem']} = ?
        </div>
    """, unsafe_allow_html=True)

    with st.form(key=f"q_form_{idx}", clear_on_submit=True):
        user_ans = st.number_input(
            "Javobingizni kiriting:", 
            step=1, 
            value=None, 
            placeholder="Son kiriting...", 
            format="%d"
        )
        submit_btn = st.form_submit_button("Keyingisi ➔")

        if submit_btn:
            if user_ans is not None:
                st.session_state.answers.append({
                    "№": idx + 1,
                    "Misol": curr_q["problem"],
                    "O'quvchi javobi": int(user_ans),
                    "To'g'ri javob": curr_q["correct"],
                    "Natija": "To'g'ri ✅" if int(user_ans) == curr_q["correct"] else "Xato ❌"
                })

                if idx + 1 < total:
                    st.session_state.current_index += 1
                else:
                    st.session_state.started = False
                    st.session_state.finished = True
                st.rerun()
            else:
                st.warning("Iltimos, avval javobni yozing!")

# 3-BOSQICH: 15 misoldan so'ng javoblar jadvali
elif st.session_state.finished:
    st.success("Tabriklaymiz! Barcha 15 ta misol yechildi.")
    st.write(f"👤 **O'quvchi:** {st.session_state.student_name}")

    df = pd.DataFrame(st.session_state.answers)
    correct_count = sum(1 for a in st.session_state.answers if "To'g'ri" in a["Natija"])
    accuracy = round((correct_count / 15) * 100, 1)

    # Xulosa kartalari
    c1, c2, c3 = st.columns(3)
    c1.metric("Jami misollar", "15")
    c2.metric("To'g'ri javoblar", f"{correct_count} ta")
    c3.metric("Aniqlik", f"{accuracy}%")

    st.write("---")
    st.subheader("📋 Batafsil natijalar jadvali")

    # Aniq chizilgan HTML jadval
    html_table = df.to_html(index=False, classes="custom-table", justify="center")
    st.markdown(html_table, unsafe_allow_html=True)

    st.write("")
    if st.button("Qaytadan boshlash 🔄"):
        st.session_state.finished = False
        st.session_state.started = False
        st.rerun()
