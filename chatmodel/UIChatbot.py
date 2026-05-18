from dotenv import load_dotenv
import streamlit as st
from gtts import gTTS
import tempfile

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from streamlit_mic_recorder import speech_to_text

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Mood Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
    color:white;
}

/* Hide Streamlit Branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Main Title */
.main-title{
    text-align:center;
    font-size:60px;
    font-weight:800;
    color:white;
    margin-top:20px;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:20px;
    margin-bottom:20px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: rgba(255,255,255,0.05);
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Mode Card */
.mode-card{
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:15px;
    margin-bottom:15px;
    border:1px solid rgba(255,255,255,0.08);
}

/* User Message */
.user-message{
    background: linear-gradient(135deg,#2563eb,#3b82f6);
    padding:15px;
    border-radius:18px 18px 4px 18px;
    margin-left:auto;
    margin-top:10px;
    margin-bottom:10px;
    width:fit-content;
    max-width:75%;
    color:white;
    font-size:16px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.3);
}

/* Bot Message */
.bot-message{
    background: linear-gradient(135deg,#10b981,#059669);
    padding:15px;
    border-radius:18px 18px 18px 4px;
    margin-right:auto;
    margin-top:10px;
    margin-bottom:10px;
    width:fit-content;
    max-width:75%;
    color:white;
    font-size:16px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.3);
}

/* Chat Input */
.stChatInput{
    position:fixed;
    bottom:15px;
    left:58%;
    transform:translateX(-50%);
    width:60%;
}

.stChatInput input{
    background: rgba(255,255,255,0.08)!important;
    color:white!important;
    border-radius:20px!important;
    padding:20px!important;
    border:1px solid rgba(255,255,255,0.08)!important;
}

/* Radio Buttons */
div[role="radiogroup"]{
    gap:10px;
}

div[role="radiogroup"] label{
    background: rgba(255,255,255,0.06);
    padding:12px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.08);
}

/* Voice Section */
.voice-box{
    margin-top:20px;
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:15px;
}

/* Animation */
.user-message,
.bot-message{
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(10px);
    }

    to{
        opacity:1;
        transform:translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="main-title">
        🤖 AI Mood Chatbot
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
        Chat with Angry 😡, Funny 😂 or Sad 😔 AI
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.markdown("## 🎭 Choose AI Mode")

    st.markdown("""
    <div class="mode-card">
        <h4>Available Modes</h4>

        <p>😡 Angry AI</p>
        <p>😂 Funny AI</p>
        <p>😔 Sad AI</p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # CHOICE SELECTOR
    # =========================
    choice = st.selectbox(
        "Select Your Mode",
        (
            "😡 Angry Mode",
            "😂 Funny Mode",
            "😔 Sad Mode"
        )
    )

    st.markdown("---")

    st.markdown("""
    <div class="voice-box">
        <h4>🎤 Voice Assistant</h4>
        <p>Use microphone to talk with AI.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SYSTEM PROMPT
# =========================
if choice == "😡 Angry Mode":

    made = (
        "You are an angry AI agent. "
        "You respond aggressively and impatiently."
    )

elif choice == "😂 Funny Mode":

    made = (
        "You are a funny AI agent."
    )

else:

    made = (
        "You are a sad AI agent. "
        "Respond emotionally and sadly."
    )

# =========================
# MODEL
# =========================
model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_mode" not in st.session_state:
    st.session_state.current_mode = choice

# RESET CHAT WHEN MODE CHANGES
if st.session_state.current_mode != choice:

    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.current_mode = choice

# SYSTEM MESSAGE
if len(st.session_state.messages) == 0:

    st.session_state.messages.append(
        SystemMessage(content=made)
    )

# =========================
# SHOW CHAT HISTORY
# =========================
for sender, message in st.session_state.chat_history:

    if sender == "You":

        st.markdown(
            f"""
            <div class="user-message">
                <b>🧑 You</b><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-message">
                <b>🤖 AI</b><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# VOICE INPUT
# =========================
voice_text = speech_to_text(
    language="en",
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True,
    use_container_width=True,
    key='voice'
)

# =========================
# TEXT INPUT
# =========================
text_prompt = st.chat_input(
    "Type your message..."
)

prompt = None

# PRIORITY
if voice_text:
    prompt = voice_text

if text_prompt:
    prompt = text_prompt

# =========================
# GENERATE RESPONSE
# =========================
if prompt:

    # USER MESSAGE
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    st.session_state.chat_history.append(
        ("You", prompt)
    )

    # AI RESPONSE
    response = model.invoke(
        st.session_state.messages
    )

    ai_reply = response.content

    # SAVE AI MESSAGE
    st.session_state.messages.append(
        AIMessage(content=ai_reply)
    )

    st.session_state.chat_history.append(
        ("Bot", ai_reply)
    )

    # =========================
    # TEXT TO SPEECH
    # =========================
    tts = gTTS(ai_reply)

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as fp:

        tts.save(fp.name)

        audio_file = open(fp.name, "rb")
        audio_bytes = audio_file.read()

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

    st.rerun()