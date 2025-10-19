import os

import streamlit as st
import requests
from streamlit import set_page_config

# Configuration de la page
st.set_page_config(page_title="Démonstration API - Articles", layout="wide", initial_sidebar_state="collapsed")

# Titre de l'application
st.title("Liste des articles depuis l'API")
st.markdown("""
Cette application affiche la liste des articles récupérés depuis l'API REST.
""")

API_URL = os.environ.get('API_URL')

# Fonction pour récupérer les articles
def fetch_articles():
    try:
        response = requests.get(f"{API_URL}/articles")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des articles : {e}")
        return []

# Bouton pour rafraîchir la liste
if st.button("Rafraîchir la liste des articles"):
    st.rerun()

st.markdown("[Ajouter un article](/add)")

# Récupération des articles
articles = fetch_articles()

# Affichage des articles
if articles:
    st.subheader(f"Nombre d'articles : {len(articles)}")
    for article in articles:
        # Affiche chaque article sous forme de carte
        with st.container():
            st.markdown(f"""
            <div style="border:1px solid #e1e4e8; border-radius:5px; padding:10px; margin:10px 0;">
                <h3>{article.get('title')}</h3>
                <p><strong>Auteur:</strong> {article.get('author')}</p>
                <p><a href="/detail?id={article.get('id')}" target="_self">Voir le détail</a></p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Aucun article trouvé ou erreur de connexion à l'API.")

