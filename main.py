from fastapi import FastAPI
from pydantic import BaseModel
#from calculs import calcul_tri  # Importation déplacée en haut pour optimiser
from calculs import calcul_business_plan
from calculs import calcul_tri
from fastapi.middleware.cors import CORSMiddleware


# Créer une instance de l'application FastAPI
app = FastAPI()

# Ajouter CORS pour permettre les requêtes depuis ton frontend React
origins = [
    "http://localhost:3000",  # Frontend React en local
    "https://id4sun-api.vercel.app",  # Si tu utilises Vercel en production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Définir un modèle de données pour les entrées de la simulation
class SimulationInput(BaseModel):
    puissance: float      # Par exemple, la puissance installée en kWc
    productible: float
    capex: float
    tarif_achat: float
    inflation: float
   
            

# Créer un endpoint pour la simulation
@app.post("/simulate")
def simulate(data: SimulationInput):
    # Définir les paramètres de la simulation
    duree = 40
    degrad=0.4
    tpsonduleur=12
    tpsamortissement=20
        # Calcul des résultats
    #result = data.puissance * data.productible
    #tri = calcul_tri(data.puissance, data.productible, taux_inflation, duree)
    business_plan = calcul_business_plan(data.capex, data.puissance, data.productible, data.tarif_achat, duree, data.inflation, degrad,tpsonduleur,tpsamortissement)
    flux_tresorerie = [-data.capex * data.puissance * 1000]  # CAPEX initial négatif
    #flux_tresorerie += [annee["profit"] for annee in business_plan["cashflow"]]  # Ajout des flux annuels

    ir = calcul_tri(flux_tresorerie)
    # Retourner les résultats sous forme de dictionnaire


    return business_plan, ir
        #"ir": ir
    
    

