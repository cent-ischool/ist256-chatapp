from streamlit_javascript import st_javascript


def get_url():
    url = st_javascript("await fetch('').then(r => window.parent.location.href)")
    return url
