from django import forms
from tempus_dominus.widgets import DatePicker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # removing helper text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    

class ProfileUpdateForm(forms.ModelForm):
    education_level = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your educational level here ..."}
        ),
        required=True
    )

    skills = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your skills here ..."}
        ),
        required=True
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your bior here ..."}
        ),
        required=True
    )

    date_of_birth = forms.DateTimeField(
        label=False,
        required=True,
        widget=DatePicker(
            attrs = {
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'job_title',
            'education_level',
            'skills',
            'bio',
            'location',
            'phone',
            'date_of_birth'
        ]