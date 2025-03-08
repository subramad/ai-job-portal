import streamlit as st
import hmac
import base64

# Function to get the base64 encoding of the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Path to your local image
header_img_path = 'data/header.jpg'
header_img_base64 = get_base64_of_bin_file(header_img_path)

bg_img_path = 'data/background.jpg'
bg_img_base64 = get_base64_of_bin_file(bg_img_path)

st.set_page_config(layout="wide")
page_bg_img = f"""
<style>
[data-testid="stHeader"]{{
background-image: url("data:image/jpg;base64,{header_img_base64}");
background-repeat: no-repeat;
background-size: 10%;
background: rgba(0,0,0,0);
width: 100%
height: 20%;
}}
[data-testid="stAppViewContainer"]{{
background-image: url("data:image/jpg;base64,{bg_img_base64}");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}



[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("AI-Powered Job Portal")
def login():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state['logged_in'] = True
            del st.session_state["password"] 
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not login():
    st.stop()


login_page = st.Page(login, title="Log in", icon=":material/login:")


jobs = st.Page("available-jobs.py", title="Available Jobs", icon=":material/work:", default=True)
recommender = st.Page(
    "recommender.py", title="Job Recommender", icon=":material/dashboard:"
)

if st.session_state.logged_in:
    pg = st.navigation(
        [jobs, recommender]
    )
else:
    pg = st.navigation([login_page])

pg.run()