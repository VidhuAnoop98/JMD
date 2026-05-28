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

    def perform_create(self, serializer):
        instance = serializer.save()
        self.request.session['customer_id'] = instance.id

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

    def perform_create(self, serializer):
        customer_id = self.request.session.get('customer_id')
        customer = CustomerInformation.objects.filter(id=customer_id).first() if customer_id else None
        serializer.save(customer=customer)

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
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from decimal import Decimal
import json

class dashboardView(View):
    def get(self, request):
        total_customer = CustomerInformation.objects.count()
        total_jobs = JobNumber.objects.count()
        invoices = Invoice.objects.select_related('customer', 'jobs').all().order_by('-id')
        total_sales = sum(inv.total for inv in invoices)
        return render(request, "Dashboard.html", {
            "total_customer": total_customer,
            "total_jobs": total_jobs,
            "invoices": invoices,
            "total_sales": total_sales,
        })

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

        customer = CustomerInformation.objects.create(
            select_customer=select_customer,
            gst_number=gst_number if gst_number else None,
            email=email,
            address=address,
        )
        
        request.session['customer_id'] = customer.id

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

        customer_id = request.session.get('customer_id')
        customer = CustomerInformation.objects.filter(id=customer_id).first() if customer_id else None

        job = JobNumber.objects.create(
            customer=customer,
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

    #return redirect("calculate",job_id=job_id)

    #--------------------Reportlab------------------------
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import Image
from datetime import datetime
from django.conf import settings
import os
from reportlab.platypus import HRFlowable



class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Invoice management tailored to the current Invoice model."""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class InvoiceView(View):
    def get(self, request, job_id):
        job_obj = get_object_or_404(JobNumber, id=job_id)
        customer_obj = job_obj.customer
        items = JobItems.objects.filter(job_number=job_obj)

        subtotal = sum(item.Total for item in items if item.Total)
        from decimal import Decimal
        gst = subtotal * Decimal('0.18')
        total_amount = subtotal + gst

        invoice_obj, created = Invoice.objects.get_or_create(
            jobs=job_obj,
            defaults={
                'customer': customer_obj,
                'subtotal': subtotal,
                'gst_amount': gst,
                'total': total_amount,
            }
        )

        filename = f"{customer_obj.select_customer}.pdf" if customer_obj else "invoice.pdf"

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        doc = SimpleDocTemplate(
            response,
            pagesize=A4,
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        elements = []
        styles = getSampleStyleSheet()

        # Try to load logo from MEDIA_ROOT; fall back to app static folder.
        logo_path = None
        if getattr(settings, 'MEDIA_ROOT', None):
            logo_path = os.path.join(settings.MEDIA_ROOT, 'jmd-logo.jpg')

        fallback_path = os.path.join(os.path.dirname(__file__), 'static', 'jmd-logo.jpg')

        for path in (logo_path, fallback_path):
            if path and os.path.exists(path):
                try:
                    logo = Image(path, width=170, height=70)
                    elements.append(logo)
                    break
                except (OSError, IOError):
                    # If reportlab can't open the image, skip it silently.
                    break
        
        company = Paragraph("""
        <b>JMD PVT LTD</b><br/>
        Kerala, India<br/>
        GSTIN: 32ABCDE1234F1Z5<br/>
        Phone: 9999999999
        """, styles['BodyText'])

        customer_data = f"""
        <b>Date:</b> {invoice_obj.date}<br/><br/>
        """

        inv = Paragraph(customer_data, styles['BodyText'])
        elements.append(Spacer(1, 10))

        top_table = Table([[company, inv]], colWidths=[430, 100])
        elements.append(top_table)
        elements.append(Spacer(1, 20))

        elements.append(HRFlowable(width="100%"))
        elements.append(Spacer(1, 10))

        elements.append(HRFlowable(width="100%"))
        elements.append(Spacer(1, 10))

        # Safely render customer information; invoice may not have a customer set.
        customer_info = Paragraph(
                f"""<b>Full Name:</b> {customer_obj.select_customer}<br/>
                <b>GST Number:</b> {customer_obj.gst_number}<br/>
                <b>Email:</b> {customer_obj.email}<br/>
                <b>Address:</b> {customer_obj.address}<br/>
                """, styles['BodyText']
            )
    

        job_info = Paragraph(f"""<b>Job Number:</b> {job_obj.job_number}<br/>
                        <b>Date:</b> {job_obj.date}<br/>
                        <b>Due Date:</b> {job_obj.duedate}<br/>
                        """, styles['BodyText'])

        top_table1 = Table([[customer_info, job_info]], colWidths=[380, 150])
        elements.append(top_table1)
        elements.append(Spacer(1, 20))

        invoice_style = ParagraphStyle(
            'InvoiceStyle',
            parent=styles['BodyText'],
            fontSize=20,
            leading=22,
            alignment=TA_CENTER
        )
        invoice_info = Paragraph(f"""<b>Invoice #:</b> {invoice_obj.invoice_no}<br/>
                        """, invoice_style)
        elements.append(invoice_info)
        elements.append(Spacer(1, 10))

        table_shape = [["Base Cost", "Thickness Cost", "Color Finish Cost", "Process Charge Cost"]]
        for item in items:
            table_shape.append([
                f"{item.base_cost or 0:.2f}",
                f"{item.thickness_cost or 0:.2f}",
                f"{item.color_cost or 0:.2f}",
                f"{item.process_cost or 0:.2f}",
            ])

        table1 = Table(table_shape, colWidths=[130, 130, 130, 130])
        elements.append(table1)
        elements.append(Spacer(1, 10))
        table1_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#47b1b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table1.setStyle(table1_style)
        

        table_data = [
            ["Sr. No", "Material", "Area", "Rate","Amount"]
        ]

        table = Table(table_data, colWidths=[20, 50, 30, 30, 30])

        total = 0
        for index, item in enumerate(items, start=1):
            item_total = item.Total or 0
            item_cgst = item_total * Decimal('0.09')
            item_sgst = item_total * Decimal('0.09')
            table_data.append([
                str(index),
                item.material,
                f"{item.area or 0:.2f}",
                f"IND",
                f"Rs.{item_total:.2f}"
            ])
            total = item_total
            cgst = item_cgst * Decimal('0.09')
            sgst = item_sgst * Decimal('0.09')
            grand_total = item_total + item_cgst + item_sgst
            
        table_data.append(['','','','',''])
        table_data.append(['','','','',' '])
        table_data.append(['','','','',' '])
        table_data.append(['', '', '', 'Subtotal', f"{total:.2f}"])
        table_data.append(['', '', '', 'CGST 9%', f"{cgst:.2f}"])
        table_data.append(['', '', '', 'SGST 9%', f"{sgst:.2f}"])
        table_data.append(['', '', '', 'Grand Total', f"{grand_total:.2f}"])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8D6508')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8D6508'))
        ])

        details_table = Table(table_data, colWidths=[50, 250, 50, 100, 100])
        details_table.setStyle(table_style)

        elements.append(details_table)
        elements.append(Spacer(1, 10))

        
        right_align = ParagraphStyle(
        name='Right',
        parent=styles['BodyText'],
        alignment=TA_RIGHT,
        spaceBefore=100, 
        )

        center_style = ParagraphStyle(
        name='Center',
        parent=styles['BodyText'],
        alignment=TA_CENTER,
        )
        

        total_row = Paragraph(f"<b>Grand Total: Rs.{grand_total:.2f}</b>", center_style)
        elements.append(total_row)
        elements.append(Spacer(1, 20))
        
    
        footer_to = Paragraph("""
        <b>Authorized Signature</b>
         """, right_align)

        elements.append(footer_to)
        elements.append(Spacer(1, 20))

        footer_center = Paragraph(
            "<b>Thank You</b>",
            center_style
        )

        elements.append(Spacer(1, 20))
        elements.append(footer_center)

        doc.build(elements)
    
        return response
