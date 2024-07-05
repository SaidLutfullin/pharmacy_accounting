from django import forms
from . import models
from django.core.exceptions import ValidationError
from loguru import logger
from django.utils import timezone


class ShipmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        firms = models.Firm.objects.all()
        self.fields['provider'].queryset = firms.filter(firm_type='provider')
        self.fields['producer'].queryset = firms.filter(firm_type='producer')

    class Meta:
        model = models.Shipment

        fields = ('drug', 'provider', 'producer', 'document','date_of_comming', 'use_by_date','serial_number','initial_amount','prise_for_unit')
        labels = {'drug': 'Лекарство',
                  'provider': 'Поставщик',
                  'producer': 'Производитель:',
                  'document': 'Приходной документ',
                  'date_of_comming': 'Дата прихода',
                  'use_by_date': 'Срок годности',
                  'serial_number': 'Серийный номер',
                  'initial_amount': 'Количество',
                  'prise_for_unit': 'Цена за единицу',
                  }

        widgets = {
            "drug": forms.Select(attrs={'class': 'form-select'}),
            "provider": forms.Select(attrs={'class': 'form-select'}),
            "producer": forms.Select(attrs={'class': 'form-select'}),
            "document": forms.TextInput(attrs={'class': 'form-control'}),
            "date_of_comming": forms.DateInput(format=('%Y-%m-%d'),
                                               attrs={'type': 'date',
                                                      'class': 'form-control'}),
            "use_by_date": forms.DateInput(format=('%Y-%m-%d'),
                                           attrs={'type': 'date',
                                                  'class': 'form-control'}),
            "serial_number": forms.TextInput(attrs={'class': 'form-control'}),
            "initial_amount": forms.NumberInput(attrs={'class': 'form-control',
                                                       'min': '1'}),
            "prise_for_unit": forms.NumberInput(attrs={'class': 'form-control',
                                                       'min': '1'}),
        }

    def clean_initial_amount(self):
        amount = self.cleaned_data['initial_amount']
        if amount > 0:
            return amount
        else:
            raise ValidationError('Недоупустимое количетсво')
    
    def clean_prise_for_unit(self):
        prise_for_unit = self.cleaned_data['prise_for_unit']
        if prise_for_unit > 0:
            return prise_for_unit
        else:
            raise ValidationError('Недоупустимая цена')


class FirmAdminForm(forms.ModelForm):
    class Meta:
        model = models.Firm
        fields = "__all__"
        labels = {'name': 'Название фирмы',
                  'firm_type': 'Тип фирмы'}


class FirmForm(forms.ModelForm):
    class Meta:
        model = models.Firm
        fields = ('name', )
        labels = {'name': 'Название фирмы'}

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }


class DrugUnitForm(forms.ModelForm):
    class Meta:
        model = models.DrugUnit
        fields = "__all__"
        labels = {'name': 'Единица измерения'}

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }


class MovementForm(forms.ModelForm):

    class Meta:
        model = models.Movement
        fields = ('amount', 'direction', 'date')
        labels = {'amount': 'Количество',
                  'date': 'Дата',
                  'direction': 'Направление',
                  }
        widgets = {
            "date": forms.DateInput(format=('%Y-%m-%d'),
                                    attrs={'type': 'date',
                                           'class': 'form-control'}),
            "amount": forms.NumberInput(attrs={'class': 'form-control',
                                               'min': '1'}),
            "direction": forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount > 0:
            return amount
        else:
            raise ValidationError('Недоупустимое количетсво')


class DirectionForm(forms.ModelForm):
    class Meta:
        model = models.Direction
        fields = "__all__"
        labels = {'name': 'Направление'}

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = "__all__"
        labels = {'name': 'Название'}

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }


class DrugForm(forms.ModelForm):
    class Meta:
        model = models.Drug
        fields = "__all__"
        labels = {'name': 'Название',
                  'unit': 'Единица измерения'}
        widgets = {
                "name": forms.TextInput(attrs={'class': 'form-control'}),
                "unit": forms.Select(attrs={'class': 'form-select'}),
            }


class DatePeriodForm(forms.Form):
    from_date = forms.DateField(label='Начальная дата',
                                initial=timezone.now(),
                                widget=forms.DateInput(format=('%Y-%m-%d'),
                                                       attrs={'type': 'date',
                                                              'class': 'form-control w-25'}))
    to_date = forms.DateField(label='Конечная дата',
                              initial=timezone.now(),
                              widget=forms.DateInput(format=('%Y-%m-%d'),
                                                     attrs={'type': 'date',
                                                            'class': 'form-control w-25'}))

class SingleDateForm(forms.Form):
    date = forms.DateField(label='Дата',
                           initial=timezone.now(),
                           widget=forms.DateInput(format=('%Y-%m-%d'),
                                                  attrs={'type': 'date',
                                                         'class': 'form-control w-25'}))


class DatePeriodDepartmentForm(DatePeriodForm):
    department = forms.ModelChoiceField(label='Отделение', queryset=models.Department.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-select w-25'}))


class DistributionForm(forms.ModelForm):
    class Meta:
        model = models.Distribution
        fields = ('department', 'amount')
        labels = {'department': 'Отделение',
                  'amount': 'Количество',
        }
        widgets = {
            "department": forms.Select(attrs={'class': 'form-select'}),
            "amount": forms.NumberInput(attrs={'class': 'form-control',
                                               'min': '1'}),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount > 0:
            return amount
        else:
            raise ValidationError('Недоупустимое количетсво')


class DistributionRecallForm(forms.Form):
    amount = forms.IntegerField(label='Количество',
                                widget=forms.NumberInput(attrs={'type': 'number',
                                                                'class': 'form-control',
                                                                'min': '1'}))
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount > 0:
            return amount
        else:
            raise ValidationError('Недоупустимое количетсво')


class WriteOff(forms.ModelForm):
    class Meta:
        model = models.WriteOff
        fields = ('date', 'amount', 'reason')
        labels = {'date': 'Дата',
                  'amount': 'Количество',
                  'reason': 'Причина',
                 }
        widgets = {
            "reason": forms.TextInput(attrs={'class': 'form-control'}),
            "amount": forms.NumberInput(attrs={'class': 'form-control',
                                               'min': '1'}),
            "date": forms.DateInput(format=('%Y-%m-%d'),
                                    attrs={'type': 'date',
                                           'class': 'form-control'}),
        }
