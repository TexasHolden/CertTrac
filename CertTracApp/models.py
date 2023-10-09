from django.db import models

class Tutor(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField()
    date_hired = models.DateField()
    level = models.IntegerField(default = 0)
    level_1_hours = models.DecimalField(max_digits=5, decimal_places = 2, default = 0)
    level_1_hours_in_person = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    level_2_hours = models.DecimalField(max_digits=5, decimal_places = 2, default = 0)
    level_2_hours_in_person = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    post_level_2_hours = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    logged_25_hours_level_1 = models.DateField(null = True)
    logged_25_hours_level_2 = models.DateField(null = True)
    # Additional Attributes for Level Updating Logic
    number_basic_courses = models.IntegerField(default = 0)
    number_communication_courses = models.IntegerField(default = 0)
    number_learningstudytechinque_courses = models.IntegerField(default = 0)
    number_ethicsequality_courses = models.IntegerField(default = 0)
    number_elective_courses = models.IntegerField(default = 0)

class Course(models.Model):
    name = models.CharField(max_length = 40)
    level = models.IntegerField()
    subject = models.CharField(max_length = 20)

class Takes(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
