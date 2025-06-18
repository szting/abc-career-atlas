import streamlit as st
import streamlit_authenticator as stauth
from utils.auth_manager import AuthManager
from utils.data_manager import DataManager
from utils.llm_manager import LLMManager
import yaml
from yaml.loader import SafeLoader

# Page configuration
st.set_page_config(
    page_title="Career Atlas",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Login widget
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:
    # Store authentication info in session state
    st.session_state['authentication_status'] = authentication_status
    st.session_state['name'] = name
    st.session_state['username'] = username
    
    # Sidebar
    with st.sidebar:
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout', 'sidebar')
        
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
