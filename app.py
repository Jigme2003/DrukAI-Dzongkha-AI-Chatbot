import streamlit as st
from datetime import datetime
from pathlib import Path
import base64

from src.chat_engine import get_chat_response
from src.document_processor import extract_document_text

st.set_page_config(
    page_title="DrukAI | Dzongkha AI Chatbot",
    page_icon="🇧🇹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Session state -----------------------------
def new_conversation():
    return {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "title": "New conversation",
        "messages": [],
        "chat_history": [],
        "document_context": "",
        "document_name": "",
    }

if "conversations" not in st.session_state:
    first_chat = new_conversation()
    st.session_state.conversations = [first_chat]
    st.session_state.active_chat_id = first_chat["id"]
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = st.session_state.conversations[0]["id"]
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "submitted_message" not in st.session_state:
    st.session_state.submitted_message = None


def active_conversation():
    for conversation in st.session_state.conversations:
        if conversation["id"] == st.session_state.active_chat_id:
            return conversation
    conversation = new_conversation()
    st.session_state.conversations.insert(0, conversation)
    st.session_state.active_chat_id = conversation["id"]
    return conversation


def start_new_chat():
    conversation = new_conversation()
    st.session_state.conversations.insert(0, conversation)
    st.session_state.active_chat_id = conversation["id"]
    st.session_state.page = "Home"
    st.session_state.pending_prompt = None
    st.session_state.submitted_message = None


def set_prompt(prompt):
    st.session_state.pending_prompt = prompt
    st.session_state.page = "Home"


chat = active_conversation()

# ----------------------------- Theme and assets ----------------------------
asset_path = Path(__file__).parent / "assets" / "bhutan_background.jpg"
background_css = ""
if asset_path.exists():
    encoded = base64.b64encode(asset_path.read_bytes()).decode("utf-8")
    background_css = f'''background-image: linear-gradient(180deg, rgba(8,35,54,.08) 0%, rgba(8,35,54,.26) 52%, rgba(8,35,54,.58) 100%), url("data:image/jpeg;base64,{encoded}");'''

st.markdown(
    f"""
    <style>
    :root {{ --navy:#062443; --navy2:#0b3154; --gold:#f4bd43; --ink:#102b4a; }}
    html, body, [class*="css"] {{ font-family: Georgia, 'Times New Roman', serif; }}
    .stApp {{ background:#e9eef0; color:var(--ink); }}
    [data-testid="stMain"] {{ {background_css} background-size:cover; background-position:center top; background-attachment:fixed; }}
    .block-container {{ max-width:1600px; padding:1.15rem 2rem 2.5rem; }}
    header[data-testid="stHeader"] {{ background:transparent; }}
    footer {{ visibility:hidden; }}

    /* Left navigation panel */
    section[data-testid="stSidebar"] {{
        background:linear-gradient(180deg,#031d38 0%,#062746 72%,#031a31 100%);
        border-right:2px solid rgba(244,189,67,.75);
        min-width:275px !important; max-width:275px !important;
    }}
    section[data-testid="stSidebar"] > div {{ padding:1.2rem .85rem 1rem; }}
    section[data-testid="stSidebar"] * {{ color:#f8f5ec; }}
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:#e7edf3; }}
    section[data-testid="stSidebar"] hr {{ border-color:rgba(238,192,91,.45); margin:.8rem 0; }}
    section[data-testid="stSidebar"] .stButton button {{
        width:100%; min-height:43px; text-align:left; border-radius:11px;
        border:1px solid rgba(255,255,255,.08); background:rgba(255,255,255,.055);
        color:#fff !important; font-size:15px; font-family:Georgia,serif;
        box-shadow:none; padding-left:15px;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background:rgba(244,189,67,.18); border-color:#e7b642; color:#fff !important;
    }}
    .brand {{ text-align:center; padding:8px 4px 16px; border-bottom:1px solid rgba(244,189,67,.55); margin-bottom:17px; }}
    .brand-mark {{ font-size:48px; line-height:1.1; color:#f4bd43; text-shadow:0 2px 12px rgba(244,189,67,.22); }}
    .brand-name {{ font-size:32px; font-weight:800; letter-spacing:.4px; color:#fff; line-height:1.15; }}
    .brand-name span {{ color:#f4bd43; }}
    .brand-sub {{ font-family:Arial,sans-serif; font-size:12px; color:#d8e1eb; margin-top:4px; }}
    .side-label {{ color:#f4bd43; font-family:Arial,sans-serif; font-size:11px; font-weight:700; letter-spacing:1.5px; margin:14px 0 7px; }}
    .side-quote {{ color:#f5d995; font-style:italic; text-align:center; line-height:1.55; font-size:14px; padding:10px 8px 2px; }}

    /* Language switch and welcome banner */
    .language-wrap {{ display:flex; justify-content:flex-end; margin:0 2px 5px; }}
    .hero {{
        position:relative; text-align:left; overflow:hidden; border-radius:0 0 18px 18px;
        padding:30px 30px 26px; min-height:270px; margin:0 0 17px;
        background:linear-gradient(90deg,rgba(255,247,225,.93) 0%,rgba(255,247,225,.74) 48%,rgba(255,247,225,.10) 100%),
                   linear-gradient(0deg,rgba(9,37,59,.12),rgba(9,37,59,.02));
        box-shadow:0 10px 28px rgba(8,35,54,.15); border:1px solid rgba(255,255,255,.55);
    }}
    .hero-eyebrow {{ font-family:Arial,sans-serif; color:#a77819; font-size:11px; font-weight:800; letter-spacing:2.5px; }}
    .hero-title {{ color:#092849; font-size:clamp(40px,5vw,61px); line-height:1.05; font-weight:800; margin:13px 0 2px; }}
    .hero-dzo {{ color:#092849; font-size:clamp(28px,3.2vw,40px); line-height:1.45; margin:0 0 5px; }}
    .hero-copy {{ color:#173653; font-family:Arial,sans-serif; font-size:15px; line-height:1.55; max-width:620px; margin-top:12px; }}
    .hero-rule {{ width:64px; height:3px; background:#e9b63f; margin-top:12px; border-radius:5px; }}

    /* Feature cards */
    .feature-card {{
        min-height:190px; height:100%; border-radius:19px; padding:20px 18px 17px;
        text-align:center; border:1px solid rgba(255,255,255,.9);
        box-shadow:0 10px 25px rgba(5,30,52,.18); backdrop-filter:blur(9px);
    }}
    .feature-blue {{ background:rgba(231,241,255,.94); }}
    .feature-green {{ background:rgba(226,246,237,.94); }}
    .feature-purple {{ background:rgba(241,236,255,.94); }}
    .feature-gold {{ background:rgba(255,246,222,.95); }}
    .feature-icon {{ font-family:Arial,sans-serif; font-size:36px; line-height:1.2; margin-bottom:8px; }}
    .feature-card h3 {{ color:#102b4a; font-size:19px; margin:0 0 8px; }}
    .feature-card p {{ color:#455b70; font-family:Arial,sans-serif; font-size:13px; line-height:1.55; min-height:39px; margin:0 0 10px; }}
    .feature-action {{ display:inline-block; color:#fff; font-family:Arial,sans-serif; font-size:12px; font-weight:700; border-radius:30px; padding:8px 14px; background:#123d72; }}
    .main-section-title {{ color:#fff; font-family:Arial,sans-serif; font-size:15px; font-weight:800; margin:8px 0 12px; text-shadow:0 2px 8px rgba(0,0,0,.55); }}

    /* Conversation composer and prompt area */
    .composer-panel {{ background:rgba(255,255,255,.96); border:1px solid #dbe4ed; border-radius:19px; padding:16px 18px 14px; box-shadow:0 12px 28px rgba(4,26,45,.18); margin-top:17px; }}
    .composer-heading {{ color:#102b4a; font-size:20px; font-weight:800; margin-bottom:3px; }}
    .composer-help {{ color:#64758a; font-family:Arial,sans-serif; font-size:12px; margin-bottom:10px; }}
    .suggestion-panel {{ background:rgba(255,250,237,.96); border:1px solid #ead8ad; border-radius:15px; padding:12px 15px; margin-top:12px; box-shadow:0 7px 18px rgba(4,26,45,.12); }}
    .suggestion-title {{ color:#173653; font-family:Arial,sans-serif; font-size:13px; font-weight:800; margin-bottom:8px; }}
    .stTextInput input {{ background:#fff !important; border:1px solid #cbd8e7 !important; border-radius:12px !important; color:#173653 !important; min-height:46px; }}
    .stTextInput input::placeholder {{ color:#8998a8 !important; }}
    .stButton button {{ border-radius:12px; min-height:41px; font-weight:700; border:1px solid #d3a33d; background:linear-gradient(135deg,#f6c64f,#f2b83c); color:#092849 !important; box-shadow:0 4px 12px rgba(10,35,55,.12); }}
    .stButton button:hover {{ border-color:#b8892d; background:#ffda76; color:#092849 !important; }}
    [data-testid="stChatMessage"] {{ background:rgba(255,255,255,.97); border:1px solid #dbe4ed; border-radius:15px; padding:12px 16px; box-shadow:0 5px 16px rgba(4,26,45,.12); }}
    [data-testid="stChatMessage"] p {{ color:#173653 !important; line-height:1.7; }}
    [data-testid="stFileUploader"] {{ background:rgba(255,255,255,.95); border:1px dashed #b9c9d8; border-radius:12px; padding:10px; }}
    [data-testid="stExpander"] {{ background:rgba(255,255,255,.95); border:1px solid #dbe4ed; border-radius:12px; }}
    [data-testid="stExpander"] summary {{ color:#173653 !important; font-weight:700; }}
    .footer-note {{ color:#fff; text-align:center; font-family:Arial,sans-serif; font-size:11px; padding:16px 0 2px; text-shadow:0 2px 7px rgba(0,0,0,.5); }}

    @media(max-width:900px) {{
        .block-container {{ padding:1rem .8rem 2rem; }}
        .hero {{ padding:23px 20px; min-height:230px; }}
        .feature-card {{ min-height:170px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Sidebar ------------------------------------
with st.sidebar:
    st.markdown(
        """<div class="brand">
          <div class="brand-mark">🐉</div>
          <div class="brand-name">Druk<span>AI</span></div>
          <div class="brand-sub">Dzongkha AI Chatbot</div>
        </div>""",
        unsafe_allow_html=True,
    )
    if st.button("⌂   Home", use_container_width=True, key="nav_home"):
        st.session_state.page = "Home"
        st.rerun()
    if st.button("＋   New Chat", use_container_width=True, key="nav_new"):
        start_new_chat()
        st.rerun()
    if st.button("◷   Previous Chats", use_container_width=True, key="nav_previous"):
        st.session_state.page = "Previous Chats"
        st.rerun()
    if st.button("▤   Upload Document", use_container_width=True, key="nav_upload"):
        st.session_state.page = "Upload Document"
        st.rerun()
    if st.button("⚙   Language Settings", use_container_width=True, key="nav_settings"):
        st.session_state.page = "Language Settings"
        st.rerun()

    st.markdown('<div class="side-label">RECENT CHATS</div>', unsafe_allow_html=True)
    recent = [item for item in st.session_state.conversations if item["messages"]]
    if not recent:
        st.caption("Your conversations will appear here.")
    else:
        for old in recent[:7]:
            title = old["title"]
            if len(title) > 25:
                title = title[:22] + "..."
            if st.button("◉   " + title, key=f"recent_{old['id']}", use_container_width=True):
                st.session_state.active_chat_id = old["id"]
                st.session_state.page = "Home"
                st.rerun()
    st.divider()
    st.markdown(
        '<div class="side-quote">“Knowledge brings a brighter future.”<br><br>འབྲུག་ཡུལ་ལ་ཕན་པའི་ཤེས་ཡོན།</div>',
        unsafe_allow_html=True,
    )

chat = active_conversation()

# ----------------------------- Header -------------------------------------
left, right = st.columns([5, 1.5])
with right:
    st.selectbox("Language", ["English / རྫོང་ཁ་", "English", "རྫོང་ཁ་"], label_visibility="collapsed", key="language_choice")

# ----------------------------- Pages --------------------------------------
if st.session_state.page == "Previous Chats":
    st.markdown('<div class="composer-panel"><div class="composer-heading">Previous Chats</div><div class="composer-help">Select a conversation to continue where you left off.</div></div>', unsafe_allow_html=True)
    if not recent:
        st.info("No previous conversations yet. Start a new chat to begin.")
    for old in recent:
        preview = old["messages"][-1]["content"] if old["messages"] else ""
        with st.container(border=True):
            st.markdown(f"**{old['title']}**")
            st.caption(preview[:160])
            if st.button("Open conversation", key=f"open_{old['id']}"):
                st.session_state.active_chat_id = old["id"]
                st.session_state.page = "Home"
                st.rerun()

elif st.session_state.page == "Upload Document":
    st.markdown('<div class="composer-panel"><div class="composer-heading">Upload a Document</div><div class="composer-help">Add a PDF or Word document, then ask DrukAI questions about its contents.</div></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"], key=f"page_upload_{chat['id']}")
    if uploaded is not None and chat.get("document_name") != uploaded.name:
        try:
            with st.spinner("Reading your document..."):
                chat["document_context"] = extract_document_text(uploaded)
                chat["document_name"] = uploaded.name
            st.success(f"Document ready: {uploaded.name}")
        except Exception as exc:
            chat["document_context"] = ""
            chat["document_name"] = ""
            st.error(f"Could not read the document: {exc}")
    if chat.get("document_name"):
        st.info(f"Attached: {chat['document_name']}")
        with st.expander("Preview extracted text"):
            st.text(chat["document_context"][:3000])

elif st.session_state.page == "Language Settings":
    st.markdown('<div class="composer-panel"><div class="composer-heading">Language Settings</div><div class="composer-help">DrukAI supports English and Dzongkha input and output.</div></div>', unsafe_allow_html=True)
    st.selectbox("Preferred interface language", ["English", "Dzongkha", "English and Dzongkha"], key="preferred_language")
    st.info("You can write your message in English or Dzongkha. DrukAI will respond using its translation and chat pipeline.")

else:
    # The welcome view is shown before the first message in each conversation.
    if not chat["messages"]:
        st.markdown(
            """<div class="hero">
              <div class="hero-eyebrow">འབྲུག་ཡུལ། &nbsp; · &nbsp; YOUR DZONGKHA AI ASSISTANT</div>
              <h1 class="hero-title">Kuzuzangpo La!</h1>
              <div class="hero-dzo">ཀུ་ཟུ་བཟང་པོ་ལགས།</div>
              <div class="hero-rule"></div>
              <div class="hero-copy">Welcome to DrukAI — your intelligent Dzongkha and English AI assistant.</div>
            </div>""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="main-section-title">Explore DrukAI</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.markdown('<div class="feature-card feature-blue"><div class="feature-icon">🌐</div><h3>Translation</h3><p>Translate between English and Dzongkha with ease.</p><span class="feature-action">Start Translation →</span></div>', unsafe_allow_html=True)
            if st.button("Open Translation", key="feature_translate", use_container_width=True):
                set_prompt("Please translate this sentence into Dzongkha: Hello, how are you?")
                st.rerun()
        with col2:
            st.markdown('<div class="feature-card feature-green"><div class="feature-icon">💬</div><h3>Ask DrukAI</h3><p>Get helpful answers to your questions in either language.</p><span class="feature-action">Start Chat →</span></div>', unsafe_allow_html=True)
            if st.button("Start Chat", key="feature_chat", use_container_width=True):
                set_prompt("Tell me about Bhutan.")
                st.rerun()
        with col3:
            st.markdown('<div class="feature-card feature-purple"><div class="feature-icon">📄</div><h3>Document Help</h3><p>Ask questions about your PDF or Word documents.</p><span class="feature-action">Upload Document →</span></div>', unsafe_allow_html=True)
            if st.button("Upload Document", key="feature_document", use_container_width=True):
                st.session_state.page = "Upload Document"
                st.rerun()

        st.markdown('<div class="composer-panel"><div class="composer-heading">✦ &nbsp; Start a conversation</div><div class="composer-help">Type your message below to begin chatting with DrukAI.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="composer-panel"><div class="composer-heading">Your Conversation</div><div class="composer-help">Continue chatting with DrukAI in English or Dzongkha.</div></div>', unsafe_allow_html=True)
        for item in chat["messages"]:
            with st.chat_message(item["role"]):
                st.markdown(item["content"])

    # Document status remains visible during a conversation.
    if chat.get("document_name"):
        st.caption(f"📎 Attached document: {chat['document_name']}")

    # A form keeps the message box in the same visual position as the mockup.
    with st.form(key=f"message_form_{chat['id']}", clear_on_submit=True):
        msg_col, send_col = st.columns([12, 1.2], vertical_alignment="center")
        with msg_col:
            user_text = st.text_input("Message DrukAI", placeholder="Type your message here...", label_visibility="collapsed", key=f"message_input_{chat['id']}")
        with send_col:
            send = st.form_submit_button("➤", use_container_width=True)
        if send and user_text.strip():
            st.session_state.submitted_message = user_text.strip()

    if not chat["messages"]:
        st.markdown('<div class="suggestion-panel"><div class="suggestion-title">💡 &nbsp; Suggested Prompts</div></div>', unsafe_allow_html=True)
        p1, p2, p3, p4 = st.columns(4, gap="small")
        prompts = ["Tell me about Bhutan", "Explain machine learning", "Translate this sentence", "Summarize this document"]
        for column, prompt, index in zip([p1, p2, p3, p4], prompts, range(4)):
            with column:
                if st.button(prompt, key=f"suggest_{index}", use_container_width=True):
                    st.session_state.submitted_message = prompt

# ----------------------------- Chat response ------------------------------
message = st.session_state.submitted_message
if message:
    st.session_state.submitted_message = None
    chat = active_conversation()
    chat["messages"].append({"role": "user", "content": message})
    if chat["title"] == "New conversation":
        title = message.strip().replace("\n", " ")
        chat["title"] = title[:33] + "..." if len(title) > 36 else title
    with st.spinner("DrukAI is preparing a response..."):
        try:
            answer = get_chat_response(message, chat["chat_history"], chat["document_context"])
        except Exception as exc:
            answer = (
                "Sorry, I could not complete that request. Please check that "
                "Ollama and the required models are running.\n\n"
                f"Technical details: {exc}"
            )
    chat["messages"].append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown('<div class="footer-note">DrukAI · Supporting Dzongkha communication through AI</div>', unsafe_allow_html=True)
