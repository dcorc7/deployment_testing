import os
import requests
import streamlit as st

# ---------------- Basic page setup ----------------
st.set_page_config(page_title="Simple Deployment Test", page_icon="🌍", layout="wide")

st.title("🌍 Simple Deployment Test")

# ---------------- Backend config ----------------
API_URL = os.getenv("API_URL", "https://deployment-testing-0v1x.onrender.com")

def _api_search():
    r = requests.post(f"{API_URL}/search", timeout=25)
    r.raise_for_status()
    return r.json()

# ---------------- Sidebar ----------------
st.sidebar.header("Controls")
run = st.sidebar.button("🔎 Run Search", use_container_width=True)

# ---------------- Run logic ----------------
if "results" not in st.session_state:
    st.session_state["results"] = None

if run:
    try:
        results = _api_search()
        st.session_state["results"] = results
        st.success("✅ Search complete!")
    except Exception as e:
        st.error(f"❌ API call failed: {e}")

results = st.session_state["results"]

# ---------------- Tabs ----------------
tab = st.tabs(["Results"])[0]

with tab:
    if not results:
        st.info("Press 'Run Search' in the sidebar to start.")
    else:
        st.json(results)
