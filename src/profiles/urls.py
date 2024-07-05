from django.urls import path
from .views import (LoginPage, logout_view, EmployeeCreateView, PermissionsView,
                    EmployeesListView, EmployeeUpdateView,
                    EmployeeDeleteView, AdminPanel)

urlpatterns = [
    path('login', LoginPage.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
    path('create_employee', EmployeeCreateView.as_view(), name='employee_create'),
    path('permissions/<int:user_id>', PermissionsView.as_view(), name='permissions'),
    path('employees/', EmployeesListView.as_view(), name='employees_list'),
    path('employees/<int:user_id>', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:user_id>/delete', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('admin_panel', AdminPanel.as_view(), name='admin_panel')
]
