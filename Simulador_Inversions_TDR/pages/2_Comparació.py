# LLIBRERIES
# S'importa la llibreria Streamlit, necessària per crear la interfície de l'aplicació
import streamlit as st

# S'importa pandas per treballar i organitzar les dades en estructures tabulars
import pandas as pd

# S'importa Altair per crear gràfics a partir de les dades obtingudes
import altair as alt


# CONFIGURACIÓ DE LA PÀGINA
# Es configura la pàgina perquè utilitzi tota l'amplada disponible
st.set_page_config(
    layout="wide")

# INICIALITZACIÓ DE LES VARIABLES DE SESSIÓ
# Es comprova si existeix la llista de simulacions guardades
# Si no existeix, es crea una llista buida per emmagatzemar les simulacions
if "simulacions_guardades" not in st.session_state:
       st.session_state.simulacions_guardades=[] 


# BARRA LATERAL I SIMULACIONS GUARDADES
# Es crea la barra lateral per mostrar el nombre de simulacions guardades
with st.sidebar:

    # Es defineix el nombre d'espais que es mostraran abans del comptador
    espais_superiors=16
    for i in range(espais_superiors):
        st.title(" ")


     # MOSTRAR SIMULACIONS GUARDADES
    # Es mostra el títol del comptador de simulacions guardades
    st.subheader("Simulacions guardades")

    # Es mostra el nombre de simulacions emmagatzemades a la sessió
    st.metric(
        label="Simulacions guardades",
        value= len(st.session_state.simulacions_guardades),
         # Es manté ocult el text de l'etiqueta
        label_visibility="collapsed"
    )


# TÍTOL DEL COMPARADOR DE SIMULACIONS
# Es mostra el títol principal de la pàgina
st.title("**COMPARACIÓ DE SIMULACIONS**")


# CREAR TARGETES DE LES SIMULACIONS
# Es comprova si hi ha almenys dues simulacions guardades
if len(st.session_state.simulacions_guardades)>1:
     # Es mostra el títol corresponent a la tercera etapa
     st.subheader("Etapa 3")
     # Es mostra el subtítol de les tarjetes de les simulacions
     st.subheader("Tarjetes de les simulacions: ")

     # Es crea un DataFrame a partir de la llista de simulacions guardades
     dades_simulacions_guardades= pd.DataFrame(st.session_state.simulacions_guardades)

     # Es creen dues columnes per distribuir les targetes de les simulacions
     col1,col2=st.columns([1,1])

     # Es recorren totes les files del DataFrame per obtenir les dades de cada simulació
     for index_simulació,simulació in dades_simulacions_guardades.iterrows():
     # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html
         
          # Es comprova si la posició de la simulació és parella
          # Les simulacions parelles es mostren a la columna esquerra
          if index_simulació % 2==0: #aqui mirem el residu
          # https://www.geeksforgeeks.org/python/what-is-a-modulo-operator-in-python/    

              # S'indica que es treballa amb la primera columna
              with col1:

                    # Es crea un contenidor amb una vora per agrupar la informació
                     with st.container(border=True):

                          # Es creen dues altres columnes dins del contenidor
                          col3,col4=st.columns(2)# tiene que estar dentro del borde si quieres que se vea

                          # S'indica que es treballa amb la tercera columna
                          with col3:

                              # Es mostra l'estratègia corresponent a la simulació
                              st.subheader(simulació["Estratègia"])

                              # Es mostra l'empresa corresponent a la simulació
                              st.write("**Empresa**:", simulació["Empresa"])

                               # Es mostra el capital inicial de la simulació
                              st.write("**Capital inicial:**",f"{ simulació["Capital inicial"]:,.2f} USD")

                              # Es mostra el període temporal de la simulació
                              st.write("**Període:**",f"{simulació["Data inici"]}","|",f"{simulació["Data final"]}")

                          # S'indica que es treballa amb la quarta columna
                          with col4: 

                              # Es creen espais per distribuir visualment la informació
                              st.write(" ")
                              st.write(" ")
                              st.write(" ")

                              # Es mostra en gran el valor final de la simulació
                              st.metric(
                              label="**Valor final:**", 
                              value= f"{simulació["Valor final"]:,.2f} USD")  

          # Si la posició és senar, la simulació es mostra a la columna dreta              
          else:

              # S'indica que es treballa amb la segona columna
              with col2:
                  
                  # Es crea un contenidor amb una vora per agrupar la informació
                  with st.container(border=True):

                         # Es creen dues altres columnes dins del contenidor
                         col3,col4=st.columns(2)

                         # S'indica que es treballa amb la tercera columna
                         with col3:

                              # Es mostra l'estratègia corresponent a la simulació
                              st.subheader(simulació["Estratègia"])

                              # Es mostra l'empresa corresponent a la simulació
                              st.write("**Empresa:**", simulació["Empresa"])

                              # Es mostra el capital inicial de la simulació
                              st.write("**Capital inicial:**",f"{ simulació["Capital inicial"]:,.2f} USD")

                              # Es mostra el període temporal de la simulació
                              st.write("**Període:**",f"{simulació["Data inici"]}","|",f"{simulació["Data final"]}")

                         # S'indica que es treballa amb la segona columna
                         with col4:

                              # Es creen espais per distribuir visualment la informació
                              st.write(" ")
                              st.write(" ")
                              st.write(" ")

                              # Es mostra en gran el valor final de la simulació
                              st.metric(
                               label="**Valor final:**", 
                               value= f"{simulació["Valor final"]:,.2f} USD")   

              
               
     # Es crea un divisor per separar les diferents seccions
     st.divider()

     # ELIMINAR SIMULACIONS
     # Es creen dues columnes per distribuir l'espai
     columna_eliminar,columna_espai=st.columns([0.65,2])
     
     # Es crea una nova columna amb informació simplificada per identificar la simulació que es vol eliminar
     dades_simulacions_guardades["Eliminar"] = (dades_simulacions_guardades["Estratègia"]+ " - "+ dades_simulacions_guardades["Empresa"]+" - " +dades_simulacions_guardades["Valor final"].round(2).astype(str))+" USD"
     # https://www.w3schools.com/python/ref_func_round.asp

     # Es selecciona la primera columna
     with columna_eliminar:

          # Es mostra el títol de l'apartat d'eliminació
          st.markdown("##### Eliminar simulació")

          # Es crea un selector amb les simulacions disponibles per eliminar
          simulació_eliminar= st.selectbox(
          label="Eliminar",
          options= dades_simulacions_guardades["Eliminar"],
          label_visibility="collapsed"

     ) 

     # Es busca la posició de la simulació seleccionada dins de la llista
     índex_simulació_eliminar= dades_simulacions_guardades["Eliminar"].tolist().index(simulació_eliminar)
     
                                                                 
     # Es crea un botó per confirmar l'eliminació de la simulació
     boto_acceptar_eliminació= st.button(
     label="Acceptar"
     )

     # Es crea un divisor per separar les seccions
     st.divider()

    # Es comprova si s'ha premut el botó d'eliminació
     if boto_acceptar_eliminació== True:

          # S'elimina de la llista la simulació situada a la posició seleccionada
          st.session_state.simulacions_guardades.pop(índex_simulació_eliminar)
          # https://www.freecodecamp.org/espanol/news/funcion-pop-en-python/ 

          # Es reinicia l'aplicació per actualitzar la informació mostrada
          st.rerun() #actualitzar la taula



     # PREPARAR DADES DELS GRÀFICS
     # Es crea una nova columna que identifica cada simulació mitjançant l'estratègia, l'empresa, el capital inicial i el període
     dades_simulacions_guardades["Nom"] = (dades_simulacions_guardades["Estratègia"]+ " - "+ dades_simulacions_guardades["Empresa"]+" - "+dades_simulacions_guardades["Capital inicial"].astype(str) # Amb astype s'indica que es treballa amb un número
                                           +" - "+ dades_simulacions_guardades["Data inici"].astype(str)+" | "+dades_simulacions_guardades["Data final"].astype(str))
                                           # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html

     # Es converteix la columna "Nom" en una llista
     noms_simulacions = dades_simulacions_guardades["Nom"].tolist()
     # https://pandas.pydata.org/docs/reference/api/pandas.Series.to_list.html

     # Es crea una escala de colors per associar un color a cada simulació
     escala_colors_simulacions = alt.Scale(
     # https://altair-viz.github.io/user_guide/generated/core/altair.Scale.html
       domain=noms_simulacions
     )

     # Es crea una taula amb el nom i el valor final de cada simulació per utilitzar aquestes dades en el gràfic corresponent
     dades_grafic_valor_final = dades_simulacions_guardades[["Nom", "Valor final"]]
     # https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html


     # Es crea un gràfic circular per comparar els valors finals de les simulacions
     gràfic_valor_final = alt.Chart(dades_grafic_valor_final).mark_arc(outerRadius=130).encode(  
         
        # Es representa el valor final de cada simulació 
        theta="Valor final:Q",

        # Es diferencia cada simulació mitjançant el seu color i s'oculta la llegenda
        color=alt.Color("Nom:N",scale=escala_colors_simulacions,legend=None)

     # https://altair-viz.github.io/altair-viz-v4/user_guide/encoding.html
     # https://altair-viz.github.io/user_guide/marks/arc.html

     ).properties(height=350)


     # Es crea una taula amb el nom i el benefici de cada simulació per utilitzar aquestes dades en el gràfic corresponent
     dades_grafic_benefici = dades_simulacions_guardades[["Nom","Benefici"]]


     # Es crea un gràfic de barres per comparar el benefici de les simulacions
     gràfic_benefici= alt.Chart(dades_grafic_benefici).mark_bar(width=40).encode(
         # Es representa el benefici a l'eix vertical

         y=alt.Y("Benefici:Q",title=None),

         # Es relaciona cada barra amb el nom de la simulació
         x=alt.X("Nom:N",axis=None, #axis en relaida es para lo de vertical o horizontal
         # https://altair-viz.github.io/user_guide/customization.html

         # Es configura l'eix del gràfic
         scale= alt.Scale(padding=10)),

         # Es diferencia cada simulació mitjançant el seu color i s'oculta la llegenda
         color=alt.Color("Nom:N",scale=escala_colors_simulacions,legend=None))

     # Es crea una taula amb el nom i la rendibilitat de cada simulació per utilitzar aquestes dades en el gràfic corresponent
     

     # Es crea una taula amb el nom i la volatilitat de cada simulació per utilitzar aquestes dades en el gràfic corresponent
     dades_grafic_volatilitat = dades_simulacions_guardades[
     ["Nom", "Volatilitat"]
          ]

     # Es crea un gràfic de barres per comparar la volatilitat
     gràfic_volatilitat = alt.Chart(
     dades_grafic_volatilitat
     ).mark_bar(width=43).encode(

     # Es representa la volatilitat a l'eix vertical
     y=alt.Y("Volatilitat:Q",title=None),

     # Es representa cada simulació a l'eix horitzontal
     x=alt.X("Nom:N",axis=None,scale=alt.Scale(padding=10)),

     # Es diferencia cada simulació mitjançant el seu color
     color=alt.Color("Nom:N",scale=escala_colors_simulacions,legend=None)
     ).properties(height=355)


     
     # Es crea una taula amb el nom i el Sharpe de cada simulació per utilitzar aquestes dades en el gràfic corresponent
     dades_grafic_sharpe = dades_simulacions_guardades[
          ["Nom", "Sharpe"]]

     # Es crea un gràfic de barres per comparar el Sharpe
     gràfic_sharpe = alt.Chart(
     dades_grafic_sharpe
     ).mark_bar(width=43).encode(

     # Es representa el Sharpe a l'eix vertical
     y=alt.Y("Sharpe:Q",title=None),

     # Es representa cada simulació a l'eix horitzontal
     x=alt.X("Nom:N",axis=None,scale=alt.Scale(padding=10)
     ),

     # Es diferencia cada simulació mitjançant el seu color
     color=alt.Color("Nom:N",scale=escala_colors_simulacions,legend=None)
     ).properties(height=350)

     
     # Es creen tres llistes per preparar les dades del gràfic d'evolució
     # Es crea una llista per emmagatzemar els noms de les simulacions
     noms_evolució_simulacions=[]
     # Es crea una llista per emmagatzemar les dates
     dates_evolució_simulacions=[]
     # Es crea una llista per emmagatzemar els valors de capital
     capital_evolució_simulacions=[]

    # Es recorren totes les simulacions guardades per obtenir-ne l'evolució del capital
     for index_simulació,simulació in dades_simulacions_guardades.iterrows():

         # Es recorren tots els valors de l'evolució del capital de la simulació actual
         for i in range(len(simulació["Evolució capital"])):# evolucio capital porque tiene todos los datos

             # S'afegeix el nom de la simulació a la llista corresponent
             noms_evolució_simulacions.append(simulació["Nom"])

             # S'afegeix la data corresponent a la llista d'evolució
             dates_evolució_simulacions.append(simulació["Evolució dates"][i])

             # S'afegeix el valor del capital corresponent a la llista d'evolució
             capital_evolució_simulacions.append(simulació["Evolució capital"][i])


     # Es combinen les tres llistes en una única estructura mitjançant zip
     dades_evolució= zip(noms_evolució_simulacions,dates_evolució_simulacions,capital_evolució_simulacions)

     # Es crea un DataFrame amb el nom, la data i el capital de cada simulació
     dades_grafic_evolució=pd.DataFrame(
         dades_evolució,
         columns=["Nom","Dates","Capital"]
     ) 

     # Es crea un gràfic lineal per representar l'evolució del capital de cada simulació
     gràfic_evolució= alt.Chart(dades_grafic_evolució).mark_line().encode(
         # Es representen les dates a l'eix horitzontal
         x="Dates:T",

         # Es representen els valors del capital a l'eix vertical
         y="Capital:Q", 

         # Es diferencia cada simulació mitjançant el seu color
         color=alt.Color("Nom:N",scale=escala_colors_simulacions,legend=None)
     )

     # Es defineix l'altura del gràfic d'evolució
     gràfic_evolució=(gràfic_evolució).properties(
         height=500
     )


     # COMPARAR SIMULACIONS
     # Es comprova si existeix l'estat "Comparar" si no existeix, es crea amb valor inicial False
     if "Comparar" not in st.session_state:
          st.session_state.Comparar = False

     # Es crea el botó per iniciar la comparació de les simulacions
     boto_comparar= st.button(
          label="Comparar"
     )

     # Es comprova si s'ha premut el botó de comparació
     if boto_comparar==True:
          st.session_state.Comparar=True

     # Es comprova si la comparació està activa
     if st.session_state.Comparar ==True:


          # MOSTRAR LLEGENDA
          # Es calcula l'altura necessària per mostrar la llegenda en funció del nombre de simulacions guardades
          altura_llegenda = ((len(dades_simulacions_guardades) + 1) // 2) * 80

          # Es crea una taula que conté únicament els noms de les simulacions
          dades_llegenda = dades_simulacions_guardades[["Nom"]]

          # Es crea un gràfic de punts transparent per generar la llegenda amb un color diferent per a cada simulació
          llegenda = alt.Chart(dades_llegenda).mark_point(
          opacity=0).encode(color=alt.Color( "Nom:N",scale=escala_colors_simulacions,legend=alt.Legend(orient="top",columns=1,labelLimit=2000,title=None,labelFontSize=20))).properties(
          height=altura_llegenda)
           # https://altair-viz.github.io/user_guide/marks/point.html

          # Es mostra el subtítol de la llegenda
          st.subheader("Llegenda")

          # Es mostra la llegenda creada
          st.altair_chart(llegenda)


          # MOSTRAR GRÀFIC I TAULA
          # Es creen dues pestanyes per separar el gràfic i la taula
          tab_grafic, tab_taula = st.tabs(["Gràfic"," Taula" ])
          # https://docs.streamlit.io/develop/api-reference/layout/st.tabs
               

          # Es selecciona la pestanya del gràfic
          with tab_grafic:

               # Es mostra el gràfic amb l'evolució del capital
               st.altair_chart(gràfic_evolució,use_container_width=True# ocupa el maxim de amplada possible, ns si cal de veirta
          )

          # Es selecciona la pestanya de la taula
          with tab_taula:

               # Es crea una còpia de la taula eliminant les columnes que no són necessàries per a la visualització
               dades_simulacions_visualització = dades_simulacions_guardades.drop(columns=["Nom","Evolució capital","Evolució dates","Eliminar"] )# poniendo clums no hace falta axis=1

               # Es mostra la taula amb les dades de les simulacions i s'oculta l'índex
               st.dataframe(dades_simulacions_visualització,hide_index=True # hide_index no es pot fer ma st.write
               )


          # GRÀFICS DE GUANYS
          # Es crea un divisor per separar les seccions
          st.divider()

          # Es mostra el títol de l'apartat de guanys
          st.subheader("GUANYS")

          # Es creen dues columnes per distribuir els gràfics dels guanys
          col1, col2 = st.columns([1, 1])

          # Es selecciona la primera columna
          with col1:

           # Es mostra el gràfic del valor final dins d'un contenidor amb una vora
            with st.container(border=True):
               st.subheader("Valor final")
               st.altair_chart(
                    gràfic_valor_final,
                    use_container_width=True
               )

          # Es selecciona la segona columna
          with col2:
            
                # Es mostra el gràfic del benefici dins d'un contenidor amb una vora
                with st.container(border=True):
                              st.subheader("Benefici")
                              st.altair_chart(
                                   gràfic_benefici,
                                   use_container_width=True
                              )
                         


          # GRÀFICS DE RISC
          # Es crea un divisor per separar les seccions
          st.divider()

          # Es mostra el títol de l'apartat de risc
          st.subheader("RISC")
          

          # Es creen dues columnes per distribuir els gràfics de risc
          col1, col2 = st.columns([1, 1])

          # Es selecciona la primera columna
          with col1:
           
                # Es mostra el gràfic del Sharpe dins d'un contenidor amb una vora
               with st.container(border=True):
                st.subheader("Sharpe")

                st.altair_chart(
                    gràfic_sharpe,
                    use_container_width=True
               )
          
     
          # Es selecciona la segona columna
          with col2:

            # Es mostra el gràfic de la volatilitat dins d'un contenidor amb una vora
            with st.container(border=True):
               st.subheader("Volatilitat")

               st.altair_chart(
                    gràfic_volatilitat,
                    use_container_width=True
               )


# AVÍS DE SIMULACIONS INSUFICIENTS
# En el cas que no hi hagin simulaicons guardadas, t'avisar
else: 
      st.markdown("#### Per fer servir l'espai de comparació de simulacions primer ha de guardar com a mínim dos simulacions.")
 