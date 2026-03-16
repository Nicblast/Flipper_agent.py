import streamlit as st
import json
import base64
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# GOOGLE SHEETS SETUP
# -----------------------------
def get_sheet():
    try:
        creds_json = st.secrets["gcp_service_account"]
        sheet_name = st.secrets["sheet_name"]

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(creds_json),
            ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )

        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        return sheet
    except:
        return None


# -----------------------------
# LOAD FROM GOOGLE SHEETS
# -----------------------------
def load_from_sheets():
    sheet = get_sheet()
    if sheet is None:
        return None

    data = sheet.get_all_records()
    books = []

    for row in data:
        flashcards = json.loads(row["flashcards_json"]) if row["flashcards_json"] else []
        books.append({
            "title": row["title"],
            "status": row["status"],
            "cover_base64": row["cover_base64"],
            "flashcards": flashcards
        })

    return books


# -----------------------------
# SAVE TO GOOGLE SHEETS
# -----------------------------
def save_to_sheets(books):
    sheet = get_sheet()
    if sheet is None:
        return

    rows = []
    for b in books:
        rows.append([
            b["title"],
            b["status"],
            b["cover_base64"] or "",
            json.dumps(b["flashcards"])
        ])

    sheet.clear()
    sheet.append_row(["title", "status", "cover_base64", "flashcards_json"])
    for r in rows:
        sheet.append_row(r)


# -----------------------------
# LOCAL BACKUP
# -----------------------------
LOCAL_FILE = "books_local.json"

def load_local():
    try:
        with open(LOCAL_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_local(books):
    with open(LOCAL_FILE, "w") as f:
        json.dump(books, f)


# -----------------------------
# INITIALIZE DATA
# -----------------------------
books = load_from_sheets()
if books is None:
    books = load_local()

if "books" not in st.session_state:
    st.session_state.books = books


# -----------------------------
# AUTO-SAVE FUNCTION
# -----------------------------
def autosave():
    save_local(st.session_state.books)
    save_to_sheets(st.session_state.books)


# -----------------------------
# UI
# -----------------------------
st.title("Minimalist books app to help you actually remember stuff")



# ADD BOOK
def add_book():
    st.subheader("➕ Add Book")

    title = st.text_input("Book title")
    status = st.selectbox("Status", ["Reading", "Read", "TBR"])
    cover_file = st.file_uploader("Upload cover", type=["jpg", "jpeg", "png"])

    if st.button("Add"):
        cover_b64 = None
        if cover_file:
            cover_b64 = base64.b64encode(cover_file.read()).decode("utf-8")

        st.session_state.books.append({
            "title": title,
            "status": status,
            "cover_base64": cover_b64,
            "flashcards": []
        })

        autosave()
        st.success("Book added")


# VIEW BOOKS
def view_books():
    st.subheader("📖 Your Books")

    for b in st.session_state.books:
        st.write(f"### {b['title']} — *{b['status']}*")

        if b["cover_base64"]:
            img = base64.b64decode(b["cover_base64"])
            st.image(img, width=150)


# ADD FLASHCARD
def add_flashcard():
    st.subheader("📝 Add Flashcard")

    titles = [b["title"] for b in st.session_state.books]
    if not titles:
        st.info("Add a book first")
        return

    selected = st.selectbox("Select book", titles)
    front = st.text_input("Front")
    back = st.text_area("Back")

    if st.button("Save Flashcard"):
        idx = titles.index(selected)
        st.session_state.books[idx]["flashcards"].append({"front": front, "back": back})
        autosave()
        st.success("Flashcard saved")


# STUDY
def study():
    st.subheader("🎓 Study Flashcards")

    for b in st.session_state.books:
        if not b["flashcards"]:
            continue

        st.write(f"### 📘 {b['title']}")
        for i, card in enumerate(b["flashcards"]):
            with st.expander(f"{i+1}. {card['front']}"):
                st.write(card["back"])


# MENU
menu = st.sidebar.radio("Menu", ["Add Book", "View Books", "Add Flashcard", "Study"])

if menu == "Add Book":
    add_book()
elif menu == "View Books":
    view_books()
elif menu == "Add Flashcard":
    add_flashcard()
elif menu == "Study":
    study()
