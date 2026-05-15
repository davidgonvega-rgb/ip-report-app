import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="IP Report", layout="wide")

st.sidebar.title("Betcris")
st.sidebar.title("IP Intelligence Tool")
st.sidebar.markdown("Prototype")
st.sidebar.markdown("---")
st.sidebar.write("**Search Modes**")
st.sidebar.write("- By Account")
st.sidebar.write("- By IP")
st.sidebar.markdown("---")
st.sidebar.write("**Environment**")
st.sidebar.write("Mock Data / Demo Version 1.0")

# ---------------------------
# SESSION STATE
# ---------------------------
for key, default in {
    "selected_ip": None,
    "selected_ip_type": None,
    "search_executed": False,
    "last_search_type": "Account",
    "last_search_input": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

for key in [
    "filtered_related_ips",
    "filtered_login_ips",
    "filtered_signup_ips",
    "filtered_login_ip_accounts",
    "filtered_signup_accounts",
    "filtered_related_login_accounts"
]:
    if key not in st.session_state:
        st.session_state[key] = pd.DataFrame()

# ---------------------------
# LOGIN IP ACCOUNTS
# ---------------------------
login_ip_accounts = pd.DataFrame({
    "Account": [
        "A20456","A10234","A30567","A40678",
        "A40023","A40021","A40022","A40024","A99001",
        "A20456","A40023","A51002","A51003",
        "A40023","A70001","A70002",
        "A20456","A40023","A80012","A80014",
        "A40023","A20456","A90022",
        "A20456","A91001","A91002","A91003",
        "A40023","A92001","A92002","A99002",
        "A20456","A93001","A93002","A93003",
        "A40023","A94001","A94002","A94003","A94004"
    ],
    "Customer": [
        "Bad Bunny","Taylor Swift","Ariana Grande","Rihanna",
        "Michael Jackson","Freddie Mercury","Prince","Madonna","Risk User 1",
        "Bad Bunny","Michael Jackson","Frank Sinatra","Johnny Cash",
        "Michael Jackson","Elton John","Bob Marley",
        "Bad Bunny","Michael Jackson","Jimi Hendrix","James Brown",
        "Michael Jackson","Bad Bunny","Eric Clapton",
        "Bad Bunny","Kendrick Lamar","David Bowie","Mick Jagger",
        "Michael Jackson","Chris Cornell","Axl Rose","Risk User 2",
        "Bad Bunny","Bruce Dickinson","Paul McCartney","Roger Waters",
        "Michael Jackson","Lemmy","Ozzy Osbourne","Sebastian Bach","Geddy Lee"
    ],
    "Login IP": [
        "563.123.256.32","563.123.256.32","563.123.256.32","563.123.256.32",
        "563.123.256.33","563.123.256.33","563.123.256.33","563.123.256.33","563.123.256.33",
        "563.123.256.34","563.123.256.34","563.123.256.34","563.123.256.34",
        "563.123.256.35","563.123.256.35","563.123.256.35",
        "563.123.256.36","563.123.256.36","563.123.256.36","563.123.256.36",
        "563.123.256.37","563.123.256.37","563.123.256.37",
        "563.123.256.38","563.123.256.38","563.123.256.38","563.123.256.38",
        "563.123.256.39","563.123.256.39","563.123.256.39","563.123.256.39",
        "563.123.256.40","563.123.256.40","563.123.256.40","563.123.256.40",
        "563.123.256.41","563.123.256.41","563.123.256.41","563.123.256.41","563.123.256.41"
    ],
    "Location": [
        "Lima, Perú","Lima, Perú","Lima, Perú","Lima, Perú",
        "Guatemala City, Guatemala","Guatemala City, Guatemala","Guatemala City, Guatemala","Guatemala City, Guatemala","Guatemala City, Guatemala",
        "Santiago, Chile","Santiago, Chile","Santiago, Chile","Santiago, Chile",
        "Panamá City, Panamá","Panamá City, Panamá","Panamá City, Panamá",
        "Ciudad de México, México","Ciudad de México, México","Ciudad de México, México","Ciudad de México, México",
        "San José, Costa Rica","San José, Costa Rica","San José, Costa Rica",
        "Managua, Nicaragua","Managua, Nicaragua","Managua, Nicaragua","Managua, Nicaragua",
        "Tegucigalpa, Honduras","Tegucigalpa, Honduras","Tegucigalpa, Honduras","Tegucigalpa, Honduras",
        "Quito, Ecuador","Quito, Ecuador","Quito, Ecuador","Quito, Ecuador",
        "San Pedro Sula, Honduras","San Pedro Sula, Honduras","San Pedro Sula, Honduras","San Pedro Sula, Honduras","San Pedro Sula, Honduras"
    ],
    "Risk Account": [
        False,False,False,False,
        False,False,False,False,True,
        False,False,True,False,
        False,False,True,
        False,False,False,False,
        False,False,False,
        False,False,True,False,
        False,False,False,True,
        False,False,False,True,
        False,False,False,True,False
    ],
    "Last Login": [
        "2025-01-17","2025-01-17","2025-01-17","2025-01-17",
        "2025-01-20","2025-01-20","2025-01-20","2025-01-20","2025-01-20",
        "2025-02-01","2025-02-01","2025-02-01","2025-02-01",
        "2025-02-10","2025-02-10","2025-02-10",
        "2025-03-05","2025-03-05","2025-03-05","2025-03-05",
        "2025-03-18","2025-03-18","2025-03-18",
        "2025-04-14","2025-04-14","2025-04-14","2025-04-14",
        "2025-05-19","2025-05-19","2025-05-19","2025-05-19",
        "2025-06-02","2025-06-02","2025-06-02","2025-06-02",
        "2025-07-21","2025-07-21","2025-07-21","2025-07-21","2025-07-21"
    ]
})

# ---------------------------
# LOGIN IPS WITHOUT RELATIONSHIPS
# ---------------------------
login_ips_without_relationships = pd.DataFrame({
    "Account": ["A20456","A20456","A20456","A40023","A40023","A40023","A10234","A94003","A70002"],
    "Customer": ["Bad Bunny","Bad Bunny","Bad Bunny","Michael Jackson","Michael Jackson","Michael Jackson","Taylor Swift","Sebastian Bach","Bob Marley"],
    "Login IP": ["563.230.092.22","563.230.092.77","563.230.092.78","563.230.092.41","563.230.092.88","563.230.092.89","563.230.092.21","563.230.092.90","563.230.092.91"],
    "Last Login": ["2025-01-16","2025-02-16","2025-03-10","2025-02-14","2025-06-03","2025-06-15","2025-01-17","2025-07-01","2025-07-04"],
    "Location": ["San José, Costa Rica","Lima, Perú","Quito, Ecuador","Ciudad de México, México","Quito, Ecuador","Panamá City, Panamá","San José, Costa Rica","Guatemala City, Guatemala","Managua, Nicaragua"]
})

# ---------------------------
# SIGNUP IP ACCOUNTS
# ---------------------------
signup_ip_accounts = pd.DataFrame({
    "Account": ["A20456","A10234","A30567","A40023","A40021","A99001","A51002","A80013","A94003","A94005"],
    "Customer": ["Bad Bunny","Taylor Swift","Ariana Grande","Michael Jackson","Freddie Mercury","Risk User 1","Frank Sinatra","Stevie Wonder","Sebastian Bach","Steven Tyler"],
    "Signup IP": ["563.111.111.10","563.111.111.10","563.111.111.10","563.111.111.20","563.111.111.20","563.111.111.20","563.111.111.30","563.111.111.40","563.111.111.50","563.111.111.50"],
    "Country": ["Perú","Ecuador","Honduras","Guatemala","México","Costa Rica","Chile","Rep Dominicana","Honduras","Perú"],
    "Risk Account": [False,False,False,False,False,True,True,True,True,False],
    "Created Date": ["2025-01-05","2025-01-06","2025-01-07","2025-02-10","2025-02-11","2025-02-12","2025-03-01","2025-03-14","2025-04-20","2025-04-22"]
})

# ---------------------------
# HELPERS
# ---------------------------
def add_row_numbers(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df

def highlight_risk_row(row):
    if row.get("Risk Account") == True:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def box_style(is_risk: bool) -> str:
    if is_risk:
        return "background-color:#f8d7da; padding:8px; border-radius:4px;"
    return "background-color:#ffffff; padding:8px; border-radius:4px; border:1px solid #eee;"

def build_related_ips_summary(filtered_login_accounts):
    if filtered_login_accounts.empty:
        return pd.DataFrame()

    grouped = (
        filtered_login_accounts.groupby("Login IP")
        .agg(
            Related_Accounts=("Account", "nunique"),
            Location=("Location", "first"),
            Has_Risk_Account=("Risk Account", "any")
        )
        .reset_index()
        .rename(columns={
            "Login IP": "IP Address",
            "Related_Accounts": "Related Accounts",
            "Has_Risk_Account": "Has Risk Account"
        })
    )

    grouped = grouped[grouped["Related Accounts"] > 1]
    return grouped.sort_values("IP Address").reset_index(drop=True)

def build_signup_ips_summary(filtered_signup_accounts):
    if filtered_signup_accounts.empty:
        return pd.DataFrame()

    grouped = (
        filtered_signup_accounts.groupby("Signup IP")
        .agg(
            Related_Accounts=("Account", "nunique"),
            Has_Risk_Account=("Risk Account", "any")
        )
        .reset_index()
        .rename(columns={
            "Related_Accounts": "Related Accounts",
            "Has_Risk_Account": "Has Risk Account"
        })
    )

    return grouped.sort_values("Signup IP").reset_index(drop=True)

def show_ip_summary_table(df, ip_column, related_column, info_column=None, has_risk_column="Has Risk Account"):
    display_df = add_row_numbers(df)

    if info_column and info_column in display_df.columns:
        header_cols = st.columns([1, 3, 2, 3, 2])
        header_cols[0].markdown("**#**")
        header_cols[1].markdown(f"**{ip_column}**")
        header_cols[2].markdown(f"**{related_column}**")
        header_cols[3].markdown(f"**{info_column}**")
        header_cols[4].markdown("**Details**")

        for idx, row in display_df.iterrows():
            row_cols = st.columns([1, 3, 2, 3, 2])
            style = box_style(bool(row[has_risk_column]))

            row_cols[0].markdown(f"<div style='{style}'>{idx}</div>", unsafe_allow_html=True)
            row_cols[1].markdown(f"<div style='{style}'>{row[ip_column]}</div>", unsafe_allow_html=True)
            row_cols[2].markdown(f"<div style='{style}'>{row[related_column]}</div>", unsafe_allow_html=True)
            row_cols[3].markdown(f"<div style='{style}'>{row[info_column]}</div>", unsafe_allow_html=True)

            if row_cols[4].button("View More", key=f"view_{ip_column}_{row[ip_column]}"):
                st.session_state.selected_ip = row[ip_column]
                st.session_state.selected_ip_type = "login" if ip_column == "IP Address" else "signup"
                st.rerun()
    else:
        header_cols = st.columns([1, 3, 2, 2])
        header_cols[0].markdown("**#**")
        header_cols[1].markdown(f"**{ip_column}**")
        header_cols[2].markdown(f"**{related_column}**")
        header_cols[3].markdown("**Details**")

        for idx, row in display_df.iterrows():
            row_cols = st.columns([1, 3, 2, 2])
            style = box_style(bool(row[has_risk_column]))

            row_cols[0].markdown(f"<div style='{style}'>{idx}</div>", unsafe_allow_html=True)
            row_cols[1].markdown(f"<div style='{style}'>{row[ip_column]}</div>", unsafe_allow_html=True)
            row_cols[2].markdown(f"<div style='{style}'>{row[related_column]}</div>", unsafe_allow_html=True)

            if row_cols[3].button("View More", key=f"view_{ip_column}_{row[ip_column]}"):
                st.session_state.selected_ip = row[ip_column]
                st.session_state.selected_ip_type = "signup"
                st.rerun()

def build_accounts_sharing_multiple_ips(filtered_login_accounts, searched_account):
    if filtered_login_accounts.empty:
        return pd.DataFrame()

    searched_account = searched_account.strip().upper()

    df = filtered_login_accounts[
        filtered_login_accounts["Account"].str.upper() != searched_account
    ]

    grouped = (
        df.groupby(["Account", "Customer"])
        .agg(
            Shared_IP_Count=("Login IP", "nunique"),
            Shared_IPs=("Login IP", lambda x: ", ".join(sorted(set(x))))
        )
        .reset_index()
    )

    grouped = grouped[grouped["Shared_IP_Count"] > 1]
    return grouped

# ---------------------------
# DETAIL PAGE
# ---------------------------
if st.session_state.selected_ip is not None:
    selected_ip = st.session_state.selected_ip
    selected_type = st.session_state.selected_ip_type

    st.title("Signup IP Detail" if selected_type == "signup" else "Login IP Detail")

    if selected_type == "signup":
        detail_df = signup_ip_accounts[signup_ip_accounts["Signup IP"] == selected_ip].copy()
        detail_df = detail_df[["Account", "Customer", "Created Date", "Risk Account"]]
    else:
        detail_df = login_ip_accounts[login_ip_accounts["Login IP"] == selected_ip].copy()
        detail_df = detail_df[["Account", "Customer", "Last Login", "Risk Account"]]

    st.subheader(f"Linked Accounts for IP: {selected_ip}")

    if not detail_df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Linked Accounts", len(detail_df))
        with c2:
            st.metric("Risk Accounts", int(detail_df["Risk Account"].sum()))

        styled_df = add_row_numbers(detail_df).style.apply(highlight_risk_row, axis=1)
        st.dataframe(styled_df, use_container_width=True)
        st.caption("Accounts highlighted in red are risk accounts.")
    else:
        st.warning("No linked accounts found for this IP.")

    if st.button("Back to Search"):
        st.session_state.selected_ip = None
        st.session_state.selected_ip_type = None
        st.rerun()

# ---------------------------
# MAIN PAGE
# ---------------------------
else:
    st.title("IP Report")
    st.subheader("Search by Account or IP")

    col1, col2 = st.columns([4, 1])

    with col2:
        st.image("betcrislogo.png", width=250)

    search_type = st.radio(
        "Search Type",
        ["Account", "IP"],
        horizontal=True,
        index=0 if st.session_state.last_search_type == "Account" else 1
    )

    search_col1, search_col2 = st.columns([2, 2])

    with search_col1:
        search_input = st.text_input(
            "Type Search Value",
            value=st.session_state.last_search_input,
            placeholder="A20456, A40023 or 563.123.256.33"
        )

    with search_col2:
        st.date_input(
            "Date Range",
            value=(date(2025, 1, 1), date(2025, 12, 31)),
            help="Visual filter only. Not functional in this prototype version."
        )

    if st.button("Search"):
        st.session_state.last_search_type = search_type
        st.session_state.last_search_input = search_input
        st.session_state.search_executed = True

        search_clean = search_input.strip().upper()

        if search_type == "Account":
            account_login_rows = login_ip_accounts[
                login_ip_accounts["Account"].str.upper() == search_clean
            ]

            related_ip_matches = account_login_rows["Login IP"].unique().tolist()

            filtered_related_login_accounts = login_ip_accounts[
                login_ip_accounts["Login IP"].isin(related_ip_matches)
            ]

            filtered_related_ips = build_related_ips_summary(filtered_related_login_accounts)

            filtered_login_ips = login_ips_without_relationships[
                login_ips_without_relationships["Account"].str.upper() == search_clean
            ][["Login IP", "Last Login", "Location"]]

            account_signup_row = signup_ip_accounts[
                signup_ip_accounts["Account"].str.upper() == search_clean
            ]

            signup_ip_matches = account_signup_row["Signup IP"].unique().tolist()

            filtered_signup_accounts_for_summary = signup_ip_accounts[
                signup_ip_accounts["Signup IP"].isin(signup_ip_matches)
            ]

            filtered_signup_ips = build_signup_ips_summary(filtered_signup_accounts_for_summary)

            st.session_state.filtered_related_login_accounts = filtered_related_login_accounts
            st.session_state.filtered_related_ips = filtered_related_ips
            st.session_state.filtered_login_ips = filtered_login_ips
            st.session_state.filtered_signup_ips = filtered_signup_ips

        else:
            filtered_login_ip_accounts = login_ip_accounts[
                login_ip_accounts["Login IP"].str.contains(search_clean, case=False, na=False)
            ]

            standalone_login_accounts = login_ips_without_relationships[
                login_ips_without_relationships["Login IP"].str.contains(search_clean, case=False, na=False)
            ][["Account", "Customer", "Login IP", "Location", "Last Login"]].copy()

            if not standalone_login_accounts.empty:
                standalone_login_accounts["Risk Account"] = False
                standalone_login_accounts = standalone_login_accounts[
                    ["Account", "Customer", "Login IP", "Last Login", "Risk Account"]
                ]

            filtered_login_ip_accounts = filtered_login_ip_accounts[
                ["Account", "Customer", "Login IP", "Last Login", "Risk Account"]
            ]

            filtered_login_ip_accounts = pd.concat(
                [filtered_login_ip_accounts, standalone_login_accounts],
                ignore_index=True
            )

            filtered_signup_accounts = signup_ip_accounts[
                signup_ip_accounts["Signup IP"].str.contains(search_clean, case=False, na=False)
            ]

            st.session_state.filtered_login_ip_accounts = filtered_login_ip_accounts
            st.session_state.filtered_signup_accounts = filtered_signup_accounts

    if st.session_state.search_executed:
        if st.session_state.last_search_type == "Account":
            filtered_related_ips = st.session_state.filtered_related_ips
            filtered_login_ips = st.session_state.filtered_login_ips
            filtered_signup_ips = st.session_state.filtered_signup_ips
            filtered_related_login_accounts = st.session_state.filtered_related_login_accounts

            st.markdown("## Summary")
            s1, s2, s3, s4 = st.columns(4)

            with s1:
                st.metric("Total IPs", len(filtered_related_ips) + len(filtered_login_ips) + len(filtered_signup_ips))
            with s2:
                st.metric("IPs with Relationships", len(filtered_related_ips))
            with s3:
                st.metric("Login IPs without Relationships", len(filtered_login_ips))
            with s4:
                st.metric("Signup IPs", len(filtered_signup_ips))

            st.markdown("## IPs with Related Accounts")
            if not filtered_related_ips.empty:
                show_ip_summary_table(filtered_related_ips, "IP Address", "Related Accounts", "Location")
            else:
                st.warning("No related IPs found.")

            st.markdown("## Accounts Sharing Multiple IPs")
            accounts_sharing_multiple_ips = build_accounts_sharing_multiple_ips(
                filtered_related_login_accounts,
                st.session_state.last_search_input
            )

            if not accounts_sharing_multiple_ips.empty:
                st.dataframe(add_row_numbers(accounts_sharing_multiple_ips), use_container_width=True)
            else:
                st.warning("No other accounts sharing multiple IPs found.")

            st.markdown("## Signup IP")
            if not filtered_signup_ips.empty:
                show_ip_summary_table(filtered_signup_ips, "Signup IP", "Related Accounts")
            else:
                st.warning("No signup IP found.")

            st.markdown("## Login IPs without Relationships")
            if not filtered_login_ips.empty:
                st.dataframe(add_row_numbers(filtered_login_ips), use_container_width=True)
            else:
                st.warning("No login IPs without relationships found.")

        else:
            filtered_login_ip_accounts = st.session_state.filtered_login_ip_accounts
            filtered_signup_accounts = st.session_state.filtered_signup_accounts

            st.markdown("## Summary")
            c1, c2 = st.columns(2)

            with c1:
                st.metric("Login IP Accounts", len(filtered_login_ip_accounts))
            with c2:
                st.metric("Signup IP Accounts", len(filtered_signup_accounts))

            st.markdown("## Login IP Accounts")
            if not filtered_login_ip_accounts.empty:
                styled_df = add_row_numbers(filtered_login_ip_accounts).style.apply(highlight_risk_row, axis=1)
                st.dataframe(styled_df, use_container_width=True)
            else:
                st.warning("No accounts found using this IP as Login IP.")

            st.markdown("## Signup IP Accounts")
            if not filtered_signup_accounts.empty:
                styled_df = add_row_numbers(filtered_signup_accounts).style.apply(highlight_risk_row, axis=1)
                st.dataframe(styled_df, use_container_width=True)
            else:
                st.warning("No accounts found using this IP as Signup IP.")
