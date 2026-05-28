from django.db import models
from datetime import datetime
from decimal import Decimal
# Create your models here.

class CustomerInformation(models.Model):
    select_customer = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15,unique=True,blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.gst_number:
            today = datetime.now().strftime("%Y%m%d")
            last_customer = CustomerInformation.objects.order_by('id').last()
            if last_customer:
                last_id = last_customer.id + 1
            else:
                last_id = 1
            self.gst_number = f"KL{today}{last_id:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.select_customer

class JobNumber(models.Model):
    customer = models.ForeignKey(CustomerInformation, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    job_number = models.CharField(max_length=8,unique=True,blank=True)
    date = models.DateField()
    duedate = models.DateField(null=True,blank=True)
    descriptions = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.job_number

    def save(self, *args, **kwargs):
        if not self.job_number:
            last_job = JobNumber.objects.order_by('id').last()
            if last_job:
                last_id = last_job.id + 1
            else:
                last_id = 1
            self.job_number = f"JOB-{last_id:03d}"  
        super().save(*args, **kwargs)

class JobItems(models.Model):
    job_number = models.ForeignKey(JobNumber, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    material_select=[
                        ('EXTRUSION','Aluminium Extrusion(sq.ft)'),
                        ('PROFILE','Aluminium Profile(kg)'),
                        ('SHEET','Aluminium Sheet(Nos)'),
                        ('ROD','Round Aluminium Rod(kg)'),
    ]
    anodisingtype=[
                        ('COLOUR','50-70'),
                        ('HARD','80-120'),
                        ('NATURAL','70-180'),
                        ('TYPE_II','100-150'),
                        ('TYPE_III','75-150'),
    ]
    anodising_RATE={'COLOUR':Decimal(50),'HARD':Decimal(80),'NATURAL':Decimal(70),'TYPE_II':Decimal(100),'TYPE_III':Decimal(75)}
    thickness=[('5-10','5-10µ'),('15-25','15-25µ'),('25-50','25-50µ'),('50+','50µ')] 
    THICKNESS_MULTIPLIER={'5-10':Decimal('1.5'),'15-25':Decimal('1.75'),'25-50':Decimal('2.0'),'50+':Decimal('2.2')}
    color=[('BLACK','5-8'),('BRONZE','6-8'),('CLEAR','0'),('GOLD','8-10'),('SILVER','12-15')]
    color_RATE={'BLACK':Decimal('7'),'BRONZE':Decimal('6'),'CLEAR':Decimal('0'),'GOLD':Decimal('9'),'SILVER':Decimal('13')}
    process=[('DEGREASING','3-5'),('ETCHING','5-8'),('POLISHING','8-10'),('SEALING','2-4'),('TEFLON COATING','10-15')]
    process_RATE={'DEGREASING':Decimal('4'),'ETCHING':Decimal('6'),'POLISHING':Decimal('9'),'SEALING':Decimal('3'),'TEFLON COATING':Decimal('12')}
    material = models.CharField(max_length=100,choices=material_select)
    length = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    width = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    quantity = models.IntegerField()
    area = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    anodising_type = models.CharField(max_length=100,choices=anodisingtype)
    thickness = models.CharField(max_length=20,choices=thickness)
    color_finish = models.CharField(max_length=100,choices=color) 
    process_charges = models.CharField(max_length=20,choices=process)
    base_cost=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    thickness_cost=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    color_cost=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    process_cost=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    Total=models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    
    def get_rate(self, key, data): 
       return dict(data).get(key, 0)
    
    def save(self, *args, **kwargs):
        #area
        from decimal import Decimal
        length = Decimal(str(self.length or 0))
        width = Decimal(str(self.width or 0))
        quantity = Decimal(str(self.quantity or 0))
        self.area = length * width * quantity
        
        #rate
        anodising_rate = self.anodising_RATE.get(self.anodising_type,Decimal('0'))
        multiplier = self.THICKNESS_MULTIPLIER.get(self.thickness, Decimal('1'))
        color_rate= self.color_RATE.get(self.color_finish, Decimal('0'))
        process_rate = self.process_RATE.get(self.process_charges, Decimal('0'))
 
        #calculations
        self.base_cost =self.area * anodising_rate
        self.thickness_cost = self.base_cost * (multiplier- Decimal('1'))
        self.color_cost = color_rate * self.area
        self.process_cost = self.area * process_rate

        #Total Cost
        self.Total = (self.base_cost + self.thickness_cost + self.color_cost + self.process_cost)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.material

class Invoice(models.Model):
    customer=models.ForeignKey(CustomerInformation,on_delete=models.CASCADE,related_name='invoices',null=True,blank=True)
    jobs=models.ForeignKey(JobNumber,on_delete=models.CASCADE,related_name='invoices',null=True,blank=True)
    invoice_no = models.CharField(max_length=15,unique=True,blank=True)
    details = models.ForeignKey(JobItems,on_delete=models.CASCADE,related_name='invoices',null=True,blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date=models.DateField(null=True,blank=True,default=datetime.now)
    
    def calculate_total(self):
        self.gst_amount = self.subtotal * (self.gst_percent / 100)
        self.total = self.subtotal + self.gst_amount - self.discount_amount

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            last_invoice = Invoice.objects.order_by('id').last()
            if last_invoice:
                number = last_invoice.id + 1
            else:
                number = 1
            self.invoice_no = f"INV-{datetime.today().year}{number:03d}"  
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.invoice_no
