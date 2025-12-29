import streamlit as st
import json
from module_extractor import extract_modules_from_url
from utils import is_valid_url

st.set_page_config(page_title="Pulse Module Extractor", layout="wide")
st.title("Pulse – Module Extraction AI Agent")

urls = st.text_area("Enter documentation URLs (one per line)")

if st.button("Extract Modules"):
    results = []
    for url in urls.splitlines():
        if not is_valid_url(url):
            st.error(f"Invalid URL: {url}")
            continue
        with st.spinner(f"Processing {url}"):
            results.extend(extract_modules_from_url(url))

    st.json(results)
    with open("output.json", "w") as f:
        json.dump(results, f, indent=2)
