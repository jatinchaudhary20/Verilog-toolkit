from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.views.generic import View, ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from projects.models import Project
from tasks.models import Task
from .models import Profile
# from notifications.models import Notifiction 
from teams.models import Team
from .forms import RegisterForm, ProfileUpdateForm
from comments.models import Comment


# user registration
@login_not_required
def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration is successful")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form':form})


class PasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
               

        if user.is_superuser:
            latest_projects = Project.objects.all()
            latest_tasks = Task.objects.all()
            latest_members = Profile.objects.all()
            team_count = Team.objects.all().count()
        else:
            latest_projects = Project.objects.for_user(user) 
            latest_tasks = Task.objects.for_user(user) 
            latest_members = Profile.objects.filter(
                user__teams__in=user.teams.all()
            ).distinct()
            team_count = user.teams.all().count()

        
        context = {}
        latest_notifications = user.notifications.unread(user)
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["latest_projects"] = latest_projects[:5]
        context["latest_project_count"] = latest_projects.count()
        context["projects_near_due_date"] = latest_projects.due_in_two_days_or_less()[:5]
        context["latest_task_count"] = latest_tasks.count()
        context["latest_members"] = latest_members[:8]
        context["latest_member_count"] = latest_members.count()
        context["team_count"] = team_count
        context["header_text"] = "Dashboard"
        context["title"] = "Dashboard"
        return render(request, "accounts/dashboard.html", context)


class MembersListView(ListView):
    model = Profile
    context_object_name = "members"
    template_name = "accounts/profile_list.html"
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            latest_members = Profile.objects.all()
            return latest_members
        else:
            latest_members = Profile.objects.filter(
                user__teams__in=user.teams.all()
            ).distinct()
            return latest_members


    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(MembersListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Members"
        context["title"] = "All Members"
        return context
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        profile = self.get_object()
        # latest notifications
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)    
        user_projects = Project.objects.for_user(profile.user)  

        # setting pagination for user projects
        paginator = Paginator(user_projects, 3)
        page_number = self.request.GET.get('page')
        page_obj  = paginator.get_page(page_number)

        # setting up  users comment
        user_comments = profile.user.comments.all()
        project_content_type = ContentType.objects.get_for_model(Project)
        project_comments = Comment.objects.filter(
            content_type= project_content_type,
            object_id__in=[str(id) for id in user_projects.values_list('id', flat=True)]            
        )

        # combining comments
        all_user_comments = (user_comments | project_comments).distinct()

         # setting pagination for user comments
        comment_paginator = Paginator(all_user_comments, 5)
        comment_page_number = self.request.GET.get('comment_page')
        comments  = comment_paginator.get_page(comment_page_number)


        #user tasks
        user_tasks = Task.objects.for_user(profile.user)
        task_paginator = Paginator(user_tasks, 5)
        task_page_number = self.request.GET.get('task_page')
        tasks  = task_paginator.get_page(task_page_number)



         
        context["comments"] = comments
        context["all_user_comments_count"] = all_user_comments.count()
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Profile"
        context["title"] = f"{profile.full_name}'s Profile"

        # user tasks and project count 
        context["user_tasks_count"] = user_tasks.count()
        context["tasks"] = tasks
        
        context["user_projects_count"] = user_projects.count()
        context["page_obj"] = page_obj
        return context
   

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_success_url(self):
        return reverse('accounts:profile-detail', kwargs={'pk': self.request.user.profile.pk})
    
    def get_context_data(self, **kwargs):
        # latest notifications
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        latest_notifications = self.request.user.notifications.unread(self.request.user)            
        
        context["latest_notifications"] = latest_notifications[:3]
        context["notification_count"] = latest_notifications.count()
        context["header_text"] = "Update Profile"
        context["title"] = "Update Profile"
        return context