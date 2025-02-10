import streamlit as st
from backend import read_pdf, get_embedding, generate_response

# Set Streamlit page configuration
st.set_page_config(page_title="Chat with PDF", page_icon="📄", layout="centered")

# Title
st.title("📄 Chat with Your PDF")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Step 1: Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="hidden")

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")

    # Step 2: Show Loading Spinner
    with st.spinner("🔄 Processing file... Please wait."):
        text = read_pdf(uploaded_file)
        retriever = get_embedding(text)
    st.success("✅ Processing complete!")

    # Step 3: Display Chatbot UI
    st.subheader("💬 Chat with your PDF")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input field
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Display bot response
        with st.spinner("🤖 Thinking..."):
            response = generate_response(retriever, user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)
