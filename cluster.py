#from pydoc import describe
import streamlit as st 
from streamlit_folium import folium_static
import folium
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# Membaca dataset
data = pd.read_csv("DataSkripsiGempa.csv", sep = ";")
tabel = data[["time", "place", "depth", "mag"]]
datamap = pd.read_csv("FoliumMap.csv", sep=',')
data2 = np.array(datamap)


sidebar = st.sidebar

mode = sidebar.radio("Mode", ["EDA", "Clustering"])
st.markdown("<h1 style='text-align: center; color: #ff0000;'>Pengelompokan Daerah Rawan Gempa Bumi di Pulau Sumatra</h1>", unsafe_allow_html=True)
st.markdown("# Mode: {}".format(mode), unsafe_allow_html=True)

##EDA
if mode=="EDA":
    show_data = sidebar.checkbox("Data Gempa Bumi Pulau Sumatra")
    #distribute = sidebar.checkbox("Distribusi Data")
    scatter = sidebar.checkbox("Scatter Plot")

    if show_data:
        st.markdown("### Data Gempa Bumi di Pulau Sumatra")
        st.write(tabel)
        st.markdown("### Statistik Deskriptif")
        desk = tabel.describe()
        st.dataframe(data=desk)

    #if distribute:
        #st.title("Distribusi Data")
        #fig1 = plt.figure(figsize=(18,8))
        #tabel['depth'].hist(bins=np.arange(0,80,1))
        #plt.title("Kedalaman (km)")
        #plt.tight_layout()
        #st.pyplot(fig1)
        #fig2 = plt.figure(figsize=(18,8))
        #tabel['mag'].hist(bins=np.arange(5,10,2))
        #plt.title("Magnitudo (mb)")
        #plt.tight_layout()
        #st.pyplot(fig2)

    if scatter:
        st.markdown("### Scatterplot Data")
        fig3 = plt.figure(figsize=(18,8))
        plt.scatter(tabel['depth'], tabel['mag'])
        plt.ylabel('Magnitudo (mb)')
        plt.xlabel('Kedalaman (km)')
        st.pyplot(fig3)


##Clustering
if mode=="Clustering":
    #select algorithm
    #calg = sidebar.selectbox("Select Clustering Algorithm", ["K-Means"])
    clust = sidebar.checkbox("Hasil Pengelompokan Algoritma K-Means")
    map = sidebar.checkbox("Pemetaan Hasil Pengelompokan")
        

    if clust:
        st.markdown("### Hasil Pengelompokan Algoritma K-Means")
        st.write(datamap)

    if map:
        st.markdown("### Pemetaan Daerah Rawan Gempa Bumi di Pulau Sumatra")
        map_clust = folium.Map(location=[datamap.latitude.mean(), datamap.longitude.mean()], tiles='OpenStreetMap',zoom_start=5, control_scale=True)
        
        # get a colour
        def color_producer(cluster):
            if cluster == 1:
                col = 'red'
            else:
                col = 'yellow'
            return col

        # point_layer name list
        all_gp = []
        for x in range(len(data2)):
            pg = data2[x][3]
            all_gp.append(pg)

        # Create point_layer object
        unique_gp = list(set(all_gp))
        vlist = []
        for i,k in enumerate(unique_gp):
            locals()[f'point_layer{i}'] = folium.FeatureGroup(name=k)
            vlist.append(locals()[f'point_layer{i}'])
    
        # Creating list for point_layer
        pl_group = []
        for n in all_gp:
            for v in vlist: 
                if n == vars(v)['layer_name']:
                    pl_group.append(v)

        for (lat, lng, place, cluster, pg) in zip(datamap['latitude'],datamap['longitude'],datamap['place'],datamap['cluster'], pl_group):
            folium.vector_layers.CircleMarker([lat, lng], radius=2,
            popup=str(place)+ '- Cluster ' + str(cluster),
            tooltip = str(place)+ '- Cluster ' + str(cluster),
            color = color_producer(cluster),
            fill=True,
            fill_color = color_producer(cluster),
            fill_opacity=0.9).add_to(pg)
            pg.add_to(map_clust)
    
        map_clust.add_child(folium.LayerControl(collapsed=True)) 

        folium_static(map_clust)
