from django.db import models

class Comments(models.Model):
    text = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
