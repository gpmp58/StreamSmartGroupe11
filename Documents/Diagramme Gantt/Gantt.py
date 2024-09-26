import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

# ================================================
# | Données principales du diagramme de Gantt    |
# ================================================

# Tâches avec leurs dates de début, durée, et une couleur uniformisée pour l'ensemble des tâches
donnees_taches = {
    'Tâche': [
        'Tâche 1', 'Tâche 2', 'Tâche 3', 'Tâche 4', 'Tâche 5',
        'Conception Diagramme UML', 'Vacances', 'Rapport intermédiaire', 'Rendu final', 'Soutenance'
    ],
    'Date de début': [
        '2024-09-15', '2024-10-01', '2024-10-10', '2024-10-20', '2024-11-01',
        '2024-09-11', '2024-10-25',
        '2024-10-05', '2024-11-23', '2024-12-12'
    ],
    'Durée (jours)': [
        5, 7, 4, 3, 6,
        16, 10,  # La conception a une durée, les autres sont des jalons
        0, 0, 0
    ],
    'Couleur': ['#808080'] * 10  # Couleur uniforme pour toutes les tâches (gris)
}

# Données pour les partiels avec des dates fixes et aucune durée (jalons)
donnees_partiels = {
    'Tâche': ['Partiels'] * 7,
    'Date de début': ['2024-10-07', '2024-10-24', '2024-11-04', '2024-11-06', '2024-11-19', '2024-12-02', '2024-12-10'],
    'Durée (jours)': [0] * 7,
    'Couleur': ['#FF0000'] * 7  # Rouge pour les partiels
}

# Données pour les suivis avec des dates fixes et aucune durée (jalons)
donnees_suivis = {
    'Tâche': ['Suivis'] * 6,
    'Date de début': ['2024-09-06', '2024-09-13', '2024-09-27', '2024-10-11', '2024-10-21', '2024-11-15'],
    'Durée (jours)': [0] * 6,
    'Couleur': ['#66B2FF'] * 6  # Bleu pour les suivis
}

# Données pour les rendus hebdomadaires tous les jeudis
donnees_rendu_hebdo = {
    'Tâche': ['Rendu Hebdomadaire'] * 11,
    'Date de début': [
        '2024-09-12', '2024-09-19', '2024-09-26', '2024-10-03', '2024-10-10',
        '2024-10-17', '2024-10-24', '2024-11-07', '2024-11-14', '2024-11-21', '2024-11-28'
    ],
    'Durée (jours)': [0] * 11,
    'Couleur': ['#FFD700'] * 11  # Doré pour les rendus hebdomadaires
}

# ================================================
# | Fusion et conversion des données             |
# ================================================

# Convertir toutes les données en DataFrame
df_taches = pd.DataFrame(donnees_taches)
df_partiels = pd.DataFrame(donnees_partiels)
df_suivis = pd.DataFrame(donnees_suivis)
df_rendu_hebdo = pd.DataFrame(donnees_rendu_hebdo)

# Fusionner toutes les données dans un seul DataFrame
df_gantt = pd.concat([df_taches, df_partiels, df_suivis, df_rendu_hebdo], ignore_index=True)

# Conversion des dates de début au format datetime pour faciliter les calculs
df_gantt['Date de début'] = pd.to_datetime(df_gantt['Date de début'])

# Calcul des dates de fin en ajoutant la durée à la date de début
df_gantt['Date de fin'] = df_gantt['Date de début'] + pd.to_timedelta(df_gantt['Durée (jours)'], unit='d')

# ================================================
# | Création du diagramme de Gantt               |
# ================================================

# Option pour fermer la fenêtre précédente avant de tracer un nouveau graphique
plt.close('all')  # Fermer toutes les figures ouvertes

# Définir la taille de la figure (ajustable si besoin)
fig, ax = plt.subplots(figsize=(12, 8))

# Ajuster la hauteur des barres (barres plus fines pour un affichage compact)
largeur_barre = 0.5

# Ajouter les barres horizontales pour les tâches avec une durée > 0
for i, tache in df_gantt[df_gantt['Durée (jours)'] > 0].iterrows():
    if tache['Tâche'] == 'Vacances':
        # Utiliser des hachures pour la période des vacances
        ax.barh(tache['Tâche'], (tache['Date de fin'] - tache['Date de début']).days,
                left=mdates.date2num(tache['Date de début']), color=tache['Couleur'], edgecolor='black',
                hatch='//', height=largeur_barre)
    else:
        ax.barh(tache['Tâche'], (tache['Date de fin'] - tache['Date de début']).days,
                left=mdates.date2num(tache['Date de début']), color=tache['Couleur'], edgecolor='black', height=largeur_barre)

# Ajouter les jalons pour les partiels (diamants rouges)
ax.scatter(mdates.date2num(df_partiels['Date de début']), df_partiels['Tâche'], 
           color=df_partiels['Couleur'], s=100, marker='D', edgecolor='black')

# Ajouter les jalons pour les suivis (cercles bleus)
ax.scatter(mdates.date2num(df_suivis['Date de début']), df_suivis['Tâche'], 
           color=df_suivis['Couleur'], s=100, marker='o', edgecolor='black')

# Ajouter les jalons pour les rendus hebdomadaires (diamants dorés)
ax.scatter(mdates.date2num(df_rendu_hebdo['Date de début']), df_rendu_hebdo['Tâche'], 
           color=df_rendu_hebdo['Couleur'], s=100, marker='D', edgecolor='black')

# Ajouter les jalons pour le rendu final et la soutenance (carrés rouges pour plus de distinction)
jalons_importants = df_gantt[df_gantt['Tâche'].isin(['Rendu final', 'Soutenance'])]
ax.scatter(mdates.date2num(jalons_importants['Date de début']), jalons_importants['Tâche'], 
           color='#FF6347', s=100, marker='s', edgecolor='black')  # Carrés rouges pour ces jalons

# ================================================
# | Formatage de l'axe des dates                |
# ================================================

# Convertir l'axe des X en format de dates et définir le format souhaité (Jour et Mois)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %B'))  # Ex: 12 Septembre

# Rotation des étiquettes des dates pour améliorer la lisibilité
plt.xticks(rotation=45)

# Ajouter une grille hebdomadaire pour plus de clarté
ax.xaxis.set_major_locator(mdates.WeekdayLocator())
plt.grid(axis='x', linestyle='--', color='gray')

# ================================================
# | Configuration des titres et labels           |
# ================================================

# Titre du graphique
plt.title('Diagramme de Gantt du Projet')

# Label pour l'axe X (les dates)
plt.xlabel('Dates')

# Label pour l'axe Y (les tâches)
plt.ylabel('Tâches')

# ================================================
# |    Affichage du diagramme                    |
# ================================================

# Ajustement automatique de l'affichage pour éviter que les étiquettes ne se chevauchent
plt.tight_layout()

# Afficher le diagramme
plt.show()
