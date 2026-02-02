from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import nh3
from apps.core.models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Contact form with NH3 sanitization (Bleach replacement)
    """
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-4 border-gray-900 bg-white focus:outline-none focus:bg-yellow-50 transition-colors font-medium',
                'placeholder': 'John Doe',
                'maxlength': '200',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border-4 border-gray-900 bg-white focus:outline-none focus:bg-yellow-50 transition-colors font-medium',
                'placeholder': 'john@example.com',
                'maxlength': '254',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-4 border-gray-900 bg-white focus:outline-none focus:bg-yellow-50 transition-colors font-medium resize-none',
                'placeholder': 'Tell me about your project...',
                'rows': 5,
                'maxlength': '5000',
            }),
        }
        labels = {
            'name': 'Your Name *',
            'email': 'Email Address *',
            'message': 'Your Message *',
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError('Name is required.')
        
        # NH3: Strip ALL HTML (safer than bleach)
        # tags=set() means NO tags allowed
        name = nh3.clean(
            name,
            tags=set(),  # No tags allowed
            strip_comments=True,
        )
        
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters.')
        
        if len(name) > 200:
            raise ValidationError('Name is too long.')
        
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        
        if not email:
            raise ValidationError('Email is required.')
        
        # Django's built-in EmailValidator
        validator = EmailValidator(message='Please enter a valid email address.')
        validator(email)
        
        # NH3: Sanitize
        email = nh3.clean(email, tags=set())
        
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        
        if not message:
            raise ValidationError('Message is required.')
        
        # NH3: Strip ALL HTML
        message = nh3.clean(
            message,
            tags=set(),  # No tags allowed
            strip_comments=True,
        )
        
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters.')
        
        if len(message) > 5000:
            raise ValidationError('Message is too long.')
        
        return message
