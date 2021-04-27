from webapp.models import CoffeeUser
from django.db import transaction

@transaction.atomic
def update_credits():
    obj = CoffeeUser.objects.all()
    obj.update(credits=2)
    for i in obj:
        i.save()