from django.shortcuts import render
from .models import Tutor, Takes, Course
from django.db.models import F

def index(request):
    return render(request, 'index.html')
def page25(request):
    return render(request, '25.html')
def addTutor(request):
    return render(request, 'addTutor.html')
def help(request):
    return render(request, 'help.html')

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

# View/Edit Tutor Hours
def view_edit_tutor_hours(request):
    if request.method == 'POST':
        # Assume you have a form to edit hours, handle the form submission here
        # Process the form data and update the database
        # Redirect to a new URL:
        return redirect('view_edit_tutor_hours')
    else:
        # Fetch the tutor hours data from the database
        tutor_hours = TutorHours.objects.all()  # Example model and method
        context = {'tutor_hours': tutor_hours}
        return render(request, 'view_edit_tutor_hours.html', context)

# Input Hours
def input_hours(request):
    if request.method == 'POST':
        # Handle hours input form submission
        # Save the new hours to the database
        # Redirect to a new URL or the same page to show a success message
        return redirect('input_hours')
    else:
        # Provide a blank form for inputting hours
        form = HoursForm()  # Example form
        context = {'form': form}
        return render(request, 'input_hours.html', context)

# Input Completed Courses
def input_completed_courses(request):
    if request.method == 'POST':
        # Handle completed courses form submission
        # Update the database with the completed courses
        # Redirect to show success message
        return redirect('input_completed_courses')
    else:
        # Provide a blank form for inputting completed courses
        form = CompletedCoursesForm()  # Example form
        context = {'form': form}
        return render(request, 'input_completed_courses.html', context)

# Add/Remove Tutors
def add_remove_tutors(request):
    if request.method == 'POST':
        # Handle adding or removing tutors based on the form submission
        # Update the database accordingly
        # Redirect after the operation
        return redirect('add_remove_tutors')
    else:
        # Fetch the current list of tutors to display
        tutors = Tutor.objects.all()  # Example model and method
        # Provide forms for adding and removing tutors
        add_form = AddTutorForm()  # Example form
        remove_form = RemoveTutorForm()  # Example form
        context = {
            'tutors': tutors,
            'add_form': add_form,
            'remove_form': remove_form
        }
        return render(request, 'add_remove_tutors.html', context)