from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from pyspark.ml import PipelineModel, Pipeline
from pyspark.sql import SparkSession

# Initialiser l'application FastAPI et SparkSession
app = FastAPI()
spark = SparkSession.builder \
    .master("local") \
    .appName("Mushroom_Classification_API") \
    .config("spark.sql.debug.maxToStringFields", "1000") \
    .getOrCreate()

# Charger le modèle pipeline pré-entraîné avec StringIndexer inclus
pipeline_model = PipelineModel.load("api/models/logisticRegressionPipeline")

# Définir la classe pour la description du champignon
class MushroomDescription(BaseModel):

    forme_du_chapeau: str
    surface_du_chapeau: str
    couleur_du_chapeau: str
    meurtrissures: str
    odeur: str
    attache_des_lamelles: str
    espacement_des_lamelles: str
    taille_des_lamelles: str
    couleur_des_lamelles: str
    forme_du_pied: str
    racine_du_pied: str
    surface_du_pied_au_dessus_de_lanneau: str
    surface_du_pied_en_dessous_de_lanneau: str
    couleur_du_pied_au_dessus_de_lanneau: str
    couleur_du_pied_en_dessous_de_lanneau: str
    type_de_voile: str
    couleur_du_voile: str
    nombre_danneaux: str
    type_danneau: str
    couleur_de_lempreinte_des_spores: str
    population: str
    habitat: str

# Route POST pour la prédiction
@app.post("/predict")
def predict_mushroom_class(description: MushroomDescription):
    # Convertir la description en DataFrame Spark
    data = {
        "forme_du_chapeau": description.forme_du_chapeau,
        "surface_du_chapeau": description.surface_du_chapeau,
        "couleur_du_chapeau": description.couleur_du_chapeau,
        "meurtrissures": description.meurtrissures,
        "odeur": description.odeur,
        "attache_des_lamelles": description.attache_des_lamelles,
        "espacement_des_lamelles": description.espacement_des_lamelles,
        "taille_des_lamelles": description.taille_des_lamelles,
        "couleur_des_lamelles": description.couleur_des_lamelles,
        "forme_du_pied": description.forme_du_pied,
        "racine_du_pied": description.racine_du_pied,
        "surface_du_pied_au_dessus_de_lanneau": description.surface_du_pied_au_dessus_de_lanneau,
        "surface_du_pied_en_dessous_de_lanneau": description.surface_du_pied_en_dessous_de_lanneau,
        "couleur_du_pied_au_dessus_de_lanneau": description.couleur_du_pied_au_dessus_de_lanneau,
        "couleur_du_pied_en_dessous_de_lanneau": description.couleur_du_pied_en_dessous_de_lanneau,
        "type_de_voile": description.type_de_voile,
        "couleur_du_voile": description.couleur_du_voile,
        "nombre_danneaux": description.nombre_danneaux,
        "type_danneau": description.type_danneau,
        "couleur_de_lempreinte_des_spores": description.couleur_de_lempreinte_des_spores,
        "population": description.population,
        "habitat": description.habitat
    }
    
    new_df = spark.createDataFrame([data])
    # Extraire les étapes du pipeline pour la prédiction
    # On enlève l'indexeur de "classe" qui est la première étape
    predict_stages = pipeline_model.stages[1:]  # Exclure la première étape (label_indexer)

    # Créer un nouveau pipeline pour la prédiction sans le label_indexer
    predict_pipeline = Pipeline(stages=predict_stages)
    # Appliquer le pipeline pour la prédiction
    predictions = predict_pipeline.fit(new_df).transform(new_df)  # Utilisez fit-transform pour éviter les erreurs

    # Récupérer la prédiction
    prediction = predictions.select("prediction").collect()[0][0]
    print(f"La classe prédite est : {'edible' if prediction == 0.0 else 'poisonous'}")
    
    # Retourner la classe prédite
    return {"class": "edible" if prediction == 0.0 else "poisonous"}

# Exécuter l'application FastAPI
# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)
