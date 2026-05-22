from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response

class CustomerInformationViewSet(viewsets.ModelViewSet):
    queryset = CustomerInformation.objects.all()
    serializer_class = CustomerInformationSerializer
    search_fields = ('select_customer','gst_number','email','address')
    ordering_fields = ('id',)

    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED 
        )

class JobNumberViewSet(viewsets.ModelViewSet): 
    queryset = JobNumber.objects.all()
    serializer_class = JobNumberSerializer
    search_fields = ('job_number','date','duedate','descriptions')
    ordering_fields = ('id',)

    permission_classes = [AllowAny]
    authentication_classes = []

class JobItemsViewSet(viewsets.ModelViewSet):
    queryset = JobItems.objects.all()
    serializer_class = JobItemsSerializer
    search_fields = ('material','length','width','quantity','area','anodising_type','thickness','color_finish','process_charges')
    ordering_fields = ('id',)

    permission_classes = [AllowAny]
    authentication_classes = []

class anodising_typeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = JobItems.objects.all()
        serializer = anodising_typeSerializer(queryset, many=True)
        search_fields = ('anodising_type')
        ordering_fields = ('id',)

        permission_classes = [AllowAny]
        authentication_classes = []
        return Response(serializer.data)

class thicknessViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = JobItems.objects.all()
        serializer = thicknessSerializer(queryset, many=True)
        search_fields = ('thickness')
        ordering_fields = ('id',)

        permission_classes = [AllowAny]
        authentication_classes = []
        return Response(serializer.data)

class colorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = JobItems.objects.all()
        serializer = colorSerializer(queryset, many=True)
        search_fields = ('color_finish')
        ordering_fields = ('id',)

        permission_classes = [AllowAny]
        authentication_classes = []

class process_chargesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = JobItems.objects.all()
        serializer = process_chargesSerializer(queryset, many=True)
        search_fields = ('process_charges')
        ordering_fields = ('id',)

        permission_classes = [AllowAny]
        authentication_classes = []

class materialViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = JobItems.objects.all()
        serializer = materialSerializer(queryset, many=True)
        search_fields = ('material')
        ordering_fields = ('id',)

        permission_classes = [AllowAny]
        authentication_classes = []

class calculateViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = JobItems.objects.all()
        serializer = calculateSerializer(queryset, many=True)
        search_fields = ('area')
        ordering_fields = ('id',)

        permission_classes = [AllowAny]
        authentication_classes = []
        return Response(serializer.data)

#----FrontEnd View---------------
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from decimal import Decimal
import json


class CustomerView(View):
    def get(self, request):
        return render(request, 'customer.html')

    def post(self, request):
        select_customer = (request.POST.get('select_customer') or '').strip()
        email = (request.POST.get('email') or '').strip()
        gst_number = (request.POST.get('gst_number') or '').strip()
        address = (request.POST.get('address') or '').strip()

        if not select_customer:
            messages.error(request, "Customer name is required.")
            return render(request, 'customer.html', {
                        'form': {
                            'select_customer':select_customer,
                            'gst_number': gst_number,
                            'email': email,
                            'address': address,
                        }
                    })

        CustomerInformation.objects.create(
            select_customer=select_customer,
            gst_number=gst_number if gst_number else None,
            email=email,
            address=address,
        )

        messages.success(request, "Customer added successfully.")

        return redirect('jobs')

class JobNumberView(View):
    def get(self, request):
        return render(request, "job.html")

    def post(self, request):
        job_number = (request.POST.get('job_number') or '').strip()
        date = (request.POST.get('date') or '').strip()
        duedate = (request.POST.get('duedate') or '').strip()
        descriptions = (request.POST.get('descriptions') or '').strip()
        
        if not date:
            messages.error(request, "Date is required")
            return render(request, 'job.html', {
            'form': {
                'job_number': job_number,
                'date': date,
                'duedate': duedate,
                'descriptions': descriptions
            }
        })

        job = JobNumber.objects.create(
            job_number=job_number,
            date=date,
            duedate=duedate if duedate else None,
            descriptions=descriptions
        )
        messages.success(request, "Job created successfully")
        return redirect("jobitems", job_id=job.id)

class JobItemsView(View):

    def get(self, request, job_id):

        return render(request,"jobitem.html",{"job_id": job_id})

    def post(self, request, job_id):
        material = request.POST.get('material')
        length = float(request.POST.get('length') or 0)
        width = float(request.POST.get('width') or 0)
        quantity = int(request.POST.get('quantity') or 0)
        anodising_type = request.POST.get('anodising_type')
        thickness = request.POST.get('thickness')
        color_finish = request.POST.get('color_finish')
        process_charges = request.POST.get('process_charges') 
        
        area = length * width * quantity
        
        job = get_object_or_404(JobNumber, id=job_id)


        if not material:
            messages.error(request,"Job item is required")
            return render(request,'jobitem.html',{
                    'job_id': job_id,
                    'form': {
                        'material': material,
                        'length': length,
                        'width': width,
                        'quantity': quantity,
                        'area': area,
                        'anodising_type': anodising_type,
                        'thickness': thickness,
                        'color_finish': color_finish,
                        'process_charges': process_charges
                    }
                }
            )

        job = JobNumber.objects.get(id=job_id)
        JobItems.objects.create(
            job_number=job,
            material=material,
            length=length,
            width=width,
            quantity=quantity,
            area=area,
            anodising_type=anodising_type,
            thickness=thickness,
            color_finish=color_finish,
            process_charges=process_charges
        )

        messages.success(request, "Job Item created successfully")
        return redirect("calculate",job_id=job_id)

class calculateView(View):
    def get(self, request, job_id):
        job = get_object_or_404(JobNumber, id=job_id)
        items = JobItems.objects.filter(job_number=job)
        
        subtotal = sum(item.Total for item in items if item.Total)
        gst = subtotal * Decimal('0.18')
        total = subtotal + gst
        
        return render(request, "calculate.html", {
            "job": job,
            "items": items,
            "subtotal": subtotal,
            "gst": gst,
            "total": total
        })

        return redirect("calculate",job_id=job_id)
