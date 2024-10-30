import streamlit as st
import requests
import random

# Fonction pour afficher les options en groupes de six avec des cases à cocher exclusives
def checkbox_single_row(label, options, selected_value=None):
    st.subheader(label)  # Ajouter un sous-titre pour chaque caractéristique
    option_items = list(options.items())
    for i in range(0, len(option_items), 6):
        columns = st.columns(6)  # Créer une rangée de six colonnes maximum
        for j, (option, code) in enumerate(option_items[i:i+6]):
            with columns[j]:
                # Définir `value` en fonction de `selected_value`
                if st.checkbox(f"{option} ({code})", key=f"{label}_{code}", value=(code == selected_value)):
                    # Si la case est cochée, mettre à jour la sélection dans `st.session_state`
                    st.session_state[label] = code

    # Retourne la valeur sélectionnée pour ce label
    return st.session_state.get(label)

# Interface utilisateur Streamlit
st.title("Classification des Champignons")

# Définir les options pour chaque caractéristique
characteristics = {
    "forme_du_chapeau": {
        "label": "Forme du chapeau",
        "options": {
            "Cloche": "b",
            "Conique": "c",
            "Convexe": "x",
            "Plat": "f",
            "Bombé": "k",
            "Enfoncé": "s"
        }
    },
    "surface_du_chapeau": {
        "label": "Surface du chapeau",
        "options": {
            "Fibreuse": "f",
            "Stries": "g",
            "Écailleuse": "y",
            "Lisse": "s"
        }
    },
    "couleur_du_chapeau": {
        "label": "Couleur du chapeau",
        "options": {
            "Brun": "n",
            "Crème": "b",
            "Cannelle": "c",
            "Gris": "g",
            "Vert": "r",
            "Rose": "p",
            "Violet": "u",
            "Rouge": "e",
            "Blanc": "w",
            "Jaune": "y"
        }
    },
    "meurtrissures": {
        "label": "Présence de meurtrissures",
        "options": {
            "Oui": "t",
            "Non": "f"
        }
    },
    "odeur": {
        "label": "Odeur",
        "options": {
            "Amande": "a",
            "Anis": "l",
            "Créosote": "c",
            "Poisson": "y",
            "Nauséabond": "f",
            "Moisi": "m",
            "Aucune": "n",
            "Âcre": "p",
            "Épicé": "s"
        }
    },
    "attache_des_lamelles": {
        "label": "Attache des lamelles",
        "options": {
            "Attaché": "a",
            "Descendant": "d",
            "Libre": "f",
            "Cranté": "n"
        }
    },
    "espacement_des_lamelles": {
        "label": "Espacement des lamelles",
        "options": {
            "Serré": "c",
            "Entassé": "w",
            "Éloigné": "d"
        }
    },
    "taille_des_lamelles": {
        "label": "Taille des lamelles",
        "options": {
            "Large": "b",
            "Étroite": "n"
        }
    },
    "couleur_des_lamelles": {
        "label": "Couleur des lamelles",
        "options": {
            "Noir": "k",
            "Brun": "n",
            "Crème": "b",
            "Chocolat": "h",
            "Gris": "g",
            "Vert": "r",
            "Orange": "o",
            "Rose": "p",
            "Violet": "u",
            "Rouge": "e",
            "Blanc": "w",
            "Jaune": "y"
        }
    },
    "forme_du_pied": {
        "label": "Forme du pied",
        "options": {
            "Élargissant": "e",
            "Effilé": "t"
        }
    },
    "racine_du_pied": {
        "label": "Racine du pied",
        "options": {
            "Bulbe": "b",
            "Massue": "c",
            "Coupe": "u",
            "Égal": "e",
            "Rhizomorphe": "z",
            "Enraciné": "r",
            "Absent": "?"
        }
    },
    "surface_du_pied_au_dessus_de_lanneau": {
        "label": "Surface du pied au-dessus de l'anneau",
        "options": {
            "Fibreuse": "f",
            "Écailleuse": "y",
            "Soyeuse": "k",
            "Lisse": "s"
        }
    },
    "surface_du_pied_en_dessous_de_lanneau": {
        "label": "Surface du pied en-dessous de l'anneau",
        "options": {
            "Fibreuse": "f",
            "Écailleuse": "y",
            "Soyeuse": "k",
            "Lisse": "s"
        }
    },
    "couleur_du_pied_au_dessus_de_lanneau": {
        "label": "Couleur du pied au-dessus de l'anneau",
        "options": {
            "Brun": "n",
            "Crème": "b",
            "Cannelle": "c",
            "Gris": "g",
            "Orange": "o",
            "Rose": "p",
            "Rouge": "e",
            "Blanc": "w",
            "Jaune": "y"
        }
    },
    "couleur_du_pied_en_dessous_de_lanneau": {
        "label": "Couleur du pied en-dessous de l'anneau",
        "options": {
            "Brun": "n",
            "Crème": "b",
            "Cannelle": "c",
            "Gris": "g",
            "Orange": "o",
            "Rose": "p",
            "Rouge": "e",
            "Blanc": "w",
            "Jaune": "y"
        }
    },
    "type_de_voile": {
        "label": "Type de voile",
        "options": {
            "Partiel": "p",
            "Universel": "u"
        }
    },
    "couleur_du_voile": {
        "label": "Couleur du voile",
        "options": {
            "Brun": "n",
            "Orange": "o",
            "Blanc": "w",
            "Jaune": "y"
        }
    },
    "nombre_danneaux": {
        "label": "Nombre d'anneaux",
        "options": {
            "Aucun": "n",
            "Un": "o",
            "Deux": "t"
        }
    },
    "type_danneau": {
        "label": "Type d'anneau",
        "options": {
            "Toile d'araignée": "c",
            "Évanescent": "e",
            "Flamboyant": "f",
            "Large": "l",
            "Aucun": "n",
            "Pendant": "p",
            "Gaine": "s",
            "Zone": "z"
        }
    },
    "couleur_de_lempreinte_des_spores": {
        "label": "Couleur de l'empreinte des spores",
        "options": {
            "Noir": "k",
            "Brun": "n",
            "Crème": "b",
            "Chocolat": "h",
            "Vert": "r",
            "Orange": "o",
            "Violet": "u",
            "Blanc": "w",
            "Jaune": "y"
        }
    },
    "population": {
        "label": "Population",
        "options": {
            "Abondante": "a",
            "En groupe": "c",
            "Nombreuse": "n",
            "Éparpillée": "s",
            "Plusieurs": "v",
            "Solitaire": "y"
        }
    },
    "habitat": {
        "label": "Habitat",
        "options": {
            "Herbes": "g",
            "Feuilles": "l",
            "Prairies": "m",
            "Sentiers": "p",
            "Urbain": "u",
            "Déchets": "w",
            "Forêts": "d"
        }
    }
}

# Générer des choix aléatoires si le bouton est cliqué
if st.button("Aléatoire"):
    for label, info in characteristics.items():
        random_choice = random.choice(list(info["options"].values()))
        st.session_state[label] = random_choice  # Mettre à jour st.session_state directement

# Obtenir les entrées de l'utilisateur pour chaque attribut via des cases à cocher en ligne
data = {}
for label, info in characteristics.items():
    data[label] = checkbox_single_row(info["label"], info["options"], selected_value=st.session_state.get(label))

# Vérification de sélection complète
if all(value is not None for value in data.values()):
    if st.button("Prédire la comestibilité du champignon"):
        response = requests.post("http://mushroom_api:8888/predict", json=data)
        if response.status_code == 200:
                result = response.json()["class"]
                if result == "edible":
                        st.write("Le champignon est comestible.")
                else:
                        st.write("Le champignon n'est pas comestible.")
            
        else:
            st.write("Une erreur est survenue lors de la prédiction.")
else:
    st.write("Veuillez sélectionner une option pour chaque caractéristique.")
