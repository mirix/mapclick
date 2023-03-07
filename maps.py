import json
import dash
import dash_leaflet as dl
from dash import Dash, dcc, html, Input, Output, State
import ast
from geopy.geocoders import ArcGIS

geolocator = ArcGIS(user_agent='geoapiExercises')

lat = 49.61128695437725
lon = 6.129437685012817

gmap = [dl.Map(style={'width': '1000px', 'height': '500px'},
		   center=[lat, lon],
		   zoom=12,
		   children=[
			   dl.TileLayer(url='http://www.google.com/maps/vt/lyrs=m&x={x}&y={y}&z={z}'),
			   dl.LayerGroup(id='marker-group')
		   ], id='map')]
		   
button_style = {'background-color': 'DarkOliveGreen', 'color': 'white', 'fontWeight': 'bold', 'fontFamily': 'Arial, Helvetica, sans-serif', 'border': '0px', 'border-radius': '5%', 'padding': '5px', 'margin': '5px'}

app = dash.Dash(__name__, external_scripts=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
	html.Div([html.Label('ADDRESS AND COORDINATES BY CLICKING ON THE MAP', style={'fontWeight': 'bold', 'color': 'DarkOliveGreen', 'fontSize': 18, 'fontFamily': 'Arial, Helvetica, sans-serif'})]),
	html.Div([html.Br()]),
	html.Div([dcc.Input(id='input-on-submit', type='text',
			placeholder='Type a location to RECENTRE the map and click SEARCH', 
			style={'width': '600px', 'height': '30px', 'fontFamily': 'Arial, Helvetica, sans-serif', 'fontSize': 14})], style={'display': 'inline-block'}),
	html.Div([html.Button('Search', id='submit-val', n_clicks=0, style=button_style)], style={'display': 'inline-block', 'margin-left': '20px'}),
	html.Div([html.Br()]),
	html.Div(gmap),
	html.Div([html.Br()]),
	html.Div([html.Label('ADDRESS AND COORDINATES', style={'color': 'DarkOliveGreen', 'fontSize': 16, 'fontFamily': 'Arial, Helvetica, sans-serif'})]),
	html.Div([html.Br()]),
	html.Div(id='address-coord', style={'color': 'Grey', 'fontSize': 16, 'fontFamily': 'Arial, Helvetica, sans-serif'}),
	html.Div([html.Br()]),
	html.Div(id='coordinate-click-id', style={'fontSize': 14, 'fontFamily': 'Arial, Helvetica, sans-serif'}),
])
	

@app.callback(
    [Output('map', 'children')],
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def recenter_map(n_clicks, value):
	if not value:
		lat = 49.61128695437725
		lon = 6.129437685012817
		zoom = 12
	else:
		location1 = geolocator.geocode(value)
		lat = location1.latitude
		lon = location1.longitude
		zoom = 16
	gmap = [dl.Map(style={'width': '1000px', 'height': '500px'},
		   center=[lat, lon],
		   zoom=zoom,
		   children=[
			   dl.TileLayer(url='http://www.google.com/maps/vt/lyrs=m&x={x}&y={y}&z={z}'),
			   dl.LayerGroup(id='marker-group')
		   ], id='map')]
	return gmap

@app.callback(Output('marker-group', 'children'), [Input('map', 'click_lat_lng')])
def set_marker(x):
	if not x:
		return None
	return dl.Marker(position=x, children=[dl.Tooltip('Dropped pin')])


@app.callback([Output('address-coord', 'children'), Output('coordinate-click-id', 'children')], [Input('map', 'click_lat_lng')])
def click_coord(e):
	if not e:
		string = ['[ click on the map ]', '']
		return string
	coor = json.dumps(e).strip('[]')
	location = str(geolocator.reverse(coor))
	return location, html.A(coor, href='https://www.google.com/maps/place/' + coor, target='_blank')


if __name__ == '__main__':
	app.run_server(debug=True, port=8150)
