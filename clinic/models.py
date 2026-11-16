from django.db import models


class Appointment(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('Online', 'Online'),
        ('Walk-in', 'Walk-in'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('In Consultation', 'In Consultation'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    appointment_id = models.CharField(max_length=20, unique=True)
    token_number = models.CharField(max_length=20)
    patient_name = models.CharField(max_length=200)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200, blank=True, default='')
    address = models.TextField(blank=True, default='')
    doctor = models.CharField(max_length=200)
    appointment_date = models.CharField(max_length=20)
    appointment_time = models.CharField(max_length=20)
    symptoms = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='Online')
    booking_time = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.appointment_id} - {self.patient_name}'


class Review(models.Model):
    patient_name = models.CharField(max_length=200)
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    department = models.CharField(max_length=100, blank=True, default='')
    created_at = models.CharField(max_length=50)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.patient_name} - {self.rating} stars'


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} - {self.phone}'
