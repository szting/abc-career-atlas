import streamlit as st
from utils.auth_manager import AuthManager
import yaml

# Page configuration
st.set_page_config(
    page_title="Career Atlas",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Show login page if not authenticated
if not st.session_state.get('authenticated', False):
    st.title("🧭 Career Atlas")
    st.subheader("Login to Continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                result = AuthManager.login(username, password)
                if result['authenticated']:
                    # Store user info in session state
                    st.session_state.update(result)
                    st.success(f"Welcome, {result['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.divider()
        
        # Show demo credentials
        st.info("""
        **Demo Credentials:**
        - Username: `demo` / Password: `demo123` (for testing)
        - Username: `admin` / Password: `admin123` (for admin access)
        """)

else:
    # User is authenticated - show main app
    # Sidebar
    with st.sidebar:
        st.write(f"Welcome *{st.session_state['name']}*")
        
        # Show role badge
        if st.session_state['role'] == 'admin':
            st.success("🔐 Admin Access")
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            AuthManager.logout()
            st.rerun()
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Go to",
            ["Welcome", "Assessment", "Results"],
            label_visibility="collapsed"
        )
    
    # Page routing
    if page == "Welcome":
        from pages.welcome import show_welcome
        show_welcome()
    elif page == "Assessment":
        from pages.assessment import show_assessment
        show_assessment()
    elif page == "Results":
        from pages.results import show_results
        show_results()
