from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import (
    Classe, Matiere, Professeur, Etudiant, TypeEvaluation, 
    Note, Trimestre, Bulletin, NoteTrimestre
)
from .forms import NoteForm, EtudiantForm, RechercheForm
import json


def accueil(request):
    """Vue d'accueil avec statistiques générales"""
    context = {
        'total_etudiants': Etudiant.objects.count(),
        'total_classes': Classe.objects.count(),
        'total_matieres': Matiere.objects.count(),
        'total_notes': Note.objects.count(),
        'classes': Classe.objects.annotate(
            nb_etudiants=Count('etudiants')
        ).order_by('nom')
    }
    return render(request, 'APP/accueil.html', context)


def liste_classes(request):
    """Liste toutes les classes avec leurs statistiques"""
    classes = Classe.objects.annotate(
        nb_etudiants=Count('etudiants'),
        moyenne_classe=Avg('etudiants__notes__note')
    ).order_by('nom')
    
    return render(request, 'APP/liste_classes.html', {'classes': classes})


def detail_classe(request, classe_id):
    """Détail d'une classe avec la liste des étudiants"""
    classe = get_object_or_404(Classe, id=classe_id)
    etudiants = classe.etudiants.annotate(
        moyenne=Avg('notes__note'),
        nb_notes=Count('notes')
    ).order_by('nom', 'prenom')
    
    context = {
        'classe': classe,
        'etudiants': etudiants,
        'matieres': Matiere.objects.all()
    }
    return render(request, 'APP/detail_classe.html', context)


def liste_etudiants(request):
    """Liste tous les étudiants avec recherche et pagination"""
    etudiants_list = Etudiant.objects.select_related('classe').annotate(
        moyenne=Avg('notes__note'),
        nb_notes=Count('notes')
    ).order_by('nom', 'prenom')
    
    # Recherche
    search_query = request.GET.get('search')
    if search_query:
        etudiants_list = etudiants_list.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(numero_etudiant__icontains=search_query)
        )
    
    # Filtre par classe
    classe_filter = request.GET.get('classe')
    if classe_filter:
        etudiants_list = etudiants_list.filter(classe_id=classe_filter)
    
    # Pagination
    paginator = Paginator(etudiants_list, 20)
    page_number = request.GET.get('page')
    etudiants = paginator.get_page(page_number)
    
    context = {
        'etudiants': etudiants,
        'classes': Classe.objects.all(),
        'search_query': search_query,
        'classe_filter': classe_filter
    }
    return render(request, 'APP/liste_etudiants.html', context)


def detail_etudiant(request, etudiant_id):
    """Détail d'un étudiant avec ses notes"""
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    notes = etudiant.notes.select_related(
        'matiere', 'professeur', 'type_evaluation'
    ).order_by('-date_evaluation')
    
    # Moyennes par matière
    moyennes_matieres = {}
    for matiere in Matiere.objects.all():
        notes_matiere = notes.filter(matiere=matiere)
        if notes_matiere.exists():
            moyenne = notes_matiere.aggregate(Avg('note'))['note__avg']
            moyennes_matieres[matiere.nom] = round(moyenne, 2) if moyenne else None
    
    context = {
        'etudiant': etudiant,
        'notes': notes,
        'moyennes_matieres': moyennes_matieres,
        'moyenne_generale': notes.aggregate(Avg('note'))['note__avg']
    }
    return render(request, 'APP/detail_etudiant.html', context)


@login_required
def ajouter_note(request, etudiant_id):
    """Ajouter une note à un étudiant"""
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.etudiant = etudiant
            # Récupérer le professeur connecté
            try:
                note.professeur = request.user.professeur
            except:
                messages.error(request, "Vous devez être un professeur pour ajouter des notes.")
                return redirect('detail_etudiant', etudiant_id=etudiant.id)
            
            note.save()
            messages.success(request, f"Note ajoutée avec succès pour {etudiant.nom_complet}")
            return redirect('detail_etudiant', etudiant_id=etudiant.id)
    else:
        form = NoteForm()
    
    context = {
        'form': form,
        'etudiant': etudiant
    }
    return render(request, 'APP/ajouter_note.html', context)


def notes_par_matiere(request, matiere_id):
    """Affiche toutes les notes d'une matière"""
    matiere = get_object_or_404(Matiere, id=matiere_id)
    notes = Note.objects.filter(matiere=matiere).select_related(
        'etudiant', 'professeur', 'type_evaluation'
    ).order_by('-date_evaluation')
    
    # Filtre par classe
    classe_filter = request.GET.get('classe')
    if classe_filter:
        notes = notes.filter(etudiant__classe_id=classe_filter)
    
    context = {
        'matiere': matiere,
        'notes': notes,
        'classes': Classe.objects.all(),
        'classe_filter': classe_filter
    }
    return render(request, 'APP/notes_matiere.html', context)


def statistiques(request):
    """Page de statistiques générales"""
    stats = {
        'moyennes_par_classe': {},
        'moyennes_par_matiere': {},
        'repartition_notes': {}
    }
    
    # Moyennes par classe
    for classe in Classe.objects.all():
        moyenne = Note.objects.filter(etudiant__classe=classe).aggregate(
            Avg('note')
        )['note__avg']
        stats['moyennes_par_classe'][classe.nom] = round(moyenne, 2) if moyenne else 0
    
    # Moyennes par matière
    for matiere in Matiere.objects.all():
        moyenne = Note.objects.filter(matiere=matiere).aggregate(
            Avg('note')
        )['note__avg']
        stats['moyennes_par_matiere'][matiere.nom] = round(moyenne, 2) if moyenne else 0
    
    # Répartition des notes
    notes_ranges = [
        (0, 5, "0-5"),
        (5, 10, "5-10"),
        (10, 15, "10-15"),
        (15, 20, "15-20")
    ]
    
    for min_note, max_note, label in notes_ranges:
        count = Note.objects.filter(
            note__gte=min_note, 
            note__lt=max_note if max_note < 20 else 21
        ).count()
        stats['repartition_notes'][label] = count
    
    context = {
        'stats': stats,
        'stats_json': json.dumps(stats)
    }
    return render(request, 'APP/statistiques.html', context)


def bulletin_etudiant(request, etudiant_id, trimestre_id=None):
    """Génère le bulletin d'un étudiant pour un trimestre"""
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    
    if trimestre_id:
        trimestre = get_object_or_404(Trimestre, id=trimestre_id)
    else:
        # Prendre le trimestre actuel ou le plus récent
        trimestre = Trimestre.objects.order_by('-date_debut').first()
        if not trimestre:
            messages.error(request, "Aucun trimestre défini.")
            return redirect('detail_etudiant', etudiant_id=etudiant.id)
    
    # Obtenir ou créer le bulletin
    bulletin, created = Bulletin.objects.get_or_create(
        etudiant=etudiant,
        trimestre=trimestre
    )
    
    # Calculer les moyennes par matière
    notes_trimestre = []
    total_points = 0
    total_coefficients = 0
    
    for matiere in Matiere.objects.all():
        notes_matiere = Note.objects.filter(
            etudiant=etudiant,
            matiere=matiere,
            date_evaluation__range=[trimestre.date_debut, trimestre.date_fin]
        )
        
        if notes_matiere.exists():
            moyenne = notes_matiere.aggregate(Avg('note'))['note__avg']
            moyenne = round(moyenne, 2) if moyenne else None
            
            # Créer ou mettre à jour NoteTrimestre
            note_trimestre, _ = NoteTrimestre.objects.get_or_create(
                bulletin=bulletin,
                matiere=matiere,
                defaults={'moyenne': moyenne}
            )
            if note_trimestre.moyenne != moyenne:
                note_trimestre.moyenne = moyenne
                note_trimestre.save()
            
            notes_trimestre.append({
                'matiere': matiere,
                'moyenne': moyenne,
                'notes': notes_matiere
            })
            
            if moyenne:
                total_points += moyenne * matiere.coefficient
                total_coefficients += matiere.coefficient
    
    # Calculer la moyenne générale
    if total_coefficients > 0:
        moyenne_generale = round(total_points / total_coefficients, 2)
        bulletin.moyenne_generale = moyenne_generale
        bulletin.save()
    
    context = {
        'etudiant': etudiant,
        'bulletin': bulletin,
        'trimestre': trimestre,
        'notes_trimestre': notes_trimestre,
        'trimestres': Trimestre.objects.all()
    }
    return render(request, 'APP/bulletin.html', context)


# API Views pour AJAX
def api_notes_etudiant(request, etudiant_id):
    """API pour récupérer les notes d'un étudiant"""
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    notes = Note.objects.filter(etudiant=etudiant).values(
        'matiere__nom', 'note', 'date_evaluation', 'type_evaluation__nom'
    ).order_by('-date_evaluation')
    
    return JsonResponse(list(notes), safe=False)
