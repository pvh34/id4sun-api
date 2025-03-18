import numpy as np
import pandas as pd

#def calcul_tri(puissance, productible, taux_inflation, duree):
    # Ceci est un exemple fictif pour montrer comment structurer la fonction.
    # Tu remplaceras cette logique par celle de ton fichier Excel.
    #tri = (puissance * productible) / (1 + taux_inflation) 
    #return tri

puissances = np.array([0, 3, 9, 36, 100, 250, 1000, 10000])
maintenance = np.array([60, 60, 28, 12, 11, 8, 6, 4])
assurance = np.array([12, 12, 10, 8, 7.5, 6, 4, 3])
gestion = np.array([3, 3, 1.25, 0.75, 3, 3, 2, 1])

def calcul_couts_opex(puissance):
    """
    Calcule les coûts de maintenance, assurance, maintenance batterie et gestion
    en fonction de la puissance renseignée par l'utilisateur, avec interpolation linéaire.
    """
    if puissance < 36 :
        TURPE = 34.32
    elif puissance < 100 :
        TURPE = 457.08
    else :
        TURPE = 753
    
    return {
        "maintenance": np.interp(puissance, puissances, maintenance),
        "assurance": np.interp(puissance, puissances, assurance),
        "gestion": np.interp(puissance, puissances, gestion),
        "TURPE":TURPE
    }


def calcul_business_plan(capex, puissance, productible, tarif_achat, duree):
    """
    Calcule l'évolution de la trésorerie pour un projet photovoltaïque.
    """
    # Revenus annuels = productible * tarif d'achat
    revenus_annuels = productible * puissance * tarif_achat
    annee_rentabilite = "Jamais"  # Valeur par défaut si jamais la rentabilité n'est pas atteinte
    opex=calcul_couts_opex(puissance)
    # Création d'un tableau de suivi avec des objets/dictionnaires
    tab = []
    tresorerie = -capex * puissance * 1000  # On commence avec un CAPEX négatif
    for annee in range(1, duree + 1):
        charges = opex["maintenance"]*puissance + opex["assurance"]*puissance + opex["gestion"]*puissance + opex["TURPE"]  # Supposons des charges fixes chaque année
        profit = revenus_annuels - charges
        tresorerie += profit  # Mise à jour de la trésorerie
        tab.append({
            "année": annee,
            "revenus": revenus_annuels,
            "charges": charges,
            "profit": profit,
            "tresorerie": tresorerie
        })
        
       # On définit l'année de rentabilité dès que la trésorerie devient positive
        if tresorerie >= 0 and annee_rentabilite == "Jamais":
            annee_rentabilite = annee  # Rentabilité atteinte
           
          
    return {"cashflow": tab, "annee_rentabilite": annee_rentabilite}

    
# Exemple d'utilisation
#if __name__ == "__main__":
    capex = 50000
    opex = 1000
    puissance = 100
    productible = 1200  # kWh/kWc
    tarif_achat = 0.10  # €/kWh
    
    df, annee_rentable = calcul_business_plan(capex, opex, puissance, productible, tarif_achat)
    print(df)
    print(f"Année de rentabilité : {annee_rentable}")

