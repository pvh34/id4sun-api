import numpy as np
import pandas as pd


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

def calcul_tri(flux_tresorerie):
    return np.irr(flux_tresorerie)

def calcul_business_plan(capex, puissance, productible, tarif_achat, duree, inflation,degrad, tpsonduleur,tpsamortissement):
    """
    Calcule l'évolution de la trésorerie pour un projet photovoltaïque.
    """
    # Revenus annuels = productible * tarif d'achat
    
    annee_rentabilite = "Jamais"  # Valeur par défaut si jamais la rentabilité n'est pas atteinte
    opex=calcul_couts_opex(puissance)
    # Création d'un tableau de suivi avec des objets/dictionnaires
    renouvellement_onduleur = 0
    amortissement_onduleur = 0
    amortissement_centrale = 0
    tab = []
    tresorerie = -capex * puissance * 1000  # On commence avec un CAPEX négatif
    flux_tresorerie=[tresorerie]
    for annee in range(1, duree + 1):
        c = opex["maintenance"]*puissance + opex["assurance"]*puissance + opex["gestion"]*puissance + opex["TURPE"]  # 
        charges=c*(1+inflation/100)**(annee-1)
        revenus_annuels = productible * puissance * tarif_achat*(1-degrad/100*annee)
        profit = (revenus_annuels) - charges
        amortissement_onduleur=puissance*60/tpsonduleur
        if annee==tpsonduleur:
            renouvellement_onduleur=puissance*60
        else:
            renouvellement_onduleur=0
        if annee <= tpsamortissement :
            amortissement_centrale=(capex*puissance*1000-60*puissance)/tpsamortissement    
        else :
            amortissement_centrale=0
        resultat_brut=profit-amortissement_onduleur-amortissement_centrale
        tresorerie += profit  # Mise à jour de la trésorerie
        flux_tresorerie.append(tresorerie)
        tab.append({
            "année": annee,
            "revenus": revenus_annuels,
            "charges": charges,
            "profit": profit,
            "Renouvellement onduleurs": renouvellement_onduleur,
            "Amortissement centrale": amortissement_centrale,
            "Amortissement onduleurs":amortissement_onduleur,
            "Résultat brut":resultat_brut,
            "tresorerie": tresorerie
        })
        
       # On définit l'année de rentabilité dès que la trésorerie devient positive
        if tresorerie >= 0 and annee_rentabilite == "Jamais":
            annee_rentabilite = annee  # Rentabilité atteinte
    tri=calcul_tri(flux_tresorerie)       
          
    return {"cashflow": tab, "annee_rentabilite": annee_rentabilite, "tri":tri}

    

