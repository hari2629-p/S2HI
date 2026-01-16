from django.db import models

class ReadingSession(models.Model):
    user_id = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='reading_audio/')
    expected_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    session = models.OneToOneField(ReadingSession, on_delete=models.CASCADE)
    
    # AI Metrics
    wpm = models.IntegerField()
    accuracy_score = models.IntegerField()
    mispronunciations = models.JSONField(default=list) 
    
    # The Assessment & Solution
    risk_score = models.CharField(max_length=50) 
    feedback = models.TextField() # <--- Stores the "Recommended Solution"
    transcribed_text = models.TextField(blank=True) # Stores the summary

    def __str__(self):
        return f"Analysis for {self.session.session_id}"