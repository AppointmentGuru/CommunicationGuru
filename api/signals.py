from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Communication


@receiver(pre_save, sender=Communication, dispatch_uid="api.communication.communication_pre_save")
def communication_pre_save(sender, instance, **kwargs):
    instance.apply_template(with_save=False)

@receiver(post_save, sender=Communication, dispatch_uid="api.communication.communication_post_save")
def communication_post_save(sender, instance, created, **kwargs):
    instance.send()
