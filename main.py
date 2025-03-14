from fastapi import FastAPI
from pydantic import BaseModel
from calculs import calcul_tri  # Importation déplacée en haut pour optimiser

# Créer une instance de l'application FastAPI
app = FastAPI()

# Définir un modèle de données pour les entrées de la simulation
class SimulationInput(BaseModel):
    puissance: float      # Par exemple, la puissance installée en kWc
    productible: float    # Production moyenne pour 100 kWc, par exemple

# Créer un endpoint pour la simulation
@app.post("/simulate")
def simulate(data: SimulationInput):
    # Définir les paramètres de la simulation
    taux_inflation = 0.03
    duree = 20
    
    # Calcul des résultats
    result = data.puissance * data.productible
    tri = calcul_tri(data.puissance, data.productible, taux_inflation, duree)
    
    # Retourner les résultats sous forme de dictionnaire
    return {"result": result, "tri": tri}

    

