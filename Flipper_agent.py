import streamlit as st
import json
import os

# -----------------------------
# LOAD & SAVE FUNCTIONS
# -----------------------------
DATA_FILE = "books.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.books, f)


# -----------------------------
# INITIALIZE SESSION STATE
# -----------------------------
if "books" not in st.session_state:
    st.session_state.books = load_data()


st.title("📚 Book Tracker with Flashcards & Covers")
st.write("Your books and flashcards will now stay saved.")


# -----------------------------
# ADD BOOK (with file upload)
# -----------------------------
def add_book():
    st.subheader("➕ Add a Book")

    title = st.text_input("Enter book title")
    status = st.selectbox("Select status", ["Reading", "Read", "TBR"])

    cover_file = st.file_uploader(
        "Upload a book cover image (JPG or PNG)", 
        type=["jpg", "jpeg", "png"]
    )

    if st.button("Add Book"):
        cover_data = cover_file.read() if cover_file else None

        st.session_state.books.append({
            "title": title,
            "status": status,
            "cover": cover_data,
            "flashcards": []
        })

        save_data()
        st.success("Book added successfully!")


# -----------------------------
# VIEW BOOKS
# -----------------------------
def view_books():
    st.subheader("📖 Your Books")

    if not st.session_state.books:
        st.info("No books added yet.")
        return

    for i, book in enumerate(st.session_state.books):
        st.write(f"### {i+1}. {book['title']} — *{book['status']}*")

        if book.get("cover"):
            st.image(book["cover"], width=150)


# -----------------------------
# ADD FLASHCARD
# -----------------------------
def add_flashcard():
    st.subheader("📝 Add Flashcard")

    if not st.session_state.books:
        st.warning("Add a book first before adding flashcards.")
        return

    book_titles = [book["title"] for book in st.session_state.books]
    selected = st.selectbox("Select a book", book_titles)

    front = st.text_input("Flashcard FRONT")
    back = st.text_area("Flashcard BACK")

    if st.button("Save Flashcard"):
        index = book_titles.index(selected)
        st.session_state.books[index]["flashcards"].append({
            "front": front,
            "back": back
        })

        save_data()
        st.success("Flashcard saved!")


# -----------------------------
# STUDY FLASHCARDS
# -----------------------------
def study_flashcards():
    st.subheader("🎓 Study Flashcards")

    if not st.session_state.books:
        st.info("No books or flashcards found.")
        return

    for book in st.session_state.books:
        if not book["flashcards"]:
            continue

        st.write(f"### 📘 {book['title']}")

        for i, card in enumerate(book["flashcards"]):
            with st.expander(f"Flashcard {i+1}: {card['front']}"):
                st.write("**Answer:**")
                st.info(card["back"])


# -----------------------------
# MAIN MENU
# -----------------------------
menu = st.sidebar.radio(
    "Menu",
    ["Add Book", "View Books", "Add Flashcard", "Study Flashcards"]
)

if menu == "Add Book":
    add_book()
elif menu == "View Books":
    view_books()
elif menu == "Add Flashcard":
    add_flashcard()
elif menu == "Study Flashcards":
    study_flashcards()
