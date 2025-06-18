import streamlit as st
from utils.auth_manager import AuthManager

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
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Welcome"

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
        st.write(f"Welcome **{st.session_state['name']}**")
        
        # Show role badge
        if st.session_state['role'] == 'admin':
            st.success("🔐 Admin Access")
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        
        # Create navigation buttons
        if st.button("🏠 Welcome", use_container_width=True, type="secondary" if st.session_state['current_page'] != "Welcome" else "primary"):
            st.session_state['current_page'] = "Welcome"
            st.rerun()
            
        if st.button("📝 Assessment", use_container_width=True, type="secondary" if st.session_state['current_page'] != "Assessment" else "primary"):
            st.session_state['current_page'] = "Assessment"
            st.rerun()
            
        if st.button("📊 Results", use_container_width=True, type="secondary" if st.session_state['current_page'] != "Results" else "primary"):
            st.session_state['current_page'] = "Results"
            st.rerun()
        
        # Admin only pages
        if st.session_state['role'] == 'admin':
            st.divider()
            st.subheader("Admin Tools")
            
            if st.button("👥 User Management", use_container_width=True, type="secondary" if st.session_state['current_page'] != "User Management" else "primary"):
                st.session_state['current_page'] = "User Management"
                st.rerun()
                
            if st.button("📈 Analytics", use_container_width=True, type="secondary" if st.session_state['current_page'] != "Analytics" else "primary"):
                st.session_state['current_page'] = "Analytics"
                st.rerun()
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            AuthManager.logout()
            st.session_state['current_page'] = "Welcome"
            st.rerun()
    
    # Main content area - Page routing
    page = st.session_state['current_page']
    
    try:
        if page == "Welcome":
            from pages.welcome import show_welcome
            show_welcome()
        elif page == "Assessment":
            from pages.assessment import show_assessment
            show_assessment()
        elif page == "Results":
            from pages.results import show_results
            show_results()
        elif page == "User Management" and st.session_state['role'] == 'admin':
            st.title("👥 User Management")
            st.info("User management features coming soon!")
            st.write("This page will allow admins to:")
            st.write("- View all users")
            st.write("- Manage user accounts")
            st.write("- View user assessment history")
            st.write("- Export user data")
        elif page == "Analytics" and st.session_state['role'] == 'admin':
            st.title("📈 Analytics Dashboard")
            st.info("Analytics features coming soon!")
            st.write("This page will show:")
            st.write("- Usage statistics")
            st.write("- Assessment completion rates")
            st.write("- Popular career paths")
            st.write("- User engagement metrics")
        else:
            st.error(f"Page '{page}' not found or you don't have permission to access it.")
            st.session_state['current_page'] = "Welcome"
            st.rerun()
            
    except ImportError as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Please ensure all required files are present in the pages directory.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")
