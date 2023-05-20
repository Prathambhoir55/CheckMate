from django.urls import path
from . import views

urlpatterns = [
    path('hr-register/', views.HRRegisterAPI.as_view(), name = 'hr-registration'),
    path('emp-register/', views.EmployeeRegisterAPI.as_view(), name = 'emp-registration'),
    path('get-hr/', views.HRGetAPI.as_view(), name = 'get-employee'),
    path('get-empuser/', views.EmpGetAPI.as_view(), name = 'get-employee'),
    path('get-all-emp/', views.EmployeeListAPI.as_view(), name = 'get-all-emp'),
    path('emp-dropdown/', views.EmployeeDropDownAPI.as_view(), name = 'emp-dropdown'),
    path('all-emp/', views.AllEmployeeListAPI.as_view(), name = 'get-all-emp'),
    path('hr-get-emp/<int:pk>', views.HRGetEmployee.as_view(), name = 'hr-get-emp'),
    path('emp-update/', views.EmpPutAPI.as_view(), name = 'emp-update'),
]