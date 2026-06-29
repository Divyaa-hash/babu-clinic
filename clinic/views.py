"""
Views for babuclinic application.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

# Initialize Firebase
try:
    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        # Initialize without credentials for development
        firebase_admin.initialize_app()
    db = firestore.client()
except Exception as e:
    print(f"Firebase initialization error: {e}")
    db = None

# Function to send SMS notification
def send_sms_notification(phone_number, message):
    """Send SMS notification using Twilio"""
    try:
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return True
        else:
            print("Twilio credentials not configured")
            return False
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

# Clinic Information
CLINIC_INFO = {
    'name': 'BABU SUPER SPECIALITY CLINIC',
    'tagline': 'Your Health is Our Priority',
    'address': 'No. 84/3, TVK Street, Redhills, Chennai – 600052 (Kalyan Jewels Back Side)',
    'phone': '7305493125',
    'email': 'babusuperspecialityclinic@gmail.com',
}

# Doctors Data
DOCTORS_DATA = [
    {
        'id': 'dr-salman',
        'name': 'Dr. Salman Basha',
        'qualification': 'MBBS, FIDM',
        'specialization': 'Family & General Physician',
        'description': 'Experienced Family Physician providing comprehensive healthcare, preventive medicine, routine checkups, diagnosis, and treatment for patients of all ages.',
        'image': 'doctor1.jpg'
    },
    {
        'id': 'dr-senthil',
        'name': 'Dr. Senthil Kumar',
        'qualification': 'MBBS, MD, PGDip in Diabetology',
        'designation': 'Senior Consultant',
        'specialization': 'General Medicine & Diabetologist',
        'description': 'Specialist in Diabetes, Hypertension, Thyroid Disorders, General Medicine, and Lifestyle Disease Management.',
        'image': 'doctor2.jpg'
    },
    {
        'id': 'dr-shanmugam',
        'name': 'Dr. Shanmugam',
        'qualification': 'MBBS, MS, MCh, PG Dip',
        'specialization': 'Plastic Surgeon & Gastroenterology',
        'description': 'Experienced surgeon specializing in Plastic Surgery and Gastroenterology with advanced surgical expertise.',
        'image': 'doctor3.jpg'
    },
    {
        'id': 'dr-aswin',
        'name': 'Dr. Aswin S. Krishna',
        'qualification': 'MBBS, MD, DM',
        'designation': 'Senior Consultant',
        'specialization': 'Transplant Hematologist',
        'description': 'Expert in Blood Disorders, Bone Marrow Transplantation, Leukemia, Lymphoma, and Advanced Hematology Care.',
        'image': 'doctor4.jpg'
    },
    {
        'id': 'dr-lakshmipriya',
        'name': 'Dr. Lakshmipriya',
        'qualification': 'MBBS, MS (OBG)',
        'specialization': 'Gynecologist & Infertility Specialist',
        'description': 'Experienced Women\'s Health Specialist providing pregnancy care, infertility treatment, and complete gynecological services.',
        'image': 'doctor5.jpg'
    }
]

# Departments
DEPARTMENTS = [
    {'name': 'Gynecology', 'icon': 'fa-heartbeat', 'color': '#e91e63'},
    {'name': 'Dermatology', 'icon': 'fa-hand-sparkles', 'color': '#9c27b0'},
    {'name': 'General Medicine', 'icon': 'fa-stethoscope', 'color': '#2196f3'},
    {'name': 'Diabetology', 'icon': 'fa-droplet', 'color': '#f44336'},
    {'name': 'Cardiology', 'icon': 'fa-heart', 'color': '#e91e63'},
    {'name': 'Neurology', 'icon': 'fa-brain', 'color': '#673ab7'},
    {'name': 'ENT', 'icon': 'fa-ear-listen', 'color': '#ff9800'},
    {'name': 'Paediatrics', 'icon': 'fa-baby', 'color': '#4caf50'},
]

# Facilities
FACILITIES = [
    {'name': 'Lab Testing', 'icon': 'fa-flask', 'color': '#2196f3'},
    {'name': 'Pharmacy', 'icon': 'fa-pills', 'color': '#4caf50'},
    {'name': 'Ultra Sound Scan', 'icon': 'fa-wave-square', 'color': '#9c27b0'},
    {'name': 'ECHO', 'icon': 'fa-heart-pulse', 'color': '#e91e63'},
    {'name': 'ECG', 'icon': 'fa-heartbeat', 'color': '#f44336'},
    {'name': 'Daycare Services', 'icon': 'fa-bed', 'color': '#ff9800'},
]

# Why Choose Us
WHY_CHOOSE_US = [
    {'title': 'Experienced Doctors', 'icon': 'fa-user-doctor', 'description': 'Highly qualified specialists with years of experience'},
    {'title': 'Complete Multi-Speciality Healthcare', 'icon': 'fa-hospital', 'description': 'Comprehensive medical services under one roof'},
    {'title': 'Modern Equipment', 'icon': 'fa-microscope', 'description': 'State-of-the-art medical technology'},
    {'title': 'Affordable Consultation', 'icon': 'fa-hand-holding-dollar', 'description': 'Quality healthcare at reasonable prices'},
    {'title': 'Pharmacy Available', 'icon': 'fa-prescription-bottle', 'description': 'In-house pharmacy for your convenience'},
    {'title': 'Friendly Staff', 'icon': 'fa-face-smile', 'description': 'Caring and supportive medical team'},
    {'title': 'Emergency Care', 'icon': 'fa-truck-medical', 'description': '24/7 emergency medical services'},
    {'title': 'Patient First Approach', 'icon': 'fa-users', 'description': 'Patient-centered care philosophy'},
]

# Patient Reviews
REVIEWS = [
    {
        'name': 'Priya Sharma',
        'rating': 5,
        'text': 'Excellent care and very professional staff. Dr. Salman Basha is very knowledgeable and caring.',
        'department': 'General Medicine'
    },
    {
        'name': 'Rajesh Kumar',
        'rating': 5,
        'text': 'Best clinic in Redhills. The facilities are modern and the doctors are highly experienced.',
        'department': 'Cardiology'
    },
    {
        'name': 'Anitha R.',
        'rating': 4,
        'text': 'Very good service and affordable prices. Dr. Lakshmipriya provided excellent care during my pregnancy.',
        'department': 'Gynecology'
    },
    {
        'name': 'Suresh Babu',
        'rating': 5,
        'text': 'The diabetes management program here is excellent. Dr. Senthil Kumar is very thorough.',
        'department': 'Diabetology'
    },
]


def home(request):
    """Home page view"""
    context = {
        'clinic': CLINIC_INFO,
        'departments': DEPARTMENTS,
        'facilities': FACILITIES,
        'why_choose_us': WHY_CHOOSE_US,
        'reviews': REVIEWS,
        'page_title': f'{CLINIC_INFO["name"]} | {CLINIC_INFO["tagline"]}',
        'page_description': f'{CLINIC_INFO["name"]} offers expert healthcare services at {CLINIC_INFO["address"]}. Call {CLINIC_INFO["phone"]}.',
    }
    return render(request, 'clinic/home.html', context)


def about(request):
    """About page view"""
    context = {
        'clinic': CLINIC_INFO,
        'page_title': f'About Us - {CLINIC_INFO["name"]}',
        'page_description': f'Learn about {CLINIC_INFO["name"]} - {CLINIC_INFO["tagline"]}. Our mission, vision, and values.',
    }
    return render(request, 'clinic/about.html', context)


def doctors(request):
    """Doctors page view"""
    context = {
        'clinic': CLINIC_INFO,
        'doctors': DOCTORS_DATA,
        'page_title': f'Our Doctors - {CLINIC_INFO["name"]}',
        'page_description': f'Meet our expert doctors at {CLINIC_INFO["name"]}. Highly qualified specialists.',
    }
    return render(request, 'clinic/doctors.html', context)


def appointment(request):
    """Appointment booking page view"""
    context = {
        'clinic': CLINIC_INFO,
        'doctors': DOCTORS_DATA,
        'page_title': f'Book Appointment - {CLINIC_INFO["name"]}',
        'page_description': f'Book an appointment with our doctors at {CLINIC_INFO["name"]}. Call {CLINIC_INFO["phone"]}.',
    }
    return render(request, 'clinic/appointment.html', context)


def contact(request):
    """Contact page view"""
    context = {
        'clinic': CLINIC_INFO,
        'page_title': f'Contact Us - {CLINIC_INFO["name"]}',
        'page_description': f'Contact {CLINIC_INFO["name"]} at {CLINIC_INFO["address"]}. Phone: {CLINIC_INFO["phone"]}.',
    }
    return render(request, 'clinic/contact.html', context)


@csrf_exempt
def api_appointment(request):
    """API endpoint for appointment booking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['patient_name', 'age', 'gender', 'phone', 'email', 'doctor', 'appointment_date', 'appointment_time']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'success': False, 'error': f'{field} is required'}, status=400)
            
            # Generate appointment ID and token number
            appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
            token_number = f"TKN-{uuid.uuid4().hex[:6].upper()}"
            
            # Prepare appointment data
            appointment_data = {
                'appointment_id': appointment_id,
                'token_number': token_number,
                'patient_name': data['patient_name'],
                'age': data['age'],
                'gender': data['gender'],
                'phone': data['phone'],
                'email': data['email'],
                'address': data.get('address', ''),
                'doctor': data['doctor'],
                'appointment_date': data['appointment_date'],
                'appointment_time': data['appointment_time'],
                'symptoms': data.get('symptoms', ''),
                'notes': data.get('notes', ''),
                'status': 'Pending',
                'booking_type': 'Online',
                'booking_time': datetime.now().isoformat(),
            }
            
            # Save to Firebase
            if db:
                db.collection('appointments').add(appointment_data)
            
            return JsonResponse({'success': True, 'message': 'Appointment booked successfully!', 'appointment_id': appointment_id, 'token_number': token_number})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_contact(request):
    """API endpoint for contact form"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'phone', 'email', 'message']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'success': False, 'error': f'{field} is required'}, status=400)
            
            # Prepare contact data
            contact_data = {
                'name': data['name'],
                'phone': data['phone'],
                'email': data['email'],
                'message': data['message'],
                'submitted_at': datetime.now().isoformat(),
            }
            
            # Save to Firebase
            if db:
                db.collection('contact_messages').add(contact_data)
            
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_submit_review(request):
    """API endpoint to submit patient reviews"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            review_data = {
                'patient_name': data.get('patient_name', ''),
                'rating': int(data.get('rating', 5)),
                'review_text': data.get('review_text', ''),
                'department': data.get('department', ''),
                'created_at': datetime.now().isoformat(),
                'approved': True  # Auto-approve for immediate display
            }
            
            # Save to Firebase
            if db:
                db.collection('reviews').add(review_data)
            
            return JsonResponse({'success': True, 'message': 'Review submitted successfully! Your review is now visible.'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_get_reviews(request):
    """API endpoint to get approved patient reviews"""
    if request.method == 'GET':
        try:
            reviews = []
            if db:
                docs = db.collection('reviews').where('approved', '==', True).stream()
                for doc in docs:
                    review = doc.to_dict()
                    review['id'] = doc.id
                    reviews.append(review)
            
            return JsonResponse({'success': True, 'reviews': reviews})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required(login_url='/admin-login/')
def admin_appointments(request):
    """Admin appointment history page"""
    context = {
        'clinic': CLINIC_INFO,
        'page_title': 'Admin - Appointments',
        'page_description': 'Manage all appointments',
    }
    return render(request, 'clinic/admin_appointments.html', context)


@login_required(login_url='/admin-login/')
def walkin_appointment(request):
    """Walk-in appointment page for clinic staff"""
    context = {
        'clinic': CLINIC_INFO,
        'doctors': DOCTORS_DATA,
        'page_title': 'Walk-in Appointment',
        'page_description': 'Register walk-in patients',
    }
    return render(request, 'clinic/walkin_appointment.html', context)


def track_appointment(request):
    """Track appointment page for patients"""
    context = {
        'clinic': CLINIC_INFO,
        'page_title': 'Track Appointment',
        'page_description': 'Check your appointment status',
    }
    return render(request, 'clinic/track_appointment.html', context)


@csrf_exempt
def api_track_appointment(request):
    """API endpoint for patients to track their appointment"""
    if request.method == 'GET':
        try:
            appointment_id = request.GET.get('appointment_id', '')
            phone_number = request.GET.get('phone_number', '')
            
            if not appointment_id and not phone_number:
                return JsonResponse({'success': False, 'error': 'Appointment ID or Phone Number is required'}, status=400)
            
            # Query Firebase for matching appointment
            appointment = None
            if db:
                if appointment_id:
                    docs = db.collection('appointments').where('appointment_id', '==', appointment_id).stream()
                    for doc in docs:
                        appointment = doc.to_dict()
                        appointment['firebase_id'] = doc.id
                        break
                elif phone_number:
                    docs = db.collection('appointments').where('phone', '==', phone_number).stream()
                    for doc in docs:
                        appointment = doc.to_dict()
                        appointment['firebase_id'] = doc.id
                        break
            
            if appointment:
                return JsonResponse({'success': True, 'appointment': appointment})
            else:
                return JsonResponse({'success': False, 'error': 'No appointment found'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_walkin_appointment(request):
    """API endpoint for walk-in appointment registration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['patient_name', 'age', 'gender', 'phone', 'doctor', 'appointment_date', 'appointment_time']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'success': False, 'error': f'{field} is required'}, status=400)
            
            # Generate appointment ID and token number
            appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
            token_number = f"TKN-{uuid.uuid4().hex[:6].upper()}"
            
            # Prepare appointment data
            appointment_data = {
                'appointment_id': appointment_id,
                'token_number': token_number,
                'patient_name': data['patient_name'],
                'age': data['age'],
                'gender': data['gender'],
                'phone': data['phone'],
                'email': data.get('email', ''),
                'address': data.get('address', ''),
                'doctor': data['doctor'],
                'appointment_date': data['appointment_date'],
                'appointment_time': data['appointment_time'],
                'symptoms': data.get('symptoms', ''),
                'notes': data.get('notes', ''),
                'status': 'Pending',
                'booking_type': 'Walk-in',
                'booking_time': datetime.now().isoformat(),
            }
            
            # Save to Firebase
            if db:
                db.collection('appointments').add(appointment_data)
            
            return JsonResponse({
                'success': True, 
                'message': 'Walk-in appointment registered successfully!',
                'appointment_id': appointment_id,
                'token_number': token_number
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_get_appointments(request):
    """API endpoint to get all appointments with filters"""
    if request.method == 'GET':
        try:
            # Get filter parameters
            booking_type = request.GET.get('booking_type', '')
            status = request.GET.get('status', '')
            date = request.GET.get('date', '')
            doctor = request.GET.get('doctor', '')
            
            # Query Firebase
            appointments = []
            if db:
                query = db.collection('appointments')
                
                # Apply filters
                if booking_type:
                    query = query.where('booking_type', '==', booking_type)
                if status:
                    query = query.where('status', '==', status)
                if date:
                    query = query.where('appointment_date', '==', date)
                if doctor:
                    query = query.where('doctor', '==', doctor)
                
                docs = query.stream()
                for doc in docs:
                    appointment = doc.to_dict()
                    appointment['firebase_id'] = doc.id
                    appointments.append(appointment)
            
            return JsonResponse({'success': True, 'appointments': appointments})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_appointment_statistics(request):
    """API endpoint to get appointment statistics"""
    if request.method == 'GET':
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            statistics = {
                'total_online': 0,
                'total_walkin': 0,
                'today_online': 0,
                'today_walkin': 0,
                'total': 0,
                'today': 0,
                'pending': 0,
                'confirmed': 0,
                'in_consultation': 0,
                'completed': 0,
                'cancelled': 0,
            }
            
            if db:
                # Get all appointments
                docs = db.collection('appointments').stream()
                for doc in docs:
                    appointment = doc.to_dict()
                    statistics['total'] += 1
                    
                    # Count by booking type
                    if appointment.get('booking_type') == 'Online':
                        statistics['total_online'] += 1
                        if appointment.get('appointment_date') == today:
                            statistics['today_online'] += 1
                            statistics['today'] += 1
                    elif appointment.get('booking_type') == 'Walk-in':
                        statistics['total_walkin'] += 1
                        if appointment.get('appointment_date') == today:
                            statistics['today_walkin'] += 1
                            statistics['today'] += 1
                    
                    # Count by status
                    status = appointment.get('status', '').lower()
                    if status == 'pending':
                        statistics['pending'] += 1
                    elif status == 'confirmed':
                        statistics['confirmed'] += 1
                    elif status == 'in consultation':
                        statistics['in_consultation'] += 1
                    elif status == 'completed':
                        statistics['completed'] += 1
                    elif status == 'cancelled':
                        statistics['cancelled'] += 1
            
            return JsonResponse({'success': True, 'statistics': statistics})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_update_appointment_status(request):
    """API endpoint to update appointment status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')
            new_status = data.get('status')
            
            if not appointment_id or not new_status:
                return JsonResponse({'success': False, 'error': 'Appointment ID and Status are required'}, status=400)
            
            # Get appointment details for SMS notification
            appointment_data = None
            if db:
                doc = db.collection('appointments').document(appointment_id).get()
                if doc.exists:
                    appointment_data = doc.to_dict()
            
            # Update in Firebase
            if db:
                db.collection('appointments').document(appointment_id).update({
                    'status': new_status
                })
            
            # Send SMS notification when status is confirmed
            if new_status == 'Confirmed' and appointment_data:
                phone_number = appointment_data.get('phone', '')
                patient_name = appointment_data.get('patient_name', '')
                appointment_date = appointment_data.get('appointment_date', '')
                appointment_time = appointment_data.get('appointment_time', '')
                
                message = f"Dear {patient_name}, Your appointment at BABU SUPER SPECIALITY CLINIC has been confirmed for {appointment_date} at {appointment_time}. Please arrive 15 minutes early. For queries: 7305493125"
                
                if phone_number:
                    send_sms_notification(phone_number, message)
            
            return JsonResponse({'success': True, 'message': 'Status updated successfully'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_delete_appointment(request):
    """API endpoint to delete appointment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')
            
            if not appointment_id:
                return JsonResponse({'success': False, 'error': 'Appointment ID is required'}, status=400)
            
            # Delete from Firebase
            if db:
                db.collection('appointments').document(appointment_id).delete()
            
            return JsonResponse({'success': True, 'message': 'Appointment deleted successfully'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_get_doctor_department(request):
    """API endpoint to get doctor department"""
    if request.method == 'GET':
        try:
            doctor_name = request.GET.get('doctor_name', '')
            
            # Find doctor in DOCTORS_DATA
            department = 'General Medicine'
            for doctor in DOCTORS_DATA:
                if doctor['name'] == doctor_name:
                    department = doctor['specialization']
                    break
            
            return JsonResponse({'success': True, 'department': department})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_export_appointments_pdf(request):
    """API endpoint to export all appointments as PDF"""
    if request.method == 'GET':
        try:
            # Get filter parameters
            booking_type = request.GET.get('booking_type', '')
            
            # Fetch appointments from Firebase
            appointments = []
            if db:
                query = db.collection('appointments')
                if booking_type:
                    query = query.where('booking_type', '==', booking_type)
                
                docs = query.stream()
                for doc in docs:
                    appointment = doc.to_dict()
                    appointment['id'] = doc.id
                    appointments.append(appointment)
            
            # Create PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="appointments_report.pdf"'
            
            doc = SimpleDocTemplate(response, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Add clinic logo and header
            try:
                logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'logo.png')
                if os.path.exists(logo_path):
                    logo = Image(logo_path, width=1*inch, height=1*inch)
                    elements.append(logo)
            except:
                pass
            
            # Clinic name and address
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#2c3e50'),
                alignment=1
            )
            
            elements.append(Paragraph("BABU SUPER SPECIALITY CLINIC", title_style))
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(CLINIC_INFO['address'], styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Create table
            table_data = [
                ['Appointment ID', 'Token', 'Patient Name', 'Doctor', 'Phone', 'Type', 'Date', 'Time', 'Status']
            ]
            
            for apt in appointments:
                table_data.append([
                    apt.get('appointment_id', 'N/A'),
                    apt.get('token_number', 'N/A'),
                    apt.get('patient_name', 'N/A'),
                    apt.get('doctor', 'N/A'),
                    apt.get('phone', 'N/A'),
                    apt.get('booking_type', 'N/A'),
                    apt.get('appointment_date', 'N/A'),
                    apt.get('appointment_time', 'N/A'),
                    apt.get('status', 'N/A')
                ])
            
            table = Table(table_data, colWidths=[0.8*inch, 0.7*inch, 1.2*inch, 1.0*inch, 0.8*inch, 0.6*inch, 0.8*inch, 0.6*inch, 0.7*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
            
            # Total count
            elements.append(Paragraph(f"Total Appointments: {len(appointments)}", styles['Normal']))
            
            doc.build(elements)
            return response
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_export_single_appointment_pdf(request):
    """API endpoint to export single appointment as PDF"""
    if request.method == 'GET':
        try:
            appointment_id = request.GET.get('appointment_id', '')
            
            if not appointment_id:
                return JsonResponse({'success': False, 'error': 'Appointment ID is required'}, status=400)
            
            # Fetch appointment from Firebase
            appointment = None
            if db:
                docs = db.collection('appointments').where('appointment_id', '==', appointment_id).stream()
                for doc in docs:
                    appointment = doc.to_dict()
                    break
            
            if not appointment:
                return JsonResponse({'success': False, 'error': 'Appointment not found'}, status=404)
            
            # Create PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="appointment_{appointment_id}.pdf"'
            
            doc = SimpleDocTemplate(response, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Add clinic logo
            try:
                logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'logo.png')
                if os.path.exists(logo_path):
                    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
                    elements.append(logo)
            except:
                pass
            
            # Clinic name
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#2c3e50'),
                alignment=1
            )
            
            elements.append(Paragraph("BABU SUPER SPECIALITY CLINIC", title_style))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("APPOINTMENT RECEIPT", title_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Appointment details table
            details_data = [
                ['Field', 'Value'],
                ['Patient Name', appointment.get('patient_name', 'N/A')],
                ['Appointment ID', appointment.get('appointment_id', 'N/A')],
                ['Token Number', appointment.get('token_number', 'N/A')],
                ['Doctor Name', appointment.get('doctor', 'N/A')],
                ['Appointment Date', appointment.get('appointment_date', 'N/A')],
                ['Appointment Time', appointment.get('appointment_time', 'N/A')],
                ['Booking Type', appointment.get('booking_type', 'N/A')],
                ['Status', appointment.get('status', 'N/A')],
                ['Phone Number', appointment.get('phone', 'N/A')],
                ['Symptoms', appointment.get('symptoms', 'N/A')],
                ['Booking Date', appointment.get('booking_time', 'N/A')],
            ]
            
            details_table = Table(details_data, colWidths=[2*inch, 3*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            elements.append(details_table)
            elements.append(Spacer(1, 0.4*inch))
            
            # Footer
            footer_style = ParagraphStyle(
                'CustomFooter',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#2c3e50'),
                alignment=1
            )
            elements.append(Paragraph("Thank you for choosing BABU SUPER SPECIALITY CLINIC.", footer_style))
            
            doc.build(elements)
            return response
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

# Admin Authentication Views
def admin_login(request):
    """Admin login page"""
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid Username or Password.'
    
    return render(request, 'clinic/admin_login.html', {'error': error})

@login_required(login_url='/admin-login/')
def admin_logout(request):
    """Admin logout"""
    logout(request)
    return redirect('home')

@login_required(login_url='/admin-login/')
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    if not db:
        return render(request, 'clinic/admin_dashboard.html', {
            'error': 'Firebase connection not available'
        })
    
    try:
        # Get all appointments
        appointments_ref = db.collection('appointments')
        appointments = appointments_ref.get()
        
        total_appointments = len(list(appointments))
        
        # Get today's appointments
        today = datetime.now().strftime('%Y-%m-%d')
        today_ref = db.collection('appointments').where('date', '==', today)
        today_appointments = len(list(today_ref.get()))
        
        # Get online vs walk-in
        online_ref = db.collection('appointments').where('booking_type', '==', 'Online')
        online_appointments = len(list(online_ref.get()))
        
        walkin_ref = db.collection('appointments').where('booking_type', '==', 'Walk-in')
        walkin_appointments = len(list(walkin_ref.get()))
        
        # Get status counts
        pending_ref = db.collection('appointments').where('status', '==', 'Pending')
        pending_count = len(list(pending_ref.get()))
        
        confirmed_ref = db.collection('appointments').where('status', '==', 'Confirmed')
        confirmed_count = len(list(confirmed_ref.get()))
        
        in_consultation_ref = db.collection('appointments').where('status', '==', 'In Consultation')
        in_consultation_count = len(list(in_consultation_ref.get()))
        
        completed_ref = db.collection('appointments').where('status', '==', 'Completed')
        completed_count = len(list(completed_ref.get()))
        
        cancelled_ref = db.collection('appointments').where('status', '==', 'Cancelled')
        cancelled_count = len(list(cancelled_ref.get()))
        
        # Total doctors
        total_doctors = len(DOCTORS_DATA)
        
        context = {
            'total_appointments': total_appointments,
            'today_appointments': today_appointments,
            'online_appointments': online_appointments,
            'walkin_appointments': walkin_appointments,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'in_consultation_count': in_consultation_count,
            'completed_count': completed_count,
            'cancelled_count': cancelled_count,
            'total_doctors': total_doctors,
        }
        
        return render(request, 'clinic/admin_dashboard.html', context)
        
    except Exception as e:
        return render(request, 'clinic/admin_dashboard.html', {
            'error': f'Error fetching data: {str(e)}'
        })

@login_required(login_url='/admin-login/')
def admin_reports(request):
    """Admin reports page for exporting appointment data"""
    return render(request, 'clinic/admin_reports.html')
