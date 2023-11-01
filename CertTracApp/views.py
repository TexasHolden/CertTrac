from django.shortcuts import render
from .models import Tutor, Takes, Course
from django.db.models import F

def index(request):
    return render(request, 'index.html')
def session(request):
    return render(request, 'session.html')

def query_results(request):
    if request.method == 'POST':
        #Data From Web Page# 
        name = request.POST.get('name')
        course = request.POST.get('course')
        time = request.POST.get('time')
        in_person = request.POST.get('inperson')
        total = request.POST.get('total')
        date = request.POST.get('date')

        id = get_tutor_id(name)

        #Update Queries#
        add_hours(name, course, time, in_person, total)

        #Print To Web Page#
        #Tutor Information#
        tutors = Tutor.objects.filter(id = id).values()

        #Takes Table Crossed With Session Table#
        takes_history = Takes.objects.filter(tutor = id).values()
        takes_history = sorted(takes_history, key=lambda x: x['date'])
        context = {
            'tutors': tutors,
            'takes_history': takes_history,
        }

        # Check if string is over a certain limit
        # If big string, wrap in html
        # <div style="font-size: 12px (smaller font)"> + {{ item.course }} + </div>

        return render(request, 'results.html', {'tutors': tutors, 'takes_history' : takes_history})
    else:
        # Handle other request methods as needed
        return render(request, 'index.html')
    
#UPDATE HOURS#
def add_hours(name, course, time, in_person, total):
    id = get_tutor_id(name)
    course_level = get_course_level(course)

    #Update All Level 0 Tutors Because Get Get Level 1 Hours For Both Level 1 and 2 Topics
    if total:
        #UPDATE Tutor SET level_1_hours = level_1_hours + time WHERE level = 0 and id = id
        Tutor.objects.filter(level = 0, id = id).update(level_1_hours = F('level_1_hours') + time)
    if in_person:
        #UPDATE Tutor SET level_1_hours_in_person = level_1_hours_in_person + time WHERE level = 0 and id = id
        Tutor.objects.filter(level = 0, id = id).update(level_1_hours_in_person = F('level_1_hours_in_person') + time)
    
    #Update Both Level 1 and 2 Because Level 2 Hours Count For Level 2 Hours For Level 1 Tutors But Post Level 2 For Level 2 Tutors#
    if course_level == 2:
        if total:
            #UPDATE Tutor SET level_2_hours = level_2_hours + time WHERE level = 1 AND id = id
            Tutor.objects.filter(level = 1, id = id).update(level_2_hours = F('level_2_hours') + time)
        if in_person:
            #UPDATE Tutor SET level_2_hours_in_person = level_2_hours_in_person + time WHERE level = 1 AND id = id
            Tutor.objects.filter(level = 1, id = id).update(level_2_hours_in_person = F('level_2_hours_in_person') + time)
        #Add Post Level 2 Hours For Level 2 Tutors
        #UPDATE Tutor SET post_level_2_hours = post_level_2_hours + time WHERE level = 2 AND id = id
        Tutor.objects.filter(level = 2, id = id).update(post_level_2_hours = F('post_level_2_hours') + time)

#ADD TAKES#
def add_takes(name, course, date):
    #get tutor_id
    #get_course_id
    #add Takes(tutor_id, course_id, semester, date)
    pass

#ADD TRAING SESSION#
def add_session(course, semester, time, in_person, total):
    #find semester code
    #add session(course, semester, time, inperson, total)
    pass

#UPDATE LEVEL#
    
#UTILITIES#

def get_tutor_id(name):
    #Tutor First Last Name#
    name = name.split(' ')
    first_name = name[0]; last_name = name[1]

    tutor = Tutor.objects.get(first_name = first_name, last_name = last_name)
    return tutor.id

def get_course_id(name):
    course = Course.objects.get(name = name)
    return course.id

def get_course_level(name):
    course = Course.objects.get(name = name)
    return course.level

