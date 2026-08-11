from django import forms
from .models import Team
from django.contrib.auth.models import User

class TeamForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your Team here ..."}
        ),
        label=False,
        required=True
    )

    team_lead = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        label=False,
        required=True

    )

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(
             attrs={'class': 'form-control'}
        ),
         label=False,
        required=True
        
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Enter the name of your Team here ..."}
        ),
        required=True,
        label=False
    )

    class Meta:
        model = Team
        fields = ['name', 'description', 'team_lead', 'members']