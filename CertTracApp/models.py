from django.db import models
from django.utils import timezone


class Tutor(models.Model):
    '''
    Model representing a Tutor with various attributes and information.

    Fields:
        - first_name: First name of the tutor (max length: 40 characters).
        - last_name: Last name of the tutor (max length: 40 characters).
        - email: Email address of the tutor.
        - date_hired: Date when the tutor was hired.
        - level: Tutor's current level (0, 1, or 2) with a possibility of level 3 in the future.
        - level_1_hours: Total hours for level 1.
        - level_1_hours_in_person: Total in-person hours for level 1.
        - logged_25_hours_level_1: Date when 25 hours for level 1 were logged (nullable).
        - level_1_completion_date: Date when level 1 was completed (nullable).
        - level_2_hours: Total hours for level 2.
        - level_2_hours_in_person: Total in-person hours for level 2.
        - post_level_2_hours: Total hours after completing level 2.
        - level_2_completion_date: Date when level 2 was completed (nullable).
        - logged_25_hours_level_2: Date when 25 hours for level 2 were logged (nullable).
        - number_basic_courses_completed_level_1: Number of basic courses completed for level 1.
        - number_basic_courses_completed_level_2: Number of basic courses completed for level 2.
        - number_communication_courses_completed_level_1: Number of communication courses completed for level 1.
        - number_communication_courses_completed_level_2: Number of communication courses completed for level 2.
        - number_learningstudytechinque_courses_completed_level_1: Number of learning and study technique courses completed for level 1.
        - number_learningstudytechinque_courses_completed_level_2: Number of learning and study technique courses completed for level 2.
        - number_ethicsequality_courses_completed_level_1: Number of ethics and equality courses completed for level 1.
        - number_ethicsequality_courses_completed_level_2: Number of ethics and equality courses completed for level 2.
        - number_elective_courses_completed_level_1: Number of elective courses completed for level 1.
        - number_elective_courses_completed_level_2: Number of elective courses completed for level 2.
        - review_level_1_completed: Date when level 1 review was completed (nullable).

    This model represents information related to tutors and their progress through different levels and courses, including level-specific course completions.
    '''
    # General Tutor Information
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    date_hired = models.CharField(max_length=40)

    # Tutor Level 0, 1, or 2 Possibly 3 in the Future ;)
    level = models.IntegerField(default=0)

    # Level 1 Information
    level_1_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    level_1_hours_in_person = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    logged_25_hours_level_1 = models.DateField(null=True, default=None, blank=True)
    level_1_completion_date = models.DateField(null=True, default=None, blank=True)

    # Level 2 Information
    level_2_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    level_2_hours_in_person = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    post_level_2_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    level_2_completion_date = models.DateField(null=True, default=None, blank=True)
    
    # Post Level 2 Possibly Level 3 Information in Future;)
    logged_25_hours_level_2 = models.DateField(null=True, default=None, blank=True)

    # Additional Attributes for Level Updating Logic and Visualization
    number_basic_courses_completed_level_1 = models.IntegerField(default=0)
    number_basic_courses_completed_level_2 = models.IntegerField(default=0)

    number_communication_courses_completed_level_1 = models.IntegerField(default=0)
    number_communication_courses_completed_level_2 = models.IntegerField(default=0)

    number_learningstudytechinque_courses_completed_level_1 = models.IntegerField(default=0)
    number_learningstudytechinque_courses_completed_level_2 = models.IntegerField(default=0)

    number_ethicsequality_courses_completed_level_1 = models.IntegerField(default=0)
    number_ethicsequality_courses_completed_level_2 = models.IntegerField(default=0)

    number_elective_courses_completed_level_1 = models.IntegerField(default=0)
    number_elective_courses_completed_level_2 = models.IntegerField(default=0)

    review_level_1_completed = models.DateField(null=True, default=None, blank=True)


class Subtopic(models.Model):
    '''
    Model representing a Course with various attributes and information.

    Fields:
        - name: The name or title of the course (max length: 40 characters).
        - level: The level of the course.
        - topic: The subject or category of the course (max length: 40 characters).

    This model represents information related to courses offered in an educational context.
    '''
    name = models.CharField(max_length=40)
    level = models.IntegerField()
    topic = models.CharField(max_length=40)


class Takes(models.Model):
    '''
    Model representing a record of a tutor taking a course.

    Fields:
        - tutor: A foreign key to the Tutor model, representing the tutor who is taking the course.
        - subtopic: A foreign key to the Subtopic model, representing the course that the tutor is taking.
        - semester: The semester when the tutor took the course.
        - date: The date when the tutor took the course.

    This model serves as a record of tutors taking specific courses on particular dates, establishing a relationship
    between tutors and courses they have taken.
    '''
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.DO_NOTHING)
    semester = models.CharField(max_length=40)
    date = models.DateField()


class Session(models.Model):
    '''
    Model representing a session with various attributes and information.

    Fields:
        - subtopic: A foreign key to the Subtopic model, representing the course related to this session.
        - semester: The semester of the session.
        - in_person_hours: The number of in-person hours for the session.
        - async_hours: The number of asynchronous hours for the session.

    This model serves as a record of sessions associated with specific courses, including the semester, in-person hours,
    and asynchronous hours.
    '''
    subtopic = models.ForeignKey(Subtopic, on_delete = models.DO_NOTHING, null = True)
    semester = models.CharField(max_length=40, null = True)
    in_person_hours = models.DecimalField(max_digits=5, decimal_places=2, null = True)
    async_hours = models.DecimalField(max_digits=5, decimal_places=2, null = True)

