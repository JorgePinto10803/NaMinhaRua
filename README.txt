########################################################################################################################################################################################################################################################
#Ocorrências Analysis - "Na Minha Rua" App                                                                                                                                                                                                             #
#This project provides an analysis of occurrences in the "Na Minha Rua" application, a platform where citizens report issues within their neighborhoods. The data is processed and visualized using interactive maps and charts.                       #
#                                                                                                                                                                                                                                                      #
########################################################################################################################################################################################################################################################
Features
Interactive map with heatmaps and marker clusters to visualize occurrences by geographical location.
Customizable filtering by freguesia, subseção, area, and tipo.
Visualizations of occurrences over time with line and bar charts.
Integrated with Streamlit for building interactive web applications.

############################################################################################################################
Requirements
To run this project, you need the following Python libraries:

pandas - for data manipulation and analysis.
folium - for interactive maps.
folium.plugins - for heatmaps and marker clusters.
branca - for color intensity in maps.
streamlit - for creating interactive web applications.
pathlib - for handling file paths.
streamlit_folium - for integrating maps in Streamlit.
plotly.express - for interactive charts.

############################################################################################################################
Run the following command to install the libraries:
pip install pandas folium streamlit plotly streamlit-folium branca

How to run?#################################################################################################################
Confidentiality Notice: The dataset (combined_sorted_ym.gopi_data.csv) is required to run the script. Due to confidentiality reasons, the data files are not provided in this repository. Please ensure you have access to the necessary data and place it in the NaMinhaRua/Ficheiros de dados Manipulados directory (adjust the path if needed).
Run the Streamlit app using the following command: streamlit run Search_Engine_Dashboard.py
The application will open in your default web browser, where you can select filters and explore the data.


Description of the Code#####################################################################################################
Data Loading and Caching
The data is loaded from a CSV file and cached to improve performance. The dataset contains columns such as Freguesia, Subseccao, Tipo, Area, and geographical coordinates (Latitude_Subseccao, Longitude_Subseccao). Each row represents an occurrence.

Data Filtering##############################################################################################################
You can filter the occurrences by:
--> Freguesia: The area or district (e.g., Lisbon, Porto).
-->Subseccao: A subsection within the freguesia.
-->Tipo: Type of occurrence (e.g., potholes, garbage collection issues).
-->Area: The geographical area of the occurrence.


Interactive Features#######################################################################################################
HeatMap: Displays the intensity of occurrences based on their geographical locations.
MarkerCluster: Groups nearby markers to reduce clutter and improve map performance.
Charts: Interactive line and bar charts show the distribution of occurrences over time and by type.
Map and Visualizations
Map: The map is centered on Lisbon with adjustable zoom and filtering options.
Charts: The line chart shows the trend of occurrences over time, and the bar chart shows the distribution by occurrence type.
Customization
You can adjust the minimum number of occurrences to be displayed on the map. The default is set to 3 occurrences for better performance, but you can change this through a slider in the Streamlit interface.
