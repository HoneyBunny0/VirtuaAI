import streamlit as st

st.markdown("# Settings ⚙️")
st.sidebar.markdown("# Settings ⚙️")

accuracy = st.checkbox("Accuracy percent visible", True)

def getAccuracyVisible():
    return accuracy
