from django.contrib import admin
from .models import (
    Classe, Matiere, Professeur, Etudiant, TypeEvaluation, 
    Note, Trimestre, Bulletin, NoteTrimestre
)


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau', 'annee_scolaire', 'nombre_etudiants']
    list_filter = ['niveau', 'annee_scolaire']
    search_fields = ['nom', 'niveau']
    
    def nombre_etudiants(self, obj):
        return obj.etudiants.count()
    nombre_etudiants.short_description = 'Nombre d\'étudiants'


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'coefficient']
    search_fields = ['nom', 'code']


@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'get_matieres', 'get_classes']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    filter_horizontal = ['matieres', 'classes']
    
    def get_matieres(self, obj):
        return ', '.join([matiere.nom for matiere in obj.matieres.all()])
    get_matieres.short_description = 'Matières'
    
    def get_classes(self, obj):
        return ', '.join([classe.nom for classe in obj.classes.all()])
    get_classes.short_description = 'Classes'


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'numero_etudiant', 'classe', 'date_naissance']
    list_filter = ['classe', 'date_inscription']
    search_fields = ['nom', 'prenom', 'numero_etudiant', 'email']
    date_hierarchy = 'date_inscription'


@admin.register(TypeEvaluation)
class TypeEvaluationAdmin(admin.ModelAdmin):
    list_display = ['nom', 'coefficient']


class NoteAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'matiere', 'note', 'type_evaluation', 'date_evaluation', 'professeur']
    list_filter = ['matiere', 'type_evaluation', 'date_evaluation', 'professeur']
    search_fields = ['etudiant__nom', 'etudiant__prenom', 'matiere__nom']
    date_hierarchy = 'date_evaluation'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('etudiant', 'matiere', 'professeur', 'type_evaluation')

admin.site.register(Note, NoteAdmin)


@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    list_display = ['nom', 'date_debut', 'date_fin', 'annee_scolaire']
    list_filter = ['annee_scolaire']
    date_hierarchy = 'date_debut'


class NoteTrimestreInline(admin.TabularInline):
    model = NoteTrimestre
    extra = 0


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'trimestre', 'moyenne_generale', 'rang']
    list_filter = ['trimestre', 'etudiant__classe']
    search_fields = ['etudiant__nom', 'etudiant__prenom']
    inlines = [NoteTrimestreInline]


@admin.register(NoteTrimestre)
class NoteTrimestreAdmin(admin.ModelAdmin):
    list_display = ['bulletin', 'matiere', 'moyenne', 'appreciation']
    list_filter = ['matiere', 'bulletin__trimestre']
    search_fields = ['bulletin__etudiant__nom', 'bulletin__etudiant__prenom']


# Configuration du site d'administration
admin.site.site_header = "Administration - Gestion des Notes"
admin.site.site_title = "Gestion des Notes"
admin.site.index_title = "Bienvenue dans l'administration"
