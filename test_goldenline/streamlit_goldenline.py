import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import chardet
st.set_option('deprecation.showPyplotGlobalUse', False)
# détecte l'encodage du fichier
with open('\\database\\goldenline_client.csv', 'rb') as f:
    result1 = chardet.detect(f.read())
    

with open('\\database\\goldenline_collecte.csv', 'rb') as f:
    result2 = chardet.detect(f.read())


df = pd.read_csv('database\\goldenline_client.csv',encoding=result1['encoding'],sep =';|,')
df_collecte = pd.read_csv('database\\goldenline_collecte.csv',encoding = result2 ['encoding'],sep=';|,')

df_final=df
df_final['jacket'] = df_collecte['jacket']
df_final['sweater'] = df_collecte['sweater']
df_final['pant'] = df_collecte['pant']
df_final['t_shirt'] = df_collecte['t_shirt']
df_final['underwear'] = df_collecte['underwear']

moyenne_sp_price = df_final.groupby("social_categorie")['total_price'].mean().reset_index()
depense_categorie = df_final.groupby(["social_categorie"])[["jacket", "sweater", "pant", "t_shirt", "underwear"]].sum()

# Afficher le graphique de distribution de la catégorie sociale
st.write('**Distribution de la catégorie sociale**')
sns.countplot(df_final['social_categorie'])
plt.xticks(rotation=75)
plt.xlabel('')
plt.ylabel('nombre de personne')
plt.title('')
st.pyplot()

    # Afficher le graphique de la dépense moyenne du panier par catégorie sociale
st.write('**Dépense moyenne du panier par catégorie sociale**')
sns.barplot(x='social_categorie', y='total_price', data=moyenne_sp_price)
plt.xticks(rotation=75)
plt.xlabel('')
plt.ylabel('dépense moyenne en euros')
plt.title('')
st.pyplot()

    # Afficher le graphique de la somme de la dépense du panier par catégorie sociale
st.write('**Dépenses par catégorie et par catégorie socio-professionnelle**')
        # tracer un graphique à barres empilées pour chaque catégorie socio-professionnelle
ax = depense_categorie.plot(kind="bar", stacked=True, figsize=(10, 8))
        # ajouter une légende, des titres et des étiquettes aux axes
ax.set_xlabel("Catégorie socio-professionnelle")
ax.set_ylabel("Dépenses en euros")
ax.legend(title="Catégorie", loc="upper right")
st.pyplot()

    
        #export de donnée 
    
n_rows_to_export = st.number_input("Nombre de lignes à exporter", min_value=1, max_value=len(df_collecte))
export_button = st.download_button(
label="Exporter les données",
data=df_collecte.head(n_rows_to_export).to_csv(index=False),
file_name='collecte_export.csv')