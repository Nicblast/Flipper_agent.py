import streamlit as st

# In-memory storage using Streamlit session state
if "books" not in st.session_state:
    st.session_state.books = []

st.title("📚 Book Tracker with Flashcards")
st.write("Create books, add flashcards with front/back, and study them interactively.")


# -----------------------------
# ADD BOOK (now with cover image)
# -----------------------------
def add_book():
    st.subheader("➕ Add a Book")

    title = st.text_input("Enter book title")
    status = st.selectbox("Select status", ["Reading", "Read", "TBR"])

    cover_url = st.text_input(
        "Optional: Paste a book cover image URL (from Amazon, Goodreads, Google Books, etc.)"
    )

    if st.button("Add Book"):
        st.session_state.books.append({
            "title": title,
            "status": status,
            "cover": cover_url,      # <-- NEW FIELD
            "flashcards": []
        })
        st.success("Book added successfully!")


# -----------------------------
# VIEW BOOKS (now shows covers)
# -----------------------------
def view_books():
    st.subheader("📖 Your Books")

    if not st.session_state.books:
        st.info("No books added yet.")
        return

    for i, book in enumerate(st.session_state.books):
        st.write(f"### {i+1}. {book['title']} — *{book['status']}*")

        # Show cover image if available
        if book.get("cover"):
            st.image(book["cover"], width=150)


# -----------------------------
# ADD FLASHCARD (FRONT + BACK)
# -----------------------------
def add_flashcard():
    st.subheader("📝 Add Flashcard")

    if not st.session_state.books:
        st.warning("Add a book first before adding flashcards.")
        return

    book_titles = [book["title"] for book in st.session_state.books]
    selected = st.selectbox("Select a book", book_titles)

    front = st.text_input("Flashcard FRONT (question, keyword, prompt)")
    back = st.text_area("Flashcard BACK (answer, explanation, quote)")

    if st.button("Save Flashcard"):
        index = book_titles.index(selected)
        st.session_state.books[index]["flashcards"].append({
            "front": front,
            "back": back
        })
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
# MAIN MENU (Sidebar Navigation)
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
