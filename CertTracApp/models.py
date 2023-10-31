from django.db import models


class Tutor(models.Model):
    '''
    Model representing a Tutor with various attributes and information.

    Fields:
        - first_name: First name of the tutor (max length: 20 characters).
        - last_name: Last name of the tutor (max length: 20 characters).
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

    This model represents information related to tutors and their progress through different levels and courses, including level-specific course completions.
    '''
    #General Tutor Information
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    date_hired = models.CharField(max_length = 40)

    #Tutor Level 0, 1, or 2 Possibly 3 in the Future ;)
    level = models.IntegerField(default=0)

    #Level 1 Information
    level_1_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    level_1_hours_in_person = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    logged_25_hours_level_1 = models.DateField(null=True, default=None)
    level_1_completion_date = models.DateField(null=True, default=None)

    #Level 2 Information
    level_2_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    level_2_hours_in_person = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    post_level_2_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    level_2_completion_date = models.DateField(null=True, default=None)
    
    #Post Level 2 Possibly Level 3 Information in Future;)
    logged_25_hours_level_2 = models.DateField(null=True)

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


class Course(models.Model):
    '''
    Model representing a Course with various attributes and information.

    Fields:
        - name: The name or title of the course (max length: 40 characters).
        - level: The level of the course.
        - subject: The subject or category of the course (max length: 20 characters).

    This model represents information related to courses offered in an educational context.
    '''
    name = models.CharField(max_length = 40)
    level = models.IntegerField()
    subject = models.CharField(max_length = 40)


class Takes(models.Model):
    '''
    Model representing a record of a tutor taking a course.

    Fields:
        - tutor: A foreign key to the Tutor model, representing the tutor who is taking the course.
        - course: A foreign key to the Course model, representing the course that the tutor is taking.
        - date: The date when the tutor took the course.

    This model serves as a record of tutors taking specific courses on particular dates, establishing a relationship
    between tutors and courses they have taken.
    '''
    tutor = models.IntegerField()
    course = models.CharField(max_length = 40)
    semester = models.CharField(max_length = 40)
    date = models.DateField()


class InPersonTrainingSession(models.Model):
    sub_topic = models.CharField(max_length = 40)
    date = models.CharField(max_length = 40)
    training_time = models.DecimalField(max_digits = 5, decimal_places = 2)


class TotalTrainingSession(models.Model):
    sub_topic = models.CharField(max_length = 40)
    date = models.CharField(max_length = 40)
    training_time = models.DecimalField(max_digits = 5, decimal_places = 2)


#class TrainingSession(models.Model):
    '''
    #Model representing sessions that contribute exclusively to in-person training time for courses.

    #Fields:
        #- course: A foreign key to the Course model, indicating the course related to this in-person training session.
        #- date: The date for which the in-person training session is logged (max length: 40 characters).
        #- training_time: The amount of in-person training time logged for the course (hours and minutes).

    #This model serves as a record of in-person training sessions associated with specific courses, including the date and the amount of in-person training time logged for the course. These sessions exclusively contribute to the in-person training time for the course.
    '''
    #sub_topic = models.ForeignKey(SubTopic)
    #semester = models.CharField(max_length=40)
    #in_person_hours = models.DecimalField(max_digits=5, decimal_places=2)
    #total_hours = models.DecimalField(max_digits=5, decimal_places=2)


