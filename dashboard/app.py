import streamlit as st
from prompt_lab.core import PromptLab
st.title('Prompt Experiments'); l=PromptLab(); eid=st.number_input('Experiment ID',min_value=1,value=1)
if st.button('Load results'): st.json(l.results(int(eid)))
