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

# CONSTANTES

# dictionnaire des vins avec leur localisation et leur couleur
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

# dictionnaire pour enregistrer les marqueurs affichés ou non sur la carte
DICT_MARKERS = {}

COORD_BASE = (40.463667, -3.749220) # coordonnées de départ de la carte centrée sur l'Espagne
COORD_ALL = (36.140751, -5.353585) # coordonnées centrées sur Gibraltar afin de centrer la carte pour voir tous les vins affichés
ZOOM_BASE = 6 # zoom de départ de la carte de l'Espagne
ZOOM_ALL = 5 # zoom plus large pour voir tous les vins sur la carte
ZOOM_VIN = 7 # zoom sur les régions viticoles de l'Espagne

# chemin vers le dossier contenant les images à utiliser pour les icons
CUR_DIR = Path.cwd()
CHEMIN_IMG = CUR_DIR / "img"

# ---------- fonctions des boutons d'action ----------
# fonction d'affichage des icons sur la carte
def icon_vin(vin: str, carte_vins, dict_vins: dict = DO_VINOS, zoom: int = ZOOM_VIN):
    # récupérer le chemin de l'image correspondant à l'icon "Tinto" ou "Blanco" à afficher sur la carte en fonction de la couleur du vin
    chemin_image = CHEMIN_IMG / "tinto.webp" if dict_vins[vin][1] == "Tinto" else CHEMIN_IMG / "blanco.webp"
    image_vin = ImageTk.PhotoImage(Image.open(chemin_image).resize((40, 40))) # définir le format de l'icon à afficher

    # vérifier si un icon est placé sur la carte
    if vin in DICT_MARKERS:
        DICT_MARKERS[vin].delete() # efface l'icon de la carte
        del DICT_MARKERS[vin] # supprime le vin du dictionnaire des marqueurs affichés
    # créer un icon avec l'image correspondante et l'afficher sur la carte
    else:
        coordonnees = dict_vins[vin][0] #récupère les coordonnées du vin
        icon = carte_vins.set_marker(coordonnees[0], coordonnees[1], text=vin, font=("Snell Roundhand", 20, "bold"), icon=image_vin) # crée l'icon
        carte_vins.set_position(coordonnees[0], coordonnees[1]) # positionne la carte centrée sur le vin sélectionné
        carte_vins.set_zoom(zoom) # zoom sur la région du vin sélectionné
        DICT_MARKERS[vin] = icon # ajoute le vin dans le dictionnaire des marqueurs affichés
        return icon

# fonction pour réinitialiser la carte
def clear(carte_vins, coordonees: tuple = COORD_BASE, zoom: int = ZOOM_BASE):
    # effacer tous les icons de la carte
    for vin in DICT_MARKERS:
        DICT_MARKERS[vin].delete()
    DICT_MARKERS.clear() # efface tout le dictionnaire des marqueurs affichés
    # réinitialiser la carte avec l'affichage de départ
    carte_vins.set_position(coordonees[0], coordonees[1])
    carte_vins.set_zoom(zoom)

# fonction pour afficher tous les vins sur la carte
def show_all(carte_vins, zoom: int = ZOOM_ALL, dict_vins: dict = DO_VINOS):
    # réinitialiser la carte
    clear(carte_vins=carte_vins)
    # afficher les vins
    for vin in dict_vins:
        chemin_image = CHEMIN_IMG / "tinto.webp" if dict_vins[vin][1] == "Tinto" else CHEMIN_IMG / "blanco.webp"
        image_vin = ImageTk.PhotoImage(Image.open(chemin_image).resize((40, 40)))
        coordonnees = dict_vins[vin][0]
        icon = carte_vins.set_marker(coordonnees[0], coordonnees[1], text=vin, font=("Snell Roundhand", 20, "bold"), icon=image_vin)
        DICT_MARKERS[vin] = icon
    # repositionner la carte avec un zoom plus large afin de visualiser tous les vins en même temps sur la carte
    carte_vins.set_position(COORD_ALL[0], COORD_ALL[1])
    carte_vins.set_zoom(zoom)
    return icon

# ---------- créer la fenêtre principale ----------
fenetre_principale = Tk()
fenetre_principale.title("Vinos Ibericos")
fenetre_principale.geometry("1080x720")
fenetre_principale.minsize(1000, 630)
fenetre_principale.config(background="#C1121F")

# ---------- créer 2 frames principales ----------
# configuration de la grille principale
fenetre_principale.columnconfigure(0, weight=0)
fenetre_principale.columnconfigure(1, weight=1)
fenetre_principale.rowconfigure(0, weight=1)

# frame de la carte de l'Espagne
frame_carte = Frame(fenetre_principale, background="#C1121F")
frame_carte.grid(row=0, rowspan=1, column=1, columnspan=1, padx=(0, 30), pady=20, sticky="nswe")

# frame contenant les boutons d'affichage des vins
frame_boutons_vins = Frame(fenetre_principale, background="#C1121F")
frame_boutons_vins.grid(row=0, column=0, padx=(30, 30), pady=20)

# ---------- frame de la carte de l'Espagne ----------
# configuration de la grille de la frame
frame_carte.columnconfigure(0, weight=1)
frame_carte.columnconfigure(1, weight=0)
frame_carte.columnconfigure(2, weight=0)
frame_carte.columnconfigure(3, weight=1)
frame_carte.rowconfigure(0, weight=0)
frame_carte.rowconfigure(1, weight=1)
frame_carte.rowconfigure(2, weight=0)

# créer widget de la carte
carte_des_vins = Tkmv.TkinterMapView(frame_carte, corner_radius=20)
carte_des_vins.set_position(COORD_BASE[0], COORD_BASE[1])
carte_des_vins.set_zoom(ZOOM_BASE)
carte_des_vins.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nswe")

# nom de la carte
nom_carte = Label(frame_carte, text="Vinos Ibericos", font=("Snell Roundhand", 28, "bold"), foreground="black", background="#C1121F")
nom_carte.grid(row=0, column=1, columnspan=2, padx=0, pady=0, sticky="we")

# bouton pour réinitialiser la carte
bouton_clear = Button(frame_carte, text="Clear All", font=("Snell Roundhand", 20, "bold"), border=0, command=partial(clear, carte_des_vins))
bouton_clear.grid(row=2, column=1, padx=(0, 2), pady=(5, 0), sticky="we")

# bouton pour afficher tous les vins sur la carte
bouton_show_all = Button(frame_carte, text="Show All", font=("Snell Roundhand", 20, "bold"), border=0, command=partial(show_all, carte_des_vins))
bouton_show_all.grid(row=2, column=2, padx=(2, 0), pady=(5, 0), sticky="we")

# ---------- frame des boutons d'action ----------
# configuration de la grille de la frame
frame_boutons_vins.columnconfigure(0, weight=1)

# créer les boutons d'affichage des vins
row = 0
for vin in DO_VINOS:
    bouton_vin = Button(frame_boutons_vins, text=vin, font=("Snell Roundhand", 18), background="#C1121F", border=0, command=partial(icon_vin, vin, carte_des_vins))
    bouton_vin.grid(row=row, column=0, padx=0, pady=2, sticky="ew")
    row += 1

# lancement de l'appli
if __name__ == "__main__":
    fenetre_principale.mainloop()

