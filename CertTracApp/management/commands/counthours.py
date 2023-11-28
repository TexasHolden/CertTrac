from django.core.management.base import BaseCommand
from CertTracApp.models import Takes, Tutor
from django.db.models import Sum
from datetime import datetime

class Command(BaseCommand):
    help = 'Parses CSV Files to Populate Database'

    def handle(self, *args, **kwargs):
        #For this testing script loop through all the tutors
        #In the app, loop through tutors who got session added
        for tutor in Tutor.objects.all():
            '''
            Check Level 0 Tutors
            Add All Their Hours Since Can Only Have Level 1 Hours
            Course Does Not Matter Since Any Course Counts Level 1
            '''
            if not tutor.level_1_completion_date:
                #Sums In Person Hours
                level_1_hours_in_person = (
                    Takes.objects.filter(
                        tutor_id = tutor.id,
                    )
                    .aggregate(hours_sum = Sum('session__in_person_hours'))
                )['hours_sum'] or 0

                #Sums Async Hours
                level_1_hours_async = (
                    Takes.objects.filter(
                        tutor_id = tutor.id,
                    )
                    .aggregate(hours_sum = Sum('session__async_hours'))
                )['hours_sum'] or 0

                #Total Hours In Person + Async
                level_1_hours_total = level_1_hours_in_person + level_1_hours_async
        
                if level_1_hours_in_person != tutor.level_1_hours_in_person:
                    print(f"IP1 {tutor.first_name} {tutor.last_name} {tutor.date_hired} : {level_1_hours_in_person} {tutor.level_1_hours_in_person}")
                if level_1_hours_total != tutor.level_1_hours:
                    print(f"T1  {tutor.first_name} {tutor.last_name} {tutor.date_hired} : {level_1_hours_total} {tutor.level_1_hours}")

            '''
            Level 1 Tutors
            Can Get Both Level 1 and Level 2 Hours
            Level 1 Hours is ANY Session Completed Before Level 1 Completion
            If Level 1 Completion is 05-11-22, Then BEFORE OR EQUAL TO 05-11-22
            Else, Count Strictly Before Level 1 Completion
            Level 2 Hours Would then Be All Hours After Level 1 Completion if Course IS Level 2 and Level 1 Completion is 05-11-22
            Else, Level 2 Hours Would then Be All Hours After or Equal to Level 1 Completion
            Holds Both In Person and Total
            '''
            if tutor.level_1_completion_date: #and not tutor.level_2_completion_date:
                if tutor.level_1_completion_date == datetime.strptime("2022-05-11", "%Y-%m-%d").date():
                    level_1_hours_in_person = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__lte = tutor.level_1_completion_date
                        )
                        .aggregate(hours_sum = Sum('session__in_person_hours'))
                    )['hours_sum'] or 0

                    level_1_hours_async = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__lte = tutor.level_1_completion_date
                        )
                        .aggregate(hours_sum = Sum('session__async_hours'))
                    )['hours_sum'] or 0

                    level_2_hours_in_person = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__gt = tutor.level_1_completion_date,
                            session__subtopic__level = 2
                        )
                        .aggregate(hours_sum = Sum('session__in_person_hours'))
                    )['hours_sum'] or 0

                    level_2_hours_async = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__gt = tutor.level_1_completion_date,
                            session__subtopic__level = 2
                        )
                        .aggregate(hours_sum = Sum('session__async_hours'))
                    )['hours_sum'] or 0
                    
                elif tutor.level_1_completion_date > datetime.strptime("2022-05-11", "%Y-%m-%d").date():
                    level_1_hours_in_person = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__lte = tutor.level_1_completion_date
                        )
                        .aggregate(hours_sum = Sum('session__in_person_hours'))
                    )['hours_sum'] or 0

                    level_1_hours_async = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__lte = tutor.level_1_completion_date
                        )
                        .aggregate(hours_sum = Sum('session__async_hours'))
                    )['hours_sum'] or 0

                    level_2_hours_in_person = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__gt = tutor.level_1_completion_date,
                            session__subtopic__level = 2
                        )
                        .aggregate(hours_sum = Sum('session__in_person_hours'))
                    )['hours_sum'] or 0

                    level_2_hours_async = (
                        Takes.objects.filter(
                            tutor_id = tutor.id,
                            date__gt = tutor.level_1_completion_date,
                            session__subtopic__level = 2
                        )
                        .aggregate(hours_sum = Sum('session__async_hours'))
                    )['hours_sum'] or 0

                else:
                    assert(False)

                level_1_hours_total = level_1_hours_in_person + level_1_hours_async
                level_2_hours_total = level_2_hours_in_person + level_2_hours_async
    
                if level_1_hours_in_person != tutor.level_1_hours_in_person:
                    print(f"IP1 {tutor.first_name} {tutor.last_name} {tutor.date_hired} : {level_1_hours_in_person} {tutor.level_1_hours_in_person} {tutor.level_1_completion_date}")
                if level_1_hours_total != tutor.level_1_hours:
                    print(f"T1  {tutor.first_name} {tutor.last_name} {tutor.date_hired} : {level_1_hours_total} {tutor.level_1_hours} {tutor.level_1_completion_date}")

                if level_2_hours_in_person != tutor.level_2_hours_in_person:
                    print(f"IP2 {tutor.first_name} {tutor.last_name} {tutor.date_hired} : {level_2_hours_in_person} {tutor.level_2_hours_in_person} {tutor.level_1_completion_date}")
                if level_2_hours_total != tutor.level_2_hours:
                    print(f"T2 {tutor.first_name} {tutor.last_name} {tutor.date_hired} : {level_2_hours_total} {tutor.level_2_hours} {tutor.level_1_completion_date}")