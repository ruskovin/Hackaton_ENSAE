from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Classe(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    niveau = models.CharField(max_length=20)
    annee_scolaire = models.CharField(max_length=10, default="2024-2025")
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} - {self.niveau}"


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    coefficient = models.FloatField(default=1.0)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15, blank=True)
    matieres = models.ManyToManyField(Matiere, related_name='professeurs')
    classes = models.ManyToManyField(Classe, related_name='professeurs')
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    numero_etudiant = models.CharField(max_length=20, unique=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='etudiants')
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    adresse = models.TextField(blank=True)
    date_inscription = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.numero_etudiant})"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class TypeEvaluation(models.Model):
    nom = models.CharField(max_length=50)  # Contrôle, Devoir, Examen, etc.
    coefficient = models.FloatField(default=1.0)
    
    def __str__(self):
        return self.nom


class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    type_evaluation = models.ForeignKey(TypeEvaluation, on_delete=models.CASCADE)
    note = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Note sur 20"
    )
    date_evaluation = models.DateField()
    commentaire = models.TextField(blank=True)
    date_saisie = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_evaluation']
        unique_together = ['etudiant', 'matiere', 'type_evaluation', 'date_evaluation']
    
    def __str__(self):
        return f"{self.etudiant.nom_complet} - {self.matiere.nom} - {self.note}/20"


class Trimestre(models.Model):
    nom = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField()
    annee_scolaire = models.CharField(max_length=10)
    
    class Meta:
        ordering = ['date_debut']
    
    def __str__(self):
        return f"{self.nom} {self.annee_scolaire}"


class Bulletin(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='bulletins')
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    moyenne_generale = models.FloatField(null=True, blank=True)
    rang = models.IntegerField(null=True, blank=True)
    appreciation_generale = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['etudiant', 'trimestre']
        ordering = ['-trimestre__date_debut']
    
    def __str__(self):
        return f"Bulletin {self.etudiant.nom_complet} - {self.trimestre}"


class NoteTrimestre(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE, related_name='notes_trimestre')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    moyenne = models.FloatField(null=True, blank=True)
    appreciation = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['bulletin', 'matiere']
    
    def __str__(self):
        return f"{self.bulletin.etudiant.nom_complet} - {self.matiere.nom} - {self.moyenne}/20"
