from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Communication
from .helpers import (
    send_communication,
    firebase_sync,
    firebase_sync_remove
)

@receiver(pre_save, sender=Communication, dispatch_uid="api.communication.communication_pre_save")
def communication_pre_save(sender, instance, **kwargs):
    instance.apply_template(with_save=False)

@receiver(post_save, sender=Communication, dispatch_uid="api.communication.communication_post_save")
def communication_post_save(sender, instance, created, **kwargs):
    if created:
        # only send on creation (otherwise it will loop)
        send_communication.delay(instance.id)
        # return instance.send()

# call that function in a delayed manner
@receiver(post_save, dispatch_uid="django_nosql.sync")
def sync_readonly_db(sender, instance, created, **kwargs):
    firebase_sync.delay(instance, created)

@receiver(post_delete, dispatch_uid="django_nosql.sync.delete")
def sync_remove_readonly_db(sender, instance, **kwargs):
    firebase_sync_remove.delay(instance)

