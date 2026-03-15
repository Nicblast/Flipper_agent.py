import streamlit as st

# In-memory storage using Streamlit session state
if "books" not in st.session_state:
    st.session_state.books = []

st.title("📚 Book Tracker")
st.write("Track books, quotes, and study flashcards — one step at a time.")


# -----------------------------
# ADD BOOK
# -----------------------------
def add_book():
    st.subheader("➕ Add a Book")

    title = st.text_input("Enter book title")
    status = st.selectbox("Select status", ["Reading", "Read", "TBR"])

    if st.button("Add Book"):
        st.session_state.books.append({
            "title": title,
            "status": status,
            "quotes": []
        })
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
        st.write(f"**{i+1}. {book['title']}** — *{book['status']}*")


# -----------------------------
# ADD QUOTE
# -----------------------------
def add_quote():
    st.subheader("📝 Add Quote / Flashcard")

    if not st.session_state.books:
        st.warning("Add a book first before adding quotes.")
        return

    book_titles = [book["title"] for book in st.session_state.books]
    selected = st.selectbox("Select a book", book_titles)

    quote = st.text_area("Enter the quote or flashcard text")

    if st.button("Save Quote"):
        index = book_titles.index(selected)
        st.session_state.books[index]["quotes"].append(quote)
        st.success("Quote saved!")


# -----------------------------
# STUDY FLASHCARDS
# -----------------------------
def study_flashcards():
    st.subheader("🎓 Study Flashcards")

    if not st.session_state.books:
        st.info("No books or quotes found.")
        return

    for book in st.session_state.books:
        if not book["quotes"]:
            continue

        st.write(f"### 📘 {book['title']}")

        for quote in book["quotes"]:
            if st.button(f"Show flashcard from {book['title']}: {quote[:20]}..."):
                st.info(quote)


# -----------------------------
# MAIN MENU (Sidebar Navigation)
# -----------------------------
menu = st.sidebar.radio(
    "Menu",
    ["Add Book", "View Books", "Add Quote", "Study Flashcards"]
)

if menu == "Add Book":
    add_book()
elif menu == "View Books":
    view_books()
elif menu == "Add Quote":
    add_quote()
elif menu == "Study Flashcards":
    study_flashcards()
