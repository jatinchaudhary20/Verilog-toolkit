from django import forms
from django.contrib.auth.models import User
from tempus_dominus.widgets import DatePicker
from .models import Task
from projects.utils import STATUS_CHOICES, PRIORITY_CHOICES


class TaskUpdateForm(forms.ModelForm):
    # hidden input
    task_id = forms.CharField(widget=forms.HiddenInput(), required=True)

    description = forms.CharField(
        widget= forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Describe your task here ...'}
        ),
        required=False
    )

    start_date = forms.DateTimeField(
        widget=DatePicker(
            attrs= {
                'append': 'fa fa-calendar',
                'icon_toggle': True
            }
        )
    )

    due_date = forms.DateTimeField(
        widget=DatePicker(
            attrs= {
                'append': 'fa fa-calendar',
                'icon_toggle': True
            }
        )
    )

    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        required=True
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'start_date', 'due_date']


class TaskUserAssignmentForm(forms.ModelForm):
    task_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )

    user_assigned_to = forms.ModelChoiceField(
        label=False,
        required=True,
        queryset= User.objects.none(),
        empty_label= 'Select User',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
    )
    class Meta:
        model = Task
        fields = ['task_id', 'user_assigned_to']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        task_id = self.initial.get("task_id") or self.data.get("task_id")
        print(task_id)
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
                self.fields['user_assigned_to'].queryset = task.project.team.members.all()
            except Task.DoesNotExist:
                self.fields['user_assigned_to'].queryset = User.objects.none()

                