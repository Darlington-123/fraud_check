from django.db import models


# Create your models here.
class ScamEntity(models.Model):
    """
    Represents individual testimonies or reports submitted by citizens
    when they fall victim or spot a scam. Multiple reports can link to one ScamEntity.
    """
    ENTITY_TYPES = [
        ('phone', 'phone Number/Mobile Money'),
        ('url', 'Website Link'),
        ('email', 'Email Address'),
        ('name', 'Individual / Business Name'),
    ]
    STATUS_CHOICES = [
        ('clear', 'Clear'),
        ('suspicious', 'Suspicious'),
        ('flagged', 'Flagged'),
    ]

    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)
    value = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='clear')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_status(self):
        approved_reports = self.reports.filter(review_status='approved').count()
        if approved_reports >= 3:
            self.status = 'flagged'
        elif approved_reports >= 1:
            self.status = 'suspicious'
        else:
            self.status = 'clear'
        self.save()

    @property
    def approved_reports(self):
            return self.reports.filter(review_status='approved').count()

class ScamReport(models.Model):
    """
    Represents individual testimonies or reports submitted by citizens
    when they fall victim or spot a scam. Multiple reports can link to one ScamEntity.
    """
    REVIEW_STATUS = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    SCAM_CATEGORIES = [
        ('momo', 'Fake Mobile Money Deposit / Request'),
        ('market', 'Facebook / Online Marketplace Fraud'),
        ('job', 'Fake Job Recruitment / Visa Scam'),
        ('loan', 'Rogue Online Loan App / Fee Scam'),
        ('other', 'Other Fraudulent Activity'),
    ]

    entity = models.ForeignKey(ScamEntity, on_delete=models.CASCADE, related_name='reports')
    scam_category = models.CharField(max_length=50, choices=SCAM_CATEGORIES)
    description = models.TextField(help_text="Describe how the scam happened to warn others.")
    evidence_image = models.ImageField(upload_to='evidence/', blank=True, null=True, help_text="Optional screenshot proof.")
    created_at = models.DateTimeField(auto_now_add=True)
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS, default='pending')
    

    def __str__(self):
        return f"Report for {self.entity.value} ({self.get_scam_category_display()})"


def __str__(self):
        return f"{self.entity_type} - {self.value}"