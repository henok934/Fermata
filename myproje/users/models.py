import uuid
import random
import string
import qrcode
import base64
from io import BytesIO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# ==========================================
# 1. AUTHENTICATION & ROLE MODELS
# ==========================================


"""
class CustomUser(AbstractUser):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)  # <-- Added City field
    registered_time = models.DateTimeField(auto_now_add=True)
"""


"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
     Acts as the SYSTEM ADMIN and handles Payment Accounts 
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    # ---- አዳዲስ የክፍያ አካውንት ፊልዶች ----
    cbe_account = models.CharField(max_length=25, null=True, blank=True, verbose_name="CBE Account Number")
    telebirr_account = models.CharField(max_length=15, null=True, blank=True, verbose_name="Telebirr Number")
    boa_account = models.CharField(max_length=25, null=True, blank=True, verbose_name="Bank of Abyssinia Account")

    def __str__(self):
        return self.username
"""


import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    cbe_account = models.CharField(max_length=25, null=True, blank=True, verbose_name="CBE Account Number")
    telebirr_account = models.CharField(max_length=15, null=True, blank=True, verbose_name="Telebirr Number")
    boa_account = models.CharField(max_length=25, null=True, blank=True, verbose_name="Bank of Abyssinia Account")

    is_approved = models.BooleanField(default=False, verbose_name="Is Approved/Active")

    def save(self, *args, **kwargs):
        if self.username == 'henok':
            self.is_approved = True
        super(CustomUser, self).save(*args, **kwargs)
    def __str__(self):
        return self.username


class Sc(models.Model):
    """ SHARE COMPANY Admin """
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128) 
    name = models.CharField(max_length=50, null=True, blank=True) # Company Name

    #logo = models.ImageField(upload_files="company_logos/", null=True, blank=True)
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)

    side = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)


"""
class Worker(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField('auth.Group', related_name='worker_set', blank=True)
    worker_permissions = models.ManyToManyField('auth.Permission', related_name='worker_permissions_set', blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
"""


"""
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Worker
class ToggleDriverStatusView(View):
    def post(self, request, pk):
        # Security Guard: Ensure user is logged in via session
        if not request.session.get('user_id'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        # Get the specific worker/driver instance using their primary key (id)
        driver = get_object_or_404(Worker, pk=pk)
        # Toggle the boolean value smoothly
        driver.is_active = not driver.is_active
        driver.save()
        return JsonResponse({
            'success': True,
            'is_active': driver.is_active
        })
"""

import uuid
from django.db import models
from django.contrib.auth.hashers import make_password
class Worker(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)

    # የጠየቅከው አዲስ ፊልድ (ነባሪው False ነው)
    is_active = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='worker_set', blank=True)
    worker_permissions = models.ManyToManyField('auth.Permission', related_name='worker_permissions_set', blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)



# ==========================================
# 2. INFRASTRUCTURE & LOGIC MODELS
# ==========================================

class City(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    depcity = models.CharField(max_length=50, unique=True)


class Bus(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    owner_sc = models.ForeignKey(Sc, on_delete=models.CASCADE, related_name='buses', null=True) # Added null=True
    firstname = models.CharField(max_length=100, null=True, blank=True) # Add this
    lastname = models.CharField(max_length=100, null=True, blank=True)  # Add this
    phone = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    plate_no = models.CharField(max_length=50, unique=True)
    sideno = models.CharField(max_length=50)
    no_seats = models.IntegerField(default=45) # Added default=45
    level = models.CharField(max_length=50, default='Level 1') # Added default

class Route(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    depcity = models.CharField(max_length=50)
    descity = models.CharField(max_length=50)
    kilometer = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=50)
    plate_no = models.CharField(max_length=50)
    side_no = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

class Service_fee(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)

# ==========================================
# 3. TRANSACTIONAL & FEEDBACK MODELS
# ==========================================


"""
import uuid
import random
import string
import qrcode
import base64
from io import BytesIO
from django.db import models
from django.utils import timezone
class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=10, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    passenger_type = models.CharField(max_length=20, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True, default="Guest")
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} - {self.pnr}"

    def save(self, *args, **kwargs):
        # 1. Generate Unique PNR
        if not self.pnr:
            while True:
                new_pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Ticket.objects.filter(pnr=new_pnr).exists():
                    self.pnr = new_pnr
                    break
        
        # 2. Save first to get ID
        super().save(*args, **kwargs)

        # 3. Generate QR Code (only if not already there)
        if not self.qr_code:
            #qr_data = f"PNR: {self.pnr}\nPassenger: {self.firstname} {self.lastname}\nSeat: {self.no_seat}"
            qr_data = (
            f"--- BUSFERMATA DIGITAL TICKET ---\n"
            f"PNR Reference: {self.pnr}\n"
            f"Passenger: {self.firstname} {self.lastname}\n"
            f"Route Path: {self.depcity.upper()} ➔ {self.descity.upper()}\n"
            f"Departure Date: {self.date}\n"
            f"Seat Allocation: {self.no_seat}\n"
            f"---------------------------------"
            )
            qr = qrcode.QRCode(version=1, box_size=5, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            encoded_qr = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()
            
            # Update without triggering save() recursion
            Ticket.objects.filter(pk=self.pk).update(qr_code=encoded_qr)
            self.qr_code = encoded_qr
"""


import base64
import secrets
import string
import uuid
from datetime import timedelta
from io import BytesIO
import qrcode
from django.db import models
from django.utils import timezone
class TicketManager(models.Manager):
    """
    ያልተከፈሉ እና ከተያዙ 30 ደቂቃ ያለፋቸውን ትኬቶች
    በራስ-ሰር የሚያጸዳ Custom Manager።
    """

    def get_queryset(self):
        # ማንኛውም የትኬት ጥያቄ በዳታቤዝ ላይ ሲመጣ ጊዜ ያለፈባቸውን መጀመሪያ ያጠፋል
        expiry_time = timezone.now() - timedelta(minutes=30)
        super().get_queryset().filter(is_paid=False, booked_time__lt=expiry_time).delete()
        return super().get_queryset()

class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=10, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    passenger_type = models.CharField(max_length=20, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True, default="Guest")
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    # Custom ማናጀሩን እዚህ ጋር እናገናኘዋለን
    objects = TicketManager()

    def __str__(self):
        status_label = "Paid" if self.is_paid else "Unpaid"
        return f"{self.firstname} - {self.pnr} ({status_label})"

    def save(self, *args, **kwargs):
        # 1. ዩዘርኔም ካለው እና 'Guest' ካልሆነ በራስ-ሰር Paid (True) ይሆናል
        if not self.pk:
            if self.username and self.username != "Guest":
                self.is_paid = True
            else:
                self.is_paid = False

        # 2. አስተማማኝ PNR ማመንጫ
        if not self.pnr:
            while True:
                alphabet = string.ascii_uppercase + string.digits
                new_pnr = "".join(secrets.choice(alphabet) for _ in range(6))
                if not Ticket.objects.filter(pnr=new_pnr).exists():
                    self.pnr = new_pnr
                    break

        # 3. ትኬቱን ሴቭ ማድረግ
        super().save(*args, **kwargs)

        # 4. QR ኮድ በክፍያ ሁኔታው ላይ ተመስርቶ በዲናሚክ መልኩ ማመንጨት
        dep_city_upper = self.depcity.upper() if self.depcity else ""
        des_city_upper = self.descity.upper() if self.descity else ""
        status_text = "PAID (VALID TICKET)" if self.is_paid else "UNPAID (EXPIRES IN 30 MIN)"

        qr_data = (
            f"--- BUSFERMATA DIGITAL TICKET ---\n"
            f"PNR Reference: {self.pnr}\n"
            f"Ticket Status: {status_text}\n"
            f"Passenger: {self.firstname} {self.lastname}\n"
            f"Route: {dep_city_upper} ➔ {des_city_upper}\n"
            f"Date: {self.date}\n"
            f"Seat: {self.no_seat}\n"
            f"---------------------------------"
        )

        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        encoded_qr = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

        Ticket.objects.filter(pk=self.pk).update(qr_code=encoded_qr)
        self.qr_code = encoded_qr





"""
import uuid
import random
import string
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
import base64

class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=6, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    #username = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True, default="Guest")
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - PNR: {self.pnr} - username: {self.username}"

    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    # CORRECTED INDENTATION: This must be inside the class
    def generate_qr_data(self):
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"PNR: {self.pnr}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Phone: {self.phone}\n"
            f"Departure City: {self.depcity}\n"
            f"Destination City: {self.descity}\n"
            f"Date: {self.date}\n"
            f"No. of Seats: {self.no_seat}\n"
            f"Price: {self.price}\n"
            f"Side No: {self.side_no}\n"
            f"Plate No: {self.plate_no}\n"
            f"Booked Time: {self.booked_time}"
        )

    def generate_qr_code(self):
        data = self.generate_qr_data()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()

        # Save first to ensure we have a ticket_id and a PNR
        super().save(*args, **kwargs)

        # Now generate the QR code using the saved data
        generated_qr = self.generate_qr_code()

        # Use update() to save the qr_code without triggering save() again (avoids recursion)
        self.__class__.objects.filter(ticket_id=self.ticket_id).update(qr_code=generated_qr)
        self.qr_code = generated_qr  # Update current instance
"""





"""
import uuid
import random
import string
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
import base64

class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=6, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - PNR: {self.pnr} - username: {self.username}"

    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    # CORRECTED INDENTATION: This must be inside the class
    def generate_qr_data(self):
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"PNR: {self.pnr}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Phone: {self.phone}\n"
            f"Departure City: {self.depcity}\n"
            f"Destination City: {self.descity}\n"
            f"Date: {self.date}\n"
            f"No. of Seats: {self.no_seat}\n"
            f"Price: {self.price}\n"
            f"Side No: {self.side_no}\n"
            f"Plate No: {self.plate_no}\n"
            f"Booked Time: {self.booked_time}"
        )

    def generate_qr_code(self):
        data = self.generate_qr_data()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()
        
        # Save first to ensure we have a ticket_id and a PNR
        super().save(*args, **kwargs)
        
        # Now generate the QR code using the saved data
        generated_qr = self.generate_qr_code()
        
        # Use update() to save the qr_code without triggering save() again (avoids recursion)
        self.__class__.objects.filter(ticket_id=self.ticket_id).update(qr_code=generated_qr)
        self.qr_code = generated_qr  # Update current instance
"""



"""
import uuid
import random
import string
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
import base64
class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=6, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - PNR: {self.pnr}"

    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    def generate_qr_data(self):
        # This method pulls data from the current instance
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"PNR: {self.pnr}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Phone: {self.phone}\n"
            f"From: {self.depcity} To: {self.descity}\n"
            f"Date: {self.date}\n"
            f"Seat: {self.no_seat}\n"
            f"Price: {self.price} ETB"
        )

    def generate_qr_code(self):
        data = self.generate_qr_data()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()

         # 1. Save the new names to the DB first
        super().save(*args, **kwargs)

        # 2. Generate the QR using the updated names
        new_qr = self.generate_qr_code()

        # 3. Update the instance and the DB record with the NEW QR string
        self.qr_code = new_qr
        Ticket.objects.filter(id=self.id).update(qr_code=new_qr)
"""




class Buschange(models.Model):
    new_side_no = models.CharField(max_length=50)
    new_plate_no = models.CharField(max_length=50)
    depcity = models.CharField(max_length=50)
    descity = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    side_no = models.CharField(max_length=20)
    plate_no = models.CharField(max_length=20)
    groups = models.ManyToManyField('auth.Group', related_name='buschange_set', blank=True)

class Feedback(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField()





"""
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.email} - {self.fname} - {self.lname} - {self.gender} - {self.phone} - {self.registration_id} - {self.registered_time}"



import uuid
from django.db import models
class Feedback(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)  # Increased length for messages

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='feedback_set',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='feedback_permissions_set',  # Unique related name
        blank=True
    )
    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone} - {self.message} - {self.registration_id} - {self.registered_time}"




import uuid
from django.db import models
class Bus(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    plate_no = models.CharField(max_length=50, null=True, blank=True)
    sideno = models.CharField(max_length=50, null=True, blank=True)
    no_seats = models.CharField(max_length=50, null=True, blank=False)
    level = models.CharField(max_length=50, null=False, blank=False, default='unknown')  # Replace 'unknown' with your desired default
    groups = models.ManyToManyField('auth.Group', related_name='bus_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='bus_permissions_set', blank=True)
    def __str__(self):
        return f"{self.plate_no} - {self.sideno} - {self.lastname} {self.firstname} - {self.name} {self.level} - {self.registration_id} - {self.registered_time}"



import uuid
from django.db import models
class City(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='city_set',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='city_permissions_set',  # Unique related name
        blank=True
    )
    def __str__(self):
        return f"{self.depcity} - {self.registration_id} - {self.registered_time}"

import uuid
from django.db import models
class Service_fee(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    service_fee = models.CharField(max_length=50, null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='service_fee_set',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='service_fee_permissions_set',  # Unique related name
        blank=True
    )
    def __str__(self):
        return f"{self.service_fee} - {self.registration_id} - {self.registered_time}"


import uuid
from django.db import models
class Route(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    kilometer = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    plate_no = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)  # Add this line
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='route_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='route_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.depcity} - {self.descity}, {self.plate_no} - {self.side_no} - {self.kilometer} - {self.price} - {self.date} - {self.registration_id} - {self.registered_time} - {self.is_active}"


import uuid
from django.db import models
from django.contrib.auth.hashers import make_password
class Sc(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    side = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sc_set',
        blank=True
    )
    sc_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sc_permissions_set',
        blank=True
    )
    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hash the password
    def __str__(self):
        return f"{self.username} - {self.firstname} - {self.lastname} - {self.gender} - {self.name} - {self.side} - {self.email} - {self.level} - {self.phone} - {self.registration_id} - {self.registered_time}"





import uuid
from django.db import models
class Worker(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password
    #side_no = models.CharField(max_length=50, null=True, blank=True)
    #plate_no = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='worker_set',
        blank=True
    )
    worker_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='worker_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.username} - {self.fname} - {self.lname} - {self.gender} - {self.phone} - {self.city}  - {self.registration_id} - {self.registered_time}"


from django.contrib.auth.models import AbstractUser
from django.db import models
class Admin(models.Model):
    #id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    registered_time = models.DateTimeField(auto_now_add=True)


    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_set',
        blank=True
    )
    admin_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_permissions_set',
        blank=True
    )

    def formatted_registered_time(self):
        # Convert registered_time to the current timezone
        local_registered_time = self.registered_time.astimezone(timezone.get_current_timezone())
        return local_registered_time.strftime('%m,%d,%Y %I:%M %p')

    def save(self, *args, **kwargs):
        # Populate date and time components before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.fname} - {self.lname} - {self.gender} - {self.password} - {self.phone} - {self.registration_id} - {self.registered_time}"


import uuid
import random
import string
import qrcode
import base64
from io import BytesIO
from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=6, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - PNR: {self.pnr}"

    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    def generate_qr_data(self):
        # This method pulls data from the current instance
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"PNR: {self.pnr}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Phone: {self.phone}\n"
            f"From: {self.depcity} To: {self.descity}\n"
            f"Date: {self.date}\n"
            f"Seat: {self.no_seat}\n"
            f"Price: {self.price} ETB"
        )

    def generate_qr_code(self):
        data = self.generate_qr_data()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()
        
        # 1. Save the new names to the DB first
        super().save(*args, **kwargs)
        
        # 2. Generate the QR using the updated names
        new_qr = self.generate_qr_code()
        
        # 3. Update the instance and the DB record with the NEW QR string
        self.qr_code = new_qr
        Ticket.objects.filter(id=self.id).update(qr_code=new_qr)











import uuid
import random
import string
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
import base64
class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=6, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - PNR: {self.pnr} - username: {self.username}"
    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    def generate_qr_data(self):
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"PNR: {self.pnr}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Phone: {self.phone}\n"
            f"Departure City: {self.depcity}\n"
            f"Destination City: {self.descity}\n"
            f"Date: {self.date}\n"
            f"No. of Seats: {self.no_seat}\n"
            f"Price: {self.price}\n"
            f"Side No: {self.side_no}\n"
            f"Plate No: {self.plate_no}\n"
            f"Booked Time: {self.booked_time}"
        )

    def generate_qr_code(self):
        data = self.generate_qr_data()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_code = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()
        
        return qr_code

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()

        super().save(*args, **kwargs)
        self.qr_code = self.generate_qr_code()
        self.__class__.objects.filter(ticket_id=self.ticket_id).update(qr_code=self.qr_code)






class Buschange(models.Model):
    new_side_no = models.CharField(max_length=50, null=True, blank=True)
    new_plate_no = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='buschange_set',
        blank=True
    )
    buschange_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='buschange_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.depcity} - {self.descity}, {self.new_side_no} - {self.new_plate_no}, - {self.plate_no} - {self.side_no} - {self.date}"
from django.db import models

class Buschange(models.Model):
    new_side_no = models.CharField(max_length=50, null=True, blank=True)
    new_plate_no = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='buschange_set',
        blank=True
    )
    buschange_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='buschange_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.depcity} - {self.descity}, {self.new_side_no} - {self.new_plate_no}, - {self.plate_no} - {self.side_no} - {self.date}"

"""
