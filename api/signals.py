from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Communication
from django.conf import settings


@receiver(pre_save, sender=Communication, dispatch_uid="api.communication.communication_pre_save")
def communication_pre_save(sender, instance, **kwargs):
    if not instance.cancel_signal:
        instance.apply_template(with_save=False)


@receiver(post_save, sender=Communication, dispatch_uid="api.communication.communication_post_save")
def communication_post_save(sender, instance, created, **kwargs):
    if not instance.cancel_signal and created:
        # only send on creation (otherwise it will loop)
        return instance.send()
