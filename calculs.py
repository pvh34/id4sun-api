import numpy as np
import pandas as pd

#def calcul_tri(puissance, productible, taux_inflation, duree):
    # Ceci est un exemple fictif pour montrer comment structurer la fonction.
    # Tu remplaceras cette logique par celle de ton fichier Excel.
    #tri = (puissance * productible) / (1 + taux_inflation) 
    #return tri


def calcul_business_plan(capex, opex, puissance, productible, tarif_achat, duree):
    """
    Calcule l'évolution de la trésorerie pour un projet photovoltaïque.
    """
    # Revenus annuels = productible * tarif d'achat
    revenus_annuels = productible * puissance * tarif_achat
    
    # Création d'un tableau de suivi avec des objets/dictionnaires
    tab = []
    tresorerie = -capex * puissance * 1000  # On commence avec un CAPEX négatif
    for annee in range(1, duree + 1):
        charges = opex  # Supposons des charges fixes chaque année
        profit = revenus_annuels - charges
        tresorerie += profit  # Mise à jour de la trésorerie
        tab.append({
            "année": annee,
            "revenus": revenus_annuels,
            "charges": charges,
            "profit": profit,
            "tresorerie": tresorerie
        })
        
        if tresorerie >= 0:
            annee_rentabilite = annee
            break
    else:
        annee_rentabilite = "Jamais"

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

