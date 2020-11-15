#!/usr/bin/env python3
import folium, pandas

data = pandas.read_csv("volcanoes.txt")
# print(data.columns)
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
# print(len(lat), len(lon))

# folium icon color
def color_producer(elevation):
  if elevation < 1000:
    return 'green'
  elif 1000 <= elevation < 3000:
    return 'orange'
  else:
    return 'red'

# we can remove or leave in zoom_start and tiles
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="OpenStreetMap") #tiles = "Stamen Terrain"

# instead of throwing everythiing in our add_child method we can use a FeatureGroup method and use add_child within it
fg = folium.FeatureGroup(name="Volcano and Population WebMap")

html = """
<strong>Volcano information:</strong>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

# for loop over multiple coordinates and add the folium properties
for lt, ln, name, el in zip(lat, lon, name, elev): # The zip function allows you to iterate through two list
  iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
  fg.add_child(
    folium.CircleMarker(
      location=[lt, ln],
      radius=6,
      popup=folium.Popup(iframe),
      fill_color=color_producer(el),
      color="grey",
      fill_opacity=0.7
      # fill=True, Might have to use this if circles show up as blanks
    )
  )# passing the elevation into color_producer(el)


fg.add_child(folium.GeoJson())


map.add_child(fg)
map.save("volcano_and_population_webmap.html")