from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient
from collections import Counter
import pandas as pd

# replace here with your mongodb url 
uri = "mongodb+srv://rodrigomencias08:o8Nl0JitEmFTB6YB@cluster0.7ipkl3j.mongodb.net/?retryWrites=true&w=majority"

# Connect to meme MongoDB database

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.peliculas
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

# streamlit run streamlit-mongo.py --server.enableCORS false --server.enableXsrfProtection false

st.title("Peliculas info")
# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_dataReactions():
    items = db.peliculas_reactions.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_dataReactions()

def commentsDataframe():
    db = client['peliculas']
    collection = db['peliculas_comments']
    documentos = collection.find()
    datos = []
    for documento in documentos:
        datos.append(documento)

    df = pd.DataFrame(datos)
    return df

def reactionsDataframe():
    db = client['peliculas']
    collection = db['peliculas_reactions']
    documentos = collection.find()
    datos = []
    for documento in documentos:
        datos.append(documento)

    df = pd.DataFrame(datos)
    return df
datos_reactions= reactionsDataframe()

def grafico_pastel_reactions(datos_reactions):
    fig = px.pie(datos_reactions, names='reactionId')
    st.plotly_chart(fig)



datos_df = commentsDataframe()
def grafico_barras_usuarios(datos_df):
    fig = px.bar(datos_df.groupby('userId').count().reset_index(), x='userId', y='comment')
    st.plotly_chart(fig)

def grafico_pastel_objetos(datos_df):
    fig = px.pie(datos_df, names='objectId')
    st.plotly_chart(fig)

def grafico_caja_usuarios(datos_df):
    fig = px.box(datos_df, x='userId', y='comment')
    st.plotly_chart(fig)

@st.cache_data(ttl=600)
def get_dataComents():
    itemsC = db.peliculas_comments.find()
    itemsC = list(itemsC)
    return itemsC

itemsC = get_dataComents()

def mostrarComents():
    listasdb = db.peliculas_comments.distinct("comentId")
    listasdb = list(listasdb)
    return listasdb

def mostrar():
    listasdb = db.peliculas_reactions.distinct("reactionId")
    listasdb = list(listasdb)
    return listasdb

print(mostrar())


items = get_dataReactions()

sidebar = st.sidebar
sidebar.title("Rodrigo Mencias Gonzalez")
sidebar.write("Matricula: S2006748")
sidebar.write("zs200067481@estudiantes.uv.mx")
sidebar.markdown("_")

sidebar.header("Vistas")
sidebar.header("Selecciona una opción")

agree = sidebar.checkbox("Ver resultados de comentarios en tabla ? ")
if agree:
    st.header("info de comentarios...")
    st.dataframe(itemsC)
    st.markdown("_")

agree = sidebar.checkbox("Ver resultados de comentarios raw ? ")
if agree:
    st.header("info de comentarios...")
    st.write(itemsC)
    st.markdown("_")
#
agree = sidebar.checkbox("Ver resultados en tabla ? ")
if agree:
    st.header("Resultados...")
    st.dataframe(items)
    st.markdown("_")
    
agree = sidebar.checkbox("Ver resultados raw ? ")
if agree:
    st.header("Resultados...")
    st.write(items)
    st.markdown("_")

if st.sidebar.checkbox('Tabla de comentarios'):
    collection = db['peliculas_comments']
    registros = collection.find()

    # Crear una lista con los campos "comment" y "objectId"
    data = [["Comentario", "Publicacion", "Usuario"]]
    for registro in registros:
        comment = registro['comment']
        objectId = registro['objectId']
        userId = registro['userId']
        data.append([comment, objectId, userId])

    # Mostrar la tabla en Streamlit
    st.table(data)

sidebar.header("Graficas")
sidebar.header("Selecciona una opción")

if st.sidebar.checkbox('Grafica de pastel reactions'):
    st.header("Gráfico de pastel para mostrar la proporción de reacciones por tipo:")
    grafico_pastel_reactions(datos_reactions)

if st.sidebar.checkbox('Grafica de barras reactions'):

    collection = db['peliculas_reactions']
    registros = collection.find()

    # Obtener los "reactionId" y contar la cantidad de cada uno
    reaction_ids = [registro['reactionId'] for registro in registros]
    contador_reaction_ids = Counter(reaction_ids)

    # Obtener los datos para la gráfica
    reaction_ids_list = list(contador_reaction_ids.keys())
    cantidad_list = list(contador_reaction_ids.values())

    # Crear la gráfica de barras con Plotly
    fig = go.Figure(data=[go.Bar(x=reaction_ids_list, y=cantidad_list)])

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title="Cantidad de reacciones por tipo",
        xaxis_title="Reaction ID",
        yaxis_title="Cantidad"
    )
    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)

if st.sidebar.checkbox('Grafica de pastel comments'):
    st.header("Gráfico de pastel para mostrar la proporción de comentarios por objeto:")
    grafico_pastel_objetos(datos_df)

if st.sidebar.checkbox('Grafica de barras usuarios'):
    st.header("Gráfico de barras para contar el número de comentarios por usuario:")
    grafico_barras_usuarios(datos_df)


def grafico_barras_agrupadas(datos_df):
    fig = px.bar(datos_df, x='userId', y='comment', color='objectId', barmode='group')
    st.plotly_chart(fig)

if st.sidebar.checkbox('Grafica de barras agrupadas'):
    st.header("Gráfico de barras agrupadas para mostrar el número de comentarios por usuario y por objeto:")
    grafico_barras_agrupadas(datos_df)

