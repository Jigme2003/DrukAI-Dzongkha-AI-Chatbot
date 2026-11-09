import streamlit as st
from src.chat_engine import get_chat_response
from src.document_processor import extract_document_text

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DrukAI | Dzongkha AI Assistant",
    page_icon="🇧🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize displayed messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 2. SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Initialize uploaded document content
if "document_context" not in st.session_state:
    st.session_state.document_context = ""

if "document_name" not in st.session_state:
    st.session_state.document_name = ""

# ==========================================
# 3. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F4F7FB;
    color: #172B4D;
}

/* Main content spacing */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

/* Header */
header[data-testid="stHeader"] {
    background-color: #F4F7FB;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #14243A;
    border-right: 1px solid #263B55;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

/* Sidebar captions */
section[data-testid="stSidebar"] .stCaption {
    color: #B9C8DA !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton button {
    background-color: #263E5D;
    color: white !important;
    border: 1px solid #405A79;
    border-radius: 9px;
    text-align: left;
    min-height: 42px;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background-color: #365779;
    border-color: #7DA5D1;
}

/* Main headings */
.main-title {
    color: #172B4D;
    font-size: 40px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 2px;
}

.main-subtitle {
    color: #61738B;
    font-size: 16px;
    margin-top: 5px;
}

/* Welcome card */
.welcome-card {
    background: linear-gradient(
        120deg,
        #FFFFFF,
        #EAF2FF
    );
    border: 1px solid #D7E3F4;
    border-radius: 18px;
    padding: 32px;
    margin-top: 25px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(30, 55, 90, 0.05);
}

.welcome-card h2 {
    color: #172B4D !important;
    font-size: 27px;
    margin-bottom: 10px;
}

.welcome-card p {
    color: #536780 !important;
    font-size: 15px;
    line-height: 1.7;
}

/* Feature cards */
.feature-card {
    background-color: #FFFFFF;
    border: 1px solid #E0E7F0;
    border-radius: 14px;
    padding: 20px;
    min-height: 150px;
    box-shadow: 0 3px 12px rgba(30, 55, 90, 0.04);
}

.feature-card h4 {
    color: #1C3557 !important;
    font-size: 17px;
}

.feature-card p {
    color: #64748B !important;
    font-size: 14px;
    line-height: 1.6;
}

/* Main conversation text */
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #172B4D;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid #DFE7F0;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 12px;
}

/* Chat message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #263B55 !important;
    line-height: 1.7;
}

/* Chat input */
[data-testid="stChatInput"] {
    background-color: #FFFFFF;
    border: 1px solid #D8E1EC;
    border-radius: 14px;
    box-shadow: 0 3px 15px rgba(30, 55, 90, 0.06);
}

[data-testid="stChatInput"] textarea {
    color: #172B4D !important;
    background-color: #FFFFFF !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8796A9 !important;
}

/* General buttons */
.stButton > button {
    background-color: #315D91;
    color: white !important;
    border: 1px solid #315D91;
    border-radius: 9px;
    min-height: 40px;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #244A77;
    border-color: #244A77;
    color: white !important;
}

/* Dividers */
hr {
    border-color: #DFE7F0;
}

/* Status text */
.status-text {
    color: #B9C8DA;
    font-size: 13px;
    margin-bottom: 10px;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .main-title {
        font-size: 30px;
    }

    .welcome-card {
        padding: 20px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div style="padding-top:15px; padding-bottom:15px;">

        <h1 style="color:#FFFFFF; font-size:30px;">
            🇧🇹 DrukAI
        </h1>

        <p style="color:#B9C8DA; font-size:13px;">
            Your Intelligent Dzongkha AI Assistant
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Workspace")

    if st.button("＋  New Conversation",
                 use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    if st.button("🗑️  Clear Conversation",
                 use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.divider()

    st.markdown("### AI Capabilities")

    st.markdown("""
    <div style="line-height:2.5; font-size:14px;">

    💬 &nbsp; Dzongkha Chat

    <br>

    🌐 &nbsp; English to Dzongkha

    <br>

    📄 &nbsp; PDF Translation

    <br>

    📝 &nbsp; Word Document Translation

    <br>

    🖼️ &nbsp; Image Text Translation

    <br>

    📚 &nbsp; Document Summarisation

    <br>

    ❓ &nbsp; Question Answering

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### System Information")

    st.markdown("""
    <div class="status-text">
        🟢 Dashboard: Running
    </div>

    <div class="status-text">
        🟡 Ollama: Not Connected
    </div>

    <div class="status-text">
        🟡 Dzongkha AI: Under Development
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <p style="color:#B9C8DA; font-size:12px;">
        DrukAI v1.0<br>
        Generative AI & Prompt Engineering Project
    </p>
    """, unsafe_allow_html=True)


# ==========================================
# 5. MAIN HEADER
# ==========================================

st.markdown("""
<div class="main-title">
    DrukAI 🇧🇹
</div>

<div class="main-subtitle">
    Your Intelligent Dzongkha AI Assistant
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# 6. WELCOME SCREEN
# ==========================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome-card">

        <h2>
            ཀུན་ལ་བཀྲ་ཤིས་བདེ་ལེགས།
        </h2>

        <h2>
            Welcome to DrukAI!
        </h2>

        <p>
            Your personal AI assistant for understanding,
            translating and communicating in Dzongkha.
        </p>

        <p>
            Ask questions, translate English text,
            upload documents and explore the Dzongkha language.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("### What would you like to do today?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="feature-card">

            <h4>🌐 Translation</h4>

            <p>
                Translate English words, sentences
                and paragraphs into Dzongkha.
            </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Try Translation", key="translate"):
            st.session_state.pending_prompt = (
                "Translate Hello, how are you? into Dzongkha."
            )
            st.rerun()

    with col2:

        st.markdown("""
        <div class="feature-card">

            <h4>💬 AI Chatbot</h4>

            <p>
                Ask questions and communicate
                with your intelligent AI assistant.
            </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Ask a Question", key="question"):
            st.session_state.pending_prompt = (
                "Explain what artificial intelligence is."
            )
            st.rerun()

    with col3:

        st.markdown("""
        <div class="feature-card">

            <h4>📄 Document AI</h4>

            <p>
                Translate and summarise documents
                using artificial intelligence.
            </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore Documents", key="documents"):
            st.session_state.pending_prompt = (
                "I want to translate a document into Dzongkha."
            )
            st.rerun()


# ==========================================
# 7. CONVERSATION AREA
# ==========================================

st.markdown("### 💬 Conversation")

# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# ==========================================
# 8. USER INPUT
# ==========================================

# Document uploader
st.subheader("Upload a Document")

uploaded_file = st.file_uploader(
    "Upload your PDF or Word document",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    try:
        document_text = extract_document_text(uploaded_file)

        st.session_state.document_context = document_text
        st.session_state.document_name = uploaded_file.name

        st.success(
            f"Document loaded: {uploaded_file.name}"
        )

        with st.expander("Preview extracted text"):
            st.text(document_text[:3000])

    except Exception as error:
        st.error(f"Document processing failed: {error}")
        st.session_state.document_context = ""
        st.session_state.document_name = ""
        
# Chat input
user_input = st.chat_input("Ask DrukAI something...")

if user_input:

    # Display user's message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate AI response
    with st.spinner("DrukAI is thinking..."):

        try:
            response = get_chat_response(
                user_input,
                st.session_state.chat_history,
                st.session_state.document_context
            )

        except Exception as error:
            response = f"Sorry, an error occurred: {error}"

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# Handle suggested prompts

if st.session_state.pending_prompt:

    user_input = st.session_state.pending_prompt

    st.session_state.pending_prompt = None


# ==========================================
# 9. TEMPORARY RESPONSE
# ==========================================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = (
        "Thank you for your message!\n\n"
        "DrukAI's dashboard is working successfully. "
        "The local AI model and Dzongkha translation "
        "system will be integrated in the upcoming stages."
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

