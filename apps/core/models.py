from django.db import models

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending Response'),
        ('completed', 'Completed'),
    ]
    
    # Form Fields
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    
    # Status & Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for tracking conversation")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"
