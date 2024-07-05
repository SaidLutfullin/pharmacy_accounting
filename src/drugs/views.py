from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView, CreateView, UpdateView, TemplateView, DeleteView
from . import models
from django.core.exceptions import PermissionDenied
from . import forms
from loguru import logger

from .services import ShipmentService, DistributionService
from .report import Report
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import DrugUnit
from django.utils import timezone
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView


# drugs CRUD
class DrugsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'drugs/drugs.html'
    model = models.Drug
    context_object_name = 'drugs'
    paginate_by = 10
    permission_required = 'drugs.view_drug'

    def post(self, request, *args, **kwargs):
        if 'drug_save' in request.POST:
            form = forms.DrugForm(request.POST)
        elif 'unit_save' in request.POST:
            form = forms.DrugUnitForm(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            if 'drug_save' in request.POST:
                return self.form_invalid(drug_form=form)
            elif 'unit_save' in request.POST:
                return self.form_invalid(drug_unit_form=form)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.pk = self.request.POST.get('object_id')
        object.save()
        return HttpResponseRedirect(reverse_lazy('drugs_list'))

    def form_invalid(self, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_queryset(self):
        search_query = self.request.GET.get("search-quesry", "")
        search_query = search_query.replace(' ', '')
        drugs = self.model.objects.all().select_related('unit')
        if search_query != "":
            drugs = drugs.filter(name__icontains=search_query)
        return drugs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # check if there is GET arguments
        # that means editing
        drug_id = self.request.GET.get('drud_id')
        drud_unit_id = self.request.GET.get('drud_unit_id')
        drug = None
        drud_unit = None
        # initializing form for editing
        if drug_id is not None:
            drug = get_object_or_404(self.model, pk=drug_id)
            context['editing'] = 'drug'
            context['drug_id'] = drug_id
        elif drud_unit_id is not None:
            drud_unit = get_object_or_404(DrugUnit, pk=drud_unit_id)
            context['editing'] = 'drug_unit'
            context['drud_unit_id'] = drud_unit_id
        # when invalid form is returned it presences in kwargs
        if "drug_form" not in kwargs:
            context['drug_form'] = forms.DrugForm(instance=drug)
        if "drug_unit_form" not in kwargs:
            context['drug_unit_form'] = forms.DrugUnitForm(instance=drud_unit)
        context['units'] = models.DrugUnit.objects.all()

        search_query = self.request.GET.get("search-quesry")
        if search_query is not None and search_query != "":
            context['search_query'] = search_query
        return context


class DrugDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Drug
    success_url = reverse_lazy('drugs_list')
    template_name = "common/confirm_deleting.html"
    pk_url_kwarg = "drug_id"
    permission_required = 'drugs.view_drug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'Лекарство {self.object.name}'
        return context


class DrugUnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.DrugUnit
    success_url = reverse_lazy('drugs_list')
    template_name = "common/confirm_deleting.html"
    pk_url_kwarg = "drug_unit_id"
    permission_required = 'drugs.view_drug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'Единица измерения {self.object.name}'
        return context


# FirmsCRUD
class FirmsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'drugs/firms.html'
    model = models.Firm
    context_object_name = 'firms'
    permission_required = 'drugs.view_firm'
    form_class = forms.FirmForm
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search-quesry", "")
        search_query = search_query.replace(' ', '')
        queryset = self.model.objects.filter(firm_type=self.kwargs['firm_type'])
        if search_query != "":
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_object(self):
        firm_id = self.request.GET.get('firm_id')
        object = None
        if firm_id is not None:
            object = get_object_or_404(self.model, pk=firm_id)
        return object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = forms.FirmForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form=form)

    def get_success_url(self):
        if self.kwargs['firm_type'] == 'provider':
            return reverse('providers_list')
        elif self.kwargs['firm_type'] == 'producer':
            return reverse('producers_list')

    def form_valid(self, form):
        firm = form.save(commit=False)
        firm.firm_type = self.kwargs['firm_type']

        firm_pk = self.request.POST.get('firm_id')
        if firm_pk is not None:
            firm.pk = firm_pk
        firm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['firm_type'] = self.kwargs['firm_type']
        if 'form' not in kwargs:
            context['form'] = forms.FirmForm(instance=self.object)

        context['firm_id'] = self.request.GET.get('firm_id')

        search_query = self.request.GET.get("search-quesry")
        if search_query is not None and search_query != "":
            context['search_query'] = search_query

        if self.kwargs['firm_type'] == 'provider':
            context['verbose_firm_type'] = 'поставщики'
            context['firm_delete_url'] = 'provider_delete'
            context['firms_list'] = 'providers_list'
        elif self.kwargs['firm_type'] == 'producer':
            context['verbose_firm_type'] = 'производители'
            context['firm_delete_url'] = 'producer_delete'
            context['firms_list'] = 'producers_list'
        return context


# TODO fix deleting if protected
class DeleteFirmView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Firm
    template_name = "common/confirm_deleting.html"
    pk_url_kwarg = "firm_id"
    permission_required = 'drugs.view_firm'

    def get_success_url(self):
        if self.kwargs['firm_type'] == 'provider':
            return reverse('providers_list')
        elif self.kwargs['firm_type'] == 'producer':
            return reverse('producers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'Фирма {self.object.name}'     
        return context


# departemnts CRUD
class DepartmentsView(LoginRequiredMixin, ListView):
    template_name = 'drugs/departments.html'
    model = models.Department
    form_class = forms.DepartmentForm
    context_object_name = 'departments'
    permission_required = 'drugs.view_department'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("search-quesry", "")
        search_query = search_query.replace(' ', '')
        queryset = self.model.objects.all()
        if search_query != "":
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_object(self):
        firm_id = self.request.GET.get('department_id')
        object = None
        if firm_id is not None:
            object = get_object_or_404(self.model, pk=firm_id)
        return object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form=form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = self.form_class(instance=self.object)

        context['department_id'] = self.request.GET.get('department_id')
        search_query = self.request.GET.get("search-quesry")
        if search_query is not None and search_query != "":
            context['search_query'] = search_query
        return context

    def form_valid(self, form):
        department = form.save(commit=False)
        department_pk = self.request.POST.get('department_id')
        if department_pk is not None:
            department.pk = department_pk
        department.save()
        return HttpResponseRedirect(reverse('departments_list'))

    def form_invalid(self, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(**kwargs))


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Department
    success_url = reverse_lazy('departments_list')
    template_name = "common/confirm_deleting.html"
    pk_url_kwarg = "department_id"
    permission_required = 'drugs.view_department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'Отделение {self.object.name}'
        return context


# shipments
class Shipments(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'drugs/shipments_list.html'
    model = models.Shipment
    context_object_name = 'shipments'
    permission_required = 'drugs.view_shipment'
    shipment_service = ShipmentService()
    paginate_by = 10

    def get_queryset(self):
        mode = self.request.GET.get('mode', None)
        return self.model.get_shipments(mode)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = self.request.GET.get('mode', None)
        return context


class ShipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = forms.ShipmentForm
    template_name = 'drugs/shipment.html'
    success_url = reverse_lazy('shipments_list')
    permission_required = 'drugs.view_shipment'
    pk_url_kwarg = "shipment_id"
    model = models.Shipment

    def get_object(self, queryset=None):
        obj = self.get_queryset().get(pk=self.kwargs.get(self.pk_url_kwarg))
        if obj.initial_amount == obj.undistributed_amount:
            return obj
        else:
            raise PermissionDenied()


class CreateShipment(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = forms.ShipmentForm
    template_name = 'drugs/shipment.html'
    success_url = reverse_lazy('shipments_list')
    permission_required = 'drugs.view_shipment'

    def form_valid(self, form):
        shipment = form.save(commit=False)
        shipment.current_amount = shipment.initial_amount
        shipment.save()
        return HttpResponseRedirect(self.success_url)


class CreateMovementView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = forms.MovementForm
    template_name = 'drugs/movement.html'
    success_url = reverse_lazy('shipments_list')
    permission_required = 'drugs.view_movement'
    shipment_service = ShipmentService()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = models.Department.objects.get(pk=self.kwargs['department_id'])
        context['shipment'] = models.Shipment.objects.get(pk=self.kwargs['shipment_id'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            movement = form.save(commit=False)
            shipment_id = self.kwargs['shipment_id']
            department_id = self.kwargs['department_id']
            employee = self.request.user
            successfull = self.shipment_service.create_movement(movement, employee,
                                                                shipment_id, department_id)
            if successfull:
                return self.form_valid(form)
            else:
                form.add_error(self.shipment_service.error['field'],
                               self.shipment_service.error['text'])
        return self.form_invalid(form)


class MovementsListView(LoginRequiredMixin, ListView):
    template_name = 'drugs/movements_list.html'
    model = models.Movement
    context_object_name = 'movements'
    paginate_by = 10
    permission_required = 'drugs.view_movement'

    def get_queryset(self):
        query = self.model.objects.all()
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        if from_date is not None:
            query = query.filter(date__gte=from_date)
        if to_date is not None:
            query = query.filter(date__lte=to_date)
        if from_date is None and to_date is None:
            today_date = timezone.now().date().strftime('%Y-%m-%d')
            query = query.filter(date=today_date)

        query = query.select_related('shipment',
                                     'shipment__drug',
                                     'shipment__drug__unit',
                                     'department',
                                     'employee')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        today_date = timezone.now().date().strftime('%Y-%m-%d')
        if from_date is None:
            from_date = today_date
        if to_date is None:
            to_date = today_date
        context['can_delete'] = self.request.user.has_perm('drugs.delete_movement')
        context['from_date'] = from_date
        context['to_date'] = to_date

        return context


class DeleteMovementView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Movement
    success_url = reverse_lazy('movements_list')
    template_name = "drugs/confirm_deleting_movement.html"
    pk_url_kwarg = "movement_id"
    context_object_name = 'movement'
    permission_required = 'drugs.view_direction'

    def form_valid(self, form):
        success_url = self.get_success_url()
        shipment_service = ShipmentService()
        shipment_service.delete_movement(self.object.id)
        return HttpResponseRedirect(success_url)


class DirectionsView(LoginRequiredMixin,
                     SingleObjectTemplateResponseMixin,
                     ModelFormMixin,
                     ProcessFormView):
    model = models.Direction
    success_url = reverse_lazy('directions')
    template_name = 'drugs/directions.html'
    form_class = forms.DirectionForm
    pk_url_kwarg = "direction_id"
    permission_required = 'drugs.view_direction'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['directions'] = self.get_queryset()
        if self.object is not None:
            context['editing'] = True
        else:
            context['editing'] = False
        return context


class DirectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Direction
    success_url = reverse_lazy('directions')
    template_name = "common/confirm_deleting.html"
    pk_url_kwarg = "direction_id"
    permission_required = 'drugs.view_direction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'Напралвение {self.object.name}'
        return context


class ReportTypesView(LoginRequiredMixin, TemplateView):
    template_name = 'drugs/report_types.html'
    permission_required = 'drugs.view_movement'


class ReportsCreateView(LoginRequiredMixin, FormView):
    template_name = 'drugs/create_report.html'
    permission_required = 'drugs.view_movement'

    def get_form_class(self):
        report_type = self.kwargs.get('report_type')

        if report_type == 'use_by_date' or report_type == 'presence':
            return forms.SingleDateForm
        elif report_type == 'expenditure' or \
             report_type == 'expenditure_with_date' or \
             report_type == 'shipment_report' or \
             report_type == 'spent_drugs_report_all_departments' or \
             report_type == 'movement_report':
            return forms.DatePeriodForm
        elif report_type == 'spent_drugs_report':
            return forms.DatePeriodDepartmentForm

    def form_valid(self, form):
        report_type = self.kwargs.get('report_type')

        if report_type == 'use_by_date':
            report = Report.use_by_date_report(form.cleaned_data['date'])
        elif report_type == 'presence':
            report = Report.presence_report(form.cleaned_data['date'])
        elif report_type == 'expenditure':
            report = Report.expenditure_report(form.cleaned_data['from_date'],
                                               form.cleaned_data['to_date'])
        elif report_type == 'expenditure_with_date':
            report = Report.expenditure_report(form.cleaned_data['from_date'],
                                               form.cleaned_data['to_date'],
                                               date_of_movement_needed=True)
        elif report_type == 'shipment_report':
            report = Report.shipment_report(form.cleaned_data['from_date'], form.cleaned_data['to_date'])
        elif report_type == 'spent_drugs_report':
            report = Report.spent_drugs_report(form.cleaned_data['from_date'], form.cleaned_data['to_date'], form.cleaned_data['department'])
        elif report_type == 'spent_drugs_report_all_departments':
            report = Report.spent_drugs_report_all_departments(form.cleaned_data['from_date'], form.cleaned_data['to_date'])
        elif report_type == 'movement_report':
            report = Report.movement_report(form.cleaned_data['from_date'], form.cleaned_data['to_date'])
        report.save()

        return FileResponse(open('report.xlsx', 'rb'))


class DistributionsListView(LoginRequiredMixin, ListView):
    """distribution list for user"""
    template_name = 'drugs/distributions_list.html'
    model = models.Distribution
    context_object_name = 'distributions'
    permission_required = 'drugs.view_shipment'

    def get_queryset(self):
        department_id = self.request.GET.get('department_id')
        return self.model.objects.select_related('shipment', 'shipment__drug', 'shipment__drug__unit')\
            .filter(department_id=department_id, amount__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = self.request.user.department.all()
        department_id = self.request.GET.get('department_id')
        if department_id is not None:
            context['selected_department'] = get_object_or_404(models.Department, pk=department_id)
        return context


# distribution view for admin
# create, edit, view distribution on the concrete shipment
class DistributionsView(LoginRequiredMixin, FormView):
    template_name = 'drugs/distributions.html'
    distribution_service = None
    permission_required = 'drugs.view_shipment'

    def get_form_class(self):
        if 'distribution_id' in self.kwargs:
            return forms.DistributionRecallForm
        elif self.kwargs.get('write_off', False):
            return forms.WriteOff
        else:
            return forms.DistributionForm

    def get_success_url(self):
        return reverse_lazy('distributions',
                            kwargs={'shipment_id': self.kwargs.get('shipment_id')})

    def get_queryset(self):
        distributions = models.Distribution.objects.filter(shipment_id=self.kwargs.get('shipment_id'))
        return distributions

    def get_service(self):
        if self.distribution_service is None:
            self.distribution_service = DistributionService(shipment_id=self.kwargs.get('shipment_id'),
                                                            distribution_id=self.kwargs.get('distribution_id'))
        return self.distribution_service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'distribution_id' in self.kwargs:
            context['mode'] = 'recalling'
        elif self.kwargs.get('write_off', False):
            context['mode'] = 'write_off'
        context['shipment'] = get_object_or_404(models.Shipment, pk=self.kwargs.get('shipment_id'))
        
        context['distributions'] = self.get_queryset()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():

            if 'distribution_id' in self.kwargs:
                success = self.get_service().recall_distribution(form.cleaned_data['amount'])
                if success:
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    form.add_error('amount', f'В наличии только {self.get_service().available_amount}')
            elif self.kwargs.get('write_off', False):
                shipment_service = ShipmentService()
                write_off = form.save(commit=False)

                write_off.shipment_id = self.kwargs.get('shipment_id')
                success = shipment_service.write_off_shipment(write_off)
                if success:
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    form.add_error(shipment_service.error['field'],
                                   shipment_service.error['text'])
            else:
                distribution = form.save(commit=False)
                success = self.get_service().create_distribution(distribution)

                if success:
                    return self.form_valid(form)
                else:
                    form.add_error('amount', f'В наличии только {self.get_service().available_amount}')
        return self.form_invalid(form)


class WriteOffListView(LoginRequiredMixin, ListView):
    model = models.WriteOff
    template_name = 'drugs/write_off_list.html'
    permission_required = 'drugs.view_shipment'
    context_object_name = 'write_offs'
    paginate_by = 20

    def get_from_date(self):
        now = datetime.datetime.now()
        return (datetime.datetime(now.year, now.month, 1).date()).strftime('%Y-%m-%d')

    def get_to_date(self):
        now = datetime.datetime.now()
        next_month = now.month + 1 if now.month < 12 else 1
        next_year = now.year if now.month < 12 else now.year + 1
        return (datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    def get_time_period(self):
        from_date = self.request.GET.get('from_date', "")
        to_date = self.request.GET.get('to_date', "")

        if from_date == "":
            from_date = self.get_from_date()

        if to_date == "":
            to_date = self.get_to_date()
        return from_date, to_date

    def get_queryset(self):
        query = self.model.objects.all()
        from_date, to_date = self.get_time_period()

        query = query.filter(date__gte=from_date)
        query = query.filter(date__lte=to_date)

        query = query.select_related('shipment',
                                     'shipment__drug',
                                     'shipment__drug__unit',)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from_date, to_date = self.get_time_period()
        context['from_date'] = from_date
        context['to_date'] = to_date
        context['can_delete'] = self.request.user.has_perm('drugs.delete_writeoff')
        return context


class WriteOffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.WriteOff
    success_url = reverse_lazy('write_off_list')
    template_name = "drugs/confirm_deleting_write_off.html"
    pk_url_kwarg = "write_off_id"
    context_object_name = 'write_off'
    permission_required = 'drugs.delete_writeoff'

    def form_valid(self, form):
        success_url = self.get_success_url()
        shipment_service = ShipmentService()
        shipment_service.delete_write_off(self.object.id)
        return HttpResponseRedirect(success_url)
