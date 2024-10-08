import sys
import json
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PySide6.QtGui import QPixmap
from ui.ventana_principal import Ui_Ventana_principal
from ui.actores_peliculas import Ui_dialog_actor
from ui.datos_pelicula import Ui_Dialog

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__ui = Ui_Ventana_principal()
        self.__ui.setupUi(self)
        self.setWindowTitle("Ventana principal")

    def __obtener_nombres_actores(self):
        actor_1 = self.__ui.line_ingreso_actor_1.text()
        actor_2 = self.__ui.line_ingreso_actor_2.text()
        return actor_1, actor_2

    def __buscar_peliculas_actores(self):
        actor_1, actor_2 = self.__obtener_nombres_actores()
        try:
            with open('peliculas/peliculas.txt', 'r') as file:
                peliculas = json.load(file)
                peliculas_encontradas = []
                for pelicula in peliculas:
                    actores = [actor.lower() for actor in pelicula['actores']]
                    print(f"Buscando en: {actores}")  # Imprime los actores de la película
                    if actor_1.lower() in actores and actor_2.lower() in actores:
                        peliculas_encontradas.append(pelicula)
                        ventana_actor = VentanaActor(actor_1, actor_2, peliculas_encontradas)
                        ventana_actor.exec()

                return peliculas_encontradas
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "El archivo de películas no fue encontrado.")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Error al leer el archivo de películas.")
        return []


    def obtener_nombre_pelicula(self):
        return self.__ui.line_ingreso_nombre.text()

    def __buscar_peliculas(self):
        self.hide()
        nombre_pelicula = self.obtener_nombre_pelicula()

        if not nombre_pelicula:
            QMessageBox.warning(self, "Error", "Ingresa una película")
            return

        pelicula = self.pelicula_existe(nombre_pelicula)
        if pelicula:
            ventana_pelicula = VentanaPelicula(pelicula)
            ventana_pelicula.exec()
        else:
            QMessageBox.warning(self, "Película no encontrada", f"La película '{nombre_pelicula}' no está disponible.")

    def pelicula_existe(self, nombre_pelicula):
        try:
            with open('peliculas/peliculas.txt', 'r') as file:
                peliculas = json.load(file)
                for pelicula in peliculas:
                    if pelicula['titulo'].lower() == nombre_pelicula.lower():
                        return pelicula
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "El archivo de películas no fue encontrado.")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Error al leer el archivo de películas.")

class VentanaActor(QDialog):
    def __init__(self, actor_1, actor_2, peliculas):
        super().__init__()
        self.__ui = Ui_dialog_actor()
        self.__ui.setupUi(self)
        self.setWindowTitle("Ventana Actores")
        self.__ui.actor_ingresado.setText(f"{actor_1} y {actor_2}")
        self.__ui.label_peliculas_juntos.setText(", ".join([p['titulo'] for p in peliculas]))

class VentanaPelicula(QDialog):
    def __init__(self, pelicula):
        super().__init__()
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.setWindowTitle("Ventana Pelicula")

        self.__ui.label_titulo_ingresado.setText(pelicula["titulo"])
        self.__ui.label_sinopsis.setText(pelicula["sinopsis"])
        self.__ui.label_actores.setText(", ".join(pelicula["actores"]))
        self.__ui.label_puntuacion.setText(str(pelicula["puntuacion"]))
        self.cargar_poster(pelicula['poster'])

    def cargar_poster(self, archivo):
        ruta = os.path.join("peliculas", "imagen", archivo)
        pixmap = QPixmap(ruta)

        if not pixmap.isNull():
            self.__ui.label_poster.setPixmap(pixmap.scaled(350, 280))
        else:
            print("Error al cargar la imagen: archivo no encontrado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana_principal = VentanaPrincipal()
    ventana_principal.show()

    sys.exit(app.exec())
