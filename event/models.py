import uuid
from django.db import models


class Lead(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name
