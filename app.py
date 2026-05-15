import streamlit as st
import pandas as pd

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

if "selected_ip" not in st.session_state:
    st.session_state.selected_ip = None
if "selected_ip_type" not in st.session_state:
    st.session_state.selected_ip_type = None
if "search_executed" not in st.session_state:
    st.session_state.search_executed = False
if "last_search_type" not in st.session_state:
    st.session_state.last_search_type = "Account"
if "last_search_input" not in st.session_state:
    st.session_state.last_search_input = ""

for key in [
    "filtered_related_ips",
    "filtered_login_ips",
    "filtered_signup_ips",
    "filtered_login_ip_accounts",
    "filtered_signup_accounts"
]:
    if key not in st.session_state:
        st.session_state[key] = pd.DataFrame()

related_accounts_detail = {
    "563.123.256.32": pd.DataFrame({
        "Account": ["A20456", "A10234", "A30567", "A40678"],
        "Customer": ["Bad Bunny", "Taylor Swift", "Ariana Grande", "Rihanna"],
        "Country": ["Perú", "Ecuador", "Honduras", "Guatemala"],
        "Risk Account": [False, False, False, False]
    }),
    "563.123.256.33": pd.DataFrame({
        "Account": ["A40023", "A40021", "A40022", "A40024", "A99001"],
        "Customer": ["Michael Jackson", "Freddie Mercury", "Prince", "Madonna", "Risk User 1"],
        "Country": ["Guatemala", "México", "Perú", "Panamá", "Costa Rica"],
        "Risk Account": [False, False, False, False, True]
    }),
    "563.123.256.34": pd.DataFrame({
        "Account": ["A20456", "A40023", "A51002", "A51003"],
        "Customer": ["Bad Bunny", "Michael Jackson", "Frank Sinatra", "Johnny Cash"],
        "Country": ["Perú", "Guatemala", "Chile", "México"],
        "Risk Account": [False, False, True, False]
    }),
    "563.123.256.35": pd.DataFrame({
        "Account": ["A40023", "A70001", "A70002"],
        "Customer": ["Michael Jackson", "Elton John", "Bob Marley"],
        "Country": ["Guatemala", "Ecuador", "Panamá"],
        "Risk Account": [False, False, True]
    }),
    "563.123.256.36": pd.DataFrame({
        "Account": ["A20456", "A40023", "A80012", "A80014"],
        "Customer": ["Bad Bunny", "Michael Jackson", "Jimi Hendrix", "James Brown"],
        "Country": ["Perú", "Guatemala", "México", "Perú"],
        "Risk Account": [False, False, False, False]
    }),
    "563.123.256.37": pd.DataFrame({
        "Account": ["A40023", "A20456", "A90022"],
        "Customer": ["Michael Jackson", "Bad Bunny", "Eric Clapton"],
        "Country": ["Guatemala", "Perú", "Guatemala"],
        "Risk Account": [False, False, False]
    }),
    "563.123.256.38": pd.DataFrame({
        "Account": ["A20456", "A91001", "A91002", "A91003"],
        "Customer": ["Bad Bunny", "Kendrick Lamar", "David Bowie", "Mick Jagger"],
        "Country": ["Perú", "Panamá", "Nicaragua", "Ecuador"],
        "Risk Account": [False, False, True, False]
    }),
    "563.123.256.39": pd.DataFrame({
        "Account": ["A40023", "A92001", "A92002", "A99002"],
        "Customer": ["Michael Jackson", "Chris Cornell", "Axl Rose", "Risk User 2"],
        "Country": ["Guatemala", "México", "Nicaragua", "Honduras"],
        "Risk Account": [False, False, False, True]
    }),
    "563.123.256.40": pd.DataFrame({
        "Account": ["A20456", "A93001", "A93002", "A93003"],
        "Customer": ["Bad Bunny", "Bruce Dickinson", "Paul McCartney", "Roger Waters"],
        "Country": ["Perú", "Perú", "Honduras", "Nicaragua"],
        "Risk Account": [False, False, False, True]
    }),
    "563.123.256.41": pd.DataFrame({
        "Account": ["A40023", "A94001", "A94002", "A94003", "A94004"],
        "Customer": ["Michael Jackson", "Lemmy", "Ozzy Osbourne", "Sebastian Bach", "Geddy Lee"],
        "Country": ["Guatemala", "Ecuador", "México", "Honduras", "Guatemala"],
        "Risk Account": [False, False, False, True, False]
    })
}

ip_last_login_map = {
    "563.123.256.32": "1/17/2025 01:26PM",
    "563.123.256.33": "1/10/2026 02:35PM",
    "563.123.256.34": "1/17/2020 05:11PM",
    "563.123.256.35": "1/17/2020 01:05PM",
    "563.123.256.36": "2/11/2025 09:10AM",
    "563.123.256.37": "3/05/2026 10:22PM",
    "563.123.256.38": "4/14/2025 11:43AM",
    "563.123.256.39": "5/19/2025 08:17PM",
    "563.123.256.40": "6/02/2025 03:09PM",
    "563.123.256.41": "7/21/2025 07:50AM"
}

related_ips_rows = []
login_ip_accounts_rows = []

for ip, df in related_accounts_detail.items():
    related_ips_rows.append({
        "IP Address": ip,
        "Related Accounts": len(df),
        "Last Login": ip_last_login_map.get(ip, "N/A"),
        "Has Risk Account": bool(df["Risk Account"].any())
    })

    for _, row in df.iterrows():
        login_ip_accounts_rows.append({
            "Account": row["Account"],
            "Customer": row["Customer"],
            "Login IP": ip,
            "Country": row["Country"],
            "Risk Account": row["Risk Account"]
        })

related_ips_data = pd.DataFrame(related_ips_rows).sort_values("IP Address").reset_index(drop=True)
login_ip_accounts = pd.DataFrame(login_ip_accounts_rows)

login_ips_without_relationships = pd.DataFrame({
    "Account": [
        "A20456", "A20456", "A20456",
        "A40023", "A40023", "A40023",
        "A10234", "A94003", "A70002"
    ],
    "Customer": [
        "Bad Bunny", "Bad Bunny", "Bad Bunny",
        "Michael Jackson", "Michael Jackson", "Michael Jackson",
        "Taylor Swift", "Sebastian Bach", "Bob Marley"
    ],
    "Login IP": [
        "563.230.092.22",
        "563.230.092.77",
        "563.230.092.78",
        "563.230.092.41",
        "563.230.092.88",
        "563.230.092.89",
        "563.230.092.21",
        "563.230.092.90",
        "563.230.092.91"
    ],
    "Last Login": [
        "1/16/2020 08:12PM",
        "2/16/2025 10:35AM",
        "3/10/2025 06:20PM",
        "2/14/2025 09:50AM",
        "6/03/2025 09:45PM",
        "6/15/2025 01:10PM",
        "1/17/2020 01:28PM",
        "7/01/2025 11:11AM",
        "7/04/2025 08:45PM"
    ],
    "Location": [
        "San José, Costa Rica",
        "Lima, Perú",
        "Quito, Ecuador",
        "Ciudad de México, México",
        "Quito, Ecuador",
        "Panamá City, Panamá",
        "San José, Costa Rica",
        "Guatemala City, Guatemala",
        "Managua, Nicaragua"
    ]
})

signup_ip_accounts = pd.DataFrame({
    "Account": [
        "A20456", "A10234", "A30567",
        "A40023", "A40021", "A99001",
        "A51002", "A80013", "A94003", "A94005"
    ],
    "Customer": [
        "Bad Bunny", "Taylor Swift", "Ariana Grande",
        "Michael Jackson", "Freddie Mercury", "Risk User 1",
        "Frank Sinatra", "Stevie Wonder", "Sebastian Bach", "Steven Tyler"
    ],
    "Signup IP": [
        "563.111.111.10",
        "563.111.111.10",
        "563.111.111.10",
        "563.111.111.20",
        "563.111.111.20",
        "563.111.111.20",
        "563.111.111.30",
        "563.111.111.40",
        "563.111.111.50",
        "563.111.111.50"
    ],
    "Country": [
        "Perú", "Ecuador", "Honduras",
        "Guatemala", "México", "Costa Rica",
        "Chile", "Rep Dominicana", "Honduras", "Perú"
    ],
    "Risk Account": [
        False, False, False,
        False, False, True,
        True, True, True, False
    ],
    "Created Date": [
        "2025-01-05", "2025-01-06", "2025-01-07",
        "2025-02-10", "2025-02-11", "2025-02-12",
        "2025-03-01", "2025-03-14", "2025-04-20", "2025-04-22"
    ]
})

signup_ips_rows = []
for ip, df in signup_ip_accounts.groupby("Signup IP"):
    signup_ips_rows.append({
        "Signup IP": ip,
        "Related Accounts": len(df),
        "Has Risk Account": bool(df["Risk Account"].any())
    })

signup_ips_summary = pd.DataFrame(signup_ips_rows).sort_values("Signup IP").reset_index(drop=True)

account_to_related_ips = {}
for ip, df in related_accounts_detail.items():
    for account in df["Account"].tolist():
        account_to_related_ips.setdefault(account, []).append(ip)

account_to_login_ips_without_relationships = {}
for _, row in login_ips_without_relationships.iterrows():
    account_to_login_ips_without_relationships.setdefault(row["Account"], []).append(row["Login IP"])

account_to_signup_ip = {}
for _, row in signup_ip_accounts.iterrows():
    account_to_signup_ip[row["Account"]] = row["Signup IP"]

def add_row_numbers(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df

def highlight_risk_row(row):
    if row["Risk Account"] == True:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def box_style(is_risk: bool) -> str:
    if is_risk:
        return "background-color:#f8d7da; padding:8px; border-radius:4px;"
    return "background-color:#ffffff; padding:8px; border-radius:4px; border:1px solid #eee;"

def show_ip_summary_table(df, ip_column, related_column, last_login_column=None, has_risk_column="Has Risk Account"):
    display_df = add_row_numbers(df)

    if last_login_column and last_login_column in display_df.columns:
        header_cols = st.columns([1, 3, 2, 3, 2])
        header_cols[0].markdown("**#**")
        header_cols[1].markdown(f"**{ip_column}**")
        header_cols[2].markdown(f"**{related_column}**")
        header_cols[3].markdown("**Last Login**")
        header_cols[4].markdown("**Details**")

        for idx, row in display_df.iterrows():
            row_cols = st.columns([1, 3, 2, 3, 2])
            style = box_style(bool(row[has_risk_column]))

            row_cols[0].markdown(f"<div style='{style}'>{idx}</div>", unsafe_allow_html=True)
            row_cols[1].markdown(f"<div style='{style}'>{row[ip_column]}</div>", unsafe_allow_html=True)
            row_cols[2].markdown(f"<div style='{style}'>{row[related_column]}</div>", unsafe_allow_html=True)
            row_cols[3].markdown(f"<div style='{style}'>{row[last_login_column]}</div>", unsafe_allow_html=True)

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

def build_accounts_sharing_multiple_ips(related_accounts_detail, filtered_related_ips):
    allowed_ips = set(filtered_related_ips["IP Address"].tolist())
    account_ip_map = {}

    for ip, df in related_accounts_detail.items():
        if ip not in allowed_ips:
            continue

        for _, row in df.iterrows():
            account = row["Account"]
            customer = row["Customer"]

            if account not in account_ip_map:
                account_ip_map[account] = {
                    "Account": account,
                    "Customer": customer,
                    "Shared IPs": []
                }

            account_ip_map[account]["Shared IPs"].append(ip)

    rows = []

    for account, data in account_ip_map.items():
        unique_ips = sorted(set(data["Shared IPs"]))

        if len(unique_ips) > 1:
            rows.append({
                "Account": data["Account"],
                "Customer": data["Customer"],
                "Shared IP Count": len(unique_ips),
                "Shared IPs": ", ".join(unique_ips)
            })

    return pd.DataFrame(rows)

if st.session_state.selected_ip is not None:
    selected_ip = st.session_state.selected_ip
    selected_type = st.session_state.selected_ip_type

    if selected_type == "signup":
        st.title("Signup IP Detail")
        st.subheader(f"Linked Signup Accounts for IP: {selected_ip}")
        detail_df = signup_ip_accounts[signup_ip_accounts["Signup IP"] == selected_ip].copy()
    else:
        st.title("Login IP Detail")
        st.subheader(f"Linked Login Accounts for IP: {selected_ip}")
        detail_df = related_accounts_detail.get(selected_ip, pd.DataFrame()).copy()

    if not detail_df.empty:
        total_accounts = len(detail_df)
        total_risk_accounts = int(detail_df["Risk Account"].sum())

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Linked Accounts", total_accounts)
        with c2:
            st.metric("Risk Accounts", total_risk_accounts)

        st.markdown("### Linked Accounts Detail")
        detail_df = add_row_numbers(detail_df)
        styled_detail_df = detail_df.style.apply(highlight_risk_row, axis=1)
        st.dataframe(styled_detail_df, use_container_width=True)

        st.caption("Accounts highlighted in red are risk accounts.")
    else:
        st.warning("No linked accounts found for this IP.")

    if st.button("Back to Search", key="back_to_search"):
        st.session_state.selected_ip = None
        st.session_state.selected_ip_type = None
        st.rerun()

else:
    st.title("IP Report")
    st.subheader("Search by Account or IP")

    default_index = 0 if st.session_state.last_search_type == "Account" else 1

    search_type = st.radio(
        "Search Type",
        ["Account", "IP"],
        horizontal=True,
        index=default_index
    )

    search_input = st.text_input(
        "Type search value",
        value=st.session_state.last_search_input,
        placeholder="Example: A20456, A40023 or 563.123.256.33"
    )

    if st.button("Search"):
        st.session_state.last_search_type = search_type
        st.session_state.last_search_input = search_input
        st.session_state.search_executed = True

        filtered_related_ips = pd.DataFrame()
        filtered_login_ips = pd.DataFrame()
        filtered_signup_ips = pd.DataFrame()
        filtered_login_ip_accounts = pd.DataFrame()
        filtered_signup_accounts = pd.DataFrame()

        search_clean = search_input.strip().upper()

        if search_clean:
            if search_type == "Account":
                related_ip_matches = account_to_related_ips.get(search_clean, [])
                login_ip_matches = account_to_login_ips_without_relationships.get(search_clean, [])

                signup_ip_match = account_to_signup_ip.get(search_clean)
                signup_ip_matches = [signup_ip_match] if signup_ip_match else []

                filtered_related_ips = related_ips_data[
                    related_ips_data["IP Address"].isin(related_ip_matches)
                ]

                filtered_login_ips = login_ips_without_relationships[
                    login_ips_without_relationships["Login IP"].isin(login_ip_matches)
                ][["Login IP", "Last Login", "Location"]]

                filtered_signup_ips = signup_ips_summary[
                    signup_ips_summary["Signup IP"].isin(signup_ip_matches)
                ]

            else:
                filtered_login_ip_accounts = login_ip_accounts[
                    login_ip_accounts["Login IP"].str.contains(search_clean, case=False, na=False)
                ]

                standalone_login_accounts = login_ips_without_relationships[
                    login_ips_without_relationships["Login IP"].str.contains(search_clean, case=False, na=False)
                ][["Account", "Customer", "Login IP", "Location"]].copy()

                if not standalone_login_accounts.empty:
                    standalone_login_accounts["Country"] = standalone_login_accounts["Location"]
                    standalone_login_accounts["Risk Account"] = False
                    standalone_login_accounts = standalone_login_accounts[
                        ["Account", "Customer", "Login IP", "Country", "Risk Account"]
                    ]

                    filtered_login_ip_accounts = pd.concat(
                        [filtered_login_ip_accounts, standalone_login_accounts],
                        ignore_index=True
                    )

                filtered_signup_accounts = signup_ip_accounts[
                    signup_ip_accounts["Signup IP"].str.contains(search_clean, case=False, na=False)
                ]

        st.session_state.filtered_related_ips = filtered_related_ips
        st.session_state.filtered_login_ips = filtered_login_ips
        st.session_state.filtered_signup_ips = filtered_signup_ips
        st.session_state.filtered_login_ip_accounts = filtered_login_ip_accounts
        st.session_state.filtered_signup_accounts = filtered_signup_accounts

    if st.session_state.search_executed:
        if st.session_state.last_search_type == "Account":
            filtered_related_ips = st.session_state.filtered_related_ips
            filtered_login_ips = st.session_state.filtered_login_ips
            filtered_signup_ips = st.session_state.filtered_signup_ips

            total_ips = len(filtered_related_ips) + len(filtered_login_ips) + len(filtered_signup_ips)
            related_ips_count = len(filtered_related_ips)
            login_without_relationship_count = len(filtered_login_ips)
            signup_ips_count = len(filtered_signup_ips)

            st.markdown("## Summary")
            s1, s2, s3, s4 = st.columns(4)

            with s1:
                st.metric("Total IPs", total_ips)
            with s2:
                st.metric("IPs with Relationships", related_ips_count)
            with s3:
                st.metric("Login IPs without Relationships", login_without_relationship_count)
            with s4:
                st.metric("Signup IPs", signup_ips_count)

            st.markdown("## IPs with Related Accounts")

            if not filtered_related_ips.empty:
                show_ip_summary_table(
                    filtered_related_ips,
                    ip_column="IP Address",
                    related_column="Related Accounts",
                    last_login_column="Last Login"
                )
            else:
                st.warning("No related IPs found.")

            st.markdown("## Accounts Sharing Multiple IPs")

            accounts_sharing_multiple_ips = build_accounts_sharing_multiple_ips(
                related_accounts_detail,
                filtered_related_ips
            )

            if not accounts_sharing_multiple_ips.empty:
                st.dataframe(
                    add_row_numbers(accounts_sharing_multiple_ips),
                    use_container_width=True
                )
            else:
                st.warning("No accounts sharing multiple IPs found.")

            st.markdown("## Signup IP")

            if not filtered_signup_ips.empty:
                show_ip_summary_table(
                    filtered_signup_ips,
                    ip_column="Signup IP",
                    related_column="Related Accounts"
                )
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
            s1, s2 = st.columns(2)

            with s1:
                st.metric("Login IP Accounts", len(filtered_login_ip_accounts))
            with s2:
                st.metric("Signup IP Accounts", len(filtered_signup_accounts))

            st.markdown("## Login IP Accounts")

            if not filtered_login_ip_accounts.empty:
                styled_login_accounts = add_row_numbers(filtered_login_ip_accounts).style.apply(highlight_risk_row, axis=1)
                st.dataframe(styled_login_accounts, use_container_width=True)
                st.caption("Accounts highlighted in red are risk accounts.")
            else:
                st.warning("No accounts found using this IP as Login IP.")

            st.markdown("## Signup IP Accounts")

            if not filtered_signup_accounts.empty:
                styled_signup_accounts = add_row_numbers(filtered_signup_accounts).style.apply(highlight_risk_row, axis=1)
                st.dataframe(styled_signup_accounts, use_container_width=True)
                st.caption("Accounts highlighted in red are risk accounts.")
            else:
                st.warning("No accounts found using this IP as Signup IP.")
