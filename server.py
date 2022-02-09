from recetas_app import app
from recetas_app.controladores import controlador_receta, controlador_usuario

if __name__ == "__main__":
    app.run( debug = True )