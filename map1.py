
import folium
import pandas
from branca.element import Template, MacroElement


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
fgv = folium.FeatureGroup(name="My Map")

for latitude, lontitude, el in zip(lat, lon, elev):
    col = elev_color(el)
    fgv.add_child(folium.CircleMarker(location=[latitude, lontitude], popup=str(el)+" m", 
    color=col, fill=True, fill_color=col, radius=8, fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005']<10000000
 else 'orange' if 10000000 <= x['properties']['POP2005']<20000000 
 else 'red' if 20000000<=x['properties']['POP2005']<50000000 else 'purple'}))





map.add_child(fgv)
map.add_child(fgp)



template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='flex: 1; position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 15px; font-size:14px; right: 40px; bottom: 40px;'>
     
<div class='legend-title'>Population colors legend</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:purple;opacity:0.7;'></span>Population > 50mil</li>
    <li><span style='background:red;opacity:0.7;'></span>20mil < Population < 50mil </li>
    <li><span style='background:orange;opacity:0.7;'></span>10mil < Population <20mil</li>
    <li><span style='background:green;opacity:0.7;'></span>Population < 10mil</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    flex: 1;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    flex: 1;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    flex: 1;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 40px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    flex: 1;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

map.get_root().add_child(macro)

map


map.add_child(folium.LayerControl())
map.save("Map.html") 