import streamlit as st
import hmac

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