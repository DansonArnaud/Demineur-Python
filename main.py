from fltk import *
from random import *
import time


def choix_difficulte(taille_fenetre):
    efface_tout()
    demi = taille_fenetre/2
    tiers = taille_fenetre/3
    sixieme = taille_fenetre/6
    image(demi, demi, "image/fond.jpg", taille_fenetre, taille_fenetre)
    ligne(tiers, 0, tiers, taille_fenetre)
    ligne(tiers*2, 0, tiers*2, taille_fenetre)
    texte(sixieme, demi, "Débutant", ancrage="center")
    texte(sixieme*3, demi, "Intermédiaire", ancrage="center")
    texte(sixieme*5, demi, "Expert", ancrage="center")
    mise_a_jour()
    
    x = recup_clic(cond=False)[0]
    if x < tiers:
        return 9, 12
    elif x < tiers*2:
        return 16, 51
    else:
        return 22, 121

def terrain(taille_fenetre, taille_case_x, taille_case_y, decalage, nb_case, div):
    liste_couleur = ["#6E6E6E", "#8A8A8A", "#A6A6A6"]
    neuvieme = taille_fenetre/9
    seizieme = taille_fenetre/16
    
    efface_tout()
    rectangle(0, 0, taille_fenetre, taille_fenetre, remplissage="#D0D0D0")
    image(seizieme, seizieme, "image/drapeau.png", int(taille_fenetre/10), int(taille_fenetre/10)) 
    rectangle(neuvieme*7, 0, taille_fenetre, seizieme)
    texte(neuvieme*8, seizieme/2, "Menu", ancrage="center")
    for i in range (nb_case):
        for j in range (nb_case):
            rectangle(taille_case_x*i , decalage + taille_case_y*j, taille_case_x*(i+1), decalage + taille_case_y*(j+1), remplissage = liste_couleur[(i+j)%div])
    mise_a_jour()

def liste(nb_case):
    liste, liste_drap = [], []
    for _ in range (nb_case):
        liste.append([0]*nb_case)
        liste_drap.append([False]*nb_case)
    return liste, liste_drap

def premier_clic(taille_fenetre, taille_case_x, taille_case_y):
    while True:
        x, y, ty = recup_clic(cond=True)
        if ty == "ClicGauche":
            if taille_fenetre/8 < y:
                return int((y - taille_fenetre/8)//taille_case_y), int(x//taille_case_x)
            elif taille_fenetre/9*7 < x  and y < taille_fenetre/16:
                return None, None
                
def liste_jeu_mine(liste_jeu, nb_case, nb_mine, i, j):
    liste_mine = []
    while 0 < nb_mine :
        i2, j2 = randint(0, nb_case-2), randint(0, nb_case-2)
        i2 = i2 + 1 if i <= i2 else i2
        j2 = j2 + 1 if j <= j2 else j2
        if liste_jeu[i2][j2] == 0:
            liste_jeu[i2][j2] = -1
            liste_mine.append((i2, j2))
            nb_mine -= 1
    return liste_jeu, sorted(liste_mine)                

def initialisation(taille_fenetre, taille_case_x, taille_case_y, decalage, div, directions_voisins, nb_case, nb_mine, liste_jeu, liste_drapeau, liste_couleur_damier, liste_couleur):
    i, j = premier_clic(taille_fenetre, taille_case_x, taille_case_y)
    if (i, j) == (None, None):
        return None, None
    
    liste_jeu, liste_mine = liste_jeu_mine(liste_jeu, nb_case, nb_mine, i, j)
    
    nb_voisin = nb_voisins(liste_jeu, nb_case, i, j, directions_voisins)
    if 0 < nb_voisin:
        liste_jeu[i][j] = 1
        rectangle(taille_case_x*j, decalage + taille_case_y*i, taille_case_x*(j+1), decalage + taille_case_y*(i+1), remplissage = liste_couleur_damier[(i+j)%div])
        texte(taille_case_x*(1/2 + j), decalage + taille_case_y*(1/2 + i), str(nb_voisin), liste_couleur[nb_voisin - 1], "center", "Inter", int(taille_case_y/1.33))
        
        for iv, jv in directions_voisins:
            ni, nj = i + iv, j + jv
            if nb_voisins(liste_jeu, nb_case, ni, nj, directions_voisins) == 0 and liste_jeu[ni][nj] == 0:
                revele_zero(taille_case_x, taille_case_y, decalage, ni, nj, nb_case, directions_voisins, liste_jeu, liste_drapeau, liste_couleur, liste_couleur_damier, div, visite=[])
                break 
    else:
        revele_zero(taille_case_x, taille_case_y, decalage, i, j, nb_case, directions_voisins, liste_jeu, liste_drapeau, liste_couleur, liste_couleur_damier, div, visite=[])
    mise_a_jour()
    return liste_jeu, liste_mine

def nb_voisins(liste_jeu, nb_case, i, j, directions_voisins):
    compteur_de_mine = 0
    for vi, vj in directions_voisins:
        newi, newj = i + vi, j + vj
        if -1 < newi < nb_case and -1 < newj < nb_case:
            if liste_jeu[newi][newj] == -1:
                compteur_de_mine += 1
    return compteur_de_mine

def recup_clic(cond):
    while True:
        if cond:
            affiche_chrono(taille_fenetre, temps_debut)
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == "ClicGauche" or ty == "ClicDroit":
            x, y = abscisse(ev), ordonnee(ev)
            return x, y, ty
        elif ty == "Quitte":  
            exit()
        mise_a_jour()

def jeu(taille_fenetre, taille_case_x, taille_case_y, decalage, liste_jeu, liste_drapeau, directions_voisins, liste_couleur, liste_couleur_damier, div, nb_mine, nb_case):
    liste_jeu, liste_mine = initialisation(taille_fenetre, taille_case_x, taille_case_y, decalage, div, directions_voisins, nb_case, nb_mine, liste_jeu, liste_drapeau, liste_couleur_damier, liste_couleur)
    if (liste_jeu, liste_mine) == (None, None):
        return
    
    compteur = nb_mine
    texte(taille_fenetre/5, taille_fenetre/16, f"{compteur}", ancrage="center", taille=int(taille_fenetre/13), tag="compteur")
    while not victoire(liste_jeu):
        x, y, ty = recup_clic(cond=True)
        if taille_fenetre/8 < y:
            i, j = int((y - taille_fenetre/8)//taille_case_y), int(x//taille_case_x)
            if ty == "ClicDroit" and liste_jeu[i][j] != 1:
                compteur = affiche_drapeau(taille_fenetre, taille_case_x, taille_case_y, decalage, i, j, liste_drapeau, liste_couleur_damier, div, compteur)
            elif ty == "ClicGauche" and liste_drapeau[i][j] == False:
                if defaite(liste_jeu, i, j):
                    affiche_mine(taille_case_x, taille_case_y, decalage, liste_mine)
                    return False  
                nb_voisin = nb_voisins(liste_jeu, nb_case, i, j, directions_voisins)
                if 0 < nb_voisin:
                    liste_jeu[i][j] = 1
                    rectangle(taille_case_x*j, decalage + taille_case_y*i, taille_case_x*(j+1), decalage + taille_case_y*(i+1), remplissage = liste_couleur_damier[(i+j)%div])
                    texte(taille_case_x*(1/2 + j), decalage + taille_case_y*(1/2 + i), str(nb_voisin), liste_couleur[nb_voisin - 1], "center", "Inter", int(taille_case_y/1.33))
                else:
                    revele_zero(taille_case_x, taille_case_y, decalage, i, j, nb_case, directions_voisins, liste_jeu, liste_drapeau, liste_couleur, liste_couleur_damier, div, visite=[])
            mise_a_jour()
        elif taille_fenetre/9*7 < x  and y < taille_fenetre/16:
            return 
    return True 
                    
def revele_zero(taille_case_x, taille_case_y, decalage, i, j, nb_case, directions_voisins, liste_jeu, liste_drapeau, liste_couleur, liste_couleur_damier, div, visite):
    if not (-1 < i < nb_case and -1 < j < nb_case):
        return
    if (i, j) in visite:
        return
    if liste_drapeau[i][j] == True:
        return 
    visite.append((i, j))
    nb_voisin = nb_voisins(liste_jeu, nb_case, i, j, directions_voisins)
    if nb_voisin != 0 and liste_jeu[i][j] != -1:
        liste_jeu[i][j] = 1
        rectangle(taille_case_x*j, decalage + taille_case_y*i, taille_case_x*(j+1), decalage + taille_case_y*(i+1), remplissage=liste_couleur_damier[(i+j)%div])
        texte(taille_case_x*(1/2 + j), decalage + taille_case_y*(1/2 + i), str(nb_voisin), liste_couleur[nb_voisin - 1], "center", "Inter", int(taille_case_y/1.33))
        return
    liste_jeu[i][j] = 1 
    rectangle(taille_case_x*j, decalage + taille_case_y*i, taille_case_x*(j+1), decalage + taille_case_y*(i+1), remplissage=liste_couleur_damier[(i+j)%div])
    for vi, vj in directions_voisins:
        revele_zero(taille_case_x, taille_case_y, decalage, i + vi, j + vj, nb_case, directions_voisins, liste_jeu, liste_drapeau, liste_couleur, liste_couleur_damier, div, visite)

def affiche_mine(taille_case_x, taille_case_y, decalage, liste_mine):
    for i, j in liste_mine:
        image(taille_case_x*(1/2 + j), decalage + taille_case_y*(1/2 + i), "image/mine.png", int(taille_case_x), int(taille_case_y), "center")

def affiche_drapeau(taille_fenetre, taille_case_x, taille_case_y, decalage, i, j, liste_drapeau, liste_couleur_damier, div, compteur):
    if liste_drapeau[i][j] == False:
        rectangle(taille_case_x*j, decalage + taille_case_y*i, taille_case_x*(j+1), decalage + taille_case_y*(i+1), remplissage = liste_couleur_damier[(i+j)%div], tag=f"drapeau_{i}_{j}")
        image(taille_case_x*j, decalage + taille_case_y*i, "image/drapeau.png", int(taille_case_x), int(taille_case_y), "nw", f"drapeau_{i}_{j}")
        liste_drapeau[i][j] = True
        compteur -= 1
    else:
        efface(f"drapeau_{i}_{j}")
        liste_drapeau[i][j] = False
        compteur += 1
    efface("compteur")
    texte(taille_fenetre/5, taille_fenetre/16, f"{compteur}", ancrage="center", taille=int(taille_fenetre/13), tag="compteur")
    return compteur
        
def defaite(liste_jeu, i, j):
    if liste_jeu[i][j] == -1:
        return True
    return False

def victoire(liste_jeu):
    for i in range (len(liste_jeu)):
        for j in range (len(liste_jeu[i])):
            if liste_jeu[i][j] == 0:
                return False
    return True

def affiche_chrono(taille_fenetre, temps_debut):
    temps_ecoule = int(time.time() - temps_debut)
    minutes = temps_ecoule // 60
    secondes = temps_ecoule % 60
    
    efface("chrono")
    texte(taille_fenetre * 0.9, taille_fenetre/32*3, f"{minutes:02d}:{secondes:02d}", ancrage="center", taille=int(taille_fenetre/20), tag="chrono")
#---------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    taille_fenetre = 600
    cree_fenetre(taille_fenetre, taille_fenetre)
    decalage = taille_fenetre/8
    directions_voisins = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    liste_couleur = ["#2563EB", "#16A34A", "#DC2626", "#7C3AED", "#F97316", "#0891B2","#EAB308", "#6B7280"]
    liste_couleur_damier = ["#E6D3A3", "#C2A46D", "#A88C55"]

    while True:
        nb_case, nb_mine = choix_difficulte(taille_fenetre)
        div = 2 if nb_case%2 == 1 else 3
        taille_case_x, taille_case_y = taille_fenetre/nb_case, taille_fenetre*(7/8)/nb_case

        liste_jeu, liste_drapeau = liste(nb_case)
        
        terrain(taille_fenetre, taille_case_x, taille_case_y, decalage, nb_case, div)
        temps_debut = time.time()
        cond = jeu(taille_fenetre, taille_case_x, taille_case_y, decalage, liste_jeu, liste_drapeau, directions_voisins, liste_couleur, liste_couleur_damier, div, nb_mine, nb_case)
        if cond == True:
            texte(taille_fenetre/2, taille_fenetre/32, "Victoire", "#2E7D32", "center")
        elif cond == False:
            texte(taille_fenetre/2, taille_fenetre/32, "Lose", "#C0392B", "center")
        
        texte(taille_fenetre/2, taille_fenetre/32*3, "Cliquez pour relancer", ancrage="center")
        attend_ev()

