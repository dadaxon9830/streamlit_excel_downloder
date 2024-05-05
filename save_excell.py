import streamlit as st
import pandas as pd
from io import BytesIO

df=pd.DataFrame({'Num_col': [1000, 2000, 3000], 'Comma_col': [4000, 5000, 6000], 'PC_col': [18, 83, 64]})
st.dataframe(df)

flnme = st.text_input('Enter Excel file name (e.g. email_data.xlsx)')
if flnme != "":
    if flnme.endswith(".xlsx") == False:  # add file extension if it is forgotten
        flnme = flnme + ".xlsx"

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Report')

    st.download_button(label="Download Excel workbook", data=buffer.getvalue(), file_name=flnme, mime="application/vnd.ms-excel")