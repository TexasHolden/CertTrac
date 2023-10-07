from django.db import models

from django.db import models

class Tutor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    date_hired = models.DateField()
    level = models.IntegerField()
    level_1_hours = models.DecimalField(max_digits=5, decimal_places=2)
    level_1_hours_in_person = models.DecimalField(max_digits=5, decimal_places=2)
    level_2_hours = models.DecimalField(max_digits=5, decimal_places=2)
    level_2_hours_in_person = models.DecimalField(max_digits=5, decimal_places=2)
    post_level_2_hours = models.DecimalField(max_digits=5, decimal_places=2)
    logged_25_hours_level_1 = models.DateField()
    logged_25_hours_level_2 = models.DateField()
    # Additional Attributes for Level Updating Logic

class Course(models.Model):
    level = models.IntegerField()
    subject = models.CharField(max_length=20)

class Takes(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
