from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Team
from .forms import TeamForm


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = "teams/create_team.html"
    success_url = reverse_lazy('teams:list')

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(TeamCreateView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Team Add"
        context["title"] = "Team Add"
        context["button_text"] = "Create Team"
        context["card_title"] = "Create Teams"
        return context
    
    def form_valid(self, form):
        # set creator
        form.instance.created_by = self.request.user

        # set team lead if not provided
        if not form.cleaned_data['team_lead']:
            form.instance.team_lead = self.request.user

        messages.success(self.request, "Team created successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating team")
        return super().form_invalid(form)
        


class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 5


    def get_queryset(self):
        # user created teams
        user = self.request.user
        if user.is_superuser:
            user_teams = Team.objects.all()
        else:
            user_created_teams = Team.objects.filter(created_by=user)
            user_belonged_teams = Team.objects.filter(members=user)

            teams = user_created_teams | user_belonged_teams
            user_teams = teams.distinct()

        return user_teams


    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(TeamListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Team List"
        context["title"] = "Team List"
        return context



class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "teams/create_team.html"

    def get_object(self, queryset=None):
        # get team
        team = get_object_or_404(Team, pk=self.kwargs['pk'])

        # check permission on this team
        if team.created_by != self.request.user:
            raise Http404("Team not found.")
        return team

    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(TeamUpdateView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Team Update"
        context["title"] = "Team Update"
        context["button_text"] = "Update Team"
        context["card_title"] = "Update Teams"
        return context
    
    def form_valid(self, form):
        # show message
        messages.success(self.request, "Team updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # show message
        messages.error(self.request, "Please correct the errors and try again.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('teams:list')


class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'teams/confirm_delete.html'
    success_url = reverse_lazy('teams:list')

    def get_object(self, queryset=None):
        # get team
        team = get_object_or_404(Team, pk=self.kwargs['pk'])

        # check permission on this team
        if team.created_by != self.request.user:
            raise Http404("Team not found.")
        return team


    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(TeamDeleteView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Delete Team"
        return context
    
    def post(self, request, *args, **kwargs):
        # get team and check permissions
        team = self.get_object()

        messages.success(request, f"The team {team.name} is deleted successfully.")
        return super().post(request, *args, **kwargs)
    


