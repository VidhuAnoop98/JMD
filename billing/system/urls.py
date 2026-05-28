"""
URL configuration for billing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'customer',views.CustomerInformationViewSet,basename='customer')
router.register(r'jobs', views.JobNumberViewSet, basename='job')
router.register(r'jobitems', views.JobItemsViewSet, basename='job_item')
router.register(r'anodising-type', views.anodising_typeViewSet, basename='anodising_type')
router.register(r'thickness', views.thicknessViewSet, basename='thickness')
router.register(r'color', views.colorViewSet, basename='color')
router.register(r'process-charges', views.process_chargesViewSet, basename='process_charges')
router.register(r'material', views.materialViewSet, basename='material')
router.register(r'calculate_cost', views.calculateViewSet, basename='calculate')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'reference-data', views.ReferenceDataViewSet, basename='reference_data')


urlpatterns = [
    path('',views.dashboardView.as_view(),name='dashboard'),
    path('customer/',views.CustomerView.as_view(),name='customer'),
    path('jobs/', views.JobNumberView.as_view(), name='jobs'),
    path('jobs/<int:job_id>/items/', views.JobItemsView.as_view(), name='jobitems'),
    path('anodising-type/',views.anodising_typeViewSet.as_view({'get':'list'}), name='anodising_type'),
    path('thickness/',views.thicknessViewSet.as_view({'get':'list'}), name='thickness'),
    path('colors/',views.colorViewSet.as_view({'get':'list'}), name='color'),
    path('process-charges/',views.process_chargesViewSet.as_view({'get':'list'}), name='process_charges'),
    path('items/',views.materialViewSet.as_view({'get':'list'}), name='material'),
    path('jobs/<int:job_id>/calculate/',views.calculateView.as_view(), name='calculate'),
    path('jobs/<int:job_id>/invoice/',views.InvoiceView.as_view(), name='invoice'),
    # API custom endpoints
    path('api/get-customer-details/', views.GetCustomerDetailsView.as_view(), name='api_get_customer_details'),
    path('api/get-anodising-details/', views.anodising_typeViewSet.as_view({'get':'get_anodising_details'}), name='get_anodising_details'),
    path('api/get-thickness-details/', views.thicknessViewSet.as_view({'get':'get_thickness_details'}), name='get_thickness_details'),
    path('api/get-color-details/', views.colorViewSet.as_view({'get':'get_color_details'}), name='color_details'),
    path('api/calculate-cost/', views.calculateViewSet.as_view({'post':'calculate_cost'}), name='calculate_cost'),
    path('api/get-all-data/', views.ReferenceDataViewSet.as_view({'get':'get_all_data'}), name='get_all_data'),
    # Router URLs
    path('api/',include(router.urls)) 
] 

