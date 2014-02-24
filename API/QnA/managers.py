from django.db import models

class MessageManager(models.Manager):

    def get_by_id(self, id):
        return None
