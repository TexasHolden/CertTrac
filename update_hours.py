from CertTracApp.models import Tutor
from django.db.models import F
from datetime import datetime
from utils import get_tutor_id, get_course_level

def add_hours(name, course, date, in_person, a_sync):
    tid = get_tutor_id(name)
    course_level = get_course_level(course)
    tutor = Tutor.objects.get(id = tid)

    date = datetime.strptime(date, '%Y-%m-%d').date()
    in_person = float(in_person)
    a_sync = float(a_sync)

    if course_level == 2:
        #Level 2 Tutors
        if tutor.level_1_completion_date and tutor.level_2_completion_date:
            #Session taken after level 2 complete time added to post level 2
            if date >= tutor.level_2_completion_date: #Ask if level up and session on same day, do hours go to old level or new level?
                tutor.post_level_2_hours = in_person + a_sync
                tutor.save()

            #Session taken before level 2 complete and after level 1 complete time added to level 2
            elif date >= tutor.level_1_completion_date:
                tutor.level_2_hours_in_person = F('level_2_hours_in_person') + in_person
                tutor.level_2_hours = F('level_2_hours') + in_person + a_sync
                tutor.save()

            #Session taken before level 2 complete and before level 1 complete time added to level 1
            elif date:
                tutor.level_1_hours_in_person = F('level_1_hours_in_person') + in_person
                tutor.level_1_hours = F('level_1_hours') + in_person + a_sync
                tutor.save()

        #Level 1 Tutors
        if tutor.level_1_completion_date and not tutor.level_2_completion_date:
            #Session taken after level 1 completion time added to level 2
            if date >= tutor.level_1_completion_date:
                tutor.level_2_hours_in_person = F('level_2_hours_in_person') + in_person
                tutor.level_2_hours = F('level_2_hours') + in_person + a_sync
                tutor.save()

            #Session taken before level 1 completion time added to level 1 
            else:
                tutor.level_1_hours_in_person = F('level_1_hours_in_person') + in_person
                tutor.level_1_hours = F('level_1_hours') + in_person + a_sync
                tutor.save()

        #Level 0 Tutors
        if not tutor.level_1_completion_date and not tutor.level_2_completion_date:
            #Session taken before level 1 completion time added to level 1 
            tutor.level_1_hours_in_person = F('level_1_hours_in_person') + in_person
            tutor.level_1_hours = F('level_1_hours') + in_person + a_sync
            tutor.save()

    if course_level == 1:
            #Level 2 Tutors
            if tutor.level_1_completion_date and tutor.level_2_completion_date:
                #Session taken before level 2 complete and before level 1 complete time added to level 1
                if date < tutor.level_1_completion_date:
                    tutor.level_1_hours_in_person = F('level_1_hours_in_person') + in_person
                    tutor.level_1_hours = F('level_1_hours') + in_person + a_sync
                    tutor.save()


            #Level 1 Tutors
            if tutor.level_1_completion_date and not tutor.level_2_completion_date:
                #Session taken before level 1 completion time added to level 1 
                if date < tutor.level_1_completion_date:
                    tutor.level_1_hours_in_person = F('level_1_hours_in_person') + in_person
                    tutor.level_1_hours = F('level_1_hours') + in_person + a_sync
                    tutor.save()

            #Level 0 Tutors
            if not tutor.level_1_completion_date and not tutor.level_2_completion_date:
                #Session taken before level 1 completion time added to level 1 
                tutor.level_1_hours_in_person = F('level_1_hours_in_person') + in_person
                tutor.level_1_hours = F('level_1_hours') + in_person + a_sync
                tutor.save()
