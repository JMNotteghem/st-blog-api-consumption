import os

import streamlit as st
import requests

API_URL = os.environ.get('API_URL')


# Récupère l'ID de l'article depuis l'URL
params = st.query_params
article_id = params.get("id", [None])[0]

if not article_id:
    st.error("ID d'article manquant")
else:
    try:
        response = requests.get(f"{API_URL}/articles/{article_id}")
        response.raise_for_status()
        article = response.json()
        st.title(article.get("title"))
        st.markdown(f"**Auteur** : {article.get('author')}")
        st.markdown(f"**Slug** : {article.get('slug')}")
        st.markdown("---")
        st.markdown(article.get("content"))
        # Bouton avec un target="_self"
        st.markdown(f"""
        <div class="stButton">
            <button kind="secondary">
            <a href="/" style="color:black;text-decoration:none" target="_self">Retour à l'accueil</a>
        </button></div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur : {e}")

# <div class="stButton st-emotion-cache-8atqhb e1mlolmg0" data-testid="stButton"><button kind="secondary" data-testid="stBaseButton-secondary" aria-label="" class="st-emotion-cache-5qfegl e8vg11g2"><div data-testid="stMarkdownContainer" class="st-emotion-cache-12j140x et2rgd20"><p>Rafraîchir la liste des articles</p></div></button></div>
