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
                st.metric("Signup IP", len(filtered_signup_ips))

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

