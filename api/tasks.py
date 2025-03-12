from celery import shared_task
from .dreamscribe import DreamScribe
from .models import Dream

@shared_task
def process_dream(dream_id):
    dream = Dream.objects.get(id=dream_id)
    ds = DreamScribe()
    analysis = ds.analyze_dream(dream.text)
    dream.analysis = analysis
    dream.image_url = analysis["image_url"]
    dream.save()