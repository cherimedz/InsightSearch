import streamlit as st
import re
from collections import defaultdict

with open("styles_search.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

def extract_terms(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def create_inverted_index(documents):
    inverted_idx = defaultdict(set)
    for doc_id, content in documents.items():
        terms = extract_terms(content)
        for term in terms:
            inverted_idx[term].add(doc_id)
    return inverted_idx

def search_boolean(inverted_idx, query, document_ids):
    query = query.lower()
    query_tokens = re.findall(r'\b\w+\b', query)
    matching_docs = set(document_ids)

    if 'and' in query:
        conditions = query.split(' and ')
        matching_docs = inverted_idx.get(conditions[0].strip(), set())
        for condition in conditions[1:]:
            matching_docs = matching_docs.intersection(inverted_idx.get(condition.strip(), set()))
    elif 'or' in query:
        matching_docs = set()
        conditions = query.split(' or ')
        for condition in conditions:
            matching_docs = matching_docs.union(inverted_idx.get(condition.strip(), set()))
    elif 'not' in query:
        conditions = query.split(' not ')
        if len(conditions) == 2:
            include_term = conditions[0].strip()
            exclude_term = conditions[1].strip()
            matching_docs = inverted_idx.get(include_term, set()).difference(inverted_idx.get(exclude_term, set()))
    else:
        matching_docs = set()
        for token in query_tokens:
            matching_docs = matching_docs.union(inverted_idx.get(token, set()))

    return matching_docs

document_dict = {}

st.title("🌟 Welcome to InsightSearch, the Document Search Demo App 🌟")

st.markdown("""
**Thank you for visiting InsightSearch!**

This application allows you to easily search through a collection of text documents using Boolean logic.
You can perform powerful searches with `AND`, `OR`, and `NOT` operations to quickly find the information you need.

**Key Features:**
- Upload multiple text files to create your own searchable document repository.
- Perform complex Boolean searches with ease.
- View the contents of matching documents directly within the app.

""")

st.sidebar.header("🚀 Quick Actions")

if st.sidebar.button("📁 View Uploaded Documents"):
    if document_dict:
        st.sidebar.write("**Uploaded Documents:**")
        for doc_id in document_dict:
            st.sidebar.write(f"- {doc_id}")
    else:
        st.sidebar.write("No documents uploaded yet.")

st.sidebar.subheader("👩‍💻 About Me")
st.sidebar.write("""
Hi there! I’m Medha Reju Pillai, currently pursuing an MSc in Computer Science and Data Analytics. I’m deeply passionate about technology and AI, and I’m excited about exploring cutting-edge innovations and making meaningful contributions in these dynamic fields. Let’s connect and drive technological advancements together!

Feel free to connect with me:
- [GitHub Profile](https://github.com/cherimedz) 🤍
- [LinkedIn Profile](https://linkedin.com/in/medha-reju-pillai-42551b277) 🌐
""")

st.sidebar.subheader("💻 Check Out My Other Apps")
st.sidebar.write("Explore more of my projects and apps here:")
st.sidebar.write("🔗 [Streamlit Apps](https://share.streamlit.io/user/cherimedz)")

st.sidebar.subheader("📬 Contact Me")
st.sidebar.write("""
For inquiries or further discussions, connect with me via my [GitHub](https://github.com/cherimedz) or [LinkedIn](https://linkedin.com/in/medha-reju-pillai-42551b277) profiles. I’d love to hear from you!
""")

st.sidebar.subheader("💬 Feedback")
feedback = st.sidebar.text_area("I value your feedback! Share your thoughts here:")
if st.sidebar.button("Submit Feedback"):
    if feedback:
        st.sidebar.write("Thank you for your feedback! 😊 Your input helps me improve.")
        with open("feedback.txt", "a") as f:
            f.write(feedback + "\n")
    else:
        st.sidebar.write("Please enter your feedback before submitting.")

st.markdown("<h2 style='font-size: 24px; font-weight: bold;'>Upload Your Text Files Here</h2>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("", accept_multiple_files=True, type=['txt'])

if uploaded_files:
    st.success(f"Successfully uploaded {len(uploaded_files)} file(s)!")
    for file in uploaded_files:
        content = file.read().decode("utf-8")
        document_dict[file.name] = content

    inverted_idx = create_inverted_index(document_dict)
    
    search_query = st.text_input("Enter your search query:")

    st.markdown("""
    **Here are some example Queries:**
    - `"data science" AND "machine learning"`
    - `"deep learning" OR "neural networks"`
    - `"artificial intelligence" NOT "AI"`
    """)

    if search_query:
        results = search_boolean(inverted_idx, search_query, document_dict.keys())
        if results:
            st.write("### Matching Documents:")
            for doc_id in results:
                st.write(f"**{doc_id}:**")
                st.text(document_dict[doc_id])
        else:
            st.warning("No documents found for your query.")
else:
    st.info("Please upload text files to get started.")

st.markdown("---")
st.markdown("**About InsightSearch:** This demo app was created to showcase my assignment on simple information retrieval techniques using Streamlit. Enjoy exploring and searching through your documents!")
