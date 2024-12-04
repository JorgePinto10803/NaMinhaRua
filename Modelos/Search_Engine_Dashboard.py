#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd #Manipulation and analysis of dataframes
import folium # For interactive maps
from folium.plugins import HeatMap, MarkerCluster # Heat points, dinamic clusters animation
from branca.colormap import linear # Intensity of map colors
import streamlit as st # Allow the creation of interactive web applications
from pathlib import Path # For file Systems directory paths
from streamlit_folium import st_folium # Integrate maps into a streamlit app
import plotly.express as px # For interarctive charts

# Page layout configuration
st.set_page_config(page_title="Análise de Ocorrências", layout="wide")  # Mover para o início

# Root dir for the main object file
base_dir = Path.home()
csv_path = base_dir / "NaMinhaRua" / "Ficheiros de dados Manipulados"

# Load the dataset
gopidataset = pd.read_csv(csv_path / 'combined_sorted_ym.gopi_data.csv')

# Load data into cache
@st.cache_data
def load_data():
    gopidataset = pd.read_csv(csv_path / 'combined_sorted_ym.gopi_data.csv')
    gopidataset['occurrences'] = 1  # Cada linha é uma ocorrência
    grouped = gopidataset.groupby(['Freguesia', 'dt_registo', 'tipo', 'area', 'Subseccao', 'Longitude_Subseccao', 'Latitude_Subseccao']).agg({'occurrences': 'sum'}).reset_index()
    return grouped

# Load the data
grouped = load_data()


# Title fo streamlit interface
st.title('Análise de Ocorrências na Aplicação Na Minha Rua')

# Divide the layout into 3 columns
col1, col2, col3 = st.columns([1, 2, 1]) 

with col1:
    # Add all parish to parish list
    freguesias_options = ['Todas as Freguesias'] + list(grouped['Freguesia'].unique())
    freguesia = st.selectbox('Selecione a Freguesia', freguesias_options, key="freguesia_selectbox")

   # Set the variable 'subsec' to None at the start
    subsec = None
    
    # Radio button to choose whether to search by Subsection
    if freguesia != 'Todas as Freguesias':
        search_by_subsec = st.radio("Quer pesquisar por Subsecção?", ('Sim', 'Não'))
    else:
        search_by_subsec = 'Não'  # Force the 'No' option if "All Freguesias" is selected

    # Ensure that 'freguesia' and the 'Freguesia' column are of the same type.
    freguesia = str(freguesia)  # Ensure that the selected option is a string.
    grouped['Freguesia'] = grouped['Freguesia'].astype(str)  # Convert the 'Freguesia' column to string

    # Check if the selected 'freguesia' exists in the data, if Freguesia !=null search_by_subsec should be visible 
    if freguesia != 'Todas as Freguesias':
        if freguesia and freguesia in grouped['Freguesia'].unique():
            subseccoes = grouped[grouped['Freguesia'] == freguesia]['Subseccao'].unique().tolist()
            if search_by_subsec == 'Sim' and subseccoes:
                subsec = st.selectbox('Selecione a Subsecção', subseccoes, key="subsec_selectbox")
            else:
                subsec = None
        else:
            st.warning("Freguesia selecionada não é válida ou não existe nos dados.")
        
        
    # Optimize data filtering
    @st.cache_data
    def filter_data(freguesia, subsec=None, area=None, tipo=None):
        if freguesia != 'Todas as Freguesias':
            filtered = grouped.loc[grouped['Freguesia'] == freguesia]
        else:
            filtered = grouped.copy()  # Keep all data if 'Todas as Freguesias' is selected.
    
        if subsec and subsec != "":  # Only filter by subsecção if 'subsec' is not None or empty
            filtered = filtered.loc[filtered['Subseccao'] == subsec]
    
        if area:
            filtered = filtered.loc[filtered['area'] == area]
    
        if tipo:
            filtered = filtered.loc[filtered['tipo'] == tipo]
    
        return filtered
    
    
    # Filter the data according to the selected freguesia
    filtered_data = filter_data(freguesia, subsec=subsec)

    # Escolher como deseja pesquisar: por Área e Tipo ou Só Tipo
    search_option = st.radio("Escolha como quer pesquisar:", ['Área e Tipo', 'Só Tipo'], key="search_option_radio")

    # Choose how you want to search: by Area and Type or by Type only
    if search_option == 'Só Tipo':
        tipos = filtered_data['tipo'].unique().tolist()
        tipo = st.selectbox('Selecione o Tipo', tipos, key="tipo_selectbox")
        filtered_data = filter_data(freguesia, subsec=subsec, tipo=tipo)

    elif search_option == 'Área e Tipo':
        areas = filtered_data['area'].unique().tolist()
        area = st.selectbox('Selecione a Área', areas, key="area_selectbox")
        filtered_data = filter_data(freguesia, subsec=subsec, area=area)

        # Tipos disponíveis dependendo da área selecionada
        tipos_area = filtered_data['tipo'].unique().tolist()
        tipo = st.selectbox('Selecione o Tipo', tipos_area, key="tipo_area_selectbox")
        if tipo:
            filtered_data = filter_data(freguesia, subsec=subsec, area=area, tipo=tipo)

    # Check if the data contains null values in latitude and longitude.
    if filtered_data[['Latitude_Subseccao', 'Longitude_Subseccao']].isnull().any().any():
        st.warning("Existem valores nulos em Latitude ou Longitude.")
    
    #Limit the minimum value of occurrences based on the selected parish
    # Set up the minimum occurrence value to avoid slowness when loading the markers.
    if freguesia == 'Todas as Freguesias':
        min_ocorrencias = 3  # Minimum limit always 3 for 'Todas as Freguesias
        st.info("Por defeito, estão a ser apresentadas apenas ocorrências com um total igual ou superior a 3.")
    else:
        # If a specific freguesia is chosen, we can adjust the minimum value
        min_ocorrencias = st.slider('Selecione o valor mínimo de ocorrências a serem consideradas', 
                                     min_value=1, max_value=int(filtered_data['occurrences'].max()), value=3)
        st.info("Por defeito, estão a ser apresentadas apenas ocorrências com um total igual ou superior a 3.")

    # Filter the dataset based on the minimum occurrence value.
    filtered_data = filtered_data[filtered_data['occurrences'] >= min_ocorrencias]
    

with col2:    
    # Create the map centered in Lisbon
    m = folium.Map(location=[38.7169, -9.1399], zoom_start=13)

    # Adicionar o HeatMap para os dados filtrados
    heat_data = []
    for index, row in filtered_data.iterrows():
        heat_data.append([row['Latitude_Subseccao'], row['Longitude_Subseccao'], row['occurrences']])

    # Create the MarkerCluster to group markers
    marker_cluster = MarkerCluster().add_to(m)

    for index, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude_Subseccao'], row['Longitude_Subseccao']],
            popup=f"Ocorrências: {row['occurrences']}<br>Tipo: {row['dt_registo']}<br>Tipo: {row['tipo']}<br>Área: {row['area']}"
        ).add_to(marker_cluster)

    # Create the HeatMap if there is data
    if heat_data:
        # Add the HeatMap with the intensity of occurrences
        HeatMap(heat_data, min_opacity=0.4, radius=15, blur=20).add_to(m)
    else:
        st.warning("Sem dados para mostrar no mapa.")

    # Add a dynamic legend
    if not filtered_data.empty:
        colormap = linear.YlGnBu_09.scale(filtered_data['occurrences'].min(), filtered_data['occurrences'].max())
        colormap.caption = "Número de Ocorrências"
        colormap.add_to(m)

    # Show the map in Streamlit
    st_folium(m, width=1000, height=800)   
    
with col3:  
    # Create the chart of incidence over time
    filtered_data['dt_registo'] = pd.to_datetime(filtered_data['dt_registo'])  # Garantir que as datas são do tipo datetime
    incidence_by_date = filtered_data.groupby('dt_registo').agg({'occurrences': 'sum'}).reset_index()

    # Create a line chart with Plotly
    fig = px.line(incidence_by_date, x='dt_registo', y='occurrences', title='Oscilação no número de ocorrências ao longo do tempo')
    fig.update_layout(xaxis_title='Data', yaxis_title='Número de Ocorrências')

    # Show plot
    st.plotly_chart(fig)

    # Display the bar chart for the distribution of types
    fig = px.bar(filtered_data, x='tipo', y='occurrences', color='tipo', title='Distribuição de Ocorrências por Tipo')
    st.plotly_chart(fig, use_container_width=True)

    # Show the map in Streamlit
    st_folium(m, width=1000, height=800)


# In[ ]:




