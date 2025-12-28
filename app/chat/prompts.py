import os
import streamlit as st
import yaml

from dal.s3 import S3Client
from dal.models import ConfigurationModel


def show_prompts():
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )
    
    prompts_yaml = s3client.get_text_file(
        os.environ["S3_BUCKET"],
        os.environ["PROMPTS_FILE"],
        fallback_file_path=os.environ.get("PROMPTS_FILE_FALLBACK","/app/data/prompts.yaml")
    )
    prompts = yaml.safe_load(prompts_yaml)['prompts']
    prompt_keys = list(prompts.keys())

    prompt = st.selectbox("Select a prompt to edit", options=prompt_keys, accept_new_options=True)

    with st.form("edit_prompt_form"):
        prompt_text = st.text_area("Prompt Text", value=prompts.get(prompt, ""), height=300)
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Save Prompt")
        with col2:
            delete_submitted = st.form_submit_button("Delete Prompt")
        if submitted:
            prompts[prompt] = prompt_text
            #save to yaml
            yaml_string = yaml.dump({'prompts': prompts})
            s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"], yaml_string)
            st.success(f"Prompt '{prompt}' saved successfully!")
        if delete_submitted:
            if prompt in prompts:
                del prompts[prompt]
                yaml_string = yaml.dump({'prompts': prompts})
                s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"], yaml_string)
                st.success(f"Prompt '{prompt}' deleted successfully!")
                prompt_keys = list(prompts.keys())
                if prompt_keys:
                    prompt = prompt_keys[0]
                st.rerun()
            else:
                st.error("Prompt not found.")

