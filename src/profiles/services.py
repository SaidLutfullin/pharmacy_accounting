from django.contrib.auth.models import Permission
from .forms import PermissionsForm
from .models import Employee
from loguru import logger

class PermissionsService:
    def __init__(self, user_id):
        self.user = Employee.objects.get(pk=user_id)

    def get_user_full_name(self):
        full_name = []
        if self.user.first_name is not None:
            full_name.append(self.user.first_name)
        if self.user.last_name is not None:
            full_name.append(self.user.last_name)
        if self.user.middle_name is not None:
            full_name.append(self.user.middle_name)
        if self.user.speciality is not None:
            full_name.append(self.user.speciality)
        return " ".join(full_name)

    PERMISSION_NAMES = {
        'employee_add_permission': 'profiles.add_employee',
        'employee_edit_permission': 'profiles.change_employee',
        'movement_delete_permission': 'drugs.delete_movement',
        'write_off_delete_permission': 'drugs.delete_writeoff',
        'drugs_permission': 'drugs.view_drug',
        'firms_permission': 'drugs.view_firm',
        'departments_permission': 'drugs.view_department',
        'shipments_permission': 'drugs.view_shipment',
        'movements_permission': 'drugs.view_movement',
        'directions_permission': 'drugs.view_direction',
        'reports_permission': 'drugs.view_report',
    }

    @logger.catch
    def get_permissions_form_initial(self):
        users_all_permissions = self.user.get_all_permissions()
        initial = {}
        for form_item in self.PERMISSION_NAMES:
            permission_name = self.PERMISSION_NAMES[form_item]
            initial[form_item] = permission_name in users_all_permissions

        return initial

    @logger.catch
    def set_permissions(self, cleaned_data):

        available_permissions = Permission.objects.all()

        add_permissions_list = []
        remove_permissions_list = []
        for permission in cleaned_data:
            permission_id = available_permissions.get(codename=self.PERMISSION_NAMES[permission].split('.')[1]).pk
            if cleaned_data[permission]:
                add_permissions_list.append(permission_id)
            else:
                remove_permissions_list.append(permission_id)
        # WHY DOES IT WORK ONLY WITH *
        self.user.user_permissions.remove(*(remove_permissions_list))
        self.user.user_permissions.add(*(add_permissions_list))
