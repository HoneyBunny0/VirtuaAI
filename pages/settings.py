import re
import streamlit as st

st.markdown("# Settings ⚙️")
st.sidebar.markdown("# Settings ⚙️")

accuracy = st.checkbox("Accuracy percent visible", True)
suggestion = st.checkbox("Suggestion available", True)

def getAccuracyVisible():
    return accuracy

def getSuggestion():
    return suggestion