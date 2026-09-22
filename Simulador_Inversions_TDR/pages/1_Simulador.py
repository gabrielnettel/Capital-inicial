import streamlit as st
# https://docs.streamlit.io/get-started/installation
import datetime# per la data
# https://www.w3schools.com/python/python_datetime.asp 
import yfinance as yh 
# https://pypi.org/project/yfinance/
import pandas as pd
# https://pandas.pydata.org/docs/getting_started/install.html
import altair as alt
# https://altair-viz.github.io/getting_started/installation.html

st.set_page_config(layout="wide")
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config 

# Li dic al armari que simulacio_feta no comenci existint, el boto és (boto_per_simular)
if "simulacio_feta" not in st.session_state: 
    st.session_state.simulacio_feta = False

# Li dic al armari que Simulacions_guardades no comenci existint, el boto és ("guardar_simulació")
if "Simulacions_guardades" not in st.session_state:
    st.session_state.Simulacions_guardades = []
# https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state 

# Estableixo una condició per a que   st.session_state.boto_1 comenci sent falsa          
if "boto_1" not in st.session_state: #és ST. session"_"state
 st.session_state.boto_1=False


# Comptador de simulacions guardades a l'esquerra
with st.sidebar:
#https://docs.streamlit.io/develop/api-reference/layout/st.sidebar
    veces=16
    for i in range(veces):
    # https://www.geeksforgeeks.org/python/python-range-function/
        st.title(" ")
    # https://docs.streamlit.io/develop/api-reference/text/st.title
  
  
    st.subheader("Simulacions guardades")
    #https://docs.streamlit.io/develop/api-reference/text/st.subheader 
    st.metric(
        label="Simulacions guardades",
        value= len(st.session_state.Simulacions_guardades), 
        #https://www.w3schools.com/python/ref_func_len.asp
        label_visibility="collapsed")
        # https://docs.streamlit.io/develop/api-reference/data/st.metric 
    

    
# Diccionari de tickers, relaciona cada empresa amb el seu ticker a Yahoo finance
dicci_tickers= {
    # Tecnologia
    "Apple": "AAPL","Microsoft": "MSFT","Nvidia": "NVDA","TSMC": "TSM","Adobe": "ADBE",

    # Finançer
    "JPMorgan Chase": "JPM","Goldman Sachs": "GS","American Express": "AXP","Visa": "V","Mastercard": "MA",

    # Serveis digitals
    "Amazon": "AMZN","eBay": "EBAY","Booking Holdings": "BKNG","Cisco Systems": "CSCO","Alphabet": "GOOG",

    # Energia
    "ExxonMobil": "XOM","Chevron": "CVX","NextEra Energy": "NEE","AES": "AES","EQT": "EQT",

    # Salut
    "UnitedHealth Group": "UNH","McKesson": "MCK","CVS Health": "CVS","Amgen": "AMGN","Pfizer": "PFE",

    # Inmobiliari
    "D.R. Horton": "DHI","Lennar": "LEN","Hovnanian Enterprises": "HOV","PulteGroup": "PHM","Toll Brothers": "TOL",

    # Automoció
    "Volkswagen": "VWAGY","Toyota": "TM","PACCAR": "PCAR","Ford": "F","Honda": "HMC",

    # Consum
    "Walmart": "WMT","Nestlé": "NSRGY","Coca-Cola": "KO","PepsiCo": "PEP","Procter&Gamble": "PG",
    }
#https://www.w3schools.com/python/python_dictionaries.asp 

# Títols i subtituls
st.title("SIMULADOR D'INVERSIONS")
#OK

st.subheader("Etapa 1")
#OK

# Columnes per poder distribuir i col·locar
dades_inversió,x=st.columns(2)
#https://docs.streamlit.io/develop/api-reference/layout/st.columns

# Aquí és on es demano totes les dades inicial per després realitzar la simulació
with dades_inversió:
    # Marcar el fons del quadrat
    with st.container(border=True):
    #https://docs.streamlit.io/develop/api-reference/layout/st.container

        st.header("Dades de la inversió")
        # https://docs.streamlit.io/develop/api-reference/text/st.header

        # Demano el capital inicial amb una barra deslizable
        capital = st.slider(
            label = "Introdueix el capital inicial:",
            min_value= 100,
            max_value=50000,
            value= 15000,
            step=100,
        #https://docs.streamlit.io/develop/api-reference/widgets/st.slider     
        )

        # Estableixo una funció per al canvi d'estratègia per després posar tots els botons en False, és a dir que tot el que mostraven aquells boton ho deixin de fer
        def canvi_estratègia():
            st.session_state.simulacio_feta = False
            st.session_state.Simulació_començada =False
            st.session_state.boto_1=False
        #https://www.youtube.com/watch?v=oBiuR_Z2ac4&t=11s
           
        # Demano que es trii l'estratègia 
        estratègia= st.selectbox(
            label= "Tria l'estratègia",
            options= ["Buy&Hold","Dollar Cost Averaging(DCA)","Stop-Loss i Take-Profit","Diversificació"],
            # https://www.w3schools.com/python/python_lists.asp

            # S'emprà la funció de on_change per així cada cop que es canviï l'estratègia s'executi aquesta funció
            on_change= canvi_estratègia # Anotació: No hi ha cap parèntesis
            )
        #https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Estableixo una funció per al canvi de sector per després posar tots els botons en False, és a dir que tot el que mostraven aquells boton ho deixin de fer
        def canvi_sector():
             st.session_state.simulacio_feta=False
             st.session_state.Simulació_començada = False
             st.session_state.boto_1=False
        # OK
        # Aqui dic que si la estrategia no es igual a Diversificació, és a dir a totes les restants, que entri en aquest if, que es triar l'empresa individual i el sector, es així perquè a Diversificació es realitza amb més d'una empresa
        if estratègia != "Diversificació": 
        # https://www.geeksforgeeks.org/python/python-not-equal-operator/

            # Demano que es trii el sector en que es vulgui invertir
            sector= st.selectbox( # no multi select perquè vull que triin una 
                label ="Tria el sector",
                options =["Tecnologia","Financer","Serveis digitals","Energia","Salut","Inmobiliari","Automoció","Consum"],# ha de ser options sí o sí
                on_change=canvi_sector
            )
            # OK

            # Estableixo una funció per al canvi d'empresa per després posar tots els botons en False, és a dir que tot el que mostraven aquells boton ho deixin de fer
            def canvi_empresa():
                 st.session_state.simulacio_feta=False
                 st.session_state.Simulació_començada=False   
                 st.session_state.boto_1=False# divers
            # OK

            # Aqui estableixo condicions les quals em permeten ensenyar les opcions d'empreses depenent del sector triat mitjançant una llista 
            if sector == "Tecnologia":
            # https://stackoverflow.com/questions/35857752/what-do-the-symbols-and-mean-in-python-when-is-each-used
                empresa = st.selectbox( 
                    label ="Tria l'empresa", # Jo prefereixo sempre posar label perquè així és més polit(no és necessari)
                    options = ["Apple", "Microsoft","Nvidia","TSMC","Adobe"],
                    on_change=canvi_empresa
                )
            # OK

            elif sector == "Financer":
            # https://www.freecodecamp.org/espanol/news/sentencias-if-elif-y-else-en-python/
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["JPMorgan Chase","Goldman Sachs","American Express","Visa","Mastercard"],
                on_change=canvi_empresa
                )
            elif sector == "Serveis digitals":
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["Amazon","eBay","Booking Holdings","Cisco Systems","Alphabet"],
                on_change=canvi_empresa
                )
            elif sector == "Energia":
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["ExxonMobil","Chevron","NextEra Energy","AES","EQT"],
                on_change=canvi_empresa
                )
            elif sector == "Salut":
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["UnitedHealth Group","McKesson","CVS Health","Amgen","Pfizer"],
                on_change=canvi_empresa
                )

            elif sector == "Inmobiliari":
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["D.R. Horton","Lennar","Hovnanian Enterprises","PulteGroup","Toll Brothers"],
                on_change=canvi_empresa
                )
            elif sector == "Automoció":
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["Volkswagen","Toyota","PACCAR","Ford","Honda"],
                on_change=canvi_empresa
                )
           
            elif sector == "Consum":
                empresa = st.selectbox(
                label = "Tria l'empresa",
                options=["Walmart","Nestlé","Coca-Cola","PepsiCo","Procter&Gamble"],
                on_change=canvi_empresa
                )
            # OK OK OK OK OK OK OK
            


        # Aqui torno a dir que si la estrategia no es igual a Diversificació, és a dir a totes les restants, que entri en aquest if. Perquè diversificaicó funciona "diferent"
        if estratègia != "Diversificació":
                    # Creo una variable que busqui l'empresa triada al dicci_ticker i que aquesta variable guarda el ticker de l'empresa
                    ticker=dicci_tickers[empresa]
                    # https://www.w3schools.com/python/python_dictionaries_access.asp

                    # Ara amb la variable de empresa_triada li dic a Yahoo finance que creii/cerqui el ticker d'abans per extreu-re l'informació
                    empresa_triada= yh.Ticker(ticker)
                    # https://youtu.be/j0sBKAB75oc?si=5Em2JI4wpwI6HtXy

                    # Amb això demano l'historial de l'empresa i amb period="max" li dic a yf que em doni el màxim periode de temps possible, només faig servir aquesta variable per obtenir el dia "mínim" per quan tries les dates
                    empresa_123=empresa_triada.history(period="max")
                    
                    # https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html

                    # Aqui demano que s'introduexi la data de començament de l'inversió, és a dir, la data inicial
                    data_1= st.date_input(
                    # https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
                        label="Tria la data d'inici",   

                        # Amb el màxim historial de l'empresa, amb .index (la data), demano el primer valor d'aquesta llista amb [0], després amb .to_pydatetime aconsegueixo transformar la taula inicial que em dona .history de l'empresa a un element de dates
                        # I amb .date només agafo la data d'aquell dia sense hores ni minuts, només l'any, el dia i el mes
                        # D'aquesta manera, quan el poso a value, directament l'opció és el primer dia exacte quan es va crear aquesta empresa
                        value= empresa_123.index[0].to_pydatetime().date(),
                        # https://www.ionos.com/digitalguide/websites/web-development/python-pandas-dataframe-indexing/
                        # https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.to_pydatetime.html
                        # https://docs.python.org/es/3/library/datetime.html#datetime.date

                        # El valor mínim ha de ser el dia quan es va crear l'empresa
                        min_value=empresa_123.index[0].to_pydatetime().date(),
                        # Aqui establim que el valor màxim d'aquell dia sigui el dia actual (avui)
                        max_value=datetime.date.today()
                        # https://docs.python.org/es/3.8/library/datetime.html
                        )
                    # Ara demano la data final de la simulació, i té el dia actual predeterminat
                    data_2=st.date_input(
                        label="Tria la data final",
                        value=datetime.date.today(),
                        min_value=empresa_123.index[0].to_pydatetime().date(),
                        max_value=datetime.date.today()
                    )
                    # Amb aquesta condició dic que la data final no pot ser menor o igual a la data inicial
                    if data_2<=data_1:
                    # https://www.geeksforgeeks.org/python/comparing-dates-python/
                                st.write("La data inicial no pot ser superior a la de inici")
                                # https://docs.streamlit.io/develop/api-reference/write-magic/st.write
                    
                    # En el cas que les dates siguin correctes llavors demano ara si la taula que em proporciona yf gràcias a .history de la variable de l'empresa_triada
                    else:
                            taula= empresa_triada.history(
                                # Amb aquest paràmetres aconsegueixo que la taula només em proporcioni la informació de l'empresa de la data inicial fins la data final
                                start=data_1,
                                end= data_2 + datetime.timedelta(days=1),
                                auto_adjust=True
                                )
                            # https://algotrading101.com/learn/yfinance-guide/

                            # Si es donés l'extrany cas de que la taula estigui vuida, llavors aquesta condició t'ho dira
                            if taula.empty:
                            # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.empty.html
                                    st.write("No hi ha dades disponibles per a aquestes dates")
                            
                            else:   # Cambiar open_preu por lo de taula["Open"].iloc[0]
                                    # En el cas que si hi hagi totes les dades llavors demano a la columna de "Open" el preu el qual inicia el dia aquella empresa
                                    # Amb iloc[0] demano el primer element de la columna "Open", és a dir el preu de la data inicial
                                    open_preu_1 = taula["Open"].iloc[0]  
                                    # # Amb iloc[0] demano l'últim element de la columna "Open", és a dir el preu de la data final
                                    open_preu_2 = taula["Close"].iloc[-1]
                                    # https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
                                    # https://medium.com/@icodewithben/understanding-the-iloc-function-in-pandas-da9dec1a1ee1

        # En el cas que l'empresa si sigui divesificació demano les dates per a que es fagi la simulació
        # Tenen dates diferents perquè ja que diversificació utilitza més d'una empresa llavors potser tinc problemes amb establir el valor de la data inicial                        
        else:
              # Demano la data inicial
              data_1div=st.date_input(
              
                   label="Tria la data de inici",
                   value=datetime.date(2000,1,1),
                   min_value=datetime.date(1900,1,1),
                   max_value=datetime.date(2026,1,1)
                   )
              # Demano la data final
              data_2div=st.date_input(
                            
                    label="Tria la data de final",
                    value=datetime.date.today(),
                    min_value=datetime.date(1990,1,1),
                    max_value=datetime.date.today()
                    )
              # Estableixo la mateixa condició de que la data final no pot ser major que la final
              if data_2div<=data_1div:
                    st.write("La data inicial no pot ser superior a la de inici")

              # OK OK OK

        # Estableixo una funció la qual cada cop s'utilitzi directament torni a posar en False tot el que iniciaba el boto_de_simular
        def canvi_mensual_anual():
                st.session_state.simulacio_feta=False
                # OK

        # En el cas que l'estratègia sigui la de Dollar Cost Averaging, entro en aquesta condició
        if estratègia== "Dollar Cost Averaging(DCA)":
                            # Creo que una variable que em permet mitjançant la fórmula transformar els anys del períoda a mesos
                            mesos = (data_2.year * 12+ data_2.month)-(data_1.year*12+ data_1.month)
                            # https://es.stackoverflow.com/questions/513244/como-calcular-el-numero-de-meses-entre-dos-fechas
                            # https://docs.python.org/3/library/datetime.html

                            # Si els mesos són més o iguals de 2 anys llavors també tens l'opció de triar la frequència Anual
                            if mesos >=24:
                                    DCA_opcions = st.selectbox(
                                    label="Tria la freqüència:",
                                    options= ["Mensual","Anual"],
                                    on_change=canvi_mensual_anual
                            # OK
                                )    
                            # Si no compleix la condició d'abans en aquest cas només existirà l'opció de triar la frequència Mensual    
                            else: 
                                DCA_opcions= st.selectbox(
                                    label="Tria la freqüència:",
                                    options=["Mensual"]
                                )
                                st.write("Si desitjes fer-ho anualment el període de temps ha de ser major a 2 anys")
                                st.session_state.simulacio_feta=False                            # OK

            
# Aquest apartat només té ús informatiu, són expandibles que t'informen de què és cada element que es tracta al simulador
with x:
    st.subheader("Informació")
    with st.expander("CAPITAL INICIAL"):
    # https://docs.streamlit.io/develop/api-reference/layout/st.expander
        st.write("Quantitat de diners que s'inverteixen al començament")

    with st.expander("PERÍODE DE TEMPS"):
            st.write("Temps el qual es manté la inversió")
    
    with st.expander("ESTRATÈGIA"):
            st.write("Mètode utilitzat per gertionar els diners durant l'inversió")

            with st.expander("Buy&Hold"):
                st.write("Consisteix a comprar les accions al començament del període i mantenir-les fins al final de la simulació, sense realitzar noves compres ni vendes.")
            with st.expander("Dollar Cost Averaging(DCA)"):
                st.write("Indica cada quant de temps es realitza una nova aportació de capital a la inversió.")
            with st.expander("Stop-Loss i Take-profit"):
                st.write("**Stop-Loss**: És un límit de pèrdua. Si el valor de la inversió baixa fins al percentatge establert, la simulació s'atura.")
                # https://docs.streamlit.io/develop/api-reference/write-magic/st.write
                st.write("**Take-profit**: És un límit de benefici. Si el valor de la inversió puja fins al percentatge establert, la simulació s'atura.")
            with st.expander("Diversificació"):
                st.write("Consisteix a repartir el capital entre diferents empreses per no concentrar tota la inversió en una sola companyia.")
                st.write("**Percentatge**: Indica quina part del capital total es destina a cada empresa.")

    with st.expander("SECTOR"):
            st.write("És l'àmbit econòmic al qual pertany l'empresa seleccionada.")
    with st.expander("EMPRESA"):
            st.write("És la companyia seleccionada sobre la qual es realitzarà la simulació.")

    with st.expander("INDEX DE SECTORS I EMPRESES   "):
            st.write("...")
    # OK OK OK
        
# Creo un boto el qual serà l'encarregat de decidir si es mostren els resultats de la simulació o no
boto=st.button(
label="Simular inversió")
# https://docs.streamlit.io/develop/api-reference/widgets/st.button

# En el cas que el botó es premi, guardem a "l'armari" que s'ha premut
if boto == True:
      st.session_state.simulacio_feta = True
      # OK
# Si s'ha guardat "l'armari" de simulacio_feta llavors comença a ensenyar els resultats
if st.session_state.simulacio_feta==True:

   
    # Poso la condició que si la estratègia triada és buy&hold que entri
    if estratègia == "Buy&Hold":
        # Divideixo el capital inicial entre el preu open del primer dia, d'aquesta manera obtinc el nombre total d'accions que podem comprar
        accions_1= capital / taula["Open"].iloc[0]

        # Creo dues llistes buides, una per guardar el valors de cada dia del perióde, i una altra llista per guardar les dates
        valor_BUY=[]
        dates_BUY=[]
        # https://www.geeksforgeeks.org/python/declare-an-empty-list-in-python/

        
        # Creo un loop on amb la varibale dates_BH_act vagi recorrent tots els elements de la taula de l'empresa, en aquest cas dies, gràcias a .index ja que aquesta columna pertany als dies
        for dates_BH_act in taula.index: 
        # https://www.geeksforgeeks.org/pandas/iterating-over-rows-and-columns-in-pandas-dataframe/

            # Aqui obteninc cada preu d'obertura d'aquell dia
             preu_dia=taula.loc[dates_BH_act,"Close"]
             # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html

            # Faig el càlcul necessari per calcular el valor d'aquell dia mitjançant la multiplicació el nombre de accions que tinc per el preu d'aquell dia
             valor_dia = accions_1*preu_dia

             # Amb les llistes buides de abans afegeixo tant el valor d'aquell dia tant com la data
             valor_BUY.append(valor_dia)
             dates_BUY.append(dates_BH_act)
             # https://www.w3schools.com/python/ref_list_append.asp


        # Ara que ja tinc a la llista tots els valors i dies de l'empresa ara el que faig és crear una altra taula amb dues columnes (diccionari) per posar-li nom
        # El primer el capital i després la data
        taula_BUY = pd.DataFrame({
             "Capital":valor_BUY,
             "Data": dates_BUY
        })
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html 

        

        

        # Creo una llinea per dividir i marcar més l'espai
        st.divider()
        # https://docs.streamlit.io/develop/api-reference/text/st.divider 
        # Titol de que comença la etapa 2
        st.subheader("Etapa 2")
        st.subheader("Evolució del capital amb BUY&HOLD")
        
        # Ara creo el gràfic de l'evolució total del capital, el eix x és l'eix de les dates i l'eix y és l'eix del capital
        st.altair_chart(alt.Chart(taula_BUY).mark_line().encode( #no cal que creis una variable per desrpés fer altair_chart, ho pots fer directament
             x="Data:T",
             y="Capital:Q"
        )
        # PONER LINK DE YOUTUBE DE GRAFICOS ALTAIR
        # https://altair-viz.github.io/user_guide/marks/line.html
        # https://altair-viz.github.io/user_guide/encodings/index.html

        # Faig que l'altura del gràfic sigui major
        .properties(height=600)
        )
        # https://altair-viz.github.io/user_guide/configuration.html
        


        

        st.subheader("Detalls de la simulació")
        # OK
        
        # Aqui per causes d'estètica creo diferents columnes amb diferents mides per aconseguir un recuadra remarcat on es detalli tots els detalls de la simulació
        # Les columens 3,4,5 només són espais
        col_resultats,col3,col4,col5 = st.columns([5,1,1,1])#
        # OK
        
        # A la columna del recuadre dels detalls torno a crear dues columens per posar les dates de diferents mides depenent l'importància
        with col_resultats:

            with st.container(border=True):
             # OK

             col1,col2=st.columns(2)
        # Primera columna
        with col1: 
                
                # Creo un string (f) per aconseguir posar el número que vull del nombre d'accions totals arrodonit a 2 decimals
                st.write(f"Nombre d'accions comprades: {accions_1:,.2f}")
                # https://www.w3schools.com/PYTHON/python_string_formatting.asp 

                # Creo la variable de rendebilitat mitjançant la fórmula
                rendibilitat= (taula["Close"].iloc[-1]-taula["Open"].iloc[0])/taula["Open"].iloc[0]*100 
                # PONER FÓRMULA

                # Represento la fórmula de rendibilitat amb dos decimals en percent
                st.write(f"Rendibilitat:\n{rendibilitat:,.2f} % ")

                # Per aconseguir fer el drawdown torno a crear una altra taula de pandas de la llista de valors amb pd.Series, i gràcies amb .cummax aconsegueixo registrar obtenir el número més gran amb relació amb el anterior
                maxims_acumulats=pd.Series(valor_BUY).cummax()# cummax no fiunciona a llistes, ha de ser un pandas 
                # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.cummax.html

                # Ara creo la variable de drawdown i establexo una altra taula amb la seva fórmula corresponent en percent
                drawdonw=((pd.Series(valor_BUY)/(maxims_acumulats))-1)*100
                # PONER FÓRMULA

                # Amb -min de la taula de drawdown agafo el número més petit, és a dir la caiguda més gran (drawdonw) ja que estan en percents negatius
                caiguda_mes_gran=drawdonw.min()
                # https://www.w3schools.com/python/ref_func_min.asp
                
                # Represento el resultat del màxim drawdonw
                st.write(f"Màxim Drawdown: {caiguda_mes_gran:,.2f} %")

                # Creo una nova taula de pandas de la llista de valor_BUY, després amb .pct_change calculo el canvi que hi ha hagut entre el valors anteriors i els actuals, és a dir el percentatge de diferència que hi ha hagut d'un valor a un altre
                # Amb .dropna m'ajuda a borrar aquella primera filera ja que com no té un valor anterior em sortiria None
                rendiments = pd.Series(valor_BUY).pct_change().dropna()
                # https://www.geeksforgeeks.org/python/creating-a-pandas-series-from-lists/
                # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html
                # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
        
                # Creo la variable de que la taxa de risc és de 0
                taxa_no_risc = 0
        
                # Ara amb la variable de sharpe faig el càlcul corresponent
                # .mean fa la mitjana de tota la llista del rendiments
                # .std conterteix tots els rendiments diaris en un únic valor que mostra quan han variat entre ells
        
                sharpe = (rendiments.mean() - taxa_no_risc) / rendiments.std() * (252 ** 0.5)
                # https://pandas.pydata.org/docs/reference/api/pandas.Series.mean.html 
                # https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html
                # https://www.investopedia.com/terms/s/sharperatio.asp
                
                # Creo la variable de volatilitat on poso la seva fórmula corresponent
                volatilitat = rendiments.std() * (252 ** 0.5) * 100

                # Represento la volatilitat
                st.write(f"Volatilitat: {volatilitat:,.2f} %")

                # Represento el sharpe
                st.write(f"Sharpe: {sharpe:,.2f}")

                # Per al capital màxim agafo el valor més gran del capital de la taula de valors
                
                
        # Segona columna            
        with col2:

                # Creo la fórmula per aconseguir tenir el valor final de la simulacio amb b&H multiplicant el nombre d'accions pel preu final d'bertura del últim dia
                valor_final_BH= accions_1*taula["Close"].iloc[-1]

                # Creo la fórmula per aconseguir el benefici
                benefici= valor_final_BH-capital 

                # Represento el resultat de benefici amb números més grans
                st.metric(
                    label="Benefici",
                    value= f"{benefici:,.2f} USD") 
                
                # https://docs.streamlit.io/develop/api-reference/data/st.metric
                # Represento el resultat del valor final de la simulació amb la mateixa mida que el benefici
                st.metric(
                label="Valor final",
                value=f"{valor_final_BH:,.2f} USD"
                )
              

        # Les columnes que actuen d'espais
        with col3:
                st.write(" ")
        with col4:
                st.write(" ")
        with col5:
                st.write(" ")

        # Creo el boto de l'opció de poder guardar la simulació
        guardar_simulació= st.button("Guardar simulacio")

        # En el cas que es premi el boto de guardar_simulació...
        if guardar_simulació ==True:
             
             # Creo una variable de simulacions_repetides i la denomino com a Falsa
             simulacions_repetides=False

             # Aqui estableixo un loop on detecta totes les dades de les demés simulacions que s'han guardat
             # Si es la primera simulació que es guarda, com la llista de st.sessions_state.Simulacions_guardades no està creada, és a dir és buida, per tant totes les condicions adins del loop no s'executarán
             for simulacions in st.session_state.Simulacions_guardades:
                  
                  # Estableixo una condició on si amb una altra simulació coincideix en el: Nom de l'estratègia, l'empresa, el capital inicial, la data inicial i la data final. Directament la variable de simulacions_repetides es torna True
                  if (simulacions["Estratègia"]=="Buy&Hold" and simulacions["Empresa"]== empresa and simulacions["Capital inicial"]==capital and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_2):
                       simulacions_repetides=True

             # En el cas que simulacions_repetides sigui True t'avisara amb el següent missatge         
             if simulacions_repetides==True:
                       st.warning("No es pot repetir la mateixa simulació")

             # En el cas que no s'activi, és a dir, continui en false, llavors creo un diccionari (dicci_BH) el qual guarda: L'estratègia, l'empresa, el capital inicial, el valor fianl, el benefici, la rendibilitat, el màxim drawdown, la volatilitat, el sharpe, el capital màxim i el capital mínim, l'evolució del capital, és a dir la llista dels valors, la evolució de les dates, és a dir, la llista de totes les dates, la data d'inici i la data final
             else:
                dicci_BH= {"Estratègia":"Buy&Hold","Empresa":empresa,"Capital inicial":capital,"Valor final":valor_final_BH,"Benefici":benefici,"Rendibilitat":rendibilitat,"Màxim Drawdown":caiguda_mes_gran,"Volatilitat":volatilitat,"Sharpe":sharpe,
                            "Evolució capital": valor_BUY,"Evolució dates": dates_BUY,"Data inici":data_1,"Data final":data_2,}
                
                # Després de crear aquest diccionari amb totes les dades guardades l'afegeixo a la llista de   st.session_state.Simulacions_guardades amb .append
                st.session_state.Simulacions_guardades.append(dicci_BH)
                # T'avisa que s'ha guardat
                st.write("Simulació guardada")
                # I torna a reiniciar el programa per a que així s'actualitzi la llista de les simulacions guardades
                st.rerun()
                # https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun
    



     # Creo la condició que si l'estratègia és Dollar Cost Averaging(DCA) i no Buy&Hold, que s'excecuti el programa
    elif estratègia == "Dollar Cost Averaging(DCA)":

                # Estableixo una condició on si l'opció de la frequència és la mensual, que s'executo el codi de adins
                if DCA_opcions =="Mensual":
                   
                    nombre_aportacions = taula.index.to_period("M").nunique()

                    # Creo la fórmula de la quantitat que entrará a cada més dividint el capital incial entre els mesos
                    repartició_1= capital/nombre_aportacions# quants diners en cada mes
                    # PONER FÓRMULA

                    # Ara per crear el gràfic estableixo tres llistes
                    # Per obtenir cada valor
                    valor_DCA_m =[]

                    # Per obtenir cada data
                    dates_DCA_m_llista=[]

                    # Per obtenir el capital invertit, per posar-lo al gràfic
                    capital_metido_lista=[]

                    # Creo una variable per marcar el primer_mex com a 0
                    primer_mes=0 # l'establim a 0 perquè després aquest serà el mes_actual, i com es repeteix després farà gener=gener --> false -- no comprar res fins febrer

                    # Creo una variable per marcar el nombre d'accions totals com a 0
                    accions_totals=0

                    # Creo una variable per marcar que el capital invertit inicial són 0 fins al més que s'invirteix
                    capital_metido=0

                    # Creo un loop amb la varibale dates_DCA_m perquè vagi recorrent tots els elements de la taula de l'empresa
                    for dates_DCA_m in taula.index:
                         
                         # Amb això obtinc el preu d'obertura per cada valor a taula.index
                         preu_dia=taula.loc[dates_DCA_m,"Close"]

                         # Transformo els anys a mesos amb *12
                         mes_actual = dates_DCA_m.year * 12 + dates_DCA_m.month

                         # En el cas que el mes actual no sigui igual al primer mes, és a dir al mes 0 (el de començament), s'executa el codi de dins
                         if mes_actual != primer_mes:
                              
                              # Ara el primer mes (0) pasa a ser el mes actual, per exemple 1
                              primer_mes=mes_actual

                              # Ara que ja detecto que hi ha hagut un canvi de mes, aconsegueixo tenir el preu d'obertura del començaemnt d'aquell mes
                              preu_open_mes=taula.loc[dates_DCA_m,"Open"]

                              # Seguidament dividim els diners per al preu d'aquell mes per comprar totes les accions possibles amb el capital que introduiem en aquell moment
                              accions_mes=repartició_1/preu_open_mes

                              # Després sumo/acumulo aquest nombre d'accions que he comprat a les accions totals, que al començament eren 0 
                              accions_totals=accions_totals+accions_mes

                              # Després acumulo el capital ja introduit + la nova repartició ja que el programa detecta que estic en un nou més
                              capital_metido=capital_metido+repartició_1


                         # A més calculo el valor de cada dia 
                         valor_dia= accions_totals*preu_dia 

                         # Finalment a afegeixo cada valor del dia a la llista de tots els valor de la simulació
                         valor_DCA_m.append(valor_dia)

                         # I també afegeixo cada dia a la llista de tots els dies de la simulació
                         dates_DCA_m_llista.append(dates_DCA_m)

                         # A més de guardar també el capital introduit a cada periode 
                         capital_metido_lista.append(capital_metido)



                     # Creo la taula a partir del diccioanri per crear el gràfic
                    taula_DCA_m= pd.DataFrame({
                        "Capital":valor_DCA_m,
                        "Data":dates_DCA_m_llista,
                        "Capital invertit":capital_metido_lista
                                        })
                    
                    # Calculo el valor final del DCA
                    valor_final_DCA=accions_totals*taula["Close"].iloc[-1]
                    # PONER FÓRMULA DE TODAS

                    # Creo una variable del total invertit perquè potser el capital invertit no coincideix am el capital inicial
                    total_invertit=capital_metido_lista[-1]

                    # En el cas que això és compleixi el simulador anunciarà aquest fenòmen i et dira realment quant s'ha introduit
                  

                    # Càlculo el benefici del DCA
                    benefici_DCA= valor_final_DCA-total_invertit

                    # Calculo la rendibilitat
                    rendibilitat_DCA= (benefici_DCA)*100/total_invertit

                   


                    # Poso una llinea per separr les etapes
                    st.divider()

                    # Subtítols
                    st.subheader("Etapa 2")

                    st.subheader("Evolució del capital amb DCA - mensual")

                    # Ara gràcies a transform_fold ara puc representar les dues llistes (valors i capital invertit) en el mateix gràfic, han passat de ser columnes a fer "una i una"
                    st.altair_chart(alt.Chart(taula_DCA_m).transform_fold(
                    # https://blog.stackademic.com/3-altair-transformations-to-save-you-time-cf84521fc74c

                    fold= ["Capital","Capital invertit"]
                    ).mark_line().encode(
                         x="Data:T",

                         # Posp el valor de cada una i una
                         y="value:Q",

                         # Cada llista té la seva pròpia clau, per això tenen colors diferents
                         # Gràcies a aquesta clau, el programa detecta de quina "una i una" és, per tant sap quin color fer-ho
                         color="key:N"

                    # Canvio la mida a més altura
                    ).properties(height=600))

                    # Subtítol de detalls
                    st.subheader("Detalls de la simulació")

                    # Faig el mateix proccés que en l'estratègia de buy&hold per aconseguir tots els detalls en el mateix recuadre ordenadament

                    col_resultats,col3,col4,col5 = st.columns([5,1,1,1])
                    with col_resultats:
                         with st.container(border=True):
                            col1,col2=st.columns(2)

                    # Primera columna
                    with col1: 

                        # Ensenyo cuants diners entren cada més amb la divisó de repartició_1
                        st.write(f"Quants diners hi entren al mes: {repartició_1:,.2f} USD")

                        st.write(f"Nombre d'accions comprades: {accions_totals:,.2f} ")
                        # Ensenyo el total invertit durant tota la inversió
                        
                        # Ensenyo la rendibilitat del capital en percent
                        st.write(f"Rendibilitat: {rendibilitat_DCA:,.2f} %")

                        
                        
                        


                        # Com per calcular el sharpe necessito els rendiments hem de calularlos bé
                        # Si no ho faig això estariem calculant els rendiments també els dies que s'invirteix, és a dir que es fan aportacions, i el rendiment es veuria molt afectat a l'alça
                        # Per aquesta raó he de tenir en compte quan s'invirteix

                        # Primer per començar a treballar amb les dades hem de convertir tant els tots els valors dels dies a una taula
                        taula_de_DCA_mensual_valor_diari = pd.Series(valor_DCA_m)
                        # https://pandas.pydata.org/docs/reference/api/pandas.Series.html

                        # El matix amb el capital invertit
                        capital_invertit_serie = pd.Series(capital_metido_lista)

                        # Aqui creo la llista on s'anirán guardant tos els rendiments
                        rendiments_diaris = []

                        # Amb aquest loop recorreixo totes les posicions de la taula de valors, començant per l'1
                        for i in range(1, len(taula_de_DCA_mensual_valor_diari)):

                            # Estic calculant quant diner nou he introduit entre el dia actual i el dia anterior
                            aportacio = capital_invertit_serie.iloc[i] - capital_invertit_serie.iloc[i - 1]

                            # Si hi ha hagut una aportació llavors entro en aquesta condició
                            if aportacio > 0:

                                # Ara faig el càlcul del rendiment d'aquell dia
                                rendiment_dia =taula_de_DCA_mensual_valor_diari.iloc[i] / (taula_de_DCA_mensual_valor_diari.iloc[i - 1] + aportacio)  - 1
                                # PONER FÓRMULA

                            # En el cas que no hi hagi hagut aportació entra aqui
                            else:

                                # Faig la fórmula que em permet saber quant ha pujat l'acció ( el rendiment)
                                rendiment_dia = (taula_de_DCA_mensual_valor_diari.iloc[i] / taula_de_DCA_mensual_valor_diari.iloc[i - 1]) - 1 
                                # PONER FÓRMULA

                            # Finalmeet guardo el rendiment d'aquell dia a la llista de rendiments diaris
                            rendiments_diaris.append(rendiment_dia)

                        # Després ara que ja tinc tots els rendiments torno a crear una altra taula d'aquesta llista
                        rendiments_diaris = pd.Series(rendiments_diaris)

                        # Creo la variable de que la taxa de risc és de 0
                        taxa_no_risc =0 

                        # Ara amb la variable de sharpe faig el càlcul corresponent
                        # .mean fa la mitjana de tota la llista del rendiments
                        # .std conterteix tots els rendiments diaris en un únic valor que mostra quan han variat entre ells
                        sharpe = (rendiments_diaris.mean() - taxa_no_risc) / rendiments_diaris.std() * (252 ** 0.5)

                        # Creo la variable de volatilitat on poso la seva fórmula corresponent
                        volatilitat = rendiments_diaris.std() * (252 ** 0.5) * 100

                        valor_sense_aportacions=(1+rendiments_diaris).cumprod()

                        maxims=valor_sense_aportacions.cummax()

                        drawdonw=(valor_sense_aportacions/maxims -1)*100

                        caiguda_mes_gran=drawdonw.min()


                        # Represento el resultat del màxim drawdonw
                        st.write(f"Màxim Drawdown: {caiguda_mes_gran:,.2f} %")
                        # Represento la volatilitat
                        st.write(f"Volatilitat: {volatilitat:,.2f} %")
                    
                        # Represento el sharpe
                        st.write(f"Sharpe: {sharpe:,.2f}")

                        # Per al capital màxim agafo el valor més gran del capital de la taula de valors
                       

                    # Segona columna
                    with col2:
                        # Represento el resultat de benefici amb números més grans
                        st.metric(
                             label="Benefici del DCA:",
                             value= f"{benefici_DCA:,.2f} USD")
                        
                        # Represento el resultat del valor final de la simulació amb la mateixa mida que el benefici
                        st.metric(
                            label="Valor final del DCA:",
                            value= f"{valor_final_DCA:,.2f} USD") #AQUEST NO ÉS EL PREU DE L'ÚLTIMA COMPRA, sinó el preu que té l'acció quan acaba el període de simulació, el preu que "té avui"

                    
                    # Creo el boto de l'opció de poder guardar la simulació
                    guardar_simulació= st.button("Guardar simulacio")

                    # En el cas que es premi el boto de guardar_simulació...
                    if guardar_simulació ==True:

                        # Creo una variable de simulacions_repetides i la denomino com a Falsa
                        simulacions_repetides=False

                        # Aqui estableixo un loop on detecta totes les dades de les demés simulacions que s'han guardat
                        # Si es la primera simulació que es guarda, com la llista de st.sessions_state.Simulacions_guardades no està creada, és a dir és buida, per tant totes les condicions adins del loop no s'executarán
                        for simulacions in st.session_state.Simulacions_guardades:

                             # Estableixo una condició on si amb una altra simulació coincideix en el: Nom de l'estratègia, l'empresa, el capital inicial, la data inicial i la data final i la frequència. Directament la variable de simulacions_repetides es torna True
                             if (simulacions["Estratègia"]=="DCA mensual" and simulacions["Empresa"]== empresa and simulacions["Capital inicial"]==capital and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_2 and simulacions.get("Frequència")==DCA_opcions):
                                  simulacions_repetides=True

                        # En el cas que simulacions_repetides sigui True t'avisara amb el següent missatge         
                        if simulacions_repetides==True:
                             
                             st.warning("No es pot repetir la mateixa simulació")

                        # En el cas que no s'activi, és a dir, continui en false, llavors creo un diccionari (dicci_BH) el qual guarda: L'estratègia, l'empresa, el capital inicial, el valor fianl, el benefici, la rendibilitat, el màxim drawdown, la volatilitat, el sharpe, el capital màxim i el capital mínim, l'evolució del capital, és a dir la llista dels valors, la evolució de les dates, és a dir, la llista de totes les dates, la data d'inici i la data final i la frequència
                        else:
                            dicci_DCM= {"Estratègia":"DCA mensual","Empresa":empresa,"Capital inicial":capital,"Valor final":valor_final_DCA,"Benefici":benefici_DCA,"Rendibilitat":rendibilitat_DCA,"Màxim Drawdown":caiguda_mes_gran,"Volatilitat":volatilitat,"Sharpe":sharpe,
                                        "Evolució capital":valor_DCA_m,"Evolució dates": dates_DCA_m_llista,"Data inici":data_1,"Data final":data_2,"Frequència":DCA_opcions}
                            
                            # Després de crear aquest diccionari amb totes les dades guardades l'afegeixo a la llista de   st.session_state.Simulacions_guardades amb .append
                            st.session_state.Simulacions_guardades.append(dicci_DCM)

                            # T'avisa que s'ha guardat
                            st.write("Simulació guardada")  

                            # I torna a reiniciar el programa per a que així s'actualitzi la llista de les simulacions guardades
                            st.rerun()                  
                    




                # Estableixo una condició on si l'opció de la frequència és la anual, que s'executo el codi de adins
                elif DCA_opcions =="Anual":

                     # Primer a la taula de l'empresa de yf només agafo l'any (.year) i amb .nunique compto quants anys hi han sense que es repeteixin, també compta el primer
                     anys=taula.index.year.nunique() 
                     # https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.year.html
                     # https://pandas.pydata.org/docs/reference/api/pandas.Series.nunique.html

                     # Creo la fórmula de la quantitat que entrará a cada més dividint el capital incial entre els mesos
                     repartició_dels_anys= capital/anys

                     # Ara per crear el gràfic estableixo tres llistes
                     # Per obtenir cada valor
                     valor_DCA_a=[]

                     # Per obtenir cada data
                     dates_DCA_a_llista=[]

                     # Per obtenir el capital invertit, per posar-lo al gràfic
                     capital_invertido_lista=[]

                     # Creo una variable per marcar el primer_any com a 0
                     primer_any=0
                     # Creo una variable per marcar el nombre d'accions totals com a 0

                     # Creo una variable per marcar el nombre d'accions totals com a 0
                     accions_totals=0

                     # Creo una variable per marcar que el capital invertit inicial són 0 fins al més que s'invirteix
                     capital_invertido=0

                     # Creo un loop amb la varibale dates_DCA_a perquè vagi recorrent tots els elements de la taula de l'empresa
                     for dates_DCA_a in taula.index:
                          preu_dia=taula.loc[dates_DCA_a,"Close"]

                          # Amb això obtinc l'any actual
                          any_actual= dates_DCA_a.year

                          # En el cas que l'any actual no sigui igual al primer any, és a dir al mes 0 (el de començament), s'executa el codi de dins perquè detecta un any nou
                          if any_actual!=primer_any:

                                # Ara el primer any (0) pasa a ser el mes actual, per exemple 1
                                primer_any=any_actual

                                # Ara que ja detecto que hi ha hagut un canvi de any, aconsegueixo tenir el preu d'obertura del començaemnt d'aquell any
                                preu_open_any=taula.loc[dates_DCA_a,"Open"]

                                # Seguidament dividim els diners per al preu d'aquell any per comprar totes les accions possibles amb el capital que introduiem en aquell moment
                                accions_any= repartició_dels_anys/preu_open_any

                                # Després sumo/acumulo aquest nombre d'accions que he comprat a les accions totals, que al començament eren 0 
                                accions_totals=accions_totals+accions_any

                                # Després acumulo el capital ja introduit + la nova repartició ja que el programa detecta que estic en un nou any
                                capital_invertido=capital_invertido+repartició_dels_anys

                          # A més calculo el valor de cada dia 
                          valor_dia=accions_totals*preu_dia

                          # Finalment a afegeixo cada valor del dia a la llista de tots els valor de la simulació
                          valor_DCA_a.append(valor_dia)

                          # I també afegeixo cada dia a la llista de tots els dies de la simulació
                          dates_DCA_a_llista.append(dates_DCA_a)

                          # A més de guardar també el capital introduit a cada periode
                          capital_invertido_lista.append(capital_invertido)

                     # A més calculo el valor de cada dia 
                     valor_final_DCA_a= accions_totals*taula["Close"].iloc[-1]

                     # Creo una variable del total invertit perquè potser el capital invertit no coincideix am el capital inicial                                           
                     total_invertit_a=capital_invertido_lista[-1]

                     # # En el cas que això és compleixi el simulador anunciarà aquest fenòmen i et dira realment quant s'ha introduit
                   

                     # Càlculo el benefici del DCA
                     benefici_DCA_a= valor_final_DCA_a-total_invertit_a

                     # Calculo la rendibilitat 
                     rendibilitat_DCA_a= (benefici_DCA_a)*100/total_invertit_a

                     # Creo la taula a partir del diccioanri per crear el gràfic
                     taula_DCA_a=pd.DataFrame({
                         "Capital":valor_DCA_a,
                         "Data":dates_DCA_a_llista,
                         "Capital invertit":capital_invertido_lista
                     })


                    

                     # Poso una llinea per separr les etapes
                     st.divider()
                     # Subtítols
                     st.subheader("Etapa 2")
                     st.subheader("Evolució del capital amb DCA - anual")

                     # Ara gràcies a transform_fold ara puc representar les dues llistes (valors i capital invertit) en el mateix gràfic, han passat de ser columnes a fer "una i una"
                     st.altair_chart(alt.Chart(taula_DCA_a).transform_fold(fold=["Capital","Capital invertit"]).mark_line().encode(
                          x="Data:T",
                          # Poso el valor de cada una i una
                          y="value:Q",

                          # Cada llista té la seva pròpia clau, per això tenen colors diferents
                          # Gràcies a aquesta clau, el programa detecta de quina "una i una" és, per tant sap quin color fer-ho
                          color="key:N"

                     # Canvio la mida a més altura
                     ).properties(height=600))

                     # Subtítol de detalls
                     st.subheader("Detalls de la simulació")

                    # Faig el mateix proccés que en l'estratègia de buy&hold per aconseguir tots els detalls en el mateix recuadre ordenadament
                     
                     col_resultats,col3,col4,col5 = st.columns([5,1,1,1])#dependiendo de los numeors ya ponemso el numoer de columnas que queremos
                     with col_resultats:
                            with st.container(border=True):
                                col1,col2=st.columns(2)

                     # Segona columna
                     with col1: 
                             # Ensenyo cuants diners entren cada més amb la divisó de repartició_1
                            st.write(f"Quants diners hi entren a l'any : {repartició_dels_anys:,.2f} USD")

                            st.write(f"Nombre d'accions comprades: {accions_totals:,.2f}")

                        
                           

                             # Ensenyo la rendibilitat del capital en percent
                            st.write(f"Rendibilitat : {rendibilitat_DCA_a:,.2f} %")


                        

                            # Com per calcular el sharpe necessito els rendiments hem de calularlos bé
                            # Si no ho faig això estariem calculant els rendiments també els dies que s'invirteix, és a dir que es fan aportacions, i el rendiment es veuria molt afectat a l'alça
                            # Per aquesta raó he de tenir en compte quan s'invirteix

                            # Primer per començar a treballar amb les dades hem de convertir tant els tots els valors dels dies a una taula
                            taula_de_DCA_anual_valor_diari = pd.Series(valor_DCA_a)
                            capital_invertit_serie = pd.Series(capital_invertido_lista)

                            # Aqui creo la llista on s'anirán guardant tos els rendiments
                            rendiments_diaris = []

                              # Amb aquest loop recorreixo totes les posicions de la taula de valors, començant per l'1
                            for i in range(1, len(taula_de_DCA_anual_valor_diari)):

                                # Estic calculant quant diner nou he introduit entre el dia actual i el dia anterior
                                aportacio = capital_invertit_serie.iloc[i] - capital_invertit_serie.iloc[i - 1]

                                 # Si hi ha hagut una aportació llavors entro en aquesta condició
                                if aportacio > 0:
                                    # Ara faig el càlcul del rendiment d'aquell dia
                                    rendiment_dia = (taula_de_DCA_anual_valor_diari.iloc[i] /(taula_de_DCA_anual_valor_diari.iloc[i - 1] + aportacio)) - 1

                                # En el cas que no hi hagi hagut aportació entra aqui    
                                else:
                                     # Faig la fórmula que em permet saber quant ha pujat l'acció ( el rendiment)
                                    rendiment_dia = (taula_de_DCA_anual_valor_diari.iloc[i] / taula_de_DCA_anual_valor_diari.iloc[i - 1]) - 1

                                # Finalmeet guardo el rendiment d'aquell dia a la llista de rendiments diaris
                                rendiments_diaris.append(rendiment_dia)

                             # Després ara que ja tinc tots els rendiments torno a crear una altra taula d'aquesta llista
                            rendiments = pd.Series(rendiments_diaris)

                            # Creo la variable de que la taxa de risc és de 0
                            taxa_sense_risc = 0

                            # Ara amb la variable de sharpe faig el càlcul corresponent
                            # .mean fa la mitjana de tota la llista del rendiments
                             # .std conterteix tots els rendiments diaris en un únic valor que mostra quan han variat entre ells
                            sharpe = (rendiments.mean() - taxa_sense_risc) / rendiments.std() * (252 ** 0.5)

                             # Creo la variable de volatilitat on poso la seva fórmula corresponent
                            volatilitat = rendiments.std() * (252 ** 0.5) * 100

                            valor_sense_aportacions=(1+rendiments).cumprod()
                            
                            maxims=valor_sense_aportacions.cummax()
    
                            drawdonw=(valor_sense_aportacions/maxims -1)*100
    
                            caiguda_mes_gran=drawdonw.min()

                             # Represento el resultat del màxim drawdonw                                      
                            st.write(f"Màxim Drawdown: {caiguda_mes_gran:,.2f} %")

                            # Represento la volatilitat
                            st.write(f"Volatilitat: {volatilitat:,.2f} %")

                            # Represento el sharpe
                            st.write(f"Sharpe: {sharpe:,.2f}")
                   

                     # Segona columna
                     with col2:
                             # Represento el resultat de benefici amb números més grans
                            st.metric(
                                label="Benefici del DCA:",
                                value= f"{benefici_DCA_a:,.2f} USD")

                             # Represento el resultat del valor final de la simulació amb la mateixa mida que el benefici
                            st.metric(
                                label="Valor final del DCA:",
                                value= f"{valor_final_DCA_a:,.2f} USD")
                     
                     
                      # Creo el boto de l'opció de poder guardar la simulació
                     guardar_simulació= st.button("Guardar simulacio")

                      # En el cas que es premi el boto de guardar_simulació...
                     if guardar_simulació ==True:

                         # Creo una variable de simulacions_repetides i la denomino com a Falsa
                        simulacions_repetides=False

                         # Aqui estableixo un loop on detecta totes les dades de les demés simulacions que s'han guardat
                         # Si es la primera simulació que es guarda, com la llista de st.sessions_state.Simulacions_guardades no està creada, és a dir és buida, per tant totes les condicions adins del loop no s'executarán
                        for simulacions in st.session_state.Simulacions_guardades:

                                # Estableixo una condició on si amb una altra simulació coincideix en el: Nom de l'estratègia, l'empresa, el capital inicial, la data inicial i la data final i la frequència. Directament la variable de simulacions_repetides es torna True
                                if (simulacions["Estratègia"]=="DCA anual" and simulacions["Empresa"]== empresa and simulacions["Capital inicial"]==capital and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_2 and simulacions.get("Frequència")==DCA_opcions):
                                    simulacions_repetides=True

                        # En el cas que simulacions_repetides sigui True t'avisara amb el següent missatge    
                        if simulacions_repetides==True:
                                
                                st.warning("No es pot repetir la mateixa simulació")
                        # # En el cas que no s'activi, és a dir, continui en false, llavors creo un diccionari (dicci_BH) el qual guarda: L'estratègia, l'empresa, el capital inicial, el valor fianl, el benefici, la rendibilitat, el màxim drawdown, la volatilitat, el sharpe, el capital màxim i el capital mínim, l'evolució del capital, és a dir la llista dels valors, la evolució de les dates, és a dir, la llista de totes les dates, la data d'inici i la data final i la frequència
                        else:
                            dicci_DC_A= {"Estratègia":"DCA anual","Empresa":empresa,"Capital inicial":capital,"Valor final":valor_final_DCA_a,"Benefici":benefici_DCA_a,"Rendibilitat":rendibilitat_DCA_a,"Màxim Drawdown":caiguda_mes_gran,"Volatilitat":volatilitat,"Sharpe":sharpe,
                                        "Evolució capital": valor_DCA_a,"Evolució dates": dates_DCA_a_llista,"Data inici":data_1,"Data final":data_2,"Frequència":DCA_opcions}

                            # Després de crear aquest diccionari amb totes les dades guardades l'afegeixo a la llista de   st.session_state.Simulacions_guardades amb .append
                            st.session_state.Simulacions_guardades.append(dicci_DC_A)

                            # T'avisa que s'ha guardat
                            st.write("Simulació guardada")

                             # I torna a reiniciar el programa per a que així s'actualitzi la llista de les simulacions guardades
                            st.rerun()

                
    # Creo la condició que si l'estratègia és Stop-Loss i Take-Profit i no Dollar Cost Averaging(DCA) i Buy&Hold, que s'excecuti el programa
    elif estratègia == "Stop-Loss i Take-Profit":

        # Divideixo el capital inicial entre el preu open del primer dia, d'aquesta manera obtinc el nombre total d'accions que podem comprar
        accions_comprades= capital/taula["Open"].iloc[0]

        # Subtítol
        st.subheader("Tria els percentatges")

        # Creo una funció la qual si s'executa st.session_state.Simulació_començada es torda False, és a dir deixar de mostrar el que ja esta ensenyant el boto de "boto"
        def canvi_percentatges():
         st.session_state.Simulació_començada=False

        
        # Poso slider per a que es trii el percentatge el qual es dura a terme durant la simulaició
        # Aquest slider marca el percent de pèrdua del capital inicial on es parara la simulació
        Stop_Loss = st.slider(
        label="Stop-Loss",
        min_value= 1,
        max_value=100,
        value=20,
        step =1,
        # Si es canvia el percentatge llavors s'excecuta la funcio de canvi_percentatges
        on_change=canvi_percentatges
        )
        # Seguidament calculo el preu pèrdua que ha d'arribar l'acció  on es parara la simualció
        preu_Stop_Loss= taula["Open"].iloc[0]-(taula["Open"].iloc[0]*Stop_Loss/100)
        # Ara creo la varible del capital on ha d'arribar per a que es pari
        capital_stop_loss=preu_Stop_Loss*accions_comprades
        # També marco el valor per a que ja es sapigue al començament
        st.markdown(f"###### Valor: {capital_stop_loss:,.2f} USD")



        # Poso slider per a que es trii el percentatge el qual es dura a terme durant la simulaició
        # Aquest slider marca el percent de guanys (profit) del capital inicial 
        Take_Profit= st.slider(
        label="Take-Profit",
        min_value=1,
        max_value=300,
        value=50,
        step=1,
        on_change=canvi_percentatges
                )


        # Seguidament calculo el preu de guany que ha d'arribar l'acció  on es parara la simualció
        preu_Take_Profit = taula["Open"].iloc[0]+(taula["Open"].iloc[0]*Take_Profit/100)

        # Ara creo la varible del capital on ha d'arribar per a que es pari
        capital_take_profit= preu_Take_Profit*accions_comprades

        # També marco el valor per a que ja es sapigue al començament
        st.markdown(f"###### Valor:{capital_take_profit:,.2f} USD")



        
        


        # Aqui dic estableixo una condició a "l'armari per a que la simulacio_començada, que es la part on ensenya els resultats de ST, comenci en false"
        if "Simulació_començada" not in st.session_state: #La variable ya existe, así que no vuelve a crearla. La cajita sigue teniendo: TRUE

         st.session_state.Simulació_començada = False

        # Després creo boto començar 
        boto_començar= st.button(
        label="Començar simulació"
        )

        # Després asocio el boto_començar amb st.session_state.Simualció_començada
        # Si es prem el botó st.session_state.Simulació_començada es torna True
        if boto_començar== True:
         st.session_state.Simulació_començada = True

        # Condició on només comença si s'ha premut el botó i st.session_state.Simualció_començada es True
        if st.session_state.Simulació_començada == True:

        # # Creo dues llistes buides, una per guardar el valors de cada dia del perióde, i una altra llista per guardar les dates
            capital_ST=[]
            dates_ST=[]

            # Divideixo el capital inicial entre el preu open del primer dia, d'aquesta manera obtinc el nombre total d'accions que podem comprar
            accions_comprades= capital/taula["Open"].iloc[0]


                # Creo un loop on amb la varibale dates_ST_act vagi recorrent tots els elements de la taula de l'empresa, en aquest cas dies, gràcias a .index ja que aquesta columna pertany als dies
            for dates_ST_act in taula.index:
                        # Aqui obteninc cada preu d'obertura d'aquell dia
                        preu_dia=taula.loc[dates_ST_act,"Close"]

                        # Aqui aconsegueixo el valor més baix d'aquell dia per donar més realisme a la simulació
                        preu_minim=taula.loc[dates_ST_act,"Low"]

                        # Ara aconsegueixo el valor més alt d'aquell dia durant la simulació
                        preu_maxim=taula.loc[dates_ST_act,"High"]

                        #Nota: si un dia llega a ambos topes siempre nos marcar ael stop loss-- decirlo en TDR

                        # Si el preu minim d'aquell dia supera o iguala el valor del preu_Stop_Loss entra en aquesta condició
                        

                            # Si el preu maxim d'aquell dia supera o iguala el valor del preu_Take_Profit entra en aquesta condició
                        if preu_maxim >= preu_Take_Profit: # ejemplo si tope es 130 i tk es 120 estonces que se activ  proque para ellgar al 130 tien que pasar por el 120

                             # Després creo una variable on si es dona aquesta condició preu_dia_ST pasi a ser el preu de Take profit
                             preu_dia_ST=preu_Take_Profit

                             # I que el la variable de motiu_parada sigui el texte "take"
                             motiu_parada="take"

                            
                                # Ara calculo l'últim valor del capital on es va parar la simualció
                             capital_dia_ST=accions_comprades*preu_Take_Profit

                                # I l'agefeixo a la llista dels capitals
                             capital_ST.append(capital_dia_ST)

                                # I l'última data també
                             dates_ST.append(dates_ST_act)

                                # Després d'això directament ja no es calcula res mes, s'atura la simulació gràcies al break
                                
                             break

                        elif preu_minim <= preu_Stop_Loss:
                        
                                                    # Després creo una variable on si es dona aquesta condició preu_dia_ST pasi a ser el preu de Stop_loss
                                                    preu_dia_ST=preu_Stop_Loss
                        
                                                    # I que el motiu de la parada sigui el texte de "stop"
                                                    motiu_parada="stop"
                                                    
                        
                                                    # Ara calculo l'últim valor del capital on es va parar la simualció
                                                    capital_dia_ST=accions_comprades*preu_Stop_Loss
                        
                                                    # I l'agefeixo a la llista dels capitals
                                                    capital_ST.append(capital_dia_ST)
                        
                                                    # I l'última data també
                                                    dates_ST.append(dates_ST_act)
                        
                        
                                                    # Després d'això directament ja no es calcula res mes, s'atura la simulació gràcies al break
                                                    break
                                                    # https://www.geeksforgeeks.org/python/python-break-statement/
                        

                        # En el cas que no sobrepasi o igual qualsevol limit llavors la simulació segueix fins el seu últim dia
                        else:

                             # El preu_dia_ST serà el preu d'obertura d'aquell dia
                             preu_dia_ST=preu_dia
  
                             # I la variable motiu_parada serà el texte "no_top"
                             motiu_parada="no_top"

                             # I també es calcula el valor durant la simulació
                             capital_dia_ST=accions_comprades*preu_dia_ST

                             # A més d'afegir cada valor a la llista dels capitals
                             capital_ST.append(capital_dia_ST)

                             # Igual que faig amb les dates
                             dates_ST.append(dates_ST_act)




            # Quan la simulació ja finalitzi creo una taula a partir de les llistes on estava acumulant tant els valors com les dates

            taula_ST=pd.DataFrame({
                        "Capital":capital_ST,
                        "Data":dates_ST
                    })

            # Subtititol
            st.subheader("Detalls de la simulació")

            # Llinea
            st.divider()

            # Subtitols
            st.subheader("Etapa 2")
            st.subheader("Evolució del capital ST")

            # Primer de tot creo el gràfic de la simulació amb la taula_ST on hi havien les dades
            st.altair_chart(alt.Chart(taula_ST).mark_line().encode(
                x="Data:T",
                y="Capital:Q"
            # La faig més gran
            ).properties(height=600))

            
            # El valor final haurà de ser l'últim element de la llista de capital_ST
            valor_final_ST =  preu_dia_ST*accions_comprades

            # Creo la fórmula per aconseguir el benefici
            benefici= valor_final_ST-capital

            # Creo la variable de rendebilitat mitjançant la fórmula
            rendibilitat= (capital_ST[-1]-capital)/capital*100

                # Aqui per causes d'estètica creo diferents columnes amb diferents mides per aconseguir un recuadra remarcat on es detalli tots els detalls de la simulació
                # Les columens 3,4,5 només són espais
            col_resultats,col3,col4,col5 = st.columns([5,1,1,1])#dependiendo de los numeors ya ponemso el numoer de columnas que queremos

            # A la columna del recuadre dels detalls torno a crear dues columens per posar les dates de diferents mides depenent l'importància
            with col_resultats:
                with st.container(border=True):

                    col1,col2=st.columns(2)

            # A la primera columna
            with col1: 
                # Escric el motiu de la parada de la simulació
                st.write("Motiu:")           

                # En el cas que s'hagi parat per el Stop-Loss t'ho dira        
                if motiu_parada== "stop":
                                        
                    st.write("S'ha parat gràcies al Stop-Loss")

                # En el cas que s'hagi parat per el Take-profit t'ho dira          
                elif motiu_parada== "take":
                    st.write("S'ha parat gràcies al Take-Profit")

                #I si no s'ha parat per cap limit t'avisara també
                elif motiu_parada=="no_top":
                    st.write("La simulació no ha arribat a cap màxim i mínim")

                    # Creo un string (f) per aconseguir posar el número que vull del nombre d'accions totals arrodonit a 2 decimals              
                st.write(f"Nombre d'accions comprades: {accions_comprades:,.2f} ") 

                # Creo la variable de rendebilitat mitjançant la fórmula
                st.write(f"Rendibilitat : {rendibilitat:,.2f} %") 

                # Per aconseguir fer el drawdown torno a crear una altra taula de pandas de la llista de valors amb pd.Series, i gràcies amb .cummax aconsegueixo registrar obtenir el número més gran amb relació amb el anterior
                maxims_acumulats=pd.Series(capital_ST).cummax()

                    # Ara creo la variable de drawdown i establexo una altra taula amb la seva fórmula corresponent en percent
                drawdonw=((pd.Series(capital_ST)/(maxims_acumulats))-1)*100

                    # Amb -min de la taula de drawdown agafo el número més petit, és a dir la caiguda més gran (drawdonw) ja que estan en percents negatius
                caiguda_mes_gran=drawdonw.min()

                # I represento el resultat del màxim drawdonw                       
                st.write(f"Màxim Drawdown: {caiguda_mes_gran:,.2f} %")

                # Creo una nova taula de pandas de la llista de valor_BUY, després amb .pct_change calculo el canvi que hi ha hagut entre el valors anteriors i els actuals, és a dir el percentatge de diferència que hi ha hagut d'un valor a un altre
                # Amb .dropna m'ajuda a borrar aquella primera filera ja que com no té un valor anterior em sortiria None
                rendiments = pd.Series(capital_ST).pct_change().dropna()

                # Creo la variable de volatilitat on poso la seva fórmula corresponent
                volatilitat = rendiments.std() * (252 ** 0.5) * 100

                    # Represento la volatilitat
                st.write(f"Volatilitat: {volatilitat:,.2f} %")

                # Creo la variable de que la taxa de risc és de 0
                taxa_sense_risc = 0

                # Ara amb la variable de sharpe faig el càlcul corresponent
                # .mean fa la mitjana de tota la llista del rendiments
                # .std conterteix tots els rendiments diaris en un únic valor que mostra quan han variat entre ells
                sharpe = (rendiments.mean() - taxa_sense_risc) / rendiments.std() * (252 ** 0.5)

                # I represento el valor de Sharpe
                st.write(f"Sharpe: {sharpe:,.2f}")

            with col2:   
                    # Represento el resultat de benefici amb números més grans
                st.metric(
                    label="Benefici:",
                    value= f"{benefici:,.2f} USD")
                
                    # Represento el resultat del valor final de la simulació amb la mateixa mida que el benefici
                st.metric(
                    label="Valor finals:",
                    value= f"{valor_final_ST:,.2f} USD")
                                
            


            # Creo el boto de l'opció de poder guardar la simulació
            guardar_simulació= st.button("Guardar simulacio")

            # En el cas que es premi el boto de guardar_simulació...
            if guardar_simulació ==True:

                # Creo una variable de simulacions_repetides i la denomino com a Falsa
                simulacions_repetides=False

                # Aqui estableixo un loop on detecta totes les dades de les demés simulacions que s'han guardat
                # Si es la primera simulació que es guarda, com la llista de st.sessions_state.Simulacions_guardades no està creada, és a dir és buida, per tant totes les condicions adins del loop no s'executarán
                for simulacions in st.session_state.Simulacions_guardades:
                        
                        # Estableixo una condició on si amb una altra simulació coincideix en el: Nom de l'estratègia, l'empresa, el capital inicial, la data inicial i la data final i es igual al motiu de parada (Stop-Loss o Take-profit). Directament la variable de simulacions_repetides es torna True
                        if (simulacions["Estratègia"]=="Stop-Loss i Take-Profit" and simulacions["Empresa"]== empresa and simulacions["Capital inicial"]==capital and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_2 and simulacions["Stop-Loss"]==Stop_Loss and simulacions["Take-Profit"]==Take_Profit):
                            simulacions_repetides=True


                    # En el cas que simulacions_repetides sigui True t'avisara amb el següent missatge         
                if simulacions_repetides==True:
                        st.warning("No es pot repetir la mateixa simulació")

                    # En el cas que no s'activi, és a dir, continui en false, llavors creo un diccionari (dicci_BH) el qual guarda: L'estratègia, l'empresa, el capital inicial, el valor fianl, el benefici, la rendibilitat, el màxim drawdown, la volatilitat, el sharpe, el capital màxim i el capital mínim, l'evolució del capital, és a dir la llista dels valors, la evolució de les dates, és a dir, la llista de totes les dates, la data d'inici i la data final        
                else:
                    dicci_ST= {"Estratègia":"Stop-L i Take-P","Empresa":empresa,"Capital inicial":capital,"Valor final":valor_final_ST,"Benefici":benefici,"Rendibilitat":rendibilitat,"Màxim Drawdown":caiguda_mes_gran,"Volatilitat":volatilitat,"Sharpe":sharpe,"Stop-Loss":Stop_Loss,"Take-Profit":Take_Profit,
                            "Evolució capital":capital_ST,"Evolució dates":dates_ST,"Data inici":data_1,"Data final":data_2}

                    # Després de crear aquest diccionari amb totes les dades guardades l'afegeixo a la llista de   st.session_state.Simulacions_guardades amb .append
                    st.session_state.Simulacions_guardades.append(dicci_ST)

                    # T'avisa que s'ha guardat
                    st.write("Simulació guardada")

                        # I torna a reiniciar el programa per a que així s'actualitzi la llista de les simulacions guardades                
                    st.rerun()



            # Després en el seguent apartat creo altres dues llistes, una del capital i una altra de les dates per a l'opció de que hagués passat si no hagués topes       
            capital_ST_max = []
            dates_ST_max =[]

            # Després faig el mateix funcionament que el b&h pero amb les variables del ST
            for dates_ST_capital_max in taula.index:

                            # Obtinc el preu d'obertura
                            preu_dia_ST=taula.loc[dates_ST_capital_max,"Close"]

                            # I calculo el capital en aquell dia
                            capital_dia_ST_max=accions_comprades*preu_dia_ST

                            # Després afegeixo cada valor a les llistes del principi                                        
                            capital_ST_max.append(capital_dia_ST_max)
                            dates_ST_max.append(dates_ST_capital_max)


            # I creo una taula a partir d'aquestes dues llistes                
            taula_max = pd.DataFrame({ #aqui cal data frame i es parèntesis
                    "Capital":capital_ST_max,
                    "Dates":dates_ST_max
                })

            #MIRAR PORQUE NO HACE FALTA ST.SESSION_STATE I TU PORQUE LO PONES SI TOTAL AL FINAL LO CANCELAS OTRA VEZ
            # Després creo el boto per a que l'usuari pugui escogir l'opció sense topes
            Capital_max=st.button(
                    label= "Si no hagués topes"  
                )

                # Creo la fórmula per aconseguir tenir el valor final de la simulacio amb b&H agafant l'ultim valor de la llsita de capitals
            valor_final_ST_max = capital_ST_max[-1]

            # Creo la fórmula per aconseguir el benefici
            benefici_max= valor_final_ST_max-capital

                # Represento la fórmula de rendibilitat amb dos decimals en percent
            rentabilitat_max= (capital_ST_max[-1]-capital)/capital*100

           

            # En el cas que el boto es premi entra aqui
            if Capital_max==True:

                    #Genero el grafic total
                    st.altair_chart(alt.Chart(taula_max).mark_line().encode(
                        x="Dates:T",
                        y="Capital:Q"
                    # El faig gran
                    ).properties(height=600))

                    # I amb les columnes l'ordeno
                    col_resultats,col3,col4,col5 = st.columns([3,1,1,1])

                    
                    with col_resultats:
                        with st.container(border=True):
                                col1,col2=st.columns(2)
                    with col1: 

                        # Represento la rentabilitat
                        st.write(f"Rentabilitat: {rentabilitat_max:,.2f} %")

                        
                                        
                    with col2:

                        # Represento el benefici en numeros grans
                        st.metric(
                            label="Benefici",
                            value= f"{benefici_max:,.2f} USD") 

                        # Represento el valor final en numeros grans

                        st.metric(
                        label="Valor final",
                        value=f"{valor_final_ST_max:,.2f} USD"
                        )
                

    # En el cas que no sigui ni Buy&Hold, ni DCA ni Stop-Loss i Take-Pofit llavors entra en aquest if
    elif estratègia == "Diversificació":

        # Divisor
        st.divider()
        st.write("**Tria el número d'empreses per diversificar:**")

        # Columnes per colocar els recuadres on jo vull
        colum1,espacio = st.columns([0.35,3])
        with colum1:

        # Crear el numero d'empreses
         número_empreses=st.number_input(
                label=" ",
                min_value= 2,
                max_value=10,
                value=2,
                step=1,
                label_visibility="collapsed"# buscar video
            
        )

        # Creo un altre dicionari pero concordar els sectors amb les empreses
        empreses={"Tecnologia":["Apple","Microsoft","Nvidia","TSMC","Adobe"],
                "Financer":["JPMorgan Chase","Goldman Sachs","American Express","Visa","Mastercard"],
                "Serveis digitals":["Amazon","eBay","Booking Holdings","Cisco Systems","Alphabet"],
                "Energia":["ExxonMobil","Chevron","NextEra Energy","AES","EQT"],
                "Salut":["UnitedHealth Group","McKesson","CVS Health","Amgen","Pfizer"],
                "Inmobiliari":["D.R. Horton","Lennar","Hovnanian Enterprises","PulteGroup","Toll Brothers"],
                "Automoció":["Volkswagen","Toyota   ","PACCAR","Ford","Honda"],
                "Consum":["Walmart","Nestlé","Coca-Cola","PepsiCo","Procter&Gamble"]}#Creem això per a que ens deixi posar les mepreses i el sector al for, busacsr video

        # Creo dues liistes, una per les empreses_triades
        empreses_triades=[]

        #I un altre per als percentatges del capital amb aquella empresa
        percentatges_triats =[]

        # I un altre llista per guardar tots els percents de la simulació 
        distribució_gran=[]

        # Creo una funció la qual si s'excecuta st.session_state.boto_1 sera falsa
        def canvi_sector_empresa_percentatge():
         st.session_state.boto_1=False

    
        # Ara aqui vaig recorrent el número d'empreses seleccionades
        for i in range(número_empreses):

            # Contorn   
            with st.container(border=True):# després mirar
                ap1,ap2,ap3=st.columns(3)

                # En el primer lloc per cada empresa demano el sector
                with ap1:
                    sector_i=st.selectbox(
                            label=f"Tria el sector de l'empresa {i+1}", #la f serveix per fer càlculs dins de les cometes, comença a comptar des de el 0
                            options =["Tecnologia","Financer","Serveis digitals","Energia","Salut","Inmobiliari","Automoció","Consum"],
                            key=f"sector_{i}",#Streamlit necesita distinguirlos, i = 0 → "sector_0" i = 1 → "sector_1" i = 2 → "sector_2" para que no se qued etodo el rato con la misma ex: APPLE
                            on_change= canvi_sector_empresa_percentatge
                    )
                # L'empresa    
                with ap2:
                    empresa_1= st.selectbox(
                            label=f"Tria l'empresa {i+1}",
                            options=empreses[sector_i], # Escojer las empresas del sector escogido , sector_i porque sino es igual al primero. ex: b&H..
                            key=f"empresa_{i}",
                            on_change= canvi_sector_empresa_percentatge
                    )
                # I el percentatge del percent del capital que es fara servir a la simulacio
                with ap3:
                    percentatge=st.slider(
                            label=f"Tria el percentatge de l'empresa {i+1}",
                            min_value=1,
                            max_value=99,
                            value=50,
                            step=1,
                            key=f"percentatge{i}",
                            on_change=canvi_sector_empresa_percentatge
                    )

                    # I creo la xifra del capital que es destinara a la simulaicó
                    mostrar_percentatge= capital*percentatge/100

                    # I l'ensenyo
                    st.write(f"Capital inicial: {mostrar_percentatge:.0f} USD")

                    # I afegeixo cada percentatges en la llista de tots els percentatges
                    distribució_gran.append(mostrar_percentatge)

                
                    

            
            # Després vaig guardant les empreses a la llista del principi
            empreses_triades.append(empresa_1)

            # I també els perentatges
            percentatges_triats.append(percentatge)

        # Aqui miro si hi han empreses repetides     
        if len(empreses_triades) != len(set(empreses_triades)):
        # https://www.youtube.com/shorts/U2DcHWloBFQ
                st.write("No pot haver empreses repetides")

        # Si els percentages sumen 100 i no hi han empreses repetides entra en aquest if       
        elif sum(percentatges_triats)== 100 and len(empreses_triades)== len(set(empreses_triades)):
        

    
        
            # Creo una llista de guardar_dades        
            guardar_dades = []

            # I una variable que comença sent falsa (error_dates)
            error_dates = False

            # Ara creo un loop per extreure tota la informació de yf per fer la simualció amb la variable de emrpesa_dades de la llista de totes les empreses triades   
            for empresa_dades in empreses_triades:

                        # Creo una variable que busqui l'empresa triada al dicci_ticker i que aquesta variable guarda el ticker de l'empresa
                    ticker = dicci_tickers[empresa_dades]

                        # Ara amb la variable de empresa_triada li dic a Yahoo finance que creii/cerqui el ticker d'abans per extreu-re l'informació
                    empresa_ticker = yh.Ticker(ticker)

                    # Demano tot l'historial disponible de l'empresa
                    historial_empresa = empresa_ticker.history(period="max",auto_adjust=True)
                    

                    # En el cas que alguna empresa no tingui dades en el periode de temps ntra aqui
                    if historial_empresa.empty:
                        # T'avisa
                        st.warning(f"No hi ha dades disponibles per a {empresa_dades}.")
                        # I directament error_dates es torna positiu
                        error_dates = True

                        # I es para tot
                        break

                    # Primera data disponible de l'empresa
                    primera_data_empresa = historial_empresa.index[0].date()

                    # Si l'empresa va començar després de la data inicial escollida
                    if primera_data_empresa > data_1div:
                        st.warning(
                                # T'avisa que no té dades suficients per començar
                            f"{empresa_dades} no té dades suficients per començar la simulació el {data_1div}."
                        )
                        # I directament error_dates es torna positiu
                        error_dates = True
                    
                        # Surt
                        break

                    # Agafo les dades del període seleccionat, és a dir la seva taula que em proporciona yh
                    dades_taula = empresa_ticker.history(
                        start=data_1div,
                        end=data_2div,
                        auto_adjust=True
                    )


                    # Aqui torno a comprobar que si exiteixen totes les dates
                    if dades_taula.empty:
                        st.warning(f"No hi ha dades per a {empresa_dades} en aquest període.")

                        # I directament error_dates es torna positiu
                        error_dates = True

                        # I es para
                        break

                    # I afegeixo el periode de les dade de cada empresa a guardar dades
                    guardar_dades.append(dades_taula)


            # EN el cas que no hi hagi errors entra 
            if not error_dates:

                # Cerco les dates que tenen en comú totes les empreses, és a dir ara tenen totes el mateix període
                    dates_comunes = guardar_dades[0].index


                    # Després torno a recorrer totes les dades de la llista de dades
                    for dades in guardar_dades[1:]:
                        # https://www.askpython.com/python/list/x-in-a1-mean-python

                        #I amb intersection agafa tots els valor que son completament iguals, així ara si tinc totes les dates iguals
                        dates_comunes = dates_comunes.intersection(dades.index)
                        # https://www.w3schools.com/python/ref_set_intersection.asp


                    # En el cas que no tingui cap data de en comú t'avisa
                    if len(dates_comunes) == 0:
                        st.warning("Les empreses no tenen dates de cotització en comú.")

                    #Si si que hi han dates entra
                    else:

                    # I em quedo només amb les dates comunes
                        guardar_dades = [dades.loc[dates_comunes]

                        # De cada dada  
                        for dades in guardar_dades
                        # https://elpythonista.com/list-comprehensions-python
                    ]


                    # A partir d'aquí continua la simulació

                    # Gràcies al zip ajunto les empreses, els diners destinats i la taula on i son les dates corresponents.    
                    dades_accions= zip(empreses_triades,distribució_gran,guardar_dades)
                    # https://www.geeksforgeeks.org/python/zip-in-python/ 


                    # Creo una llista de totes les empreses per fer-á utilizar al gràfic
                    totes_les_empreses=[]

                    # I també guardo els nombs de les empreses        
                    noms_de_les_empreses=[]
                    
                
                    
                    # 
                    valor_final_individual =[]

                    dades_gràfic_empreses_individual={} #Volem un dicionari, si lo ponemls en le antes del for de despues todo se borrara caundo tenga una empresa, "como que limpia el diccionario"

                    accions_totals=[]              

                    # Aqui demano la emoresa, el capital i les dates al zip d'abans             
                    for empresa,diners_distribució,taula in dades_accions:  

                            # Demano el preu inicial
                            open_preu= taula["Open"].iloc[0]

                            # Creo el número d'accions comprades
                            accions= diners_distribució/open_preu


                            # El preu final de cada empresa
                            end_preu = taula["Close"].iloc[-1]

                            # Calculo el valor fial de cada emrpesa
                            valor_final_1= end_preu*accions

                            # I els afegeixo ala llista de valor_final_individual per a que no s'ajuntin totes les dades
                            valor_final_individual.append(valor_final_1)
                            
                            # I el amteix amb els noms, a cada volta guarda el nom d'aquella empresa al loop
                            noms_de_les_empreses.append(empresa)

                            accions_totals.append(accions)

                            # Creo una llista dels valors de cada empresa per a que sigui individual
                            valors_de_cada_empresa=[]

                                                                
                            # Creo un loop que recorre cada data de la taula de index de yf
                            for dates_DIS_act in taula.index:
                                    # I calculo tots els preus de tots els dies
                                    preu_dia=taula.loc[dates_DIS_act,"Close"]

                                    # A més de calcular el seu valor
                                    valor_dia=accions*preu_dia #las acciones no canvian, canvia su precio. EX:10 acciones, precio dia 2: 1100, 10 *110$, dia 3: 900, 10*90$

                                    # I agefir-lo a la llista de els valors de cada empresa
                                    valors_de_cada_empresa.append(valor_dia) # valors_de_cada_empresa ↓ [6000, 6050, 5900, 6100]


                            # I vaig afegint tots els valors de cada empresa a la llista de totes_les_empreses per a tenir totes les empreses juntes    
                            totes_les_empreses.append(valors_de_cada_empresa) 

                            # Això asocia el nom de la empresa amb els valors de cada empresa per saber a quins coresponen
                            dades_gràfic_empreses_individual[empresa]=valors_de_cada_empresa # aqui ponemos empresa porque asi cada vuelta detecta en que empresa esta en esa vuelta, si pusiera "APPLE" estaria mal
                            

                    # I creem una taula a partir de la associació de cada empresa amb els seus valors
                    taula_de_cada_empresa_individual=pd.DataFrame( # No cal un diccionari perque ja tinc els nombs de les columnes
                    dades_gràfic_empreses_individual)

                    # Afegeixo una nova columna a la taula anterior anomenada dates on jo associo tots els valors amb les dates
                    taula_de_cada_empresa_individual["Dates"]= dates_comunes 
                            


                    # Ara que ja tinc tots els valors de cada empresa els he de sumar per a crear un únic gràfic amb tots els valors
                    #Primer creo la llista
                    capital_total=[]

                    # I per cada valor a la taual de toes les empreses vaig recorrent els valors desde el principi
                    for i in range(len(totes_les_empreses[0])):#range no pot ser una lista
                    # https://docs.python.org/es/3.7/tutorial/introduction.html

                                        # Creo una variable per començar a el capital desde 0
                                        capital_dia=0

                                        # I un loop per recorre tot el capital d'una empresa en una
                                        for empresa in totes_les_empreses:

                                            capital_dia= capital_dia+ empresa[i] # [2000, 2000, 2200], valor de esta empresa en este dia

                                        # I el vaig sumant    
                                        capital_total.append(capital_dia)# tiene que estar fuera porque queremos guardar una solo suma por dia, no una suma por cada empresa
                            
                                
                        # Ara que ja tinc a la llista tots els valors i dies de l'empresa ara el que faig és crear una altra taula amb dues columnes (diccionari) per posar-li nom
                        # El primer el capital i després la data        
                    taula_DIS = pd.DataFrame({
                                        "Capital":capital_total,
                                        "Data":dates_comunes
                                })
                
                
                

                    # Creo el boto per començar la simualció
                    boto_1= st.button(
                        label="Començar simulació",

                        # Key perquè sinó no funciona després quan li donem a guardar simualcio perque torna a llegir i aixì estarà apagat
                        key="boto_diversificació"

                        # MIRAR ESTO!!
                )

                    

                    # Si es prem el boto  st.session_state.boto_1 es True
                    if boto_1==True:
                        st.session_state.boto_1=True

                    # SI  st.session_state.boto_1 es True entra en aquest if
                    if st.session_state.boto_1 == True:

                                    # Divisor
                                    st.divider()
                                    # Subtitols
                                    st.subheader("Etapa 2")
                                    st.subheader("Gràfic total")

                                    # I creo el gràfic total de totes les empreses
                                    st.altair_chart(alt.Chart(taula_DIS).mark_line().encode(
                                        x="Data:T",
                                        y="Capital:Q"
                                    ).properties(height=600))

                                    # Calculo el valor final amb l'ultim valor del capital
                                    valor_final= capital_total[-1]

                                    # Faig la fórmula del benefici
                                    benefici= valor_final-capital

                                    # I la de rentabilitat
                                    rentabilitat= (valor_final-capital)/capital*100
                                    
                                    
                                    # Subtitol
                                    st.subheader("Detalls de la inversió")

                                    # Aqui per causes d'estètica creo diferents columnes amb diferents mides per aconseguir un recuadra remarcat on es detalli tots els detalls de la simulació
                                    # Les columens 3,4,5 només són espais
                                    col_resultats,col3,col4,col5 = st.columns([5,1,1,1])
                                    with col_resultats:
                                        with st.container(border=True):
                                            col1,col2=st.columns(2)


                                    with col1: 

                                        accions_totals_suma=sum(accions_totals)
                                        st.write(f"Nombre d'accions comprades: {accions_totals_suma:,.2f}")
                                        # Represento la fórmula de rendibilitat amb dos decimals en percent
                                        st.write(f"Rendibilitat : {rentabilitat:,.2f} %") 

                                            # Per aconseguir fer el drawdown torno a crear una altra taula de pandas de la llista de valors amb pd.Series, i gràcies amb .cummax aconsegueixo registrar obtenir el número més gran amb relació amb el anterior
                                        maxims_acumulats=pd.Series(capital_total).cummax()

                                        # Ara creo la variable de drawdown i establexo una altra taula amb la seva fórmula corresponent en percent
                                        drawdonw=((pd.Series(capital_total)/(maxims_acumulats))-1)*100

                                            # Amb -min de la taula de drawdown agafo el número més petit, és a dir la caiguda més gran (drawdonw) ja que estan en percents negatius
                                        caiguda_mes_gran=drawdonw.min()

                                        # Represento el resultat del màxim drawdonw
                                        st.write(f"Màxim Drawdown: {caiguda_mes_gran:,.2f} %")


                                        # Creo una nova taula de pandas de la llista de valor_BUY, després amb .pct_change calculo el canvi que hi ha hagut entre el valors anteriors i els actuals, és a dir el percentatge de diferència que hi ha hagut d'un valor a un altre
                                        # Amb .dropna m'ajuda a borrar aquella primera filera ja que com no té un valor anterior em sortiria None
                                        rendiments = pd.Series(capital_total).pct_change().dropna()

                                        # Creo la variable de que la taxa de risc és de 0                                                  
                                        taxa_sense_risc = 0

                                        # Ara amb la variable de sharpe faig el càlcul corresponent
                                        # .mean fa la mitjana de tota la llista del rendiments
                                        # .std conterteix tots els rendiments diaris en un únic valor que mostra quan han variat entre ells    
                                        sharpe = (rendiments.mean() - taxa_sense_risc) / rendiments.std() * (252 ** 0.5)

                                        # Creo la variable de volatilitat on poso la seva fórmula corresponent
                                        volatilitat = rendiments.std() * (252 ** 0.5) * 100

                                        # Represento la volatilitat
                                        st.write(f"Volatilitat: {volatilitat:,.2f} %")

                                        # Represento el sharpe
                                        st.write(f"Sharpe: {sharpe:,.2f}")

                                    
                                        
                                    with col2:   

                                        # Represento el resultat de benefici amb números més grans
                                        st.metric(
                                            label="Benefici:",
                                            value= f"{benefici:,.2f} USD")

                                        # Represento el resultat del valor final de la simulació amb la mateixa mida que el benefici
                                        st.metric(
                                            label="Valor final:",
                                            value=f"{valor_final:,.2f} USD"
                                        )
                                    
                                    # I seguidament ensenyo el gràfic de cada empresa
                                    st.subheader("Gràfic de cada empresa")
                                    st.altair_chart(alt.Chart(taula_de_cada_empresa_individual).transform_fold(noms_de_les_empreses).mark_line().encode(
                                        
                                        x="Dates:T",
                                        y="value:Q",
                                        color="key:N"

                                    ).properties(height=600))

                                    st.subheader("Detalls de la simulació:")
                                    o1,espai=st.columns([1.6,3])
                                
                                    with o1:
                                        with st.container(border=True):
                                                
                                                st.markdown("##### Valor final")

                                                # Creo aquest loop perque vagi recorrent totes les empreses i escrivint el seu valor final de la llista anterior
                                                for i in range(len(noms_de_les_empreses)):
                                                        st.metric(
                                                            label=f"{noms_de_les_empreses[i]} USD",
                                                            value= f"{valor_final_individual[i]:,.2f} USD")


                                        # Creo el boto de l'opció de poder guardar la simulació
                                    guardar_simulació= st.button("Guardar simulacio")

                                    
                                    # En el cas que es premi el boto de guardar_simulació...
                                    if guardar_simulació ==True:

                                            # Creo una variable de simulacions_repetides i la denomino com a Falsa
                                        simulacions_repetides=False

                                            # Aqui estableixo un loop on detecta totes les dades de les demés simulacions que s'han guardat
                                            # Si es la primera simulació que es guarda, com la llista de st.sessions_state.Simulacions_guardades no està creada, és a dir és buida, per tant totes les condicions adins del loop no s'executarán
                                        for simulacions in st.session_state.Simulacions_guardades:

                                                # Estableixo una condició on si amb una altra simulació coincideix en el: Nom de l'estratègia, l'empresa, el capital inicial, la data inicial i la data final. Directament la variable de simulacions_repetides es torna True
                                            if (simulacions["Estratègia"]=="Diversificació" and simulacions["Empresa"]== ",".join(noms_de_les_empreses) and simulacions["Capital inicial"]==capital and simulacions["Data inici"]==data_1div and simulacions["Data final"]==data_2div):
                                                simulacions_repetides=True

                                            # En el cas que simulacions_repetides sigui True t'avisara amb el següent missatge        
                                        if simulacions_repetides==True:
                                            st.warning("No es pot repetir la mateixa simulació")

                                            # En el cas que no s'activi, és a dir, continui en false, llavors creo un diccionari (dicci_DI) el qual guarda: L'estratègia, l'empresa, el capital inicial, el valor fianl, el benefici, la rendibilitat, el màxim drawdown, la volatilitat, el sharpe, el capital màxim i el capital mínim, l'evolució del capital, és a dir la llista dels valors, la evolució de les dates, és a dir, la llista de totes les dates, la data d'inici i la data final    
                                        else:
                                            dicci_DI= {"Estratègia":"Diversificació","Empresa":",".join(noms_de_les_empreses),#join lo que hace es que el nombre de las emrpesas me las junta en solo un mismo texto TypeError: can only concatenate list (not "str") to list
                                                    "Capital inicial":capital,"Valor final":valor_final,"Benefici":benefici,"Rendibilitat":rentabilitat,"Màxim Drawdown":caiguda_mes_gran,"Volatilitat":volatilitat,"Sharpe":sharpe, "Evolució capital":  capital_total,"Evolució dates": dates_comunes,"Data inici":data_1div,"Data final":data_2div}

                                            # Després de crear aquest diccionari amb totes les dades guardades l'afegeixo a la llista de   st.session_state.Simulacions_guardades amb .append
                                            st.session_state.Simulacions_guardades.append(dicci_DI)

                                                # T'avisa que s'ha guardat
                                            st.write("Simulació guardada")

                                            # I torna a reiniciar el programa per a que així s'actualitzi la llista de les simulacions guardades
                                            st.rerun()



        # En el cas que la sume dels percentatges superi el 100% no et deixa avançar                   
        elif sum(percentatges_triats) > 100:
            st.write("La suma dels percentatges no pot superar el 100%")
            st.write("Intenta-ho modificar")
        # I el mateix si la suma és més petita que 100   
        elif sum(percentatges_triats) < 100: 
            st.write("La suma dels percentatges ha de ser igual a 100%")
            st.write("Intenta-ho modificar") 