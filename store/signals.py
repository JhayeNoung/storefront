from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer

# listen the creation of user model, and create customer profile with the newly created user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']: # return boolean
        Customer.objects.create(user=kwargs['instance'])

'''
We need to tell the Django that `create_customer_for_new_user` fucn should be called
when a user model is created.

Only @receiver(post_save) , the fcn will be called every model is created.
We only want the fucn is called when a user model is saved.

But we won't hard-code the `sender=User`

    from core.models import User
    @receiver(post_save, sender=User)

because it will make `store` app un-independents.
make `store` app depends on `core` app

So we will write

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)

We will use this `signals.py` module in `apps.py`
'''