import streamlit as st
import os
import sys
import time
from datetime import datetime
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# --- PATH SETUP ---
# Add the CODE directory to sys.path to allow importing modules from it
current_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.join(current_dir, "CODE")
sys.path.append(code_dir)

# Load environment variables from CODE/.env
dotenv_path = os.path.join(code_dir, ".env")
load_dotenv(dotenv_path)

# Bridge for Streamlit Cloud Secrets to os.environ (Ensures 'app.utils' work in Cloud)
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass # Secrets not found (Local run), using .env instead

# Import Project Modules (Try/Except to handle if user hasn't set dependencies yet)
try:
    from app.utils.celebrity_detector import CelebrityDetector
    from app.utils.qa_engine import QAEngine
    from app.utils.image_handler import process_image
    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    IMPORT_ERROR = str(e)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Celebrity Detector & QA",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    :root {
        --primary-gold: #FFD700;
        --secondary-gold: #FFC800;
        --accent-blue: #2874f0;
        --accent-green: #2ecc71;
        --accent-pink: #e84393;
        --accent-purple: #9b59b6;
        --background-dark: #141E30; 
        --text-light: #ecf0f1; 
    }
    
    .stApp {
        background: linear-gradient(to right, #141E30, #243B55);
        color: var(--text-light);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 3px solid var(--accent-pink);
    }

    h1 { color: var(--accent-pink) !important; text-shadow: 0 0 20px rgba(232, 67, 147, 0.5); }
    h2 { color: var(--accent-blue) !important; }
    h3 { color: var(--accent-green) !important; }
    
    .stCard {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.9) 0%, rgba(37, 43, 59, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-pink) 0%, var(--accent-purple) 100%);
        color: #ffffff;
        border-radius: 25px;
        font-weight: 700;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(232, 67, 147, 0.4);
    }

    /* Chat Styling */
    .user-message {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #00d4ff 100%);
        padding: 15px; border-radius: 15px; margin: 10px 0 10px 20%; color: white;
    }
    .bot-message {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px; border-radius: 15px; margin: 10px 20% 10px 0; border: 1px solid var(--accent-green); color: white;
    }

    /* Tech Card Styling */
    .tech-card {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        cursor: default;
    }
    .tech-card:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #00d4ff;
        box-shadow: 0 10px 25px rgba(0, 212, 255, 0.2);
    }
    .tech-icon {
        font-size: 2rem;
        margin-bottom: 15px;
        display: block;
    }
    .tech-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 10px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #e84393; box-shadow: 0 4px 15px rgba(232, 67, 147, 0.3);'>
        <h2 style='margin: 0; font-size: 1.6rem; font-weight: 800;'>
            <span style='color: #FFD700;'>🌟</span> 
            <span style='background: -webkit-linear-gradient(left, #e84393, #9b59b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Celebrity</span>
            <span style='background: -webkit-linear-gradient(left, #9b59b6, #2874f0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Detector</span>
        </h2>
        <p style='background: -webkit-linear-gradient(right, #2874f0, #00e5ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.8rem; font-weight: 900; margin-top: 5px; letter-spacing: 1px;'>
            AI VISUAL INTELLIGENCE
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(155, 89, 182, 0.2) 0%, rgba(40, 116, 240, 0.2) 100%); 
                padding: 15px; border-radius: 10px; border: 2px solid rgba(155, 89, 182, 0.4);'>
        <p style='margin: 5px 0; color: #00d4ff; font-weight: 600;'>Ratnesh Kumar Singh</p>
        <p style='margin: 5px 0; font-size: 0.9rem;'>
            🔗 <a href='https://github.com/Ratnesh-181998' style='color: #2874f0; text-decoration: none;'>GitHub</a> | 
            <a href='https://www.linkedin.com/in/ratneshkumar1998/' style='color: #9b59b6; text-decoration: none;'>LinkedIn</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ℹ️ About App")
    st.info("Upload a photo to detect the celebrity and ask questions using multimodal AI.")

# --- TOP RIGHT BADGE ---
col1, col2 = st.columns([3, 1])
with col1:
    st.empty()
with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2874f0 0%, #9b59b6 100%); 
                padding: 8px 12px; border-radius: 8px; 
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
                margin-bottom: 10px;'>
        <p style='margin: 0; font-weight: 700; font-size: 0.8rem; line-height: 1.4;'>
            <span style='color: #FFD700; font-size: 0.9rem;'>Ratnesh Kumar Singh</span><br>
            <span style='color: #00e5ff;'>Data Scientist (AI/ML) | 4+ Yrs</span>
        </p>
        <div style='margin-top: 5px; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; gap: 10px;'>
            <a href='https://github.com/Ratnesh-181998' target='_blank' style='color: #ffffff; text-decoration: none; font-weight: 600; display: flex; align-items: center; gap: 4px; transition: color 0.3s;'>
                <img src="https://img.icons8.com/ios-filled/50/ffffff/github.png" width="14" height="14" style="vertical-align: middle;"> GitHub
            </a>
            <span style='color: rgba(255,255,255,0.5);'>|</span>
            <a href='https://www.linkedin.com/in/ratneshkumar1998/' target='_blank' style='color: #ffffff; text-decoration: none; font-weight: 600; display: flex; align-items: center; gap: 4px; transition: color 0.3s;'>
                <img src="https://img.icons8.com/ios-filled/50/ffffff/linkedin.png" width="14" height="14" style="vertical-align: middle;"> LinkedIn
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(232, 67, 147, 0.15) 0%, rgba(40, 116, 240, 0.15) 100%); border-radius: 15px; margin-bottom: 25px; border: 2px solid rgba(232, 67, 147, 0.4);'>
    <h1 style='margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: 1px;'>
        🌟 CELEBRITY DETECTOR & Q/A SYSTEM
    </h1>
    <p style='font-size: 1.1rem; color: #b2bec3; margin-top: 10px;'>
        Powered by <b>Groq LLaMA-4 Vision</b> & <b>OpenCV</b>
    </p>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 Demo Project", 
    "📖 About Project", 
    "🔧 Tech Stack", 
    "🏗️ Architecture", 
    "📋 System Logs"
])

# --- STATE MANAGEMENT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "detected_name" not in st.session_state:
    st.session_state.detected_name = None
if "detected_info" not in st.session_state:
    st.session_state.detected_info = None

# --- TAB 1: DEMO ---
# --- TAB 1: DEMO ---
with tab1:
    st.header("📸 Live Detection Demo")


    
    # 🌟 NEW: Instructions for better UX
    with st.expander("ℹ️ How to use this interactive demo", expanded=False):
        st.markdown("""
        1. **Upload**: Select an image of a celebrity in the left panel.
        2. **Detect**: Click the 'Detect Celebrity' button to identify them.
        3. **Chat**: Once identified, use the chat panel on the right to ask questions!
        """)
    
    if not MODULES_LOADED:
        st.error(f"Failed to load project modules. Ensure you are running this from the correct directory.\nError: {IMPORT_ERROR}")
    else:
        # Layout: Vertical Stack (Upload then Chat)
        
        # 1. Upload Section
        with st.container(border=True):
            col_header, col_ref = st.columns([4, 1])
            with col_header:
                st.markdown("### 1. Upload Image")
            with col_ref:
                if st.button("🔄 Refresh", key="refresh_upload"):
                    st.session_state.chat_history = []
                    st.session_state.detected_name = None
                    st.session_state.detected_info = None
                    st.session_state.selected_sample = None
                    st.rerun()
            
            # File Uploader
            st.markdown("<p style='color: #ff4b4b; font-weight: bold; font-size: 0.9rem;'>⚠️ Note: Please upload a clear, high-quality image of the celebrity's face. Blurry or obstructed images may lead to incorrect detection.</p>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Choose a celebrity photo...", type=["jpg", "jpeg", "png"])
            
            # Quick Samples
            st.markdown("or try a sample:")
            
            # Logic to handle sample selection
            if "selected_sample" not in st.session_state:
                st.session_state.selected_sample = None
            
            if uploaded_file:
                st.session_state.selected_sample = None

            # Load all samples dynamically
            samples_dir_path = os.path.join(current_dir, "samples")
            if os.path.exists(samples_dir_path):
                # Filter out specific celebrities from samples as requested
                sample_files = sorted([f for f in os.listdir(samples_dir_path) 
                                     if f.lower().endswith(('.jpg', '.jpeg', '.png')) 
                                     and "anushka" not in f.lower()
                                     and "melinda" not in f.lower()
                                     and "vikas" not in f.lower()
                                     and "bill" not in f.lower()
                                     and "dalai" not in f.lower()])
                
                # Scrollable container for many samples (Gallery View)
                with st.container():
                    cols = st.columns(4) # 4 columns for gallery style
                    for i, sample_file in enumerate(sample_files):
                        # Create nice name: "Angelina_Jolie.jpg" -> "Angelina Jolie"
                        nice_name = os.path.splitext(sample_file)[0].replace("_", " ")
                        
                        path_to_img = os.path.join(samples_dir_path, sample_file)
                        
                        with cols[i % 4]:
                            # Display Thumbnail
                            st.image(path_to_img, use_container_width=True)
                            # Selection Button
                            if st.button(nice_name, key=f"s_{i}", use_container_width=True):
                                st.session_state.selected_sample = f"samples/{sample_file}"
            
            # Determine Active File (Upload vs Sample)
            active_file = None
            if uploaded_file:
                active_file = uploaded_file
            elif st.session_state.selected_sample:
                sample_path = os.path.join(current_dir, st.session_state.selected_sample)
                if os.path.exists(sample_path):
                    with open(sample_path, "rb") as f:
                        active_file = BytesIO(f.read())
                        active_file.name = st.session_state.selected_sample 
            
            if active_file is not None:
                # Display Image
                image = Image.open(active_file)
                st.image(image, caption="Selected Image", use_container_width=True)
                
                # Verify Groq Key
                if not os.getenv("GROQ_API_KEY"):
                    st.warning("⚠️ GROQ_API_KEY not found in .env. Please configure it.")
                
                if st.button("🔍 Detect Celebrity", type="primary", use_container_width=True):
                    with st.spinner("Processing image and identifying face..."):
                        try:
                            # Reset pointer
                            active_file.seek(0)
                            
                            # FlaskFileAdapter
                            class FlaskFileAdapter:
                                def __init__(self, streamlit_file):
                                    self.file = streamlit_file
                                def save(self, destination):
                                    self.file.seek(0)
                                    destination.write(self.file.read())
                            
                            detector = CelebrityDetector()
                            qa = QAEngine()
                            
                            adapter = FlaskFileAdapter(active_file)
                            img_bytes, face_box = process_image(adapter)
                            
                            # Detect
                            result_text, player_name = detector.identify(img_bytes)
                            
                            st.session_state.detected_name = player_name
                            st.session_state.detected_info = result_text
                            
                            if player_name and player_name != "Unknown":
                                pass # Success is handled below persistently
                            else:
                                pass # Error is handled below persistently
                                
                        except Exception as e:
                            st.error(f"Error during detection: {str(e)}")
                
                # Persistent Display of Results (so it survives chat updates)
                if st.session_state.detected_name:
                    if st.session_state.detected_name != "Unknown":
                        st.success(f"✅ Identified: **{st.session_state.detected_name}**")
                        with st.expander("See Full Analysis", expanded=True):
                            st.markdown(st.session_state.detected_info)
                    else:
                            st.error("❌ Could not identify the person.")

        # 2. Q&A Section (Now below Upload Section)
        with st.container(border=True, height=550):
            st.markdown("### 2. Q/A SYSTEM - About Above Detected Celebrity")
            
            if st.session_state.detected_name and st.session_state.detected_name != "Unknown":
                st.info(f"Ask me anything about **{st.session_state.detected_name}**!")
                
                # Chat History Display
                chat_container = st.container(height=300)
                with chat_container:
                    if not st.session_state.chat_history:
                        st.caption("Start the conversation by asking a question below.")
                    for role, msg in st.session_state.chat_history:
                        if role == "user":
                            st.markdown(f"<div class='user-message'>👤 {msg}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='bot-message'>🤖 <b>RatneshAI:</b> {msg}</div>", unsafe_allow_html=True)
                
                # Chat Input
                # Chat Input Form (Auto-clears on submit)
                with st.form(key="qa_form", clear_on_submit=True):
                    q_input = st.text_input("Ask a question:", placeholder="e.g., Which movies are they famous for?")
                    submitted = st.form_submit_button("Send", type="primary", use_container_width=True)
                
                if submitted and q_input:
                    st.session_state.chat_history.append(("user", q_input))
                    
                    with st.spinner("Thinking..."):
                        qa_eng = QAEngine()
                        ans = qa_eng.ask_about_celebrity(st.session_state.detected_name, q_input)
                        st.session_state.chat_history.append(("ai", ans))
                    
                    st.rerun()
                
                # Clear Chat Button (Now below the input)
                if st.button("🗑️ Clear Chat History", key="clear_chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            else:
                st.markdown("""
                <div style='padding: 40px; background: rgba(255,255,255,0.05); border-radius: 10px; text-align: center; color: #aaa;'>
                    <p style='font-size: 3rem; margin-bottom: 10px;'>📸</p>
                    <p>Upload and detect a celebrity first<br>to start chatting!</p>
                </div>
                """, unsafe_allow_html=True)

# --- TAB 2: ABOUT ---
with tab2:
    st.header("📖 About The Project")

    # --- Section 1: Overview & Demo (Vertical Layout) ---
    
    # 1. Project Summary
    st.info("💡 **Project Summary**: This system uses a **Vision Transformer** for celebrity detection, **Groq’s multimodal LLM** for contextual Q&A, **Flask** for backend orchestration, **OpenCV** for image preprocessing, and is deployed on **GKE** using **Docker** and **CircleCI**-based CI/CD pipelines.")

    st.write("") # Spacer

    # 2. Display Demo Image
    demo_img_path = os.path.join(current_dir, "Demo1.png")
    if os.path.exists(demo_img_path):
        st.image(demo_img_path, caption="Project Demo Preview", use_container_width=True)
    else:
        st.warning("Demo image not found.")

    st.write("") # Spacer
    
    # 3. Tech Stack & Tools
    st.markdown("### 🛠️ Tech Stack & Tools")
    st.subheader("", divider="rainbow")
    
    # Badges/Tags style
    tags = [
        "Google Cloud", "Kubernetes", "CircleCI", "Flask", "Python", 
        "HTML", "CSS", "Groq", "Vision Transformers"
    ]
    
    # Display tags in a flexible grid
    tag_html = ""
    for tag in tags:
        tag_html += f"<span style='display:inline-block; padding:5px 10px; margin:5px; border-radius:15px; background-color:#262730; border:1px solid #4B4B4B; font-size:0.9em;'>{tag}</span>"
    st.markdown(tag_html, unsafe_allow_html=True)

    st.write("") # Spacer

    # --- Section 2: Interactive Details ---
    st.subheader("🔍 Explore Project Details")
    st.markdown("---")

    # 1. Working Mechanism
    st.markdown("### 🚀 Step-by-Step Working Mechanism")
    
    with st.container(border=True):
        st.markdown("""
        **Step 1️⃣: User Interaction (Frontend)**
        *   User uploads a celebrity photo and asks a question (e.g., "Who is this?").
        *   **Frontend sends:** Image → Backend | Question → Backend API
        """)
    
    with st.container(border=True):
        st.markdown("""
        **Step 2️⃣: Flask Backend Receives Request**
        *   Flask acts as the API layer, validating inputs and routing requests.
        *   **Responsibilities:** Input validation, Request routing, Response formatting.
        """)
        
    with st.container(border=True):
        st.markdown("""
        **Step 3️⃣: Image Preprocessing (OpenCV)**
        *   OpenCV resizes, converts formats, and normalizes the image.
        *   **Output:** Clean, optimized image tensor ready for ML inference.
        """)
        
    with st.container(border=True):
        st.markdown("""
        **Step 4️⃣: Celebrity Detection (Vision Transformer)**
        *   Model extracts embeddings and matches against known celebrity representations.
        *   **Output:** Detected Celebrity Name & Confidence Score.
        """)
        
    with st.container(border=True):
        st.markdown("""
        **Step 5️⃣: Multimodal Q/A using Groq LLM**
        *   Combines **Detected Celebrity** + **User's Question**.
        *   **Groq (LLaMA-4 Vision)** performs multimodal reasoning.
        *   **Example Output:** "This is Shah Rukh Khan, a renowned Indian actor..."
        """)
        
    with st.container(border=True):
        st.markdown("""
        **Step 6️⃣: Response Returned**
        *   Flask sends the final response to the UI.
        *   **End-user** gets real-time AI-powered insights.
        """)

    st.write("")
    st.markdown("---")

    # 2. Logical Architecture
    st.markdown("### 🏗️ Logical Architecture Flow")
    st.code("""
[ User Browser ]
       |
       v
[ HTML / CSS UI ]
       |
       v
[ Flask API Layer ]
       |
       v
[ OpenCV Image Processing ]
       |
       v
[ Vision Transformer ]
       |
       v
[ Groq LLM (LLaMA-4 Vision) ]
       |
       v
[ Answer Generated ]
       |
       v
[ Response to UI ]
    """, language="text")

    st.write("")
    st.markdown("---")

    # 3. CI/CD & Deployment
    st.markdown("### 🔄 CI/CD & Cloud Deployment")
    
    c_ci1, c_ci2 = st.columns(2)
    
    with c_ci1:
        st.markdown("**Step 1️⃣ Code Versioning**\n* All code maintained in GitHub (Backend, ML, Dockerfile, K8s manifests).")
        st.markdown("**Step 2️⃣ CI/CD Pipeline (CircleCI)**\n* Triggers on push, runs tests, builds Docker image.")
        st.markdown("**Step 3️⃣ Containerization (Docker)**\n* Application packaged for consistency and scaling.")
        
    with c_ci2:
        st.markdown("**Step 4️⃣ Image Storage (GAR)**\n* Docker image pushed to Google Cloud Artifact Registry.")
        st.markdown("**Step 5️⃣ Kubernetes Deployment (GKE)**\n* GKE pulls image, creates pods, exposes service.")
        st.markdown("**Step 6️⃣ Production Access**\n* Accessed via LoadBalancer / Ingress.")
        
    st.markdown("#### ☁️ Cloud Architecture Diagram")
    st.code("""
[ Developer ] -> [ GitHub Repository ] -> [ CircleCI Pipeline ] -> [ Docker Build ] 
                                                                        |
                                                                        v
    [ Live AI Application ] < [ Google Kubernetes Engine ] < [ GCP Artifact Registry ]
    """, language="text")



# --- TAB 3: TECH STACK ---
with tab3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(155, 89, 182, 0.1) 100%); 
                padding: 30px; border-radius: 15px; border-bottom: 4px solid #00d4ff; margin-bottom: 20px;'>
        <h2 style='color: #00d4ff; margin: 0 0 10px 0;'>🛠️ The Technology Stack</h2>
        <p style='color: #e2e8f0; font-size: 1.1rem; line-height: 1.6;'>
            Built using state-of-the-art **Vision ML**, **LLMs**, and **Containerized DevOps Pipelines**.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Use Sub-tabs for better interactivity
    tech_tabs = st.tabs(["� Overview", "🧠 Intelligence Layer", "💻 Frontend & Backend", "☁️ DevOps & Cloud"])

    # --- DEFINITIONS OF CONTENT ---
    def show_ai_core():
        with st.container(border=True):
            st.markdown("### 🧠 AI Core")
            st.markdown("**Intelligence & Processing**")
            st.markdown("""
            *   **Groq LPU**: Ultra-Fast LLM Inference.
            *   **LLaMA-4 Vision**: Multimodal Reasoning (Image + Text).
            *   **OpenCV**: Real-time Image Processing & Face Detection.
            """)
            st.caption("Status: Active 🟢")

    def show_app_layer():
        with st.container(border=True):
            st.markdown("### 💻 Application")
            st.markdown("**Full Stack Framework**")
            st.markdown("""
            *   **Streamlit**: Reactive Frontend UI.
            *   **Flask**: Backend API Layer.
            *   **Python 3.11**: Core Runtime Environment.
            """)
            st.caption("Status: Active 🟢")

    def show_devops():
        with st.container(border=True):
            st.markdown("### ☁️ DevOps & Cloud")
            st.markdown("**Infrastructure & CI/CD**")
            st.markdown("""
            *   **Docker**: Containerization.
            *   **Kubernetes (GKE)**: Scalable Deployment.
            *   **CircleCI**: CI/CD Pipeline Automation.
            """)
            st.caption("Status: Active 🟢")

    # --- TAB CONTENT ---
    with tech_tabs[0]: # Overview
        st.write("### Full Stack Snapshot")
        c1, c2, c3 = st.columns(3)
        with c1: show_ai_core()
        with c2: show_app_layer()
        with c3: show_devops()

    with tech_tabs[1]: # Intelligence
        st.info("The brain of the system, handling visual perception and reasoning.")
        c_main, c_det = st.columns([2, 1])
        with c_main: show_ai_core()
        with c_det:
            st.markdown("#### Key Capability")
            st.success("**Multimodal Analysis**\nCombining pixel data with language understanding.")

    with tech_tabs[2]: # App Layer
        st.info("The user interface and orchestration layer.")
        c_main, c_det = st.columns([2, 1])
        with c_main: show_app_layer()
        with c_det:
             st.markdown("#### Key Capability")
             st.success("**Reactive UI**\nInstant feedback loops for user interactions.")

    with tech_tabs[3]: # DevOps
        st.info("The infrastructure ensuring reliability and scale.")
        c_main, c_det = st.columns([2, 1])
        with c_main: show_devops()
        with c_det:
             st.markdown("#### Key Capability")
             st.success("**Auto-Scaling**\nKubernetes handles load balancing automatically.")

    # Shared Footer Details
    st.markdown("---")
    with st.expander("📚 Advanced Component Details", expanded=False):
        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.info("**Groq LLaMA-4 Vision**\nProvides state-of-the-art multimodal understanding, allowing the system to 'see' the celebrity and reason about their identity.")
            st.warning("**OpenCV**\nHandles low-level image operations like resizing, color conversion, and face bounding box detection.")
        with c_ex2:
            st.success("**Google Kubernetes Engine (GKE)**\nEnsures the application is highly available and can scale to handle thousands of requests.")

# --- TAB 4: ARCHITECTURE ---
with tab4:
    st.header("🏗️ System Architecture")

    # --- 1. High-Level Diagrams ---
    st.subheader("📊 High-Level Diagrams", divider="gray")
    
    # Try finding the image
    img_name = "Celebrity+Detector+QA+Workflow.png"
    # Ensure we look in the current directory (Local) where the script is running
    img_path_local = os.path.join(current_dir, img_name)
    
    final_path = None
    if os.path.exists(img_path_local):
        final_path = img_path_local
    else:
        # Fallback check
        img_path_root = os.path.join(current_dir, "..", "Local", img_name)
        if os.path.exists(img_path_root):
            final_path = img_path_root
        
    if final_path:
        st.image(final_path, caption="Architecture Diagram", use_container_width=True)
    else:
        st.error(f"Architecture diagram not found at: {img_path_local}")
    
    st.info("""
    **Core Workflow Steps:**
    1. **User** uploads image via UI.
    2. **OpenCV** processes the image (resizing, face detection).
    3. **Vision Model** extracts embeddings from the face.
    4. **Groq LLM** identifies the person and provides context.
    5. **QA Engine** answers follow-up questions using the identity context.
    """)

    st.write("")
    st.markdown("---")

    # --- 2. Interactive Flow ---
    st.subheader("⚡ Interactive Flow", divider="gray")
    st.caption("The journey of your data from upload to response.")
    
    st.graphviz_chart("""
    digraph L {
        rankdir=LR;
        graph [nodesep=0.5, ranksep=0.5];
        node [shape=box, style=rounded, fontname="Arial", fontsize=20, height=2.0, fontcolor="black"];
        edge [fontsize=14, fontname="Arial", fontcolor="black"];
        
        A [label="User / Browser", style="filled,rounded", fillcolor="#ffccff"];
        B [label="Streamlit UI", shape=rect];
        C [label="Flask API", shape=diamond];
        D [label="OpenCV"];
        E [label="Vision Transformer"];
        F [label="Groq Multimodal LLM", style="filled,rounded", fillcolor="#ccccff"];
        
        A -> B [label="Uploads Image"];
        B -> C [label="Sends Request"];
        C -> D [label="Process Image"];
        D -> E [label="Normalized Tensor"];
        E -> F [label="Identity Embeddings"];
        F -> B [label="Contextual Response"];
        B -> A [label="Shows Result"];
    }
    """, use_container_width=True)

    st.write("")
    st.markdown("---")

    # --- 3. Detailed HLD & LLD ---
    st.markdown("### 📑 Detailed HLD & LLD")
    
    st.subheader("🔹 High-Level Design (HLD)", divider="gray")
    with st.expander("1️⃣ System Overview", expanded=True):
        st.write("The system allows users to upload an image of a celebrity and ask natural language questions.")
        st.write("It uses computer vision and a multimodal LLM to detect the celebrity and generate contextual answers.")
        st.write("The application is cloud-deployed, containerized, and CI/CD enabled.")

    with st.expander("2️⃣ High-Level Architecture & Components"):
        st.markdown("""
        **Architecture Flow:**
        User → Frontend (HTML/CSS) → Backend API (Flask) → AI Inference Layer (OpenCV, Vision Transformer, Groq LLM) → Response
        
        **Major Components:**
        *   **A. Frontend**: Image upload, Question input, AI response display.
        *   **B. Backend (Flask)**: Request handling, Routing, ML pipeline orchestration.
        *   **C. AI Layer**: Image preprocessing, Celebrity detection, Question answering.
        *   **D. Infrastructure**: Docker, CircleCI, GCP Artifact Registry, GKE.
        """)
        
    with st.expander("3️⃣ Deployment Flow & Design Decisions"):
        st.write("**Flow:** Developer → GitHub → CircleCI → Docker → GCP Artifact Registry → GKE → Users")
        st.write("**Key Decisions:**")
        st.write("*   Stateless backend for scalability.")
        st.write("*   Microservice-ready architecture.")
        st.write("*   Managed Kubernetes (GKE) for reliability.")
        st.write("*   LLM offloaded to Groq for low latency.")

    st.subheader("🔹 Low-Level Design (LLD)", divider="gray")
    
    with st.expander("1️⃣ Backend API & Structure"):
        st.markdown("#### API Endpoint: `POST /analyze`")
        st.json({
            "request": {"image": "uploaded_image.jpg", "question": "Who is this?"},
            "response": {"celebrity": "Name", "answer": "AI generated response"}
        })
        st.markdown("#### Flask Structure")
        st.code("""
app/
├── app.py              # Entry point
├── routes.py           # API routes
├── image_handler.py    # Upload val.
├── preprocessing.py    # OpenCV logic
├── detector.py         # Vision Transformer
├── qa_engine.py        # Groq logic
└── utils.py            # Helpers
        """, language="text")

    with st.expander("2️⃣ Logic Flows (Image, Detection, Q/A)"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Image Processing**")
            st.write("1. Receive image")
            st.write("2. Validate type/size")
            st.write("3. Resize & Normalize")
            st.write("4. Convert format")
        with c2:
            st.markdown("**Celebrity Detection**")
            st.write("1. Input processed img")
            st.write("2. Generate embeddings")
            st.write("3. Compare w/ knowns")
            st.write("4. Select match")
        with c3:
            st.markdown("**Q/A Engine**")
            st.write("1. Combine Name+Query")
            st.write("2. Create Prompt")
            st.write("3. Send to Groq")
            st.write("4. Return Answer")

    with st.expander("3️⃣ Infrastructure Details (Docker, K8s, CI/CD)"):
        st.markdown("""
        **Docker**: Single Dockerfile packaging Flask + ML dependencies.
        **Kubernetes**: Multiple replicas, Service exposing API, Auto-scaling ready.
        **CI/CD**: GitHub push → CircleCI trigger → Build Docker → Push to GAR → Deploy to GKE.
        """)
        
    st.success("**Summary**: " + "At a high level, this is a cloud-native AI system where a Flask API orchestrates image preprocessing, celebrity detection using Vision Transformers, and multimodal Q&A using Groq LLM, deployed on GKE with Docker and CI/CD via CircleCI.")

    st.write("")
    st.markdown("---")

    # --- 4. Workflow Phases ---
    st.subheader("🔄 Workflow Phases", divider="gray")
    
    c_phases = st.columns(2)
    with c_phases[0]:
        with st.container(border=True):
            st.markdown("#### 1️⃣ Development Phase")
            st.caption("Local environment setup")
            st.write("*   **Code**: Python, Flask, HTML/CSS")
            st.write("*   **Tools**: VS Code, Git")
            st.write("*   **Logic**: Image Preprocessing & Model Integration")
            
    with c_phases[1]:
        with st.container(border=True):
            st.markdown("#### 2️⃣ Containerization Phase")
            st.caption("Packaging for scale")
            st.write("*   **Docker**: Creating isolated images")
            st.write("*   **Artifact Registry**: Storing versioned images")
            st.write("*   **Reproducibility**: Ensures same behavior everywhere")

    st.write("")
    c_phases_2 = st.columns(2)
    with c_phases_2[0]:
            with st.container(border=True):
                st.markdown("#### 3️⃣ CI/CD Phase")
                st.caption("Automated Pipelines")
                st.write("*   **GitHub**: Source Control")
                st.write("*   **CircleCI**: Build, Test, Push")
                st.write("*   **Trigger**: Automatic deployment on push")
            
    with c_phases_2[1]:
            with st.container(border=True):
                st.markdown("#### 4️⃣ Production Phase")
                st.caption("Live Deployment")
                st.write("*   **GKE**: Google Kubernetes Engine")
                st.write("*   **LoadBalancer**: Traffic management")
                st.write("*   **Scaling**: Auto-scaling pods based on load")

# --- TAB 5: SYSTEM LOGS ---
# --- TAB 5: SYSTEM LOGS ---
with tab5:
    st.header("📋 System Logs")
    st.markdown("Monitor the internal state, debug information, and execution logs of the Celebrity Detector System.")

    # --- 1. Construct Live Logs (Preserving Mandatory Text) ---
    log_lines = []
    
    # Static startup logs
    log_lines.append({"content": "SYSTEM STARTUP: Initializing Application...", "level": "INFO"})
    log_lines.append({"content": f"TIME: {datetime.now()} IST", "level": "INFO"})
    
    # Module status logs
    if MODULES_LOADED:
        log_lines.append({"content": "MODULE LOAD: app.utils.celebrity_detector [OK]", "level": "SUCCESS"})
        log_lines.append({"content": "MODULE LOAD: app.utils.qa_engine [OK]", "level": "SUCCESS"})
    else:
        log_lines.append({"content": f"MODULE LOAD FAILED: {IMPORT_ERROR}", "level": "ERROR"})
        
    # Runtime action logs
    if st.session_state.detected_name:
        log_lines.append({"content": f"ACTION: Detection performed. Result: {st.session_state.detected_name}", "level": "SUCCESS"})
    
    if st.session_state.chat_history:
        log_lines.append({"content": f"ACTION: Chat session active. Messages count: {len(st.session_state.chat_history)}", "level": "INFO"})

    # --- 2. Calculate Metrics ---
    info_count = sum(1 for l in log_lines if l["level"] == "INFO")
    success_count = sum(1 for l in log_lines if l["level"] == "SUCCESS")
    error_count = sum(1 for l in log_lines if l["level"] == "ERROR")
    warning_count = sum(1 for l in log_lines if l["level"] == "WARNING")
    
    total_info = info_count + success_count # Group success with info for broader category if needed, or keep separate

    # --- 3. Refresh Control ---
    col_refresh, col_spacer = st.columns([1, 4])
    with col_refresh:
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.rerun()

    st.markdown("---")

    # --- 4. Premium Metrics Dashboard (Flipkart Style) ---
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f"""
        <div style='background: rgba(46, 204, 113, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; text-align: center;'>
            <h4 style='color: #e8e8e8; margin: 0; font-size: 0.9rem;'>INFO / SUCCESS</h4>
            <p style='color: #2ecc71; font-size: 1.8rem; font-weight: bold; margin: 5px 0;'>{total_info}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        err_color = "#e74c3c" if error_count > 0 else "#95a5a6"
        st.markdown(f"""
        <div style='background: rgba(231, 76, 60, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid {err_color}; text-align: center;'>
            <h4 style='color: #e8e8e8; margin: 0; font-size: 0.9rem;'>ERRORS</h4>
            <p style='color: {err_color}; font-size: 1.8rem; font-weight: bold; margin: 5px 0;'>{error_count}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        warn_color = "#f39c12" if warning_count > 0 else "#95a5a6"
        st.markdown(f"""
        <div style='background: rgba(243, 156, 18, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid {warn_color}; text-align: center;'>
            <h4 style='color: #e8e8e8; margin: 0; font-size: 0.9rem;'>WARNINGS</h4>
            <p style='color: {warn_color}; font-size: 1.8rem; font-weight: bold; margin: 5px 0;'>{warning_count}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 5. Filters & Download ---
    c_filter, c_down = st.columns([3, 1])
    with c_filter:
        level_filter = st.multiselect(
            "🔽 Filter Logs by Level", 
            ["INFO", "SUCCESS", "WARNING", "ERROR"], 
            default=["INFO", "SUCCESS", "WARNING", "ERROR"]
        )
    
    with c_down:
         st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True) 
         log_text = "\n".join([f"[{l['level']}] {l['content']}" for l in log_lines])
         st.download_button(
            label="📥 Download",
            data=log_text,
            file_name=f"system_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --- 6. Styled Log Feed ---
    st.markdown("### 📜 Log Feed")
    log_container = st.container(height=500, border=True)
    
    with log_container:
        if log_lines:
            # Display in reverse order (newest top) or standard?
            # Reference app uses reversed(log_lines), so we will too.
            for log in reversed(log_lines):
                if log['level'] in level_filter:
                    msg = log['content']
                    if log['level'] == 'ERROR':
                        st.error(msg, icon="🚨")
                    elif log['level'] == 'WARNING':
                        st.warning(msg, icon="⚠️")
                    elif log['level'] == 'SUCCESS':
                        st.success(msg, icon="✅")
                    else:
                        st.info(msg, icon="ℹ️")
        else:
            st.info("📭 Log stream is empty.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px 20px 10px 20px; background: linear-gradient(135deg, rgba(40, 116, 240, 0.15) 0%, rgba(155, 89, 182, 0.15) 100%); border-radius: 10px; border-top: 2px solid #2874f0;'>
    <p style='color: #00d4ff; font-weight: 600; font-size: 1.1rem; margin-bottom: 10px;'>🤖 Celebrity Detector & QA System</p>
    <p style='color: #00d4ff; font-weight: 600; font-size: 1.1rem; margin-bottom: 10px;'>Built with ❤️ by Ratnesh Kumar Singh | Data Scientist (AI/ML Engineer 4+Years Exp)</p>
    <p style='font-size: 0.9rem; color: #e8e8e8; margin-bottom: 5px;'>Powered by Groq, LLaMA-4 Vision, OpenCV, and Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Social links
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col2:
    st.markdown('<p style="text-align: center; margin: 0;"><a href="https://github.com/Ratnesh-181998" target="_blank" style="text-decoration: none; color: #2874f0; font-size: 1.1rem; font-weight: 600;">🔗 GitHub</a></p>', unsafe_allow_html=True)

with col3:
    st.markdown('<p style="text-align: center; margin: 0;"><a href="mailto:rattudacsit2021gate@gmail.com" style="text-decoration: none; color: #26a65b; font-size: 1.1rem; font-weight: 600;">📧 Email</a></p>', unsafe_allow_html=True)

with col4:
    st.markdown('<p style="text-align: center; margin: 0;"><a href="https://www.linkedin.com/in/ratneshkumar1998/" target="_blank" style="text-decoration: none; color: #0077b5; font-size: 1.1rem; font-weight: 600;">💼 LinkedIn</a></p>', unsafe_allow_html=True)

# Close the visual footer
st.markdown("""
<div style='height: 10px; background: linear-gradient(135deg, rgba(40, 116, 240, 0.15) 0%, rgba(155, 89, 182, 0.15) 100%); border-radius: 0 0 10px 10px; border-bottom: 2px solid #2874f0; margin-top: -10px;'></div>
""", unsafe_allow_html=True)
