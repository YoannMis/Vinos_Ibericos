"""Vinos ibericos

Version : 1.0
Auteur : J@nu$
Date : 17.juin.2024
"""

from tkinter import *
import tkintermapview as Tkmv
from functools import partial
from PIL import Image, ImageTk
from pathlib import Path

#CONSTANTES

#dictionnaire des vins avec leur localisation et leur couleur
DO_VINOS = {
    "Alicante": ((38.3436365, -0.4881708), "Tinto"),
    "Calatayud": ((41.3527628, -1.6422977), "Tinto"),
    "Cariñena": ((41.3382122, -1.2263149), "Tinto"),
    "Condado de Huelva": ((37.3382055, -6.5384658), "Blanco"),
    "Jumilla": ((38.4735408, -1.3285417), "Tinto"),
    "La Gomera": ((28.116, -17.248), "Blanco"),
    "Málaga": ((36.7213028, -4.4216366), "Blanco"),
    "Rías Baixas": ((42.459627886165265, -8.722862824636783), "Blanco"),
    "Ribera del Duero": ((41.49232, -3.005), "Tinto"),
    "Rioja": ((42.29993373411561, -2.486288477690506), "Tinto"),
    "Rueda": ((41.4129785, -4.9597533), "Blanco"),
    "Somontano": ((42.0883878, 0.0994041), "Tinto"),
    "Tarragona": ((41.1172364, 1.2546057), "Tinto"),
    "Txakoli de Getaria": ((43.29428414467608, -2.202397625912913), "Blanco"),
    "Xérès": ((36.6816936, -6.1377402), "Blanco")
}

#dictionnaire pour enregistrer les marqueurs affichés ou non sur la carte
DICT_MARKERS = {}

COORD_BASE = (40.463667, -3.749220) #coordonnées de départ de la carte centrée sur l'Espagne
ZOOM_BASE = 6 #zoom de départ de la carte de l'Espagne
ZOOM_VIN = 7 #zoom sur les régions viticoles de l'Espagne

CUR_DIR = Path.cwd()
CHEMIN_IMG = CUR_DIR / "img"

#fonction d'affichage des icons sur la carte
def icon_vin (vin: str, carte_vins, dict_vins=DO_VINOS, markers=DICT_MARKERS):
    chemin_image = CHEMIN_IMG / "tinto.webp" if dict_vins[vin][1] == "Tinto" else CHEMIN_IMG / "blanco.webp"
    image_vin = ImageTk.PhotoImage(Image.open(chemin_image).resize((40, 40)))

    if vin in DICT_MARKERS:
        DICT_MARKERS[vin].delete()
        del DICT_MARKERS[vin]
    else:
        coordonnees = dict_vins[vin][0]
        icon = carte_vins.set_marker(coordonnees[0], coordonnees[1], text=vin, icon=image_vin)
        carte_vins.set_position(coordonnees[0], coordonnees[1])
        carte_vins.set_zoom(ZOOM_VIN)
        DICT_MARKERS[vin] = icon
        return icon

#créer la fenêtre principale
fenetre_principale = Tk()
fenetre_principale.title("Vinos Ibericos")
fenetre_principale.geometry("1080x720")
fenetre_principale.minsize(720, 480)
fenetre_principale.config(background="#C1121F")

#créer frame contenant la carte de l'Espagne
frame_carte = Frame(fenetre_principale, background="#C1121F")
frame_carte.grid(row=0, column=1, padx=20, pady=20)

#créer le widget de la carte
carte_des_vins = Tkmv.TkinterMapView(frame_carte, width=800, height=600, corner_radius=20)
carte_des_vins.set_position(COORD_BASE[0], COORD_BASE[1])
carte_des_vins.set_zoom(ZOOM_BASE)
carte_des_vins.pack()

#créer frame contenant les boutons d'affichage des vins
frame_boutons_vins = Frame(fenetre_principale, background="#C1121F")
frame_boutons_vins.grid(row=0, column=0, padx=20)

#créer les boutons d'affichage des vins
for vin in DO_VINOS:
    bouton_vin = Button(frame_boutons_vins, text=vin, font=("Arial", 18), command=partial(icon_vin, vin, carte_des_vins))
    bouton_vin.pack(fill="x")

#ouvrir la fenetre principale
if __name__ == "__main__":
    fenetre_principale.mainloop()

