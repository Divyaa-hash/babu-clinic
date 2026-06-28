import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'babuclinic.settings')
django.setup()

from firebase_admin import credentials, firestore
from django.conf import settings
import firebase_admin

# Initialize Firebase
cred_path = settings.FIREBASE_CREDENTIALS_PATH
with open(cred_path) as f:
    cred = credentials.Certificate(json.load(f))
firebase_admin.initialize_app(cred)

db = firestore.client()

# Check reviews
docs = db.collection('reviews').where('approved', '==', True).stream()
reviews = [doc.to_dict() for doc in docs]

print('Reviews found:', len(reviews))
for review in reviews:
    print(f"- {review.get('patient_name')}: {review.get('review_text')[:50]}...")
