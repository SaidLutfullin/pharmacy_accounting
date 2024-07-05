from django.urls import path
from . import views

urlpatterns = [
    path('drugs', views.DrugsView.as_view(), name='drugs_list'),

    path('drugs/<int:drug_id>/delete', views.DrugDeleteView.as_view(),
         name='drug_delete'),

    path('drugunits/<int:drug_unit_id>/delete',
         views.DrugUnitDeleteView.as_view(),
         name='drug_unit_delete'),

    path('providers', views.FirmsView.as_view(),
         {'firm_type': "provider"},
         name='providers_list'),
    path('providers/<int:firm_id>/delete', views.DeleteFirmView.as_view(),
         {'firm_type': "provider"}, name='provider_delete'),

    path('producers', views.FirmsView.as_view(),
         {'firm_type': "producer"},
         name='producers_list'),
    path('producers/<int:firm_id>/delete', views.DeleteFirmView.as_view(),
         {'firm_type': "producer"},
         name='producer_delete'),

    path('departments', views.DepartmentsView.as_view(),
         name='departments_list'),
    path('departments/<int:department_id>/delete',
         views.DepartmentDeleteView.as_view(), name='department_delete'),

    path('shipments/', views.Shipments.as_view(), name='shipments_list'),
    path('shipments/new', views.CreateShipment.as_view(),
         name='shipment_create'),
    path('shipments/<int:shipment_id>', views.ShipmentUpdateView.as_view(),
         name='shipment_update'),

    path('movements/<int:shipment_id>/<int:department_id>', views.CreateMovementView.as_view(),
         name='movement_create'),

    path('reports', views.ReportTypesView.as_view(),
         name='reports_types_list'),
    path('reports/<str:report_type>', views.ReportsCreateView.as_view(),
         name='create_report'),
         
    path('movements_list', views.MovementsListView.as_view(),
         name='movements_list'),
    path('delete_movement/<int:movement_id>', views.DeleteMovementView.as_view(),
         name='delete_movement'),

    path('distributions/', views.DistributionsListView.as_view(),
         name='distributions_list'),
    path('distributions/write_off', views.WriteOffListView.as_view(),
         name='write_off_list'),
    path('delete_write_off/<int:write_off_id>', views.WriteOffDeleteView.as_view(),
         name='delete_write_off'),
    path('distribution/<int:shipment_id>', views.DistributionsView.as_view(),
         name='distributions'),
    path('distribution/<int:shipment_id>/<int:distribution_id>', views.DistributionsView.as_view(),
         name='distributions'),
    path('distribution/<int:shipment_id>/write_off', views.DistributionsView.as_view(),
         {'write_off': True},
         name='distributions_write_off'),
    path('directions', views.DirectionsView.as_view(),
         name='directions'),
    path('directions/<int:direction_id>', views.DirectionsView.as_view(),
         name='update_directions'),
    path('directions/<int:direction_id>/delete', views.DirectionDeleteView.as_view(),
         name='delete_directions'),
]
