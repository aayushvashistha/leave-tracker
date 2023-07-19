from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import generics
from vacation.models import Request
from vacation.serializers import RequestSerializer
from django.utils import timezone
from django.core.exceptions import ValidationError

class RequestListCreateView(generics.ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        serializer.save()

class RequestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer



class WorkerRequestListView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        # Get the authenticated worker's requests
        worker_requests = Request.objects.filter(author=self.request.user.username)

        # Filter requests by status
        status = self.request.query_params.get('status', None)
        if status is not None:
            worker_requests = worker_requests.filter(status=status)

        return worker_requests

class WorkerRequestCreateView(generics.CreateAPIView):
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        # Check if the worker has reached the request limit
        worker = self.request.user.worker
        current_year = timezone.now().year
        requests_count = Request.objects.filter(author=worker, created_at__year=current_year).count()
        if requests_count >= 30:
            raise ValidationError("You have reached the maximum limit of vacation requests for this year.")

        # Set the author of the request as the current authenticated user
        serializer.save()

class WorkerRemainingVacationDaysView(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        worker = self.request.user.worker
        current_year = timezone.now().year
        requests_count = Request.objects.filter(author=worker, created_at__year=current_year).count()
        remaining_days = 30 - requests_count  # Assuming 30 vacation days per year
        return Response({'remaining_days': remaining_days})

class EmployeeRequestOverviewView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return Request.objects.filter(author=employee_id)

class OverlappingRequestsView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        overlapping_requests = Request.objects.filter(
            Q(status='approved') | Q(status='pending')
        ).filter(
            Q(vacation_start_date__lte=self.kwargs['end_date']) & Q(vacation_end_date__gte=self.kwargs['start_date'])
        )
        return overlapping_requests

class ProcessRequestView(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class AllRequestsOverviewView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status is not None:
            return Request.objects.filter(status=status)
        return Request.objects.all()