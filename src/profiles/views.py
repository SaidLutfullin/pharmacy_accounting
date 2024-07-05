from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, FormView, UpdateView, DeleteView
from .forms import EmployeeCreationForm, EmployeeChangeForm, LoginUserForm, PermissionsForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Employee
from .services import PermissionsService
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class LoginPage(LoginView):
    form_class = LoginUserForm
    template_name = 'profiles/login_page.html'
    success_url = reverse_lazy('main')

    def get_success_url(self):
        return self.success_url

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


class PermissionsView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'profiles/permissions.html'
    success_url = reverse_lazy('employees_list')
    form_class = PermissionsForm
    permissions_service = None
    permission_required = 'profiles.change_employee'

    def get_initial(self):
        self.permissions_service = PermissionsService(self.kwargs['user_id'])
        initial = self.permissions_service.get_permissions_form_initial()
        return initial

    def form_valid(self, form):
        self.permissions_service = PermissionsService(self.kwargs['user_id'])
        self.permissions_service.set_permissions(form.cleaned_data)
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.permissions_service.get_user_full_name()
        return context


# employee crud PermissionRequiredMixin, 
class EmployeesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'profiles/employees_list.html'
    model = Employee
    context_object_name = 'employees'
    permission_required = 'profiles.add_employee'


class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'profiles/employee_create.html'
    form_class = EmployeeCreationForm
    permission_required = 'profiles.add_employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_user'] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse('permissions', kwargs={'user_id': self.object.pk})
        return HttpResponseRedirect(self.get_success_url())


class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    success_url = reverse_lazy('employees_list')
    template_name = 'profiles/employee_create.html'
    pk_url_kwarg = "user_id"
    permission_required = 'profiles.change_employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_user'] = False
        return context


class EmployeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employees_list')
    template_name = "common/confirm_deleting.html"
    pk_url_kwarg = "user_id"
    permission_required = 'profiles.change_employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'{self.object.first_name} {self.object.last_name} {self.object.middle_name} {self.object.speciality}'
        return context


class AdminPanel(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'profiles/admin_panel.html'

    def test_func(self):
        return self.request.user.has_perm('profiles.add_employee') or \
               self.request.user.has_perm('profiles.change_employee') or \
               self.request.user.has_perm('drugs.view_department') or \
               self.request.user.has_perm('drugs.view_direction')