
import folium
import pandas


def elev_color(elevation):
    if elevation < 1000:
        return "green"
    elif elevation >= 1000 and elevation < 3000:
        return "orange"
    elif elevation >=3000 and elevation < 4000 :
        return "red"
    else:
        return "black"


golina = folium.Map(location=[52.11, 18.1], zoom_start=11, tiles="Stamen Terrain")
golina.save("Golina_Map.html")

data = pandas.read_csv("Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

map = folium.Map(location=[35.58, -99.89], zoom_start=6, tiles="Stamen Terrain")
fg = folium.FeatureGroup(name="My Map")

for latitude, lontitude, el in zip(lat, lon, elev):
    col = elev_color(el)
    fg.add_child(folium.CircleMarker(location=[latitude, lontitude], popup=str(el)+" m", 
    color=col, fill=True, fill_color=col, radius=8, fill_opacity=0.7))


map.add_child(fg)

map.save("Map.html") 