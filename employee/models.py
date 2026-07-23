from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()
    photo = models.ImageField(
        upload_to="employee_photos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
  


from django.contrib.auth.models import User

class UserFace(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    face_registered = models.BooleanField(
        default=False
    )

    face_encoding = models.BinaryField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username