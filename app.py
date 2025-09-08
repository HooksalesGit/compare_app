import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.title("Compare Lists")
st.subheader("Yo se que todavia piensas en mi, si no porque estas aqui?")

with st.form("whatsapp_form"):
    st.write("Send a WhatsApp message to +1 786 553 5043")
    submitted = st.form_submit_button("Send Helloooo")
    if submitted:
        url = "https://wa.me/17865535043?text=Helloooo"
        components.html(f"<script>window.open('{url}');</script>")

uploaded = st.file_uploader(
    "Upload one or more CSVs",
    type="csv",
    accept_multiple_files=True
)

if uploaded:
    # read each file into a DataFrame and record its base-name
    dfs = []
    names = []
    for f in uploaded:
        df = pd.read_csv(f)
        dfs.append(df)
        names.append(f.name.rsplit(".",1)[0])

    # build the comparison
    all_emails = sorted(set().union(*(df['Email'] for df in dfs)))
    out = []
    for email in all_emails:
        row = {'Email': email}
        # pick first matching Name across uploads
        for df in dfs:
            match = df.loc[df['Email']==email, 'Name']
            if not match.empty:
                row['Name'] = match.iloc[0]
                break
        # presence flags
        flags = []
        for df in dfs:
            flags.append('yes' if email in df['Email'].values else 'no')
        for nm, fl in zip(names, flags):
            row[f'In list "{nm}"'] = fl
        row['All the lists'] = 'yes' if all(f=='yes' for f in flags) else 'no'
        out.append(row)

    comp = pd.DataFrame(out)
    st.dataframe(comp)

    # download button
    csv = comp.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Comparison.csv",
        csv,
        file_name="Comparison.csv",
        mime="text/csv"
    )
