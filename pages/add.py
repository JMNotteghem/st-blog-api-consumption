import os

import streamlit as st
import requests
from slugify import slugify

API_URL = os.environ.get('API_URL')

st.title("Ajouter un article")

with st.form("form_ajout_article"):
    title = st.text_input("Titre")
    slug = slugify(title) if title else ""
    author = st.text_input("Auteur")
    content = st.text_area("Contenu")
    submitted = st.form_submit_button("Créer", icon="✅")

    if submitted:
        new_article = {
            "title": title,
            "slug": slug,
            "author": author,
            "content": content
        }
        try:
            response = requests.post(f"{API_URL}/v1/articles", json=new_article)
            response.raise_for_status()
            st.success("Article créé avec succès !")
            st.link_button("Retour à la liste", "/", icon="⬅️")
        except Exception as e:
            st.error(f"Erreur lors de la création : {e}")

