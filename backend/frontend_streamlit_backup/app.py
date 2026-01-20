import streamlit as st
import requests
import os

# Constants
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CoverCraft AI", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Custom CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found: {file_name}")

# Try loading from the same directory or relative to execution
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
local_css(css_path)

# Session State for Auth and IDs
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "resume_id" not in st.session_state:
    st.session_state.resume_id = None
if "jd_id" not in st.session_state:
    st.session_state.jd_id = None

# Authentication Functions
def login(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state.access_token = response.json()["access_token"]
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Connection error: {e}")

def register(email, password, first_name, last_name):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email, 
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        })
        if response.status_code == 200:
            st.success("Registration successful! Please login.")
            return True
        else:
            st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

# --- Views ---

def show_login_page():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">CoverCraft AI</h1>
        <p class="hero-subtitle">Create a professional, tailored cover letter in minutes with our AI-powered builder.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.container(border=True):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Access Dashboard", type="primary", use_container_width=True):
                login(email, password)
        
        with tab2:
            with st.container(border=True):
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    new_first_name = st.text_input("First Name", key="reg_fn")
                with col_r2:
                    new_last_name = st.text_input("Last Name", key="reg_ln")
                
                new_email = st.text_input("Email", key="reg_email")
                new_password = st.text_input("Password", type="password", key="reg_pass")
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if new_first_name and new_last_name and new_email and new_password:
                    if register(new_email, new_password, new_first_name, new_last_name):
                        st.balloons()
                else:
                    st.error("Please fill in all fields")

def show_dashboard():
    # Top Bar
    col_logo, col_user = st.columns([6, 1])
    with col_logo:
        st.title("🚀 CoverCraft AI")
    with col_user:
        if st.button("Logout", type="secondary"):
            st.session_state.access_token = None
            st.session_state.resume_id = None
            st.session_state.jd_id = None
            st.rerun()
    
    st.divider()
    
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    
    # Grid Layout for Inputs
    col_resume, col_jd = st.columns(2)
    
    # 1. Resume Section
    with col_resume:
        with st.container(border=True):
            st.markdown('<h3><span class="step-indicator">1</span> Upload Resume</h3>', unsafe_allow_html=True)
            st.markdown("Upload your current resume to let us know your skills and experience.")
            uploaded_file = st.file_uploader("Upload PDF/DOCX", type=['pdf', 'docx', 'txt'])
            
            if uploaded_file is not None:
                if st.button("Process Resume", use_container_width=True):
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    try:
                        with st.spinner("Analyzing your profile..."):
                            response = requests.post(f"{BASE_URL}/api/upload-resume", files=files, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.resume_id = data["resume_id"]
                            st.success("Resume processed!")
                            with st.expander("View Extracted Details"):
                                st.json(data)
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # 2. JD Section
    with col_jd:
        with st.container(border=True):
            st.markdown('<h3><span class="step-indicator">2</span> Job Description</h3>', unsafe_allow_html=True)
            st.markdown("Paste the job description you are applying for.")
            jd_text = st.text_area("Job Description", height=200, label_visibility="collapsed", placeholder="Paste JD content here...")
            
            if st.button("Analyze Job Description", use_container_width=True):
                if jd_text:
                    try:
                        with st.spinner("Extracting requirements..."):
                            response = requests.post(f"{BASE_URL}/api/submit-jd", params={"jd_text": jd_text}, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.jd_id = data["jd_id"]
                            st.success("JD Processed!")
                            with st.expander("View Key Skills"):
                                st.json(data)
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please enter a job description.")

    # 3. Generation Section
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True) # Spacer
    
    st.markdown('<h3><span class="step-indicator">3</span> Generate Cover Letter</h3>', unsafe_allow_html=True)
    
    with st.container(border=True):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            tone = st.selectbox("Tone", ["Formal", "Enthusiastic", "Professional", "Creative"])
        with c2:
            focus = st.selectbox("Focus Area", ["Skills Match", "Key Achievements", "Company Culture", "General Overview"])
        with c3:
            st.write("") 
            st.write("")
            # Spacing to align button with inputs
            generate_disabled = not (st.session_state.resume_id and st.session_state.jd_id)
            if st.button("✨ Generate Letter", type="primary", disabled=generate_disabled, use_container_width=True):
                payload = {
                    "resume_id": st.session_state.resume_id,
                    "jd_id": st.session_state.jd_id,
                    "tone": tone.lower(),
                    "focus": focus.lower().split()[0] # simplified mapping
                }
                
                try:
                    with st.spinner("Drafting your cover letter..."):
                        response = requests.post(f"{BASE_URL}/api/generate-cover-letter", json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.generated_result = result # Save to session
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

        if generate_disabled:
            if not st.session_state.resume_id:
                st.info("👆 Please upload your resume first.")
            elif not st.session_state.jd_id:
                st.info("👆 Please submit the job description.")
            
    # Results Display
    if "generated_result" in st.session_state:
        result = st.session_state.generated_result
        st.markdown("### 🎉 Your Cover Letter is Ready!")
        
        res_col1, res_col2 = st.columns([2, 1])
        
        with res_col1:
            st.text_area("Edit & Copy", value=result.get("cover_letter", ""), height=500)
            st.caption("You can edit the text above before copying.")
        
        with res_col2:
            with st.container(border=True):
                st.metric("Match Score", f"{result.get('match_score', 0):.2f}")
                st.progress(min(result.get('match_score', 0)/100, 1.0))
                
                st.markdown("**Keyword Coverage:**")
                st.write(result.get("keyword_coverage", "N/A"))
                
                st.divider()
                st.download_button(
                    "Download as Text",
                    data=result.get("cover_letter", ""),
                    file_name="cover_letter.txt",
                    mime="text/plain",
                    use_container_width=True
                )


# Main Router
if not st.session_state.access_token:
    show_login_page()
else:
    show_dashboard()

