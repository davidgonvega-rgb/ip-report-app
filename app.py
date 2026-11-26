import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import base64
from PIL import Image
from html import escape

st.set_page_config(page_title="IP Report", layout="wide", initial_sidebar_state="expanded")

# Assets are read from the repository directory.
ASSET_DIR = Path(__file__).resolve().parent

@st.cache_data(show_spinner=False)
def asset_base64(filename):
    path = ASSET_DIR / filename
    return base64.b64encode(path.read_bytes()).decode("ascii") if path.is_file() else None

background = asset_base64("Background2.png")

# The background preserves its aspect ratio. The independent logo never stretches.
# For best results Background2.png should contain ONLY the purple gradient.
background_css = (
    f'background-image: url("data:image/png;base64,{background}");'
    if background else
    'background-image: radial-gradient(ellipse at 15% 25%, #73115f 0%, #350742 48%, #160421 100%);'
)
# Load the transparent logo independently from the background.
# Load the PNG through Pillow to ensure consistent rendering in Streamlit.
logo_path = ASSET_DIR / "BASlogo2.png"
if logo_path.is_file():
    try:
        with Image.open(logo_path) as source:
            logo_image = source.convert("RGBA")
        st.logo(logo_image, size="large")
    except Exception as exc:
        st.warning(f"Unable to open BASlogo2.png: {exc}")
else:
    st.warning("BASlogo2.png was not found next to app.py. Check the filename and its location in GitHub.")

st.markdown(f"""
<style>
.stApp {{
    background-color: #190723;
    {background_css}
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stSidebar"] {{
    background: rgba(32, 10, 48, 0.96);
    border-right: 1px solid rgba(255,255,255,0.15);
}}
[data-testid="stSidebar"] * {{ color: white; }}
[data-testid="stMainBlockContainer"] {{
    background: rgba(25, 7, 39, 0.12);
    border-radius: 16px;
    padding-top: 5rem;
}}
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {{ color: white; }}
[data-testid="stMetric"] {{
    background: rgba(65, 24, 85, 0.85);
    padding: 12px;
    border-radius: 10px;
}}
.stButton > button {{ background: #f7f2fb; color: #2a1039; border: 1px solid #e1cde8; }}
.stButton > button p {{ color: #2a1039 !important; }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("IP Intelligence Tool")
    st.caption("Prototype")
    st.divider()
    st.write("**Search Modes**")
    st.write("- By Account")
    st.write("- By IP")
    st.divider()
    st.write("**Environment**")
    st.write("Mock Data / Demo Version 1.0")
    st.caption("Visual demonstration only")


# Fixed fictional examples; no external data or account lookup.
LTP = {"A20456": 1560, "A40023": -265235, "A51002": 18450,
       "A51003": -8720, "A99001": -12350, "A99002": 23540}
NAMES = {"A20456": "Bad Bunny", "A40023": "Michael Jackson",
         "A51002": "Frank Sinatra", "A51003": "Johnny Cash",
         "A99001": "Bruno Mars", "A99002": "Justin Timberlake"}

def table(headers, rows, flags=None):
    flags = flags or [False] * len(rows)
    html = '<div class="demo-table"><table><thead><tr>'
    html += ''.join(f'<th>{escape(str(h))}</th>' for h in headers)
    html += '</tr></thead><tbody>'
    for row, flag in zip(rows, flags):
        html += '<tr class="flagged">' if flag else '<tr>'
        html += ''.join(f'<td>{escape(str(v))}</td>' for v in row)
        html += '</tr>'
    st.markdown(html + '</tbody></table></div>', unsafe_allow_html=True)

def accounts(ids, date_label, dates, flags):
    table(["Account", "Customer", "LTP", date_label, "Risk Account"],
          [[a, NAMES[a], f"${LTP[a]:+,}", d, "HIGH RISK" if f else "No"]
           for a,d,f in zip(ids, dates, flags)], flags)

st.markdown("""<style>
.demo-table {overflow-x:auto;}
.demo-table table {width:100%;border-collapse:separate;border-spacing:5px 10px;color:white;}
.demo-table th {text-align:left;padding:8px;color:white;}
.demo-table td {padding:12px 8px;border:1px solid #a18cac;border-radius:6px;background:rgba(53,19,75,.35);color:white;}
.demo-table tr.flagged td {background:#ffc4d1;color:#741029;border:2px solid #ff315c;font-weight:800;}
[data-testid="stSidebarCollapsedControl"] {position:fixed!important;top:50vh!important;left:8px!important;transform:translateY(-50%)!important;}
</style>""", unsafe_allow_html=True)

view = st.sidebar.radio("Demo Screen", ["Search Overview", "IP Detail"])
st.caption("Illustrative data only — not connected to live accounts.")
if view == "Search Overview":
    st.title("IP Report")
    st.subheader("Search by Account or IP")
    st.radio("Search Type", ["Account", "IP"], horizontal=True, disabled=True)
    a,b=st.columns(2)
    a.text_input("Type Search Value", "A20456", disabled=True)
    b.date_input("Date Range", (date(2025,1,1),date(2025,12,31)), disabled=True)
    st.button("Search", disabled=True)
    st.header("Summary")
    for col, label, value in zip(st.columns(4), ["Total IPs", "IPs with Relationships", "Login IPs without Relationships", "Signup IP"], [4,2,1,1]):
        col.metric(label,value)
    st.header("IPs with Related Accounts")
    table(["IP Address", "Related Accounts", "Location"], [["192.0.2.34",4,"Santiago, Chile"],["192.0.2.39",2,"Tegucigalpa, Honduras"]], [True,True])
    st.header("Accounts Sharing Multiple IPs")
    table(["Account","Customer","LTP","Shared IP Count","Shared IPs"], [["A40023",NAMES["A40023"],f"${LTP['A40023']:+,}",2,"192.0.2.34, 192.0.2.39"]])
    st.header("Signup IP")
    table(["Signup IP","Related Accounts"], [["198.51.100.10",2]])
    st.header("Login IPs without Relationships")
    table(["Login IP","Last Login","Location"], [["203.0.113.22","2025-01-16","San José, Costa Rica"]])
else:
    st.title("IP Detail")
    sample=st.selectbox("Demo example", ["192.0.2.34","192.0.2.39"])
    st.subheader(f"IP: {sample}")
    ids = ["A20456","A40023","A51002","A51003"] if sample.endswith("34") else ["A99001","A99002"]
    flags = [False,False,True,False] if len(ids)==4 else [True,True]
    for col,label,value in zip(st.columns(3),["Login Accounts","Signup Accounts","Risk Accounts"],[len(ids),0,sum(flags)]):
        col.metric(label,value)
    st.header("Logins")
    accounts(ids,"Last Login",["2025-02-01"]*len(ids),flags)
    st.header("Signup")
    st.info("No signup accounts found for this IP.")
    st.caption("Return to Search Overview using the sidebar.")
