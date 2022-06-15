from django.contrib.auth.models import User
from .models import Profile, Cars
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('Yellow')
    if created:
        print('Created')
        Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name,
                               email=instance.email)


# @receiver(post_save, sender=User)
# def cars_profile(sender, instance, created, **kwargs):
#     print('Yellow')
#     if created:
#         print('Created')
#         Cars.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(post_save, sender=User)
# def save_cars(sender, instance, **kwargs):
#     instance.cars.save()
