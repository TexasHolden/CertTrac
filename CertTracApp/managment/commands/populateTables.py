from django.core.management.base import BaseCommand
from CertTracApp.models import Tutor, Course

class Command(BaseCommand):
    help = 'Adds Tutors and Courses'

    def handle(self, *args, **kwargs):
        # Add Tutors
        tutors_data = [
            {
                "first_name": "Alice",
                "last_name": "Jones",
                "email": "ajones@kent.edu",
                "date_hired": "2023-10-15",
            },
            {
                "first_name": "Bob",
                "last_name": "Smith",
                "email": "bsmith@kent.edu",
                "date_hired": "2023-09-20",
                "level": 0,
                "level_1_hours": 9.0,
                "level_1_hours_in_person": 4.0,
                "logged_25_hours_level_1" = "2023-10-10",
            },
            {
                "first_name": "Charles",
                "last_name": "Thompson",
                "email": "cthompson@kent.edu",
                "date_hired": "2023-08-14",
                "level": 1,
                "level_1_hours": 10.0,
                "level_1_hours_in_person": 7.0,
                "level_2_hours": 0.0,
                "level_2_hours_in_person": 0.0,
                "logged_25_hours_level_1" = "2023-9-13",
            },
            {
                "first_name": "Daniel",
                "last_name": "Danielson",
                "email": "ddanielsonson@kent.edu",
                "date_hired": "2023-06-05",
                "level": 1,
                "level_1_hours": 10.0,
                "level_1_hours_in_person": 7.0,
                "level_2_hours": 9.0,
                "level_2_hours_in_person": 4.0,
                "logged_25_hours_level_1" = "2023-7-13",
                "logged_25_hours_level_2" = "2023-9-25",
            },
            {
                "first_name": "Emily",
                "last_name": "Reed",
                "email": "ereed@kent.edu",
                "date_hired": "2023-01-01",
                "level": 2,
                "level_1_hours": 10.0,
                "level_1_hours_in_person": 7.0,
                "level_2_hours": 10.0,
                "level_2_hours_in_person": 6.0,
                "logged_25_hours_level_1" = "2023-7-13",
                "logged_25_hours_level_2" = "2023-9-25",
            },
        ]

        # Create and save Tutor instances
        for tutor_data in tutors_data:
            tutor_instance = Tutor(**tutor_data)
            tutor_instance.save()

        self.stdout.write(self.style.SUCCESS('Successfully added Tutors.'))

        # Add Courses
        courses_data = [
            {
            	"name": "Administrative Policies, Record Keeping & Reporting"
                "level": 1,
                "subject": "Basic",
            },
            {
                "title": 
                "level": 1,
                "subject": "Math",
            },
            {
                "title": 
                "level": 1,
                "subject": "Math",
            },
            {
                "title": 
                "level": 1,
                "subject": "Math",
            },
        ]

        # Create and save Course instances
        for course_data in courses_data:
            course_instance = Course(**course_data)
            course_instance.save()

        self.stdout.write(self.style.SUCCESS('Successfully added Courses.'))
