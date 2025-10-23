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

# Récupérer le numéro de page depuis l'URL (si présent)
params = st.query_params
current_page = int(params.get("page", ["1"])[0])

API_URL = os.environ.get('API_URL')

# Fonction pour récupérer les articles
def fetch_articles(page=1):
    try:
        url = f"{API_URL}/v2/articles?page={page}" if page > 1 else f"{API_URL}/v2/articles"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des articles : {e}")
        return {"data": [], "links": {}}


# Bouton pour rafraîchir la liste
if st.button("Rafraîchir la liste des articles"):
    st.rerun()

st.markdown("[Ajouter un article](/add)")

# Récupérer les données
result = fetch_articles(current_page)
articles = result.get("data", [])
links = result.get("links", {})

# Affichage des articles
if articles:
    # st.subheader(f"Nombre d'articles : {len(articles.get('data', []))}")
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

# Afficher les liens de pagination
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if links.get("prev"):
        prev_url = links["prev"].split("?page=")[1] if "?page=" in links["prev"] else "1"
        st.markdown(f'<a href="/?page={prev_url}" target="_self">← Page précédente</a>', unsafe_allow_html=True)
    else:
        st.markdown(" ")

with col2:
    st.markdown(f"Page {current_page}")

with col3:
    if links.get("next"):
        next_url = links["next"].split("?page=")[1] if "?page=" in links["next"] else "1"
        st.markdown(f'<a href="/?page={next_url}" target="_self">Page suivante →</a>', unsafe_allow_html=True)
    else:
        st.markdown(" ")