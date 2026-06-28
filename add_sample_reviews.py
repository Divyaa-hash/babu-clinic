import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'babuclinic.settings')
django.setup()

from django.conf import settings
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred_path = settings.FIREBASE_CREDENTIALS_PATH
with open(cred_path) as f:
    cred = credentials.Certificate(json.load(f))
firebase_admin.initialize_app(cred)

db = firestore.client()

# Sample reviews
sample_reviews = [
    {
        'patient_name': 'Priya Sharma',
        'rating': 5,
        'review_text': 'Excellent care and very professional staff. Dr. Salman Basha is very knowledgeable and caring.',
        'department': 'General Medicine',
        'created_at': datetime.now().isoformat(),
        'approved': True
    },
    {
        'patient_name': 'Rajesh Kumar',
        'rating': 5,
        'review_text': 'Best clinic in Redhills. The facilities are modern and the doctors are highly experienced.',
        'department': 'Cardiology',
        'created_at': datetime.now().isoformat(),
        'approved': True
    },
    {
        'patient_name': 'Anitha R.',
        'rating': 5,
        'review_text': 'Very good service and affordable prices. Dr. Lakshmipriya provided excellent care during my pregnancy.',
        'department': 'Gynecology',
        'created_at': datetime.now().isoformat(),
        'approved': True
    }
]

# Add reviews to Firebase
for review in sample_reviews:
    db.collection('reviews').add(review)

print('Sample reviews added successfully!')
