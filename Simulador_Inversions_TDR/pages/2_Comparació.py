# Importo totes les llibreries
import streamlit as st
import pandas as pd
import altair as alt

# Congifuro per a que la pàgina sigui horitzontal
st.set_page_config(
    layout="wide")


    
# Establir una condició per a que  st.session_state.Simulacions_guardades sigui una llista i es vagi guardant tota l'estona a "l'armari"
if "Simulacions_guardades" not in st.session_state:
       st.session_state.Simulacions_guardades=[] 

# # Comptador de simulacions guardades a l'esquerra
with st.sidebar:

    # Espais
    veces=16
    for i in range(veces):
        st.title(" ")

     # SubtítolF
    st.subheader("Simulacions guardades")

    # Mostro el comptador de simulacions guardades ( només el numero)
    st.metric(
        label="Simulacions guardades",
        value= len(st.session_state.Simulacions_guardades),
        # Elimino el texte
        label_visibility="collapsed"
    )

# Títol 
st.title("**COMPARACIÓ DE SIMULACIONS**")

# En el cas que la llista de simulacons_guardades sigui major a 0, és a dir que hi hagi una o més entra aqui
if len(st.session_state.Simulacions_guardades)>1:
     # Subtitols
     st.subheader("Etapa 3")
     st.subheader("Tarjetes de les simulacions: ")

     # I creo una taula de tots els elements guardats de la simulació amb el seu valor corresponent
     taula_simulacions_guardades= pd.DataFrame(st.session_state.Simulacions_guardades)

     # Columnes
     a1,a2=st.columns([1,1])

     # Ara per cada element, el seu index, recorre una filera per una filera la taula de simulacions guardades gràcias a iterrows
     for numero,fila in taula_simulacions_guardades.iterrows(): #posem número perquè sinó  tidnria (0,empresa) i llavors fila["empresa"] no funcionaria perquè tmb hi ha el número. iterrows pasa n´´umero por número
     # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html
         
          # En el cas que sigui el nombre del index parell entra en aquesta condicio
          # De aquesta manera creo un mecanisme on si es parell es vegi la tarjetetea a la esquerra i si es imparell a la dreta
          if numero % 2==0: #aqui mirem el residu

          # https://www.geeksforgeeks.org/python/what-is-a-modulo-operator-in-python/    
              # En la columna de la esquerra
              with a1:
                    # Amb contorn
                     with st.container(border=True):
                          r1,r2=st.columns(2)# tiene que estar dentro del borde si quieres que se vea
                          with r1:

                              # Vaig a la fílera d'estràtegia i em retorna el seu valor
                              st.subheader(fila["Estratègia"])

                              # Vaig a la fílera de l'empresa i em retorna el seu valor
                              st.write("**Empresa**:", fila["Empresa"])

                              # Vaig a la fílera deñ capital inicial i em retorna el seu valor
                              st.write("**Capital inicial:**",f"{ fila["Capital inicial"]:,.2f} USD")

                              # Vaig a la fílera del capital inicial i el capital final i em retorna el seu valor
                              st.write("**Període:**",f"{fila["Data inici"]}","|",f"{fila["Data final"]}")

                          with r2: 
                              # Espais
                              st.write(" ")
                              st.write(" ")
                              st.write(" ")

                              # Escric en gran el valor final de la simulació
                              st.metric(
                              label="**Valor final:**", 
                              value= f"{fila["Valor final"]:,.2f} USD")  

          # Si el número es imparell entra en aquesta condició                   
          else:
              with a2:
                  #Amb contorn
                  with st.container(border=True):
                         r1,r2=st.columns(2)

                         with r1:

                              # Vaig a la fílera d'estràtegia i em retorna el seu valor
                              st.subheader(fila["Estratègia"])

                              # Vaig a la fílera de l'empresa i em retorna el seu valor
                              st.write("**Empresa:**", fila["Empresa"])

                              # Vaig a la fílera deñ capital inicial i em retorna el seu valor
                              st.write("**Capital inicial:**",f"{ fila["Capital inicial"]:,.2f} USD")

                              # Vaig a la fílera del capital inicial i el capital final i em retorna el seu valor
                              st.write("**Període:**",f"{fila["Data inici"]}","|",f"{fila["Data final"]}")

                         with r2:
                              # Espais
                              st.write(" ")
                              st.write(" ")
                              st.write(" ")

                              # Escric en gran el valor final de la simulació
                              st.metric(
                               label="**Valor final:**", 
                               value= f"{fila["Valor final"]:,.2f} USD")   

              
               
     #Divisor
     st.divider()

     # A la tuala de simualcions_guardades creo una nova columna on  afegeixo l'estratègia, la empresa, el capital inicial, i el període de temps
     taula_simulacions_guardades["Nom"] = (taula_simulacions_guardades["Estratègia"]+ " - "+ taula_simulacions_guardades["Empresa"]+" - "+taula_simulacions_guardades["Capital inicial"].astype(str)
                                           +" - "+ taula_simulacions_guardades["Data inici"].astype(str)+" | "+taula_simulacions_guardades["Data final"].astype(str))#ha de anar així perque sino spython no pot fer que isgui tot text i allo numeor) #ha de anar amb perèntesis
                                           # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html

     # Converteixo la columna nova de "Nom" en una llista
     noms = taula_simulacions_guardades["Nom"].tolist()
     # https://pandas.pydata.org/docs/reference/api/pandas.Series.to_list.html

     # Aqui creo una escala de colors per després reconèixer els colors dels gràfics
     escala_colors = alt.Scale(
     # https://altair-viz.github.io/user_guide/generated/core/altair.Scale.html
       domain=noms
     )

     # Columnes
     o1,espacio=st.columns([0.65,2])
     
     # Ara creo una nova columna de eliminar la qual només mostrara la estratègia, l'empresa i  el valor final per a que sapigues quina simulacio vols eliminar
     taula_simulacions_guardades["Eliminar"] = (taula_simulacions_guardades["Estratègia"]+ " - "+ taula_simulacions_guardades["Empresa"]+" - " +taula_simulacions_guardades["Valor final"].round(2).astype(str))+" USD"
     # https://www.w3schools.com/python/ref_func_round.asp

     # A la primera colulmna
     with o1:
          st.markdown("##### Eliminar simulació")

          # Creo una recuadre on et surten les diferents simulacions per si vols eliminar alguna
          eliminar= st.selectbox(
          label="Eliminar",
          options= taula_simulacions_guardades["Eliminar"],
          label_visibility="collapsed"

     ) 

     # Després he de calcular quina posició en la llista de tuala_simualcion_guardades és la que es vol eliminar
     posició_eliminar= taula_simulacions_guardades["Eliminar"].tolist().index(eliminar)#tolist() convierte la columna de pandas a una lsita normal porque sino no deja index pq sino pilla los diferentes elementos de las tres cosas i da error i asi lo hacemos una lsita que ahi si se puede: ["Apple", "Microsoft", "Nvidia"]
                                                                 
     # Creo un boto per confirmar que es vol elimianr aquella simulació
     eliminar_aceptar= st.button(
     label="Acceptar"
     )
     #Llinea
     st.divider()
     # Si es prem entra
     if eliminar_aceptar== True:
          # I elimina directament aquella simualció a traves de la seva posició
          st.session_state.Simulacions_guardades.pop(posició_eliminar) #pop elimina
          # I tornem a carregar tot per a que s'actualitzi
          st.rerun() #actualitzar la taula

     # Creo una nova taula per fer el gràfic agafant només les variables de la columna nom i valor final
     taula_grafic_valor_final = taula_simulacions_guardades[["Nom", "Valor final"]]
     # https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html


    # I creo el primer gràfic rodo només del valor final
     grafico_valor_final = alt.Chart(taula_grafic_valor_final).mark_arc(outerRadius=130).encode(  #altair si detecta el mismo nombre... las junta
         # El valor és el valor final
        theta="Valor final:Q",

        # I el color utilizo la columna de escala de colors sense legenda
        color=alt.Color("Nom:N",scale=escala_colors,legend=None)
     # https://altair-viz.github.io/altair-viz-v4/user_guide/encoding.html
     # https://altair-viz.github.io/user_guide/marks/arc.html
     ).properties(height=350)


     # Creo una nova taula per fer el gràfic agafant només les variables de la columna nom i el benefici
     taula_grafic_benefici = taula_simulacions_guardades[["Nom","Benefici"]]

     # I creo el primer gràfic barres només del valor final
     grafico_beneficio= alt.Chart(taula_grafic_benefici).mark_bar(width=40).encode(
         # El valor és el benefici a l'eix y
         y=alt.Y("Benefici:Q",title=None),
         # Amb relació amb el nom
         x=alt.X("Nom:N",axis=None, #axis en relaida es para lo de vertical o horizontal
         # https://altair-viz.github.io/user_guide/customization.html

         scale= alt.Scale(padding=10)),

          # I el color utilizo la columna de escala de colors sense legenda
         color=alt.Color("Nom:N",scale=escala_colors,legend=None))

      # Creo una nova taula per fer el gràfic agafant només les variables de la columna nom i la rendibiliata
     taula_grafic_rendibilitat= taula_simulacions_guardades[["Nom","Rendibilitat"]]


     # Cre tres llistes per després crear els gràfics
     # Una dels noms
     noms_evolució=[]
     # Una altre de les dates i la seva evolució
     dates_evolució=[]
     # I l'ultima del capital i la seva evouclió
     capital_evolució=[]

     # Aqui li dic que vagi recorrent filera per filera per obtenir tota l'evolució dels capitals que es va guarda previament
     for numero,fila_1 in taula_simulacions_guardades.iterrows():

         
         for i in range(len(fila_1["Evolució capital"])):# evolucio capital porque tiene todos los datos

             # I guardo el nom a la llista de noms
             noms_evolució.append(fila_1["Nom"])

             # Les dates a la llista de evolució de dates
             dates_evolució.append(fila_1["Evolució dates"][i])

             # I el capital a la llista de l'evolució del capital
             capital_evolució.append(fila_1["Evolució capital"][i])


     #Ara que le tres llistes ja estan plenes les ajunto totes tres amb zip
     ajuntar_dades= zip(noms_evolució,dates_evolució,capital_evolució)

     # I hi creo una taula amb el Nom, la data i el capital
     taula_grafic_evolució=pd.DataFrame(
         ajuntar_dades,
         columns=["Nom","Dates","Capital"]
     ) 


     
     

     # Seguidament represento el gràfic lineal de cada simualció per a que es vegi la comparació
     grafico_evolució= alt.Chart(taula_grafic_evolució).mark_line().encode(
         x="Dates:T",
         y="Capital:Q", #no admet cap espai
         color=alt.Color("Nom:N",scale=escala_colors,legend=None)
     )

     # 
     grafico_evolució=(grafico_evolució).properties(
         height=500
     )


     

     

     # Creo una condició per a que  st.session_state.Comparar comenci falsa
     if "Comparar" not in st.session_state:
          st.session_state.Comparar = False

     # I un boto de comparar la simualció
     comparar_boto= st.button(
          label="Comparar"
     )

     # Si es prem el boto  st.session_state.Comparar es tornara True
     if comparar_boto==True:
          st.session_state.Comparar=True

     # Si  st.session_state.Comparar es torna true entra en aqusta condició
     if st.session_state.Comparar ==True:

          # I creo una fórmula per calcular depenent el númeor de simulacion l'espai que es necessitarà
          altura_leyenda = ((len(taula_simulacions_guardades) + 1) // 2) * 70

          #Mirar pq abans no funcionaba = error
          taula_leyenda = taula_simulacions_guardades[["Nom"]]

          #I creo el gràfic per a que cada elemnt que hi hagi a la columna de Nom es representi amb el seu color i un punt al principi
          leyenda = alt.Chart(taula_leyenda).mark_point(
      opacity=0).encode(color=alt.Color( "Nom:N",scale=escala_colors,legend=alt.Legend(orient="top",columns=1,labelLimit=2000,title=None,labelFontSize=20))).properties(
      height=altura_leyenda)
     # https://altair-viz.github.io/user_guide/marks/point.html

          # Subtitol
          st.subheader("Llegenda")

          # I el represento
          st.altair_chart(leyenda)

          # Creo diferents caselles per representar el gràfic i la taula
          tab_grafic, tab_taula = st.tabs(["Gràfic"," Taula" ])
          # https://docs.streamlit.io/develop/api-reference/layout/st.tabs
               

          # Si la casella es te tab_grafic
          with tab_grafic:

               # Es representara el gràfic
               st.altair_chart(grafico_evolució,use_container_width=True# ocupa el maxim de amplada possible, ns si cal de veirta
          )

          # En canvi si la casella es de tab_taula
          with tab_taula:

               
               taula_simulacions_guardades_noves = taula_simulacions_guardades.drop(columns=["Nom","Evolució capital","Evolució dates","Eliminar"] )# poniendo clums no hace falta axis=1

               # Es representara la taula amb totes les dades sense les columnes inecessaries
               st.dataframe(taula_simulacions_guardades_noves,hide_index=True # hide_index no es pot fer ma st.write
               )


          
         

          # Llinea
          st.divider()
          # Subtitol
          st.subheader("GUANYS")


          # Creo dues columnes per mostrar el valor final
          v1, v2 = st.columns([1, 1])

          with v1:
           a1,a2=st.columns([7,0.2])

           with a1:
            
           
              

            # I a la ensenyo el gràfic
            with st.container(border=True):
               st.subheader("Valor final")
               st.altair_chart(
                    grafico_valor_final,
                    use_container_width=True
               )

          # Seguidament creo altres dos columnes per representar el benefici
          with v2:
           b1, b2 = st.columns([7, 0.1])

           with b1:
            
           
          
              

            #I el g`rafic del benefici`
             with st.container(border=True):
                              st.subheader("Benefici")
                              st.altair_chart(
                                   grafico_beneficio,
                                   use_container_width=True
                              )
                              

          
     

          # I agafo nomes la columna de nom i volatitilitat pel seu gràfic
          taula_grafic_volatilitat = taula_simulacions_guardades[
          ["Nom", "Volatilitat"]
               ]

          #I creo el gràfic de volatilita
          grafico_volatilitat = alt.Chart(
          taula_grafic_volatilitat
          ).mark_bar(width=43).encode(
          y=alt.Y("Volatilitat:Q",title=None),
          x=alt.X("Nom:N",axis=None,scale=alt.Scale(padding=10)),
          color=alt.Color("Nom:N",scale=escala_colors,legend=None)
          ).properties(height=355)


          

          # I agafo nomes la columna de nom i sharpe pel seu gràfic
          taula_grafic_sharpe = taula_simulacions_guardades[
               ["Nom", "Sharpe"]]

          #I creo el gràfic de Sharpe
          grafico_sharpe = alt.Chart(
          taula_grafic_sharpe
          ).mark_bar(width=43).encode(
          y=alt.Y("Sharpe:Q",title=None),
          x=alt.X("Nom:N",axis=None,scale=alt.Scale(padding=10)
          ),
          color=alt.Color("Nom:N",scale=escala_colors,legend=None)
          ).properties(height=350)

          #Llinea
          st.divider()
          # Subtitol
          st.subheader("RISC")
          

          # Creo dues columens per representar la volatilitat
          r1, r2 = st.columns([1, 1])

          # A la primera columna
          with r1:
           
         # A la primera columna represento el gràfic de Sharpe
               with st.container(border=True):
                st.subheader("Sharpe")

                st.altair_chart(
                    grafico_sharpe,
                    use_container_width=True
               )
          #I a la segona columna 
     

          # A la segona columna represento el gràfic de la volatitlita
          with r2:
           
            with st.container(border=True):
               st.subheader("Volatilitat")

               st.altair_chart(
                    grafico_volatilitat,
                    use_container_width=True
               )


          

# En el cas que no hi hagin simulaicons guardadas, t'avisar
else: 
      st.markdown("#### Per fer servir l'espai de comparació de simulacions primer ha de guardar com a mínim dos simulacions.")
 