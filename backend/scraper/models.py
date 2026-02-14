from django.db import models


class ScrapingLog(models.Model):
    """Log scraping activities"""
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial'),
    ]
    
    source_url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    records_scraped = models.IntegerField(default=0)
    records_duplicate = models.IntegerField(default=0)
    records_new = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'scraping_logs'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.source_url} - {self.status} ({self.started_at})"

