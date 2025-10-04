import gradio as gr
import sqlite3
import random

# ---------- School Chatbot ----------
def school_bot(user_input):
    conn = sqlite3.connect(":memory:")  # temporary db
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS school_info (
        keyword TEXT, answer TEXT
    )""")
    data = [
        ("admissions", "The admission process requires filling an online form and submitting documents."),
        ("fees", "The monthly fee varies by grade, starting from $50."),
        ("teachers", "Mr. John teaches Class 5 Science."),
        ("exams", "Midterm exams are scheduled in November."),
    ]
    cursor.executemany("INSERT INTO school_info (keyword, answer) VALUES (?, ?)", data)

    # simple keyword match
    cursor.execute("SELECT keyword, answer FROM school_info")
    rows = cursor.fetchall()
    conn.close()

    for keyword, ans in rows:
        if keyword.lower() in user_input.lower():
            return ans
    return "I can only answer school-related queries like admissions, fees, teachers, or exams."

# ---------- Ecommerce Chatbot ----------
def ecom_bot(user_input):
    products = [
        ("Office Chair", "chair", "office", "black", 120),
        ("Gaming Chair", "chair", "home", "red", 150),
        ("Study Table", "table", "home", "brown", 90),
        ("Office Desk", "table", "office", "white", 200),
    ]

    if "varieties" in user_input.lower():
        return "We have chairs and tables available."
    if "home" in user_input.lower():
        return "Some home products are: Gaming Chair, Study Table."
    if "office" in user_input.lower():
        return "Some office products are: Office Chair, Office Desk."
    if "red" in user_input.lower():
        return "I recommend the Red Gaming Chair for $150."
    if "black" in user_input.lower():
        return "I recommend the Black Office Chair for $120."
    return "Please specify color, type, or usage (home/office)."

# ---------- Gradio Interface ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🏫 School & 🛒 E-commerce Chatbots")

    with gr.Tab("School Bot"):
        school_chat = gr.ChatInterface(school_bot)

    with gr.Tab("E-commerce Bot"):
        ecom_chat = gr.ChatInterface(ecom_bot)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))


