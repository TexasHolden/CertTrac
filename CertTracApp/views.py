from django.shortcuts import render, get_object_or_404, redirect
from .models import Tutor, Takes, Subtopic, Session
from .forms import TutorForm, TutorSearchForm, TakesForm, SearchTakesForm
from datetime import datetime

from utils import get_tutor_id, get_course_id, count_courses
from update_hours import add_hours


def index(request):
    return render(request, 'index.html')
   

def addTutor(request):
    return render(request, 'addTutor.html')


def help(request):
    return render(request, 'help.html')


def add_subtopic_session(request):
    return render(request, 'session.html')


def add_25_logged_hours(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')

        tid = get_tutor_id(name)
        tutor = get_object_or_404(Tutor, id = tid)

        request.session['tutor_id'] = tutor.id

        date = datetime.strptime(date, '%Y-%m-%d').date()

        if tutor.logged_25_hours_level_1 is None:
            Tutor.objects.filter(id = tid).update(logged_25_hours_level_1 = date)

        elif tutor.logged_25_hours_level_2 is None:
            Tutor.objects.filter(id  = tid).update(logged_25_hours_level_2 = date)
            
        return update_level_logic(request, 'add_hours')

    return render(request, '25.html')


def add_tutor_session(request):
    if request.method == 'POST':
        #Data From Web Page# 
        name = request.POST.get('name')
        course = request.POST.get('course')
        semester = 'F23'
        #time = request.POST.get('time')
        #in_person = request.POST.get('inperson')
        #total = request.POST.get('total')
        date = request.POST.get('date')

        tid = get_tutor_id(name)

        # Retrieve the Tutor instance
        tutor = get_object_or_404(Tutor, id = tid)

        # Store tutor information in the session
        request.session['tutor_id'] = tutor.id

        #Update Queries#
        #add_hours(name, course, date, time, 0)

        date = datetime.strptime(date, '%Y-%m-%d').date()

        #semester = 'S' if date.month in (1, 2, 3, 4, 5) else 'F'
        #semester += str(date.year % 100)

        new_takes = Takes(tutor = Tutor.objects.get(id = id), sesson = Session.objects.get(subtopic_name = course, semester = semester), date = date)
        new_takes.save()

        if course == 'Review of Level 1':
            Tutor.objects.filter(id = id).update(review_level_1_completed = date)

        count_courses()

        return update_level_logic(request, 'add_hours')

    return render(request, 'index.html')


def update_level_logic(request, original_page_name):
    conditions_met = False 

    tutor_id = request.session.get('tutor_id')
    tutor = get_object_or_404(Tutor, id = tutor_id)

    if tutor.level == 0:
        conditions_met = (
            ((tutor.number_basic_courses_completed_level_1) +
            (tutor.number_communication_courses_completed_level_1) +
            (tutor.number_learningstudytechinque_courses_completed_level_1) +
            (tutor.number_ethicsequality_courses_completed_level_1) +
            (tutor.number_elective_courses_completed_level_1)) >= 10
            and (tutor.number_basic_courses_completed_level_1) >= 4
            and (tutor.number_communication_courses_completed_level_1) >= 2
            and (tutor.number_learningstudytechinque_courses_completed_level_1) >= 2
            and (tutor.number_ethicsequality_courses_completed_level_1) >= 1
            and (tutor.number_elective_courses_completed_level_1) >= 1
            and (tutor.level_1_hours_in_person) >= 5
            and (tutor.level_1_hours) >= 10
            and (tutor.logged_25_hours_level_1)
        )
    if tutor.level == 1:
        conditions_met = (
            (tutor.number_basic_courses_completed_level_2 +
            tutor.number_communication_courses_completed_level_2 +
            tutor.number_learningstudytechinque_courses_completed_level_2 +
            tutor.number_ethicsequality_courses_completed_level_2 +
            tutor.number_elective_courses_completed_level_2) >= 10
            and tutor.number_basic_courses_completed_level_2 >= 3
            and tutor.number_communication_courses_completed_level_2 >= 2
            and tutor.number_learningstudytechinque_courses_completed_level_2 >= 3
            and tutor.number_ethicsequality_courses_completed_level_2 >= 1
            and tutor.number_elective_courses_completed_level_2 >= 1
            and tutor.level_2_hours_in_person >= 5
            and tutor.level_2_hours >= 10
            and tutor.logged_25_hours_level_2
            and tutor.review_level_1_completed
        )

    if conditions_met:
        # Store the original page URL in the session
        request.session['original_page_url'] = request.build_absolute_uri()
        return render(request, 'update_level.html')
    else:
        # If conditions are not met, redirect back to the original page
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            # If referer is not available, redirect to a default page
            return redirect(original_page_name)  # Redirect to the original page passed as an argument


def update_level(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()

        # Retrieve tutor information from the session
        tutor_id = request.session.get('tutor_id')

        # Assuming the user is a Tutor, retrieve the Tutor instance
        tutor = get_object_or_404(Tutor, id = tutor_id)
        print(tutor.first_name)

        if not tutor.level_1_completion_date:
            tutor.level_1_completion_date = date
            tutor.level = 1
        elif not tutor.level_2_completion_date:
            tutor.level_2_completion_date = date
            tutor.level = 2
        tutor.save()

        # Get the original page URL from the session
        original_page_url = request.session.get('original_page_url')

        # Clear the session variable to avoid using it again
        request.session.pop('original_page_url', None)
        request.session.pop('tutor_id', None)

        # Redirect back to the original page or a default page if the URL is not available
        return redirect(original_page_url) #if original_page_url else redirect('default_page')

    # If accessed directly without a POST request, redirect to the update level page
    return redirect('update_level')


def search_tutors(request):
    if request.method == 'POST':
        form = TutorSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            search_tokens = search_query.split()  # Split the input into tokens (words)
            
            # Filter by both first name and last name using OR conditions
            tutors = Tutor.objects.none()
            for token in search_tokens:
                tutors |= Tutor.objects.filter(
                    first_name__icontains=token) | Tutor.objects.filter(
                        last_name__icontains=token)

            return render(request, 'search_tutors_results.html', {'tutors': tutors, 'search_query': search_query})
    else:
        form = TutorSearchForm()

    return render(request, 'search_tutors.html', {'form': form})


def edit_tutor(request, tutor_id):
    # Retrieve the Tutor instance from the database
    tutor = get_object_or_404(Tutor, id = tutor_id)

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a form instance with the submitted data and the instance of the Tutor
        form = TutorForm(request.POST, instance = tutor)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to a success page or wherever you want
            #return HttpResponseRedirect('/success/')
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        # If the request method is GET, create a form instance with the Tutor instance
        form = TutorForm(instance = tutor)

    # Render the template with the form
    return render(request, 'edit_tutor.html', {'form': form, 'tutor': tutor})


def search_takes(request):
    # Handle form submission
    if request.method == 'POST':
        form = SearchTakesForm(request.POST)

        if form.is_valid():
            tutor = form.cleaned_data['tutor']
            subtopic = form.cleaned_data['subtopic']
            date = form.cleaned_data['date']

            tid = get_tutor_id(tutor)
            cid = get_course_id(subtopic)

            # Filter Takes model based on search parameters
            takes = Takes.objects.none()
            takes = Takes.objects.filter(tutor = tid, subtopic = cid, date = date)

            return render(request, 'edit_takes.html', {'takes': takes, 'form': form})

    # If it's a GET request or form is invalid, render the search_takes template with the form
    else:
        form = SearchTakesForm()

    return render(request, 'search_takes.html', {'form': form})


def edit_takes(request, takes_id):
    takes = get_object_or_404(Takes, id = takes_id)

    if request.method == 'POST':
        form = TakesForm(request.POST, instance = takes)
        if form.is_valid():
            form.save()
            # Redirect or do something else upon successful form submission
            print('Form Changed')
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = TakesForm(instance = takes)

    return render(request, 'edit_takes.html', {'form': form, 'takes': takes})

def search(request):
    query = request.GET.get('q', '')
    if query:
        tid = get_tutor_id(query)
        print(tid)
        # Perform search operation, e.g., filter your models based on the query
        tutor = Tutor.objects.filter(id = tid)
        takes = Takes.objects.filter(tutor_id = tid)
    else:
        results = []

    return render(request, 'results.html', {'tutor': tutor, 'takes': takes})