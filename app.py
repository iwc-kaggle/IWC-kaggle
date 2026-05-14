import streamlit as st
import pandas as pd
from collections import Counter
from pathlib import Path
import html
import requests


# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="📚 UniLibrary - Book Recommendations",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
    .stApp {
        background-color: #f7f4ef;
    }

    .section-header {
        font-size: 28px;
        font-weight: 700;
        color: #2c1e1a;
        margin: 30px 0 18px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #8c1746;
    }

    .welcome-banner {
        background: linear-gradient(rgba(60,40,30,0.38), rgba(60,40,30,0.38)),
            url("https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        color: white;
        padding: 54px 38px;
        border-radius: 18px;
        margin-bottom: 28px;
    }

    .welcome-banner h1 {
        font-size: 42px;
        margin-bottom: 10px;
    }

    .welcome-banner p {
        font-size: 18px;
        opacity: 0.95;
        max-width: 760px;
    }

    .user-summary {
        background: white;
        color: #2c1e1a;
        padding: 22px;
        border-radius: 14px;
        margin-bottom: 20px;
        border-left: 6px solid #8c1746;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .shelf-card {
        background: white;
        padding: 10px;
        margin-bottom: 12px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .shelf-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 28px rgba(0,0,0,0.16);
        z-index: 10;
        position: relative;
    }

    .book-cover-frame {
        width: 100%;
        height: 220px;
        border-radius: 12px;
        overflow: hidden;
        position: relative;
        margin-bottom: 10px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.14);
        background: #ddd6cc;
    }

    .shelf-card:hover .book-cover-frame {
        box-shadow: 0 10px 24px rgba(0,0,0,0.20);
    }

    .book-cover-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    .fallback-cover {
        width: 100%;
        height: 220px;
        border-radius: 12px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 18px 16px;
        color: #f7e7b4;
        box-sizing: border-box;
        overflow: hidden;
    }

    .fallback-cover.theme-blue {
        background:
            linear-gradient(90deg, #0f235a 0%, #173b7a 16%, #0d2a66 18%, #0f235a 28%, #13316f 100%);
    }

    .fallback-cover.theme-red {
        background:
            linear-gradient(90deg, #7b1e1e 0%, #992626 16%, #6d1717 18%, #7b1e1e 28%, #8d2323 100%);
    }

    .fallback-cover::before {
        content: "";
        position: absolute;
        inset: 10px;
        border: 2px solid rgba(247, 231, 180, 0.72);
        border-radius: 10px;
        pointer-events: none;
    }

    .fallback-cover::after {
        content: "";
        position: absolute;
        top: 12px;
        bottom: 12px;
        left: 22%;
        width: 2px;
        background: rgba(247, 231, 180, 0.35);
        pointer-events: none;
    }

        .fallback-spine-title {
        display: none !important;
        }

    .fallback-front {
        margin-left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        padding: 8px 12px;
    }

    .fallback-title {
        font-size: 15px;
        font-weight: 700;
        line-height: 1.25;
        margin-bottom: 12px;
        max-height: 86px;
        overflow: hidden;
    }

    .fallback-author {
        font-size: 11px;
        line-height: 1.3;
        color: rgba(247, 231, 180, 0.92);
        max-height: 32px;
        overflow: hidden;
    }

    .book-title {
        font-size: 12px;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 3px;
        line-height: 1.3;
        height: 32px;
        overflow: hidden;
    }

    .book-meta {
        font-size: 11px;
        color: #5c5c5c;
        margin-bottom: 3px;
        height: 16px;
        overflow: hidden;
    }

    .book-subject {
        font-size: 10px;
        color: #444;
        background: #efe8df;
        padding: 2px 6px;
        border-radius: 10px;
        display: inline-block;
        margin-bottom: 4px;
    }

    .reason-text {
        font-size: 10px;
        color: #8c1746;
        font-style: italic;
        margin-top: 4px;
        margin-bottom: 6px;
        height: 14px;
        overflow: hidden;
    }

    .shelf-line {
        width: 100%;
        height: 4px;
        background: #e8dece;
        border-radius: 4px;
        margin-top: 6px;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.08);
    }

    .detail-container {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 24px;
    }

    .detail-title {
        font-size: 30px;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 8px;
    }

    .detail-author {
        font-size: 17px;
        color: #5c5c5c;
        margin-bottom: 16px;
    }

    .detail-description {
        font-size: 15px;
        color: #333;
        line-height: 1.7;
        margin-bottom: 20px;
    }

    .detail-meta-label {
        font-size: 12px;
        font-weight: 700;
        color: #8c1746;
        margin-bottom: 2px;
    }

    .detail-meta-value {
        font-size: 14px;
        color: #333;
        margin-bottom: 12px;
    }

    .bookclub-card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        border-left: 5px solid #8c1746;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_recommendations():
    try:
        df = pd.read_csv("recommendations.csv", sep=None, engine="python")
        df.columns = [str(c).strip() for c in df.columns]
        if "user_id,recommendation" in df.columns and len(df.columns) == 1:
            df = pd.read_csv("recommendations.csv", sep=",")
            df.columns = [str(c).strip() for c in df.columns]
        rec_dict = {}
        for _, row in df.iterrows():
            user_id = int(row["user_id"])
            recs = [int(x) for x in str(row["recommendation"]).split()]
            rec_dict[user_id] = recs
        return rec_dict
    except Exception as e:
        st.error(f"Error loading recommendations: {e}")
        return {}

@st.cache_data
def load_books():
    try:
        books = pd.read_csv("items.csv")
    except Exception as e:
        st.error(f"Error loading books: {e}")
        return pd.DataFrame()

    if not books.empty:
        cols = books.columns.tolist()
        col_mapping = {}
        for col in cols:
            col_lower = str(col).lower().strip()
            if col_lower == "i":
                col_mapping[col] = "book_id"
            elif col_lower == "title":
                col_mapping[col] = "title"
            elif col_lower == "author":
                col_mapping[col] = "author"
            elif col_lower == "subjects":
                col_mapping[col] = "subjects"
            elif col_lower == "publisher":
                col_mapping[col] = "publisher"
            elif col_lower == "isbn valid":
                col_mapping[col] = "isbn"
            elif col_lower == "language":
                col_mapping[col] = "language"
            elif col_lower == "api_description":
                col_mapping[col] = "api_description"
            elif col_lower == "api_thumbnail":
                col_mapping[col] = "api_thumbnail"
            elif col_lower == "api_categories":
                col_mapping[col] = "api_categories"
            elif col_lower == "api_published_date":
                col_mapping[col] = "api_published_date"
            elif col_lower == "api_authors":
                col_mapping[col] = "api_authors"
            elif col_lower == "api_publisher":
                col_mapping[col] = "api_publisher"
            elif col_lower == "api_title":
                col_mapping[col] = "api_title"
            elif col_lower == "description_x":
                col_mapping[col] = "description_x"
            elif col_lower == "description_y":
                col_mapping[col] = "description_y"
            elif col_lower == "categories":
                col_mapping[col] = "categories"
            elif col_lower == "metadata":
                col_mapping[col] = "metadata"
            elif col_lower == "isbn_clean":
                col_mapping[col] = "isbn_clean"
            elif col_lower == "first_isbn":
                col_mapping[col] = "first_isbn"

        books = books.rename(columns=col_mapping)

        if "book_id" in books.columns:
            books["book_id"] = pd.to_numeric(books["book_id"], errors="coerce")
            books = books.dropna(subset=["book_id"])
            books["book_id"] = books["book_id"].astype(int)

        for col in ["title", "author", "subjects", "publisher", "isbn", "language",
                    "api_description", "api_thumbnail", "api_categories",
                    "api_published_date", "api_authors", "api_publisher", "api_title",
                    "description_x", "description_y", "categories", "metadata",
                    "isbn_clean", "first_isbn"]:
            if col in books.columns:
                books[col] = books[col].fillna("")

    return books

@st.cache_data
def load_user_history():
    try:
        df = pd.read_csv("interactions_train.csv")
        cols = df.columns.tolist()
        if len(cols) >= 3:
            df.columns = ["user_id", "book_id", "timestamp"] + cols[3:] if len(cols) > 3 else ["user_id", "book_id", "timestamp"]
            df = df[["user_id", "book_id", "timestamp"]]
            df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
            df["book_id"] = pd.to_numeric(df["book_id"], errors="coerce")
            df = df.dropna(subset=["user_id", "book_id"])
            df["user_id"] = df["user_id"].astype(int)
            df["book_id"] = df["book_id"].astype(int)
        return df
    except Exception as e:
        st.error(f"Error loading user history: {e}")
        return pd.DataFrame()

@st.cache_data
def get_popular_books(user_history):
    if user_history.empty:
        return []
    return user_history["book_id"].value_counts().head(20).index.tolist()

@st.cache_data
def is_valid_subject(subject):
    subject = str(subject).strip()
    if len(subject) < 4 or len(subject) > 50:
        return False
    if subject.replace("-", "").replace("(", "").replace(")", "").isdigit():
        return False
    if subject.startswith("--") or subject.startswith('"') or subject.startswith("'"):
        return False
    bad_patterns = ["[", "]", "--", "0000", "119e", "115-117"]
    if any(p in subject for p in bad_patterns):
        return False
    if not any(ch.isalpha() for ch in subject):
        return False
    return True

def get_all_subjects(books_df):
    all_subjects = set()
    if "subjects" in books_df.columns:
        for subj in books_df["subjects"].dropna():
            for s in str(subj).split(";"):
                s = s.strip()
                if is_valid_subject(s):
                    all_subjects.add(s)
    return sorted(all_subjects, key=lambda x: x.lower())

@st.cache_data
def get_all_authors(books_df):
    if "author" in books_df.columns:
        authors = books_df["author"].dropna().unique().tolist()
        return sorted([a for a in authors if len(str(a)) > 2], key=lambda x: str(x).lower())
    return []

@st.cache_data
def get_all_titles(books_df):
    if "title" in books_df.columns:
        titles = books_df["title"].dropna().unique().tolist()
        return sorted([t for t in titles if len(str(t)) > 2], key=lambda x: str(x).lower())
    return []

# ============================================================
# HELPER: Find similar readers (Book Club Feature)
# ============================================================
@st.cache_data
def find_similar_readers(_user_history, current_user_id, min_common=3, top_n=5):
    current_user_books = set(_user_history[_user_history["user_id"] == current_user_id]["book_id"].tolist())
    if not current_user_books:
        return []
    other_users = _user_history[_user_history["user_id"] != current_user_id]
    user_groups = other_users.groupby("user_id")["book_id"].apply(set)
    similar = []
    for other_id, other_books in user_groups.items():
        common = current_user_books & other_books
        if len(common) >= min_common:
            new_books = other_books - current_user_books
            similar.append({
                "user_id": int(other_id),
                "common_count": len(common),
                "common_books": list(common)[:5],
                "new_books": list(new_books)[:6]
            })
    similar.sort(key=lambda x: x["common_count"], reverse=True)
    return similar[:top_n]

# ============================================================
# HELPERS
# ============================================================
@st.cache_data(show_spinner=False)
def is_valid_image_url(url):
    """Check if the image URL actually returns a valid image (Status 200)."""
    if not url:
        return False
    try:
        response = requests.head(url, timeout=1.5, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_book_cover_url(book_row):
    """Get cover URL - prefer api_thumbnail, fallback to Open Library ISBN lookup."""
    if "api_thumbnail" in book_row.index and str(book_row.get("api_thumbnail", "")).startswith("http"):
        url = str(book_row["api_thumbnail"])
        if is_valid_image_url(url):
            return url

    isbn_field = book_row.get("isbn", "")
    if pd.isna(isbn_field) or not isbn_field:
        return None
        
    isbn_str = str(isbn_field).replace(" ", "")
    isbns = [i.strip() for i in isbn_str.split(";")]
    
    for isbn in isbns:
        if (len(isbn) == 13 and isbn.startswith("97")) or len(isbn) == 10:
            test_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
            if is_valid_image_url(test_url):
                return test_url
                
    return None

def get_cover_theme(book_id):
    try:
        return "theme-blue" if int(book_id) % 2 == 0 else "theme-red"
    except Exception:
        return "theme-blue"

def show_cover(book_row, title, author):
    """Display book cover - real if available, elegant fallback otherwise."""
    cover_url = get_book_cover_url(book_row)
    safe_title = html.escape(str(title)) if str(title).strip() else "Library Book"
    safe_author = html.escape(str(author)) if str(author).strip() else "Unknown Author"
    safe_spine = html.escape(str(title)[:28]) if str(title).strip() else "BOOK"
    theme = get_cover_theme(book_row.get("book_id", 0))

    if cover_url:
        # We include both the image AND the hidden fallback. 
        # The 'onerror' script hides the broken image and reveals the fallback if the URL is dead.
        st.markdown(
            f"""
            <div class="book-cover-frame">
                <img src="{cover_url}" alt="{safe_title}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                <div class="fallback-cover {theme}" style="display: none; height: 100%;">
                    <div class="fallback-spine-title">{safe_spine}</div>
                    <div class="fallback-front">
                        <div class="fallback-title">{safe_title}</div>
                        <div class="fallback-author">{safe_author}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="book-cover-frame">
                <div class="fallback-cover {theme}">
                    <div class="fallback-spine-title">{safe_spine}</div>
                    <div class="fallback-front">
                        <div class="fallback-title">{safe_title}</div>
                        <div class="fallback-author">{safe_author}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def get_book_description(book_row):
    for field in ["api_description", "description_x", "description_y", "metadata"]:
        if field in book_row.index:
            val = str(book_row.get(field, "")).strip()
            if val and val != "nan" and len(val) > 10:
                return val
    return "No description available for this book."

def get_book_categories(book_row):
    for field in ["api_categories", "categories", "subjects"]:
        if field in book_row.index:
            val = str(book_row.get(field, "")).strip()
            if val and val != "nan" and len(val) > 2:
                return val
    return ""

def find_similar_books(books_df, book_row, limit=10):
    book_id = int(book_row.get("book_id", -1))
    similar_ids = []
    subjects = str(book_row.get("subjects", ""))
    if subjects:
        keywords = [s.strip().lower() for s in subjects.split(";")][:3]
        subject_matches = books_df[books_df["subjects"].apply(
            lambda x: any(kw in str(x).lower() for kw in keywords) if pd.notna(x) else False
        )]
        subject_matches = subject_matches[subject_matches["book_id"] != book_id]
        similar_ids.extend(subject_matches.head(6)["book_id"].tolist())
    author = str(book_row.get("author", ""))
    if author and author != "nan":
        author_matches = books_df[(books_df["author"] == author) & (books_df["book_id"] != book_id)]
        similar_ids.extend(author_matches.head(4)["book_id"].tolist())
    seen = set()
    unique_ids = []
    for bid in similar_ids:
        if bid not in seen:
            seen.add(bid)
            unique_ids.append(bid)
    return unique_ids[:limit]

def display_book_shelf(books_df, book_ids, reason="", section_title="", section_key=""):
    """Display books in rows of 5 with pagination arrows."""
    if section_title:
        st.markdown(f'<div class="section-header">{section_title}</div>', unsafe_allow_html=True)

    disliked = st.session_state.get("disliked_books", set())
    book_ids = [bid for bid in book_ids if bid not in disliked]

    if not book_ids:
        st.info("No books found for this section.")
        return

    display_books = books_df[books_df["book_id"].isin(book_ids)].copy()
    if display_books.empty:
        st.info("No books found for this section.")
        return

    display_books["sort_order"] = display_books["book_id"].apply(lambda x: book_ids.index(x) if x in book_ids else 999999)
    display_books = display_books.sort_values("sort_order")

    page_size = 5
    state_key = f"{section_key}_page"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    total_books = len(display_books)
    max_page = max((total_books - 1) // page_size, 0)

    if total_books > page_size:
        nav1, nav2, nav3 = st.columns([1, 3, 1])
        with nav1:
            if st.button("‹ Prev", key=f"prev_{section_key}", use_container_width=True):
                if st.session_state[state_key] > 0:
                    st.session_state[state_key] -= 1
                    st.rerun()
        with nav2:
            start_show = st.session_state[state_key] * page_size + 1
            end_show = min((st.session_state[state_key] + 1) * page_size, total_books)
            st.markdown(
                f"<div style='text-align:center; padding-top:6px; font-size:12px; color:#6c757d;'>Showing {start_show}–{end_show} of {total_books}</div>",
                unsafe_allow_html=True
            )
        with nav3:
            if st.button("Next ›", key=f"next_{section_key}", use_container_width=True):
                if st.session_state[state_key] < max_page:
                    st.session_state[state_key] += 1
                    st.rerun()

    start_idx = st.session_state[state_key] * page_size
    end_idx = start_idx + page_size
    page_books = display_books.iloc[start_idx:end_idx]

    cols = st.columns(5)

    for idx, (_, book) in enumerate(page_books.iterrows()):
        with cols[idx]:
            title = str(book.get("api_title", "")).strip() or str(book.get("title", "Unknown Title"))
            author = str(book.get("api_authors", "")).strip() or str(book.get("author", "Unknown Author"))
            subjects = str(book.get("api_categories", "")).strip() or str(book.get("subjects", ""))
            book_id = int(book.get("book_id", 0))

            short_title = title[:45] + "..." if len(title) > 45 else title
            short_subjects = subjects[:25] + "..." if len(subjects) > 25 else subjects

            st.markdown('<div class="shelf-card">', unsafe_allow_html=True)
            show_cover(book, title, author)
            st.markdown(f'<div class="book-title">{short_title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="book-meta">{author[:28]}</div>', unsafe_allow_html=True)

            if subjects:
                st.markdown(f'<div class="book-subject">{short_subjects}</div>', unsafe_allow_html=True)

            if reason:
                st.markdown(f'<div class="reason-text">{reason}</div>', unsafe_allow_html=True)

            a, b, c, d = st.columns(4)
            with a:
                if st.button("♡", key=f"like_{section_key}_{book_id}_{idx}"):
                    st.session_state.liked_books.add(book_id)
                    st.toast("Added to liked books")
            with b:
                if st.button("×", key=f"hide_{section_key}_{book_id}_{idx}"):
                    st.session_state.disliked_books.add(book_id)
                    st.toast("Added to not interested")
                    st.rerun()
            with c:
                if st.button("☆", key=f"save_{section_key}_{book_id}_{idx}"):
                    st.session_state.saved_books.add(book_id)
                    st.toast("Saved for later")
            with d:
                if st.button("📖", key=f"detail_{section_key}_{book_id}_{idx}", help="Read more"):
                    st.session_state.page = "book_detail"
                    st.session_state.detail_book_id = book_id
                    st.rerun()

            st.markdown('<div class="shelf-line"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def get_user_favorite_subjects(user_history_df, books_df, user_id):
    user_books = user_history_df[user_history_df["user_id"] == user_id]["book_id"].tolist()
    user_book_info = books_df[books_df["book_id"].isin(user_books)]
    if "subjects" in user_book_info.columns and not user_book_info.empty:
        all_subjects = []
        for subj in user_book_info["subjects"].dropna():
            all_subjects.extend([s.strip() for s in str(subj).split(";")])
        if all_subjects:
            subject_counts = Counter(all_subjects)
            return [s for s, _ in subject_counts.most_common(5)]
    return []

def get_user_favorite_authors(user_history_df, books_df, user_id):
    user_books = user_history_df[user_history_df["user_id"] == user_id]["book_id"].tolist()
    user_book_info = books_df[books_df["book_id"].isin(user_books)]
    if "author" in user_book_info.columns and not user_book_info.empty:
        authors = user_book_info["author"].dropna().tolist()
        author_counts = Counter(authors)
        return [a for a, _ in author_counts.most_common(5)]
    return []

def get_recommendations_for_new_user(books_df, preferences):
    filtered = books_df.copy()
    if preferences.get("subjects") and "subjects" in filtered.columns:
        subject_keywords = preferences["subjects"]
        mask = filtered["subjects"].apply(
            lambda x: any(kw.lower() in str(x).lower() for kw in subject_keywords) if pd.notna(x) else False
        )
        subject_filtered = filtered[mask]
        if not subject_filtered.empty:
            filtered = subject_filtered
    if preferences.get("authors") and "author" in filtered.columns:
        author_keywords = preferences["authors"]
        mask = filtered["author"].apply(
            lambda x: any(kw.lower() in str(x).lower() for kw in author_keywords) if pd.notna(x) else False
        )
        author_filtered = filtered[mask]
        if not author_filtered.empty:
            filtered = pd.concat([author_filtered, filtered]).drop_duplicates(subset="book_id")
    if filtered.empty and not books_df.empty:
        filtered = books_df.sample(min(20, len(books_df)))
    return filtered.head(20)

# ============================================================
# MAIN
# ============================================================
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "liked_books" not in st.session_state:
        st.session_state.liked_books = set()
    if "disliked_books" not in st.session_state:
        st.session_state.disliked_books = set()
    if "saved_books" not in st.session_state:
        st.session_state.saved_books = set()
    if "last_user_name" not in st.session_state:
        st.session_state.last_user_name = ""
    if "last_user_id" not in st.session_state:
        st.session_state.last_user_id = None
    if "existing_user_submitted" not in st.session_state:
        st.session_state.existing_user_submitted = False
    if "detail_book_id" not in st.session_state:
        st.session_state.detail_book_id = None
    if "reading_log" not in st.session_state:
        st.session_state.reading_log = []
    if "new_user_submitted" not in st.session_state:
        st.session_state.new_user_submitted = False

    recommendations = load_recommendations()
    books_df = load_books()
    user_history = load_user_history()
    popular_book_ids = get_popular_books(user_history)

    all_subjects = get_all_subjects(books_df)
    all_authors = get_all_authors(books_df)
    all_titles = get_all_titles(books_df)

    with st.sidebar:
        st.title("UniLibrary")
        st.markdown("---")

        st.subheader("Navigation")
        if st.button("Home", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.user_type = None
            st.session_state.user_id = None
            st.session_state.existing_user_submitted = False
            st.rerun()

        st.markdown("---")
        st.subheader("User Type")
        st.write("Choose your access type from the home page.")

        show_activity = (
            (st.session_state.page == "existing_user" and st.session_state.existing_user_submitted)
            or st.session_state.page in ["liked_page", "saved_page", "hidden_page", "book_detail"]
            or (st.session_state.page == "new_user" and st.session_state.get("new_user_submitted", False))
        )

        if show_activity:
            st.markdown("---")
            st.subheader("Your Activity")

            if st.session_state.user_id is not None and not user_history.empty:
                user_books_count = len(user_history[user_history["user_id"] == st.session_state.user_id])
                st.metric("📖 Books Borrowed", user_books_count)

            if st.button(f"Liked ({len(st.session_state.liked_books)})", use_container_width=True, key="liked_page_btn"):
                st.session_state.page = "liked_page"
                st.rerun()

            if st.button(f"Saved ({len(st.session_state.saved_books)})", use_container_width=True, key="saved_page_btn"):
                st.session_state.page = "saved_page"
                st.rerun()

            if st.button(f"Not Interested ({len(st.session_state.disliked_books)})", use_container_width=True, key="hidden_page_btn"):
                st.session_state.page = "hidden_page"
                st.rerun()

            st.markdown("---")
            st.subheader("📝 Log Your Reading")

            import datetime

            with st.form("log_reading_form", clear_on_submit=True):
                log_book_options = []
                if st.session_state.user_id is not None and not user_history.empty:
                    user_book_ids = user_history[user_history["user_id"] == st.session_state.user_id]["book_id"].tolist()
                    user_books_info = books_df[books_df["book_id"].isin(user_book_ids)]
                    if not user_books_info.empty:
                        log_book_options = [(int(row["book_id"]), str(row.get("title", "Unknown"))[:50]) for _, row in user_books_info.iterrows()]

                extra_ids = list(st.session_state.liked_books | st.session_state.saved_books)
                if extra_ids:
                    extra_books = books_df[books_df["book_id"].isin(extra_ids)]
                    for _, row in extra_books.iterrows():
                        entry = (int(row["book_id"]), str(row.get("title", "Unknown"))[:50])
                        if entry not in log_book_options:
                            log_book_options.append(entry)

                if log_book_options:
                    book_choices = {f"{title} (#{bid})": bid for bid, title in log_book_options[:50]}
                    selected_book = st.selectbox("📖 Book read", options=list(book_choices.keys()), key="log_book_select")
                else:
                    selected_book = None
                    st.caption("Borrow or like books first to log reading.")

                log_minutes = st.number_input("⏱️ Minutes read", min_value=1, max_value=600, value=30, step=5, key="log_minutes_input")
                log_date = st.date_input("📅 Date finished", value=datetime.date.today(), key="log_date_input")

                log_submitted = st.form_submit_button("✅ Log Reading", use_container_width=True)

            if log_submitted and selected_book:
                book_id = book_choices[selected_book]
                st.session_state.reading_log.append({
                    "book_id": book_id,
                    "minutes": log_minutes,
                    "date": str(log_date),
                    "title": selected_book
                })
                st.toast(f"✅ Logged {log_minutes} min reading!")
                st.rerun()

            if st.session_state.reading_log:
                st.caption("Recent logs:")
                for entry in st.session_state.reading_log[-3:][::-1]:
                    st.markdown(
                        f"<div style='font-size:11px;color:#5c5c5c;padding:2px 0;'>📖 {entry['minutes']} min — {entry['date']}</div>",
                        unsafe_allow_html=True
                    )

            st.markdown("---")
            st.subheader("🏆 Monthly Challenge")

            current_month = datetime.datetime.now().strftime("%B")
            current_month_num = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            challenge_goal = 180

            user_minutes = 0
            books_logged_this_month = 0
            for entry in st.session_state.reading_log:
                try:
                    entry_date = datetime.datetime.strptime(entry["date"], "%Y-%m-%d")
                    if entry_date.month == current_month_num and entry_date.year == current_year:
                        user_minutes += entry["minutes"]
                        books_logged_this_month += 1
                except:
                    pass

            st.markdown(f"**📅 {current_month} Challenge:**")
            st.markdown(f"Read **{challenge_goal} minutes** this month")

            progress = min(user_minutes / challenge_goal, 1.0)
            st.progress(progress)
            st.caption(f"{user_minutes} / {challenge_goal} min ({int(progress * 100)}%)")

            if progress >= 1.0:
                st.success("🎉 Challenge complete! You're a champion!")
            elif progress >= 0.5:
                st.info(f"🔥 Halfway there! {challenge_goal - user_minutes} min to go!")
            else:
                st.warning(f"📖 Keep going! {challenge_goal - user_minutes} min remaining")

            st.markdown("---")
            st.subheader("🎯 Your Reading Goal")
            yearly_goal = st.slider("Books to read this year", 5, 50, 12, key="yearly_goal_slider")

            total_books_logged = len(set(entry["book_id"] for entry in st.session_state.reading_log))
            goal_progress = min(total_books_logged / yearly_goal, 1.0)
            st.progress(goal_progress)
            st.caption(f"{total_books_logged} / {yearly_goal} books ({int(goal_progress * 100)}%)")

            st.markdown("---")
            st.subheader("🥇 Leaderboard")
            st.caption(f"{current_month} reading challenge")

            fake_users = [
                {"name": "Emma L.", "user_id": 3421, "minutes": 245},
                {"name": "Lucas M.", "user_id": 1587, "minutes": 210},
                {"name": "Chloé R.", "user_id": 5903, "minutes": 198},
                {"name": "Noah B.", "user_id": 2744, "minutes": 185},
                {"name": "Léa K.", "user_id": 6218, "minutes": 172},
                {"name": "Hugo S.", "user_id": 4092, "minutes": 160},
                {"name": "Manon D.", "user_id": 7501, "minutes": 145},
                {"name": "Arthur P.", "user_id": 892, "minutes": 130},
            ]

            current_user_name = st.session_state.last_user_name if st.session_state.last_user_name else "You"
            current_user_entry = {"name": f"⭐ {current_user_name}", "user_id": st.session_state.user_id or 0, "minutes": user_minutes}

            all_entries = fake_users + [current_user_entry]
            all_entries.sort(key=lambda x: x["minutes"], reverse=True)

            for rank, entry in enumerate(all_entries[:8], 1):
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f" {rank}."
                is_current = entry["name"].startswith("⭐")
                style = "font-weight:700; color:#8c1746;" if is_current else "color:#333;"
                st.markdown(
                    f"<div style='{style} font-size:13px; padding:3px 0;'>{medal} {entry['name']} — {entry['minutes']} min</div>",
                    unsafe_allow_html=True
                )

    # ============================================================
    # BOOK DETAIL PAGE
    # ============================================================
    if st.session_state.page == "book_detail":
        book_id = st.session_state.detail_book_id
        book_data = books_df[books_df["book_id"] == book_id]

        if st.button("← Back", key="back_from_detail"):
            if st.session_state.user_type == "existing":
                st.session_state.page = "existing_user"
            elif st.session_state.user_type == "new":
                st.session_state.page = "new_user"
            else:
                st.session_state.page = "home"
            st.rerun()

        if book_data.empty:
            st.error("Book not found.")
            return

        book = book_data.iloc[0]
        title = str(book.get("api_title", "")).strip() or str(book.get("title", "Unknown Title"))
        author = str(book.get("api_authors", "")).strip() or str(book.get("author", "Unknown Author"))
        description = get_book_description(book)
        categories = get_book_categories(book)
        publisher = str(book.get("api_publisher", "")) or str(book.get("publisher", ""))
        published_date = str(book.get("api_published_date", ""))
        isbn = str(book.get("isbn", ""))
        subjects = str(book.get("subjects", ""))
        lang = str(book.get("language", ""))

        st.markdown('<div class="detail-container">', unsafe_allow_html=True)
        col_cover, col_info = st.columns([1, 2])

        with col_cover:
            cover_url = get_book_cover_url(book)
            if cover_url:
                st.image(cover_url, width=250)
            else:
                st.markdown(
                    f'<div class="fallback-cover {get_cover_theme(book_id)}" style="height:300px;">'
                    f'<div class="fallback-spine-title">{html.escape(title[:28])}</div>'
                    f'<div class="fallback-front"><div class="fallback-title">{html.escape(title)}</div>'
                    f'<div class="fallback-author">{html.escape(author)}</div></div></div>',
                    unsafe_allow_html=True
                )

        with col_info:
            st.markdown(f'<div class="detail-title">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-author">by {author}</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f'<div class="detail-description">{description}</div>', unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("♡ Like", key="detail_like", use_container_width=True):
                    st.session_state.liked_books.add(book_id)
                    st.toast("Added to liked books!")
            with col_b:
                if st.button("☆ Save", key="detail_save", use_container_width=True):
                    st.session_state.saved_books.add(book_id)
                    st.toast("Saved for later!")
            with col_c:
                if st.button("× Not Interested", key="detail_hide", use_container_width=True):
                    st.session_state.disliked_books.add(book_id)
                    st.toast("Removed from recommendations")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="detail-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="detail-meta-label">Publisher</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-meta-value">{publisher if publisher and publisher != "nan" else "Not available"}</div>', unsafe_allow_html=True)
            st.markdown('<div class="detail-meta-label">Published Date</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-meta-value">{published_date if published_date and published_date != "nan" else "Not available"}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="detail-meta-label">Categories</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-meta-value">{categories if categories else "Not available"}</div>', unsafe_allow_html=True)
            st.markdown('<div class="detail-meta-label">Subjects</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-meta-value">{subjects if subjects else "Not available"}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="detail-meta-label">ISBN</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-meta-value">{isbn if isbn and isbn != "nan" else "Not available"}</div>', unsafe_allow_html=True)
            st.markdown('<div class="detail-meta-label">Language</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-meta-value">{lang if lang and lang != "nan" else "Not specified"}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        similar_ids = find_similar_books(books_df, book)
        if similar_ids:
            display_book_shelf(books_df, similar_ids, reason="Similar to this book", section_title="Similar Books", section_key="detail_similar")

        return

    # ============================================================
    # HOME PAGE
    # ============================================================
    if st.session_state.page == "home":
        hero_path = Path("library_hero.jpg")
        if hero_path.exists():
            st.image(str(hero_path), use_container_width=True)
        else:
            st.markdown("""
            <div class="welcome-banner">
                <h1>UniLibrary Recommendation System</h1>
                <p>This application helps university library users discover relevant books based on borrowing history or reading preferences.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## Welcome")
        st.write(
            "Use this recommendation system to explore books from the university library. "
            "Existing users receive personalized suggestions based on borrowing history. "
            "New users receive recommendations based on field of study, favorite subjects, authors, and language preferences."
        )

        st.markdown("### Please choose how you would like to continue")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Existing User")
            st.write("Access recommendations based on your library history.")
            if st.button("Continue as Existing User", use_container_width=True, type="primary"):
                st.session_state.page = "existing_user"
                st.session_state.user_type = "existing"
                st.session_state.existing_user_submitted = False
                st.rerun()

        with col2:
            st.markdown("#### New User")
            st.write("Receive recommendations based on your preferences.")
            if st.button("Continue as New User", use_container_width=True):
                st.session_state.page = "new_user"
                st.session_state.user_type = "new"
                st.rerun()

        st.markdown("---")
        st.info("Choose 'Existing User' or 'New User' to start exploring personalized recommendations.")

    # ============================================================
    # EXISTING USER PAGE
    # ============================================================
    elif st.session_state.page == "existing_user":
        st.markdown("## Existing Member Access")
        st.markdown("Enter your library details to receive personalized book recommendations.")

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            user_name = st.text_input("Your name (optional)", value=st.session_state.last_user_name, placeholder="e.g. nini")
        with col2:
            user_id_input = st.number_input("Your Library ID (1 - 7837)", min_value=1, max_value=7837,
                value=int(st.session_state.last_user_id) if st.session_state.last_user_id is not None else 606, step=1)
        with col3:
            st.markdown("")
            st.markdown("")
            get_recs = st.button("Get Recommendations", type="primary", use_container_width=True)

        if get_recs:
            st.session_state.last_user_name = user_name
            st.session_state.last_user_id = user_id_input
            st.session_state.existing_user_submitted = True

        active_user_id = st.session_state.last_user_id
        active_user_name = st.session_state.last_user_name

        if st.session_state.existing_user_submitted and active_user_id in recommendations:
            st.session_state.user_id = active_user_id

            if active_user_name and str(active_user_name).strip():
                welcome_text = f"Welcome back, {str(active_user_name).strip()}! Here are your book recommendations."
            else:
                welcome_text = "Welcome back! Here are your book recommendations."

            st.markdown(f"""
            <div class="user-summary">
                <h3>{welcome_text}</h3>
                <p>These recommendations are based on your borrowing history in the university library.</p>
            </div>
            """, unsafe_allow_html=True)

            user_books = user_history[user_history["user_id"] == active_user_id]["book_id"].tolist()

            # 1. RECOMMENDATIONS FOR YOU (Max 10 books)
            rec_book_ids = recommendations[active_user_id]
            unread_recs = [bid for bid in rec_book_ids if bid not in user_books]
            if not unread_recs:
                unread_recs = rec_book_ids
            display_book_shelf(books_df, unread_recs[:10], reason="💡 Based on your borrowing history", section_title="⭐ Recommended For You", section_key="existing_rec")

            # 2. BOOKCLUB
            st.markdown('<div class="section-header">👥 Book Club — Connect With Similar Readers</div>', unsafe_allow_html=True)
            st.write("Connect with other readers who borrowed the same books as you.")

            similar_readers = find_similar_readers(user_history, active_user_id)
            if similar_readers:
                for reader in similar_readers[:1]: # Show top match to keep UI clean
                    st.markdown(f"""
                    <div class="bookclub-card" style="border-left: 5px solid #8c1746;">
                        <strong style="color: #8c1746;">Reader #{reader['user_id']}</strong> — {reader['common_count']} books in common with you
                    </div>
                    """, unsafe_allow_html=True)
                    if reader["new_books"]:
                        display_book_shelf(books_df, reader["new_books"][:5], reason=f"Reader #{reader['user_id']} also enjoyed this", section_title="", section_key=f"bookclub_{reader['user_id']}")
            else:
                st.info("We haven't found similar readers yet. Keep borrowing to build connections!")

            # 3. MORE FROM FAVORITE AUTHORS
            fav_authors = get_user_favorite_authors(user_history, books_df, active_user_id)
            if fav_authors:
                author_books = books_df[books_df["author"].isin(fav_authors)]
                author_books = author_books[~author_books["book_id"].isin(user_books)]
                if not author_books.empty:
                    display_book_shelf(books_df, author_books.head(10)["book_id"].tolist(), reason="✍️ By authors you already enjoy", section_title="✍️ More From Your Favorite Authors", section_key="existing_authors")

            # 4. MOST READ BOOKS (Popular in Library)
            if popular_book_ids:
                display_book_shelf(books_df, popular_book_ids[:10], reason="📈 Most borrowed in our library", section_title="🇨🇭 Popular in Switzerland (Most Read)", section_key="existing_popular")

            # 5. SAVED
            if st.session_state.saved_books:
                saved_ids = list(st.session_state.saved_books)
                display_book_shelf(books_df, saved_ids[:10], reason="🔖 Saved for later", section_title="🔖 Saved Books", section_key="existing_saved")

        elif st.session_state.existing_user_submitted:
            st.error("Non-existing user. Please check your ID (valid range: 1-7837).")

    # ============================================================
    # NEW USER PAGE
    # ============================================================
    elif st.session_state.page == "new_user":
        st.markdown("## New Library User")
        st.markdown("Tell us about your reading preferences and we'll recommend books for you.")

        with st.form("new_user_form"):
            st.markdown("### Your Reading Profile")
            col1, col2 = st.columns(2)

            with col1:
                language = st.selectbox("Preferred reading language", ["French", "English", "German", "Italian", "Spanish", "Other"])
                study_subject = st.selectbox("Field of study", options=["Select your field of study"] + all_subjects, index=0)
                fav_subjects_selected = st.multiselect("Favorite reading subjects", options=all_subjects[:200])

            with col2:
                fav_authors_selected = st.multiselect("Favorite authors", options=all_authors[:500])
                liked_books_selected = st.multiselect("Books you've enjoyed", options=all_titles[:500])
                reading_type = st.selectbox("What type of reading do you prefer?", ["Fiction", "Non-Fiction", "Academic", "Comics/Manga", "Mix of everything"])

            submitted = st.form_submit_button("Generate My Recommendations", type="primary", use_container_width=True)

        if submitted:
            st.session_state.new_user_submitted = True
            selected_study_subject = "" if study_subject == "Select your field of study" else study_subject
            preferences = {
                "language": language,
                "subjects": fav_subjects_selected + ([selected_study_subject] if selected_study_subject else []),
                "authors": [str(a) for a in fav_authors_selected],
                "reading_type": reading_type,
            }
            type_mapping = {
                "Fiction": ["Roman", "Fiction", "Littérature"],
                "Non-Fiction": ["Essai", "Sciences", "Histoire"],
                "Academic": ["Manuels", "enseignement", "Sciences"],
                "Comics/Manga": ["Bandes dessinées", "Mangas", "Comics"],
                "Mix of everything": []
            }
            preferences["subjects"].extend(type_mapping.get(reading_type, []))

            rec_books = get_recommendations_for_new_user(books_df, preferences)

            if not rec_books.empty:
                display_book_shelf(books_df, rec_books.head(10)["book_id"].tolist(), reason="Based on your stated preferences", section_title="Recommended For You", section_key="new_rec")

                if preferences["subjects"]:
                    subject_popular = books_df[books_df["subjects"].apply(
                        lambda x: any(s.lower() in str(x).lower() for s in preferences["subjects"][:3]) if pd.notna(x) else False
                    )]
                    if not subject_popular.empty:
                        display_book_shelf(books_df, subject_popular.sample(min(10, len(subject_popular)))["book_id"].tolist(), reason="Popular in your field of interest", section_title="Popular in Your Field", section_key="new_field")

                if preferences["authors"]:
                    author_recs = books_df[books_df["author"].apply(
                        lambda x: any(a.lower() in str(x).lower() for a in preferences["authors"]) if pd.notna(x) else False
                    )]
                    if not author_recs.empty:
                        display_book_shelf(books_df, author_recs.head(10)["book_id"].tolist(), reason="By authors you mentioned", section_title="From Authors You Like", section_key="new_authors")

                if st.session_state.saved_books:
                    saved_ids = list(st.session_state.saved_books)
                    display_book_shelf(books_df, saved_ids[:10], reason="Saved for later", section_title="Next Up", section_key="new_saved")

    # ============================================================
    # LIKED PAGE
    # ============================================================
    elif st.session_state.page == "liked_page":
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back", key="back_from_liked"):
                if st.session_state.user_type == "existing":
                    st.session_state.page = "existing_user"
                elif st.session_state.user_type == "new":
                    st.session_state.page = "new_user"
                else:
                    st.session_state.page = "home"
                st.rerun()
        with col_title:
            st.title("Your Liked Books")

        liked_ids = list(st.session_state.liked_books)
        if len(liked_ids) == 0:
            st.info("You have not liked any books yet.")
        else:
            display_book_shelf(books_df, liked_ids, reason="From your liked books", section_title="Liked Books", section_key="liked_page")

    # ============================================================
    # SAVED PAGE
    # ============================================================
    elif st.session_state.page == "saved_page":
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back", key="back_from_saved"):
                if st.session_state.user_type == "existing":
                    st.session_state.page = "existing_user"
                elif st.session_state.user_type == "new":
                    st.session_state.page = "new_user"
                else:
                    st.session_state.page = "home"
                st.rerun()
        with col_title:
            st.title("Your Saved Books")

        saved_ids = list(st.session_state.saved_books)
        if len(saved_ids) == 0:
            st.info("You have not saved any books yet.")
        else:
            display_book_shelf(books_df, saved_ids, reason="Saved for later", section_title="Saved Books", section_key="saved_page")

    # ============================================================
    # HIDDEN PAGE
    # ============================================================
    elif st.session_state.page == "hidden_page":
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("← Back", key="back_from_hidden"):
                if st.session_state.user_type == "existing":
                    st.session_state.page = "existing_user"
                elif st.session_state.user_type == "new":
                    st.session_state.page = "new_user"
                else:
                    st.session_state.page = "home"
                st.rerun()
        with col_title:
            st.title("Not Interested")

        hidden_ids = list(st.session_state.disliked_books)
        if len(hidden_ids) == 0:
            st.info("You have not hidden any books yet.")
        else:
            hidden_books = books_df[books_df["book_id"].isin(hidden_ids)]
            cols = st.columns(5)
            for idx, (_, book) in enumerate(hidden_books.head(20).iterrows()):
                with cols[idx % 5]:
                    title = str(book.get("api_title", "")).strip() or str(book.get("title", "Unknown Title"))
                    author = str(book.get("api_authors", "")).strip() or str(book.get("author", "Unknown Author"))
                    book_id = int(book.get("book_id", 0))
                    show_cover(book, title, author)
                    st.markdown(f'<div class="book-title">{title[:40]}</div>', unsafe_allow_html=True)
                    if st.button("Restore", key=f"restore_hidden_{book_id}_{idx}"):
                        st.session_state.disliked_books.remove(book_id)
                        st.toast("Book restored")
                        st.rerun()

    # ============================================================
    # SEARCH
    # ============================================================
    if st.session_state.page not in ["home", "book_detail"]:
        st.markdown('<div class="section-header">Search the Catalog</div>', unsafe_allow_html=True)
        search_query = st.text_input("Search by title, author, or subject", placeholder="Type to search...")
        if search_query:
            results = books_df[
                books_df.apply(
                    lambda row: search_query.lower() in str(row.get("title", "")).lower()
                    or search_query.lower() in str(row.get("author", "")).lower()
                    or search_query.lower() in str(row.get("subjects", "")).lower(),
                    axis=1
                )
            ]
            if not results.empty:
                display_book_shelf(books_df, results.head(10)["book_id"].tolist(), reason="Search result", section_title=f"Results for '{search_query}'", section_key="search")
            else:
                st.info("No books found matching your search.")

if __name__ == "__main__":
    main()