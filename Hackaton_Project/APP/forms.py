from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Note, Etudiant, Matiere, TypeEvaluation


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['matiere', 'type_evaluation', 'note', 'date_evaluation', 'commentaire']
        widgets = {
            'date_evaluation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'note': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20', 'step': '0.5'}),
            'matiere': forms.Select(attrs={'class': 'form-control'}),
            'type_evaluation': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'matiere': 'Matière',
            'type_evaluation': 'Type d\'évaluation',
            'note': 'Note (sur 20)',
            'date_evaluation': 'Date d\'évaluation',
            'commentaire': 'Commentaire (optionnel)'
        }


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'date_naissance', 'numero_etudiant', 'classe', 'email', 'telephone', 'adresse']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_etudiant': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'numero_etudiant': 'Numéro étudiant',
            'classe': 'Classe',
            'email': 'Email',
            'telephone': 'Téléphone',
            'adresse': 'Adresse'
        }


class RechercheForm(forms.Form):
    recherche = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un étudiant...'
        })
    )
    classe = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Toutes les classes",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    matiere = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Toutes les matières",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Classe, Matiere
        self.fields['classe'].queryset = Classe.objects.all()
        self.fields['matiere'].queryset = Matiere.objects.all()


class BulkNoteForm(forms.Form):
    """Formulaire pour saisir plusieurs notes à la fois"""
    matiere = forms.ModelChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type_evaluation = forms.ModelChoiceField(
        queryset=TypeEvaluation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_evaluation = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    commentaire = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )


class FiltreNotesForm(forms.Form):
    """Formulaire de filtrage des notes"""
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    matiere = forms.ModelChoiceField(
        queryset=Matiere.objects.all(),
        required=False,
        empty_label="Toutes les matières",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    classe = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Toutes les classes",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    note_min = forms.FloatField(
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20', 'step': '0.5'})
    )
    note_max = forms.FloatField(
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20', 'step': '0.5'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Classe
        self.fields['classe'].queryset = Classe.objects.all()
