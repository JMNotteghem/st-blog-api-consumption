import os
from datetime import datetime

import streamlit as st
import requests

API_URL = os.environ.get('API_URL')


# Récupère l'ID de l'article depuis l'URL
params = st.query_params
article_id = params.get("id", [None])

if not article_id:
    st.error("ID d'article manquant")
else:
    try:
        response = requests.get(f"{API_URL}/v1/articles/{article_id}")
        response.raise_for_status()
        article = response.json()
        st.title(article.get("title"))
        st.markdown(f"**Auteur** : {article.get('author')}")
        st.markdown(f"**Slug** : {article.get('slug')}")
        st.markdown("---")
        st.markdown(article.get("content"))

        comments_response = requests.get(f"{API_URL}/v1/articles/{article_id}/comments")
        comments_response.raise_for_status()
        comments = comments_response.json()

        st.subheader("Commentaires")
        if comments:
            for comment in comments:
                with st.container():
                    st.markdown(f"""
                            <div style="border-left: 3px solid #4CAF50; padding: 10px; margin: 10px 0; background-color: #f9f9f9; border-radius: 5px;">
                                <p><strong>{comment.get('author', 'Auteur inconnu')}</strong> • {datetime.strptime(comment['created_at'], "%Y-%m-%dT%H:%M:%S.%f").strftime('%d/%m/%Y à %H:%M')}</p>
                                <p>{comment.get('content')}</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("Aucun commentaire pour cet article.")

        with st.form("form_commentaire"):
            author = st.text_input("Votre nom")
            content = st.text_area("Votre commentaire")
            submitted = st.form_submit_button("Poster le commentaire")

            if submitted:
                if not author or not content:
                    st.error("Veuillez remplir tous les champs.")
                else:
                    try:
                        new_comment = {
                            "author": author,
                            "content": content
                        }
                        post_response = requests.post(f"{API_URL}/v1/articles/{article_id}/comments", json=new_comment)
                        post_response.raise_for_status()
                        st.success("Commentaire posté avec succès !")
                        # Rafraîchir la page pour afficher le nouveau commentaire
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur lors de l'envoi du commentaire : {e}")

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
