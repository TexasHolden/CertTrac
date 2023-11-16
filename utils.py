from CertTracApp.models import Tutor, Takes, Subtopic
from django.db.models import Count

def get_tutor_id(name):
    #Tutor First Last Name#
    name = name.split(' ')
    first_name = name[0]; last_name = name[1]

    tutor = Tutor.objects.get(first_name = first_name, last_name = last_name)
    return tutor.id

def get_course_id(name):
    course = Subtopic.objects.get(name = name)
    return course.id

def get_course_level(name):
    course = Subtopic.objects.get(name = name)
    return course.level


def count_courses():
    for tutor in Tutor.objects.all():
        count = (
            Takes.objects.filter(
                tutor_id = tutor.id,
                session__subtopic__topic = 'Basics',
                session__subtopic__level = 1
            )
            .values('subtopic__name')
            .annotate(course_count=Count('subtopic__name', distinct = True))
            .count()
        )
        tutor.number_basic_courses_completed_level_1 = count
        tutor.save()

        count = (
            Takes.objects.filter(
                tutor_id = tutor.id,
                subtopic__topic = 'Communication',
                subtopic__level = 1,
            )
            .values('subtopic__name')
            .annotate(course_count=Count('subtopic__name', distinct = True))
            .count()
        )
        tutor.number_communication_courses_completed_level_1 = count
        tutor.save()

        count = (
            Takes.objects.filter(
                tutor_id = tutor.id,
                subtopic__topic = 'Learning & Study Techniques',
                subtopic__level = 1
            )
            .values('subtopic__name')
            .annotate(course_count=Count('subtopic__name', distinct = True))
            .count()
        )
        tutor.number_learningstudytechinque_courses_completed_level_1 = count
        tutor.save()

        count = (
            Takes.objects.filter(
                tutor_id = tutor.id,
                subtopic__topic = 'Ethics & Equality',
                subtopic__level = 1
            )
            .values('subtopic__name')
            .annotate(course_count=Count('subtopic__name', distinct = True))
            .count()
        )
        tutor.number_ethicsequality_courses_completed_level_1 = count
        tutor.save()

        count = (
            Takes.objects.filter(
                tutor_id = tutor.id,
                subtopic__topic = 'Electives',
                subtopic__level = 1
            )
            .values('subtopic__name')
            .annotate(course_count=Count('subtopic__name', distinct = True))
            .count()
        )
        tutor.number_elective_courses_completed_level_1 = count
        tutor.save()

        if tutor.level_1_completion_date is not None:
            count = (
                Takes.objects.filter(
                    tutor_id = tutor.id,
                    subtopic__topic = 'Basics',
                    subtopic__level = 2,
                    date__gte = tutor.level_1_completion_date
                )
                .values('subtopic__name')
                .annotate(course_count=Count('subtopic__name', distinct = True))
                .count()
            )
            tutor.number_basic_courses_completed_level_2 = count
            tutor.save()

            count = (
                Takes.objects.filter(
                    tutor_id = tutor.id,
                    subtopic__topic = 'Communication',
                    subtopic__level = 2,
                    date__gte = tutor.level_1_completion_date
                )
                .values('subtopic__name')
                .annotate(course_count=Count('subtopic__name', distinct = True))
                .count()
            )
            tutor.number_communication_courses_completed_level_2 = count
            tutor.save()

            count = (
                Takes.objects.filter(
                    tutor_id = tutor.id,
                    subtopic__topic = 'Learning & Study Techniques',
                    subtopic__level = 2,
                    date__gte = tutor.level_1_completion_date
                )
                .values('subtopic__name')
                .annotate(course_count=Count('subtopic__name', distinct = True))
                .count()
            )
            tutor.number_learningstudytechinque_courses_completed_level_2 = count
            tutor.save()

            count = (
                Takes.objects.filter(
                    tutor_id = tutor.id,
                    subtopic__topic = 'Ethics & Equality',
                    subtopic__level = 2,
                    date__gte = tutor.level_1_completion_date
                )
                .values('subtopic__name')
                .annotate(course_count=Count('subtopic__name', distinct = True))
                .count()
            )
            tutor.number_ethicsequality_courses_completed_level_2 = count
            tutor.save()

            count = (
                Takes.objects.filter(
                    tutor_id = tutor.id,
                    subtopic__topic = 'Electives',
                    subtopic__level = 2,
                    date__gte = tutor.level_1_completion_date
                )
                .values('subtopic__name')
                .annotate(course_count=Count('subtopic__name', distinct = True))
                .count()
            )
            tutor.number_elective_courses_completed_level_2 = count
            tutor.save()
