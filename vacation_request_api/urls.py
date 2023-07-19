"""
URL configuration for vacation_request_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vacation.views import (RequestListCreateView, 
                            RequestRetrieveUpdateDestroyView, 
                            WorkerRequestListView, 
                            WorkerRequestCreateView, 
                            WorkerRemainingVacationDaysView,
                            EmployeeRequestOverviewView,
                            OverlappingRequestsView,
                            ProcessRequestView,
                            AllRequestsOverviewView,
                            RequestRetrieveUpdateDestroyView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('requests/', RequestListCreateView.as_view(), name='request-list-create'),
    path('requests/<uuid:pk>/', RequestRetrieveUpdateDestroyView.as_view(), name='request-retrieve-update-destroy'),
    path('worker/requests/', WorkerRequestListView.as_view(), name='worker-request-list'),
    path('worker/requests/create/', WorkerRequestCreateView.as_view(), name='worker-request-create'),
    path('worker/requests/remaining-days/', WorkerRemainingVacationDaysView.as_view(), name='worker-remaining-days'),
    path('manager/employee/<str:employee_id>/overview/', EmployeeRequestOverviewView.as_view(), name='manager-employee-overview'),
    path('manager/requests/overlapping/', OverlappingRequestsView.as_view(), name='manager-overlapping-requests'),
    path('manager/requests/<uuid:pk>/process/', ProcessRequestView.as_view(), name='manager-process-request'),
    path('manager/requests/overview/', AllRequestsOverviewView.as_view(), name='manager-all-requests-overview'),


]
