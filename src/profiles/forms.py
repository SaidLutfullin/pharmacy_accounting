from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee
from loguru import logger
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Пароль'}))


class EmployeeCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm):
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'middle_name', 'speciality', 'department')

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "middle_name": forms.TextInput(attrs={'class': 'form-control'}),
            "speciality": forms.TextInput(attrs={'class': 'form-control'}),
            "department": forms.CheckboxSelectMultiple(),
        }
        labels = {'department': 'Отделения'}


class EmployeeChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'middle_name', 'speciality', 'department')
        labels = {'department': 'Отделения'}

        widgets = {
                "username": forms.TextInput(attrs={'class': 'form-control'}),
                "first_name": forms.TextInput(attrs={'class': 'form-control'}),
                "last_name": forms.TextInput(attrs={'class': 'form-control'}),
                "middle_name": forms.TextInput(attrs={'class': 'form-control'}),
                "speciality": forms.TextInput(attrs={'class': 'form-control'}),
                "department": forms.CheckboxSelectMultiple(),
            }


class PermissionsForm(forms.Form):
    employee_add_permission = forms.BooleanField(label='Добавлять сотрудников', required=False,
                                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    employee_edit_permission = forms.BooleanField(label='Редактировать сотрудников', required=False,
                                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    movement_delete_permission = forms.BooleanField(label='Удалять расходы', required=False,
                                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    write_off_delete_permission = forms.BooleanField(label='Удалять списание', required=False,
                                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))

    drugs_permission = forms.BooleanField(label='Управление лекарствами и единицами измерения', required=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    firms_permission = forms.BooleanField(label='Управление фирмами', required=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    departments_permission = forms.BooleanField(label='Отделения', required=False,
                                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    shipments_permission = forms.BooleanField(label='Поставки и распределения', required=False,
                                              widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    movements_permission = forms.BooleanField(label='Расходы', required=False,
                                              widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
    directions_permission = forms.BooleanField(label='Направления', required=False,
                                               widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))