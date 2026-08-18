import streamlit as st

from api import add_document, search_documents


st.set_page_config(
    page_title="Semantic Search",
    page_icon="🔎",
    layout="wide",
)


st.title("Semantic Search")

page = st.sidebar.radio(
    "Menu",
    ["Search", "Add Document", "About"],
)


# Search
if page == "Search":

    st.header("Search Documents")

    query = st.text_input(
        "Search",
        placeholder="Enter your search query...",
    )

    col1, col2 = st.columns(2)

    with col1:
        limit = st.number_input(
            "Limit",
            min_value=1,
            max_value=50,
            value=5,
        )

    with col2:
        min_score = st.number_input(
            "Minimum similarity",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
        )

    col1, col2 = st.columns(2)

    with col1:
        category = st.text_input(
            "Category",
            placeholder="technology",
        )

    with col2:
        source = st.text_input(
            "Source",
            placeholder="documentation",
        )

    page_number = st.number_input(
        "Page",
        min_value=1,
        value=1,
    )

    if st.button("Search", type="primary"):

        if not query.strip():
            st.warning("Please enter a search query.")
            st.stop()

        try:
            with st.spinner("Searching..."):
                data = search_documents(
                    query=query.strip(),
                    limit=limit,
                    min_score=min_score,
                    category=category.strip() or None,
                    source=source.strip() or None,
                    page=page_number,
                )

        except Exception as e:
            st.error(f"Search failed: {e}")
            st.stop()

        results = data.get("results", [])
        count = data.get("count", len(results))

        st.divider()

        st.write(f"Found {count} result(s)")

        if not results:
            st.info("No matching documents found.")

        for result in results:

            st.subheader(
                f"Document {result.get('id')}"
            )

            st.write(
                result.get("content", "")
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                score = result.get(
                    "similarity",
                    result.get("score"),
                )

                if score is not None:
                    st.write(
                        f"Similarity: {float(score):.4f}"
                    )

            with col2:
                category_value = result.get("category")

                if category_value:
                    st.write(
                        f"Category: {category_value}"
                    )

            with col3:
                source_value = result.get("source")

                if source_value:
                    st.write(
                        f"Source: {source_value}"
                    )

            st.divider()


# Add Document
elif page == "Add Document":

    st.header("Add Document")

    content = st.text_area(
        "Content",
        height=200,
        placeholder="Enter document content...",
    )

    category = st.text_input(
        "Category",
        value="technology",
    )

    source = st.text_input(
        "Source",
        value="documentation",
    )

    if st.button("Add Document", type="primary"):

        if not content.strip():
            st.warning("Content is required.")
            st.stop()

        if not category.strip():
            st.warning("Category is required.")
            st.stop()

        if not source.strip():
            st.warning("Source is required.")
            st.stop()

        try:
            with st.spinner("Adding document..."):
                result = add_document(
                    content=content.strip(),
                    category=category.strip(),
                    source=source.strip(),
                )

        except Exception as e:
            st.error(f"Could not create document: {e}")
            st.stop()

        st.success("Document created successfully.")

        if result.get("id"):
            st.write(f"ID: {result['id']}")


# About
elif page == "About":

    st.header("Architecture")

    st.code(
        """
Streamlit
    ↓
FastAPI
    ↓
BGE-small-en-v1.5
    ↓
Supabase PostgreSQL
    ↓
pgvector + HNSW
        """,
        language="text",
    )

    st.subheader("Features")

    features = [
        "384-dimensional embeddings",
        "Cosine similarity",
        "HNSW index",
        "Metadata filtering",
        "Pagination",
        "Similarity threshold",
        "Transaction rollback",
        "Embedding failure handling",
        "Automated tests",
    ]

    for feature in features:
        st.write(f"✓ {feature}")

    st.subheader("Project")

    st.write(
        """
This is a small semantic search project built to
understand embeddings, pgvector, similarity search,
and vector indexes with PostgreSQL.
        """
    )
