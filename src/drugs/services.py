from src.drugs.models import Shipment, Movement, Distribution, Department, WriteOff
from loguru import logger
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import PermissionDenied


class ShipmentService:
    @transaction.atomic
    def create_movement(self, movement, employee, shipment_id, department_id):
        # checking movement to department, that is inavailable for user
        department = Department.objects.get(pk=department_id)
        if not department.employee_set.filter(pk=employee.id):
            raise PermissionDenied()

        distribution = Distribution.objects.get(shipment_id=shipment_id,
                                                department_id=department_id)

        if movement.amount <= distribution.amount:
            shipment = get_object_or_404(Shipment, pk=shipment_id)
            # moving only after date of comming
            if movement.date >= shipment.date_of_comming:
                distribution.amount -= movement.amount
                shipment.current_amount -= movement.amount

                if shipment.current_amount == 0:
                    self.set_date_of_run_out(self, shipment, movement.date)

                movement.shipment_id = shipment_id
                movement.department_id = department_id
                movement.employee = employee
                shipment.save()
                movement.save()
                distribution.save()
                return True
            else:
                # TODO proped date format
                self.error = {
                    'field': 'date',
                    'text': f'Дата поступления {shipment.date_of_comming}. Расход возможен только после этой даты.'
                }
                return False
        else:
            self.error = {
                    'field': 'amount',
                    'text': f'В наличии только {distribution.amount}.'
                }
            return False


    @transaction.atomic
    def delete_movement(self, movement_id):
        movement = Movement.objects.select_for_update().get(pk=movement_id)
        distribution = Distribution.objects.filter(shipment_id=movement.shipment.id,
                                                   department_id=movement.department_id).first()
        movement.shipment.current_amount += movement.amount
        distribution.amount += movement.amount
        if movement.shipment.date_of_run_out is not None:
            movement.shipment.date_of_run_out = None

        movement.shipment.save()
        distribution.save()
        movement.delete()

    @transaction.atomic
    def write_off_shipment(self, write_off):
        shipment = Shipment.objects.get(pk=write_off.shipment_id)
        if shipment.undistributed_amount >= write_off.amount:
            if shipment.date_of_comming <= write_off.date:
                shipment.current_amount -= write_off.amount
                shipment.undistributed_amount -= write_off.amount
                shipment.initial_amount -= write_off.amount
                shipment.save()
                write_off.save()
                return True
            else:
                self.error = {
                    'field': 'date',
                    'text': f'Неверная дата.'
                }
                return False
        else:
            self.error = {
                'field': 'amount',
                'text': f'В наличии только {shipment.undistributed_amount}.'
            }
            return False

    @transaction.atomic
    def delete_write_off(self, write_off_id):
        write_off = WriteOff.objects.select_for_update().get(pk=write_off_id)
        write_off.shipment.current_amount += write_off.amount
        if write_off.shipment.date_of_run_out is not None:
            write_off.shipment.date_of_run_out = None
        write_off.shipment.save()
        write_off.delete()

    def set_date_of_run_out(self, shipment, expense_date):
        last_movement = Movement.objects.filter(shipment_id=shipment.pk).latest('date')
        last_write_off = WriteOff.objects.filter(shipment_id=shipment.pk).latest('date')
        # when previous movement/write_off added to base
        # by later date than current movement
        if last_movement.date > expense_date:
            date_of_run_out = last_movement.date
        elif last_write_off.date > expense_date:
            date_of_run_out = last_write_off.date
        else:
            date_of_run_out = expense_date
        shipment.date_of_run_out = date_of_run_out


class DistributionService:
    def __init__(self, shipment_id=None, distribution_id=None):
        if shipment_id is None:
            self.shipment = None
        else:
            self.shipment = Shipment.objects.get(pk=shipment_id)

        if distribution_id is None:
            self.distribution = None
        else:
            self.distribution = Distribution.objects.select_related('shipment').get(pk=distribution_id)

    @transaction.atomic
    def create_distribution(self, distribution):
        # can distribute only undestributed amount

        if distribution.amount <= self.shipment.undistributed_amount:
            self.shipment.undistributed_amount -= distribution.amount

            previous_distribution = Distribution.objects.filter(shipment_id=self.shipment.id,
                                                                department=distribution.department)

            if previous_distribution.exists():

                # amount and initial amount of current distribution
                amount = distribution.amount
                initial_amount = distribution.amount

                distribution = previous_distribution.first()
                distribution.amount += amount
                distribution.initial_amount += initial_amount
            else:
                distribution.shipment_id = self.shipment.id
            
            distribution.save()
            self.shipment.save()
            return True
        else:
            self.available_amount = self.shipment.undistributed_amount
            return False

    @transaction.atomic
    def recall_distribution(self, amount):
        if amount <= self.distribution.amount:
            self.distribution.amount -= amount
            self.distribution.initial_amount -= amount
            self.distribution.shipment.undistributed_amount += amount

            self.distribution.shipment.save()
            # all distributed are recalled
            if self.distribution.amount == 0 and self.distribution.initial_amount == 0:
                self.distribution.delete()
            else:
                self.distribution.save()

            return True
        else:
            self.available_amount = self.distribution.amount
            return False
