# S'importa la llibreria de streamlit per utilitzarla
import streamlit as st
# https://docs.streamlit.io/get-started/installation

# L'estructura de la pàgina cambia a totalment horitzontal per àmbits d'estètica
st.set_page_config(layout="wide")
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config

# S'estableix un títol
st.title("Treball de Recerca")
# https://docs.streamlit.io/develop/api-reference/text/st.title

# S'utilitza la funció de warning per destacar el text 
st.warning("### Què hauria passat si haguessis invertit en una empresa anys enrere amb una estratègia concreta?")
# https://docs.streamlit.io/develop/api-reference/status/st.warning

# S'utilitza la funció de caption per aconseguir que els textos siguin de color gris
st.caption("### - Potser ara series milionari.")
st.caption("### - Potser hauries perdut una gran part dels teus diners.")
st.caption("### - Potser, si haguessis emprat una altra estratègia, hi hauries guanyat molts més diners.")
# https://docs.streamlit.io/develop/api-reference/text/st.caption 

# S'estableix una llínea per diferència el següent apartat
st.divider()
# https://docs.streamlit.io/develop/api-reference/text/st.divider 

# Es marca l'espai amb el delineat
with st.container(border=True):
# #https://docs.streamlit.io/develop/api-reference/layout/st.container 

    # S'utilitza la funció de markdown per triar la mida del text a partir del número de #. 
    # Amb més nombres de # més petita és la lletra
    # Aquest funcionament també és possible amb altres funcions com caption, warning...
    st.markdown("#### Per intentar respondre aquestes hipotètiques situacions, s'ha desenvolupat un simulador capaç de representar inversionsfictícies del passat per analitzar què hauria passat.")
    # https://docs.streamlit.io/develop/api-reference/text/st.markdown
    # https://www.youtube.com/watch?v=OWWGhqL5ylY&t=8s 

    # S'estableix un subtítol
    st.subheader("El simulador es divideix en tres etapes:")
    # #https://docs.streamlit.io/develop/api-reference/text/st.subheader 

    # Es creen diferents columnes per ordenar les diferents explicacions de les etapes
    pas1,pas2,pas3 = st.columns(3)
    # #https://docs.streamlit.io/develop/api-reference/layout/st.columns 

    # S'indica que es traballarà dins de la primera columna:
    with pas1:
        # Es marca l'espai amb el delineat
        with st.container(border=True):

            # S'estableixen dos subtítols
            st.subheader("Etapa 1.")
            st.subheader("Establir les dades de la inversió")

            # S'estableix la funció per mostrar l'explicació breu en format de text
            st.text("Estableix el capital inicial, el sector, l'empresa i elperíode de temps depenent de l'estratègia.")
            # https://docs.streamlit.io/develop/api-reference/text/st.text

    # S'indica que es traballarà dins de la segona columna;            
    with pas2:
        # Es marca l'espai amb el delineat
        with st.container(border=True):

            # S'estableixen dos subtítols
            st.subheader("Etapa 2.")
            st.subheader(" Simular la inversió i observar els resultats")

            # S'estableix la funció per mostrar l'explicació breu en format de text
            st.text("Descobreix què hauria passat amb la teva hipotètica inversió.")

    # S'indica que es traballarà dins de la tercera columna; 
    with pas3:

        # Es marca l'espai amb el delineat
        with st.container(border=True):

            # Spestableixen dos subtítols
            st.subheader("Etapa 3.")
            st.subheader("Comparar les diferents simulacions")

            # S'estableix la funció per mostrar l'explicació breu en format de text
            st.text("A l'apartat de comparació, esbrina quina estratègia ha obtingut els millors resultats.")

   