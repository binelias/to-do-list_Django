from sre_constants import SUCCESS
from django.shortcuts import render, redirect
# Return template and query set of data
from django.views.generic.list import ListView
# Return template detail view
from django.views.generic.detail import DetailView
# Return template for create view
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# redirect user to certain page/view
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
# Account access to page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Inherit TaskList from ListView


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # redirect to main page after login successfully

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    # automatic login after reg then redirect to main page

    def form_valid(self, form):
        user = form.save()
        # login user after reg
        if user is not None:
            login(self.request, user)
        # redirect to main page
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    # a query set default by django
    model = Task
    # Change name
    context_object_name = 'tasks'
    # ensure the user can only see their own data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        # Search function
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)
        # value stays in search function
        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    # a query set default by django
    model = Task
    # Change name
    context_object_name = 'task'
    # change template name
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    # a query set default by django
    model = Task
    # Default model forms
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    # set user default in create page
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    # a query set default by django
    model = Task
    # Default model forms
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    # a query set default by django
    model = Task
    # Change name
    context_object_name = 'task'
    # After delete an item redirect to main page
    success_url = reverse_lazy('tasks')
