from django.db.models.signals import post_delete
from django.dispatch import receiver
from fightcrctrials.models import CRCTrial, DeletedCRCTrial

@receiver(post_delete, sender=CRCTrial)
def track_deleted_trials(sender, instance, using, **kwargs):
    DeletedCRCTrial.objects.create(nct_id=instance.nct_id)
