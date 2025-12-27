import os
import streamlit as st


def show_session():
    st.title("Session variables:")
    st.json({k: str(v) for k, v in st.session_state.items()})
