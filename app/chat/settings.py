import os
import streamlit as st
import yaml

from dal.s3 import S3Client
from dal.models import ConfigurationModel

def show_settings():
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )

    config_yaml = s3client.get_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"])
    prompts_yaml = s3client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
    config = ConfigurationModel.from_yaml_string(config_yaml)
    prompts = yaml.safe_load(prompts_yaml)['prompts']
    prompt_keys = list(prompts.keys())
    bucket_files = s3client.list_objects(os.environ["S3_BUCKET"], prefix="")
    whitelist_files = [f for f in bucket_files if not f.endswith('.yaml')]
    

    """Render the Settings page in Streamlit."""
    st.set_page_config(page_title="Settings")
    st.title("Settings")

    st.markdown("Use this page to view and tweak session-level settings for the chat app.")

    #todo create a form bnased on the config model
    ai_model = st.text_input("AI Model", value=config.ai_model)
    system_prompt = st.selectbox("System Prompt", options=prompt_keys, index=prompt_keys.index(config.system_prompt) if config.system_prompt in prompt_keys else 0)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=float(config.temperature), step=0.05)
    whitelist = st.selectbox("Whitelist File", options=whitelist_files, index=whitelist_files.index(config.whitelist) if config.whitelist in whitelist_files else 0)
    st.header("Prompt Preview")
    st.markdown(prompts[system_prompt])

    submitted = st.button("Save Settings")
    if submitted:
        #update config model
        config.ai_model = ai_model
        config.system_prompt = system_prompt
        config.temperature = temperature
        config.whitelist = whitelist

        #save to yaml
        yaml_string = config.to_yaml_string()
        s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"], yaml_string)
        st.success("Settings saved successfully!")
        if st.button("Restart Application"):
            st.session_state.clear()
            st.rerun()
            st.write("Application restarted. Reload the browser.")

