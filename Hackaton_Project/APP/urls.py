from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.accueil, name='accueil'),
    
    # Gestion des classes
    path('classes/', views.liste_classes, name='liste_classes'),
    path('classes/<int:classe_id>/', views.detail_classe, name='detail_classe'),
    
    # Gestion des étudiants
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/<int:etudiant_id>/', views.detail_etudiant, name='detail_etudiant'),
    
    # Gestion des notes
    path('etudiants/<int:etudiant_id>/ajouter-note/', views.ajouter_note, name='ajouter_note'),
    path('matieres/<int:matiere_id>/notes/', views.notes_par_matiere, name='notes_matiere'),
    
    # Bulletins
    path('etudiants/<int:etudiant_id>/bulletin/', views.bulletin_etudiant, name='bulletin_etudiant'),
    path('etudiants/<int:etudiant_id>/bulletin/<int:trimestre_id>/', views.bulletin_etudiant, name='bulletin_etudiant_trimestre'),
    
    # Statistiques
    path('statistiques/', views.statistiques, name='statistiques'),
    
    # API
    path('api/notes/<int:etudiant_id>/', views.api_notes_etudiant, name='api_notes_etudiant'),
]
