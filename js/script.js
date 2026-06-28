// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functions
    initAnimations();
    initFormValidation();
    initScrollEffects();
    initMobileMenu();
    initAppointmentForm();
    initSearchFunctionality();
});

// Animation on scroll
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.service-card, .specialty-card, .feature-card, .doctor-card, .package-card, .testimonial-card');
    animateElements.forEach(el => observer.observe(el));
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Scroll effects
function initScrollEffects() {
    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = 'white';
            navbar.style.backdropFilter = 'none';
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Mobile menu functionality
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInside = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
            if (!isClickInside && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }
}

// Appointment form functionality
function initAppointmentForm() {
    const appointmentForm = document.getElementById('appointmentForm');
    const doctorSelect = document.getElementById('doctorSelect');
    const departmentSelect = document.getElementById('departmentSelect');
    const dateInput = document.getElementById('appointmentDate');

    if (appointmentForm) {
        appointmentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(appointmentForm);
            const appointmentData = {
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                doctor: formData.get('doctor'),
                department: formData.get('department'),
                date: formData.get('date'),
                time: formData.get('time'),
                message: formData.get('message')
            };

            // Validate form data
            if (validateAppointmentData(appointmentData)) {
                submitAppointment(appointmentData);
            }
        });
    }

    // Filter doctors based on department
    if (departmentSelect && doctorSelect) {
        departmentSelect.addEventListener('change', function() {
            filterDoctorsByDepartment(this.value);
        });
    }

    // Set minimum date to today
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
}

// Validate appointment data
function validateAppointmentData(data) {
    let isValid = true;
    const errors = [];

    // Name validation
    if (!data.name || data.name.trim().length < 2) {
        errors.push('Please enter a valid name');
        isValid = false;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!data.email || !emailRegex.test(data.email)) {
        errors.push('Please enter a valid email address');
        isValid = false;
    }

    // Phone validation
    const phoneRegex = /^[0-9]{10}$/;
    if (!data.phone || !phoneRegex.test(data.phone.replace(/[-\s]/g, ''))) {
        errors.push('Please enter a valid 10-digit phone number');
        isValid = false;
    }

    // Doctor validation
    if (!data.doctor) {
        errors.push('Please select a doctor');
        isValid = false;
    }

    // Date validation
    if (!data.date) {
        errors.push('Please select an appointment date');
        isValid = false;
    } else {
        const selectedDate = new Date(data.date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            errors.push('Appointment date cannot be in the past');
            isValid = false;
        }
    }

    // Time validation
    if (!data.time) {
        errors.push('Please select an appointment time');
        isValid = false;
    }

    if (!isValid) {
        showFormErrors(errors);
    }

    return isValid;
}

// Show form errors
function showFormErrors(errors) {
    const errorContainer = document.getElementById('formErrors');
    if (errorContainer) {
        errorContainer.innerHTML = '';
        errorContainer.classList.remove('d-none');
        
        errors.forEach(error => {
            const errorElement = document.createElement('div');
            errorElement.className = 'alert alert-danger';
            errorElement.textContent = error;
            errorContainer.appendChild(errorElement);
        });

        // Scroll to error container
        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Hide errors after 5 seconds
        setTimeout(() => {
            errorContainer.classList.add('d-none');
        }, 5000);
    }
}

// Submit appointment
function submitAppointment(data) {
    // Show loading state
    const submitButton = document.querySelector('#appointmentForm button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Booking...';

    // Simulate API call
    setTimeout(() => {
        // Show success message
        showSuccessMessage('Appointment booked successfully! We will contact you soon.');
        
        // Reset form
        document.getElementById('appointmentForm').reset();
        
        // Reset button
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }, 2000);
}

// Show success message
function showSuccessMessage(message) {
    const successContainer = document.getElementById('successMessage');
    if (successContainer) {
        successContainer.innerHTML = `<div class="alert alert-success">${message}</div>`;
        successContainer.classList.remove('d-none');
        
        // Scroll to success message
        successContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Hide message after 5 seconds
        setTimeout(() => {
            successContainer.classList.add('d-none');
        }, 5000);
    }
}

// Filter doctors by department
function filterDoctorsByDepartment(department) {
    const doctorSelect = document.getElementById('doctorSelect');
    if (!doctorSelect) return;

    // Doctor data (in real application, this would come from API)
    const doctors = {
        'cardiology': [
            { id: 'dr-ramesh', name: 'Dr. Ramesh Babu' },
            { id: 'dr-vidya', name: 'Dr. Vidya Sagar' }
        ],
        'neurology': [
            { id: 'dr-priya', name: 'Dr. Priya Nair' },
            { id: 'dr-karthik', name: 'Dr. Karthik Ramesh' }
        ],
        'orthopedics': [
            { id: 'dr-arjun', name: 'Dr. Arjun Kumar' },
            { id: 'dr-meera', name: 'Dr. Meera Krishnan' }
        ],
        'gynecology': [
            { id: 'dr-sneha', name: 'Dr. Sneha Reddy' },
            { id: 'dr-anita', name: 'Dr. Anita Desai' }
        ],
        'pediatrics': [
            { id: 'dr-rahul', name: 'Dr. Rahul Menon' },
            { id: 'dr-nisha', name: 'Dr. Nisha Patel' }
        ]
    };

    // Clear existing options
    doctorSelect.innerHTML = '<option value="">Select a doctor</option>';

    // Add doctors based on selected department
    if (department && doctors[department]) {
        doctors[department].forEach(doctor => {
            const option = document.createElement('option');
            option.value = doctor.id;
            option.textContent = doctor.name;
            doctorSelect.appendChild(option);
        });
    }

    // Enable/disable doctor select
    doctorSelect.disabled = !department;
}

// Search functionality
function initSearchFunctionality() {
    const searchInput = document.getElementById('doctorSearch');
    const searchResults = document.getElementById('searchResults');

    if (searchInput && searchResults) {
        let searchTimeout;

        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();

            if (query.length < 2) {
                searchResults.classList.add('d-none');
                return;
            }

            // Debounce search
            searchTimeout = setTimeout(() => {
                searchDoctors(query);
            }, 300);
        });

        // Close search results when clicking outside
        document.addEventListener('click', function(event) {
            if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
                searchResults.classList.add('d-none');
            }
        });
    }
}

// Search doctors
function searchDoctors(query) {
    const searchResults = document.getElementById('searchResults');
    if (!searchResults) return;

    // Mock doctor data (in real application, this would be an API call)
    const doctors = [
        { id: 'dr-ramesh', name: 'Dr. Ramesh Babu', specialty: 'Cardiology', experience: '15+ years' },
        { id: 'dr-priya', name: 'Dr. Priya Nair', specialty: 'Neurology', experience: '12+ years' },
        { id: 'dr-arjun', name: 'Dr. Arjun Kumar', specialty: 'Orthopedics', experience: '18+ years' },
        { id: 'dr-sneha', name: 'Dr. Sneha Reddy', specialty: 'Gynecology', experience: '10+ years' },
        { id: 'dr-rahul', name: 'Dr. Rahul Menon', specialty: 'Pediatrics', experience: '8+ years' }
    ];

    // Filter doctors based on query
    const filteredDoctors = doctors.filter(doctor => 
        doctor.name.toLowerCase().includes(query.toLowerCase()) ||
        doctor.specialty.toLowerCase().includes(query.toLowerCase())
    );

    // Display results
    if (filteredDoctors.length > 0) {
        searchResults.innerHTML = '';
        searchResults.classList.remove('d-none');

        filteredDoctors.forEach(doctor => {
            const resultItem = document.createElement('div');
            resultItem.className = 'search-result-item p-3 border-bottom';
            resultItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${doctor.name}</h6>
                        <small class="text-muted">${doctor.specialty} • ${doctor.experience}</small>
                    </div>
                    <a href="doctor-profile.html?id=${doctor.id}" class="btn btn-sm btn-outline-primary">View Profile</a>
                </div>
            `;
            searchResults.appendChild(resultItem);
        });
    } else {
        searchResults.innerHTML = '<div class="p-3 text-center text-muted">No doctors found</div>';
        searchResults.classList.remove('d-none');
    }
}

// Contact form functionality
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const contactData = {
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                subject: formData.get('subject'),
                message: formData.get('message')
            };

            if (validateContactData(contactData)) {
                submitContactForm(contactData);
            }
        });
    }
}

// Validate contact data
function validateContactData(data) {
    let isValid = true;
    const errors = [];

    // Name validation
    if (!data.name || data.name.trim().length < 2) {
        errors.push('Please enter your name');
        isValid = false;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!data.email || !emailRegex.test(data.email)) {
        errors.push('Please enter a valid email address');
        isValid = false;
    }

    // Message validation
    if (!data.message || data.message.trim().length < 10) {
        errors.push('Please enter a message with at least 10 characters');
        isValid = false;
    }

    if (!isValid) {
        showFormErrors(errors);
    }

    return isValid;
}

// Submit contact form
function submitContactForm(data) {
    const submitButton = document.querySelector('#contactForm button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Sending...';

    // Simulate API call
    setTimeout(() => {
        showSuccessMessage('Message sent successfully! We will get back to you soon.');
        document.getElementById('contactForm').reset();
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }, 2000);
}

// Utility functions
function formatPhoneNumber(input) {
    const phoneNumber = input.value.replace(/\D/g, '');
    const formattedNumber = phoneNumber.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
    input.value = formattedNumber;
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/[-\s]/g, ''));
}

// Initialize contact form when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initContactForm();
});

// Export functions for external use
window.BabuClinic = {
    formatPhoneNumber,
    validateEmail,
    validatePhone,
    showFormErrors,
    showSuccessMessage
};
