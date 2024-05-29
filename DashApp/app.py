from flask import Flask, render_template, session, redirect, url_for
import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Crear instancia de Flask
server = Flask(__name__)
server.secret_key = (
    "a9b8c7d6e5f4a3b2c1d0e9f8g7h6i5j4"  # Reemplaza con tu clave secreta generada
)


# Página principal de Flask
@server.route("/")
def index():
    return render_template("index.html")


# Ruta para el usuario no logueado
@server.route("/guest")
def guest():
    session["user_type"] = 0
    return redirect("/dashboard/?user_type=0")


# Ruta para el usuario logueado
@server.route("/logged")
def logged():
    session["user_type"] = 1
    return redirect("/dashboard/?user_type=1")


# Configurar Dash
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/dashboard/",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    ],
)
app.layout = layout
app.config.suppress_callback_exceptions = True

# Registrar los callbacks de Dash
register_callbacks(app)

# Ejecutar el servidor
if __name__ == "__main__":
    server.run(debug=True)
