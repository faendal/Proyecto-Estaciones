# Import de las librerías relevantes
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State, callback

# Conexión con la api que contiene le información de las estaciones
url = "http://172.17.0.2:5000/mostrar_estacionesnivel?psw=12345678"
# Lectura de la información en formato json
data = pd.read_json(url, convert_dates = 'True')
# Lectura de la base de datos de ingreso y creación de pares de valores válidos
login_info = pd.read_csv('./db/login_info.csv')
login_tuples = [(str(user), str(pw)) for (user, pw) in login_info.values]

# Captura de la información de las estaciones
latr = []
lonr = []
zr = []

for i in range(0, 100):
        zr.append(data['datos'][i]['porcentajeNivel'])
        latr.append(data['datos'][i]['coordenadas'][0]['latitud'])
        lonr.append(data['datos'][i]['coordenadas'][0]['longitud'])

# Creación de la figura que irá en la página principal
fig = go.Figure(go.Densitymapbox(lat = latr, lon = lonr, z = zr, radius = 20, opacity = 0.9, zmin = 0, zmax= 100))
fig.update_layout(mapbox_style = 'stamen-terrain', mapbox_center_lon = -75.589, mapbox_center_lat = 6.2429)
fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})

# Creación de la aplicación web
app = dash.Dash(__name__)

# Layout principal que cambiará dependiendo de la url accedida
principal_layout = html.Div([
        html.H1("Proyecto de nivel de agua en Medellín"),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')])

# Layout del login. Persistence se encuentra en true para que la página no se actualice cada vez que se escriba algo o se pierda foco del input
login_layout = html.Div(
    [
        html.H1("Login"),
        html.Label('Nombre de usuario: '),
        dcc.Input(id='user', type='text', value="", persistence=True),
        html.Label('Contraseña: '),
        dcc.Input(id='pw', type='password', value="", persistence=True),
        html.Div(style={'margin-top': '20px'}),
        html.Button(children="Ingresar", id='btn_ingresar', n_clicks=0),
    ], style={'display': 'flex', 'flexDirection': 'column'})

# Layout que contiene la gráfica
info_estaciones = html.Div([html.H3("Información de las estaciones"), dcc.Graph(figure=fig)])

# Asignación del layout de la página
app.layout = principal_layout

# Validación que permite saber que elementos contienen todas las url de la aplicación. Gracias a esto reconoce elementos que no pertenecen al layout actual
app.validation_layout = html.Div([
        principal_layout,
        login_layout,
        info_estaciones
])

# Función para desplegar diferentes layouts dependiendo de la url
@callback(Output('page-content', 'children'),
                Input('url', 'pathname'))
def display_page(pathname):
        if pathname == "/":
                return login_layout
        elif pathname == "/estaciones":
                return info_estaciones
        else:
                return html.Div([html.H1("Acceso denegado"), dcc.Link("Regresar", href='/')])

# Función para cambiar la url dependiendo si pasó la autenticación o no
@callback(Output('url', 'pathname'),
                [Input('btn_ingresar', 'n_clicks'),
                Input('user', 'value'),
                Input('pw', 'value')])
def update_page(n_clicks, input_user, input_pw):
        if n_clicks > 0:
                if (input_user, input_pw) in login_tuples:
                        return '/estaciones'
                else:
                        return '/other'

# Ejecución del programa
if __name__=='__main__':
        app.run_server(host='0.0.0.0', port=80, debug=True)