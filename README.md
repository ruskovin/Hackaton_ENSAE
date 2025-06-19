# Hackaton_ENSAE
Projet pour le  hackaton organisé par le club informatique de L"ENSAE de Dakar

Thème : Plateforme de suivi de la progression académique des classes

# Description de la structure du projet Django

- **README.md**  
  Fichier de documentation du projet. Sert à expliquer le but, l’installation et l’utilisation du projet.

- **ENV_Hackaton/**  
  Environnement virtuel Python contenant les dépendances installées (Django, etc.).  
  - `pyvenv.cfg` : Configuration de l’environnement virtuel.
  - `Include/`, `Lib/`, `Scripts/` : Dossiers internes de l’environnement virtuel (ne pas modifier).
  - `Lib/site-packages/` : Contient les paquets Python installés (Django, pip, etc.).

- **Hackaton_Project/**  
  Dossier principal du projet Django.
  - `db.sqlite3` : Base de données SQLite utilisée par défaut par Django.
  - `manage.py` : Script de gestion du projet (lancer le serveur, migrations, etc.).

  - **APP/**  
    Application Django personnalisée.
    - `__init__.py` : Indique que ce dossier est un module Python.
    - `admin.py` : Configuration de l’interface d’administration Django pour l’application.
    - `apps.py` : Configuration de l’application (nom, etc.).
    - `models.py` : Définition des modèles de données (tables de la base).
    - `tests.py` : Tests unitaires de l’application.
    - `views.py` : Logique des vues (fonctions ou classes qui traitent les requêtes).
    - `migrations/` : Dossier contenant les fichiers de migration de la base de données.
      - `__init__.py` : Indique que c’est un module Python.

  - **Hackaton_Project/**  
    Dossier de configuration du projet Django (même nom que le projet).
    - `__init__.py` : Indique que ce dossier est un module Python.
    - `asgi.py` : Point d’entrée pour les serveurs ASGI (asynchrone).
    - `settings.py` : Fichier de configuration principal du projet (base de données, apps, etc.).
    - `urls.py` : Définition des routes (URL) du projet.
    - `wsgi.py` : Point d’entrée pour les serveurs WSGI (synchrones).
    - `__pycache__/` : Dossier contenant les fichiers compilés Python (automatique).

N’hésite pas si tu veux une description détaillée d’un fichier spécifique ou d’un dossier !
