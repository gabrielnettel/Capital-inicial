import streamlit as st

pas1,pas2,pas3 = st.columns(3)
with pas1:
    st.subheader("1.")
    st.subheader("Tria els teus criteris d'inversió")
    st.text("Estableixi el capital inicial, el període de temps,\nuna estratègia i finalment el sector i l'empresa")# mirar que es lo que st.text dejaba i write no, creo que era negrtia

with pas2:
    st.subheader("2.")
    st.subheader("Vegi el resultat de la seva simulació")
    st.text("Descubreixi que haguès passat amb la seva hipotètica inversió")
with pas3:
    st.subheader("3")
    st.subheader("Compari diferents simulacions")
    st.text("En l'apartat de comparar esbrini quin mètode té mes eficàcia")