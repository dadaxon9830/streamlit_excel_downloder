import streamlit as st

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
def callback():
    st.session_state.button_clicked=True
if (
st.sidebar.button("Open next part",on_click=callback)
or st.session_state.button_clicked
 ):
    st.write("v")
    # if st.button("Pop out balloons"):
    sll=st.multiselect("whic",["va","ba"])
    if sll:
        st.write(sll)