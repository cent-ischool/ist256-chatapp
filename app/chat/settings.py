import os
import streamlit as st

from dal.s3 import S3Client
from dal.models import AppSettingsModel


def show_settings():
    """Render the Settings page in Streamlit."""
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )

    # Load config from S3
    config_yaml = s3client.get_text_file(
        os.environ["S3_BUCKET"],
        os.environ["CONFIG_FILE"],
        fallback_file_path=os.environ.get("CONFIG_FILE_FALLBACK", "/app/data/config.yaml")
    )
    config = AppSettingsModel.from_yaml_string(config_yaml)

    # Get whitelist files from S3 bucket
    bucket_files = s3client.list_objects(os.environ["S3_BUCKET"], prefix="")
    whitelist_files = [""] + [f for f in bucket_files if not f.endswith('.yaml')]

    st.title("Settings")
    st.markdown("Configure AI model settings and system prompts.")

    # Model Settings Section
    st.header("Model Settings")
    ai_model = st.text_input("AI Model", value=config.ai_model)
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=float(config.temperature),
        step=0.05
    )
    whitelist = st.selectbox(
        "Whitelist File",
        options=whitelist_files,
        index=whitelist_files.index(config.whitelist) if config.whitelist in whitelist_files else 0
    )

    # System Prompts Section
    st.header("System Prompts")
    st.markdown("Configure the AI's behavior in each mode.")

    tutor_prompt = st.text_area(
        "Tutor Mode Prompt",
        value=config.tutor_prompt,
        height=200,
        help="Used when AI mode is 'Tutor' - guides students with questions"
    )

    answer_prompt = st.text_area(
        "Answer Mode Prompt",
        value=config.answer_prompt,
        height=200,
        help="Used when AI mode is 'Answer' - provides direct answers"
    )

    # Save Button
    submitted = st.button("Save Settings")
    if submitted:
        config.ai_model = ai_model
        config.temperature = temperature
        config.whitelist = whitelist
        config.tutor_prompt = tutor_prompt
        config.answer_prompt = answer_prompt

        yaml_string = config.to_yaml_string()
        s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"], yaml_string)
        st.success("Settings saved successfully!")
        if st.button("Restart Application"):
            st.session_state.clear()
            st.rerun()
