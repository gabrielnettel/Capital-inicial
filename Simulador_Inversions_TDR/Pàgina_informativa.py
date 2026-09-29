# LLIBRERIES
# S'importa la llibreria Streamlit, necessària per crear la interfície de l'aplicació
import streamlit as st
# https://docs.streamlit.io/get-started/installation


# CONFIGURACIÓ DE LA PÀGINA
# Es configura la pàgina perquè els elements es distribueixin aprofitant tota l'amplada disponible
st.set_page_config(layout="wide")
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config


# TÍTOL I INTRODUCCIÓ DEL TREBALL
# S'estableix el títol principal de la pàgina
st.title("Treball de Recerca")
# https://docs.streamlit.io/develop/api-reference/text/st.title

# Es mostra un missatge destacat per introduir la pregunta inicial del simulador
st.warning("### Què hauria passat si haguessis invertit en una empresa anys enrere amb una estratègia concreta?")
# https://docs.streamlit.io/develop/api-reference/status/st.warning

# Es mostren diferents possibles resultats de la inversió com a introducció del simulador
st.caption("### - Potser ara series milionari.")
st.caption("### - Potser hauries perdut una gran part dels teus diners.")
st.caption("### - Potser, si haguessis emprat una altra estratègia, hi hauries guanyat molts més diners.")
# https://docs.streamlit.io/develop/api-reference/text/st.caption 

# Es crea una línia horitzontal per separar els diferents apartats de la pàgina
st.divider()
# https://docs.streamlit.io/develop/api-reference/text/st.divider 


# PRESENTACIÓ DEL SIMULADOR
# Es crea un contenidor amb una vora per agrupar visualment el contingut introductori
with st.container(border=True):
#https://docs.streamlit.io/develop/api-reference/layout/st.container 

    # Es mostra una introducció al funcionament general del simulador
    st.markdown("#### Per intentar respondre aquestes hipotètiques situacions, s'ha desenvolupat un simulador capaç de representar inversions fictícies del passat per analitzar què hauria passat.")
    # https://docs.streamlit.io/develop/api-reference/text/st.markdown
    # https://www.youtube.com/watch?v=OWWGhqL5ylY&t=8s 

    # Es mostra el subtítol que introdueix les tres etapes del simulador
    st.subheader("El simulador es divideix en tres etapes:")
    # https://docs.streamlit.io/develop/api-reference/text/st.subheader 


    # ORGANITZACIÓ DE LES TRES ETAPES
    # Es divideix l'espai disponible en tres columnes per organitzar les etapes
    col1,col2,col3 = st.columns(3)
    # https://docs.streamlit.io/develop/api-reference/layout/st.columns 


    # ETAPA 1: CONFIGURACIÓ DE LA INVERSIÓ
    # Es treballa dins de la primera columna
    with col1:
        # Es crea un contenidor amb una vora per agrupar el contingut de l'etapa
        with st.container(border=True):

            # Es mostra el número i el títol de la primera etapa
            st.subheader("Etapa 1.")
            st.subheader("Establir les dades de la inversió")

            # Es mostra una breu explicació de les dades que ha d'introduir l'usuari
            st.text("Estableix el capital inicial, el sector, l'empresa i el període de temps depenent de l'estratègia.")
            # https://docs.streamlit.io/develop/api-reference/text/st.text


    # ETAPA 2: SIMULACIÓ DE LA INVERSIÓ
    # Es treballa dins de la segona columna    
    with col2:
        # Es crea un contenidor amb una vora per agrupar el contingut de l'etapa
        with st.container(border=True):

            # Es mostra el número i el títol de la segona etapa
            st.subheader("Etapa 2.")
            st.subheader(" Simular la inversió i observar els resultats")

            # Es mostra una breu explicació de l'objectiu d'aquesta etapa
            st.text("Descobreix què hauria passat amb la teva hipotètica inversió.")


    # ETAPA 3: COMPARACIÓ DELS RESULTATS
    # Es treballa dins de la tercera columna
    with col3:

        # Es crea un contenidor amb una vora per agrupar el contingut de l'etapa
        with st.container(border=True):

            # Es mostra el número i el títol de la tercera etapa
            st.subheader("Etapa 3.")
            st.subheader("Comparar les diferents simulacions")

            # Es mostra una breu explicació de l'objectiu d'aquesta etapa
            st.text("A l'apartat de comparació, esbrina quina estratègia ha obtingut els millors resultats.")

   