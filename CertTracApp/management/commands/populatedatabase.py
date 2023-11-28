from django.core.management.base import BaseCommand
from CertTracApp.models import Tutor, Takes, Course, InPersonTrainingSession, TotalTrainingSession
from datetime import datetime
import csv
from django.db import connection

main_csv_file = "CRLA Master Tracker.csv"

# List of training session CSV files
training_sessions = [
    "Pre-S22 Hours.csv", "Pre-S22 In-Person Hours.csv",
    "F22 Hours.csv", "F22 In-Person Hours.csv",
    "S23 Hours.csv", "S23 In-Person Hours.csv",
    "F23 Hours.csv", "F23 In-Person Hours.csv",
]


# UTILITY FUNCTIONS #

# Fills Tutor Table
def parse_tutors(file):
    '''
    Parses a CSV file and populates the Tutor table with data.

    Parameters:
        - file (str): The path to the CSV file to be parsed.

    This function reads a CSV file containing tutor information and populates the Tutor table in the database.

    The CSV file is expected to have the following columns:
    1. Tutor Name
    2. Email
    3. Date Hired
    4. Level 1 Hours
    5. Level 1 Hours In-Person
    6. Logged 25 Hours for Level 1
    7. Level 1 Completion Date
    8. Level 2 Hours
    9. Level 2 Hours In-Person
    10. Logged 25 Hours for Level 2
    11. Level 2 Completion Date

    The function processes the CSV data, extracts relevant columns, and calculates the tutor's level based on the information provided.

    The resulting tutor data is formatted and saved to the Tutor table in the database.

    Note: This function currently prints tutor entries but should be updated to save them to the database.

    Args:
        file (str): The path to the CSV file.

    Returns:
        None
    '''
    with open(file, 'r', newline='') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)

        # Initialize a counter for the current row
        current_row = 1

        # Iterate through the CSV rows
        for row in csv_reader:
            # Skip header rows
            if current_row > 3 and current_row < 115:
                tutor_name = row[0]

                # Extract first and last name from tutor_name
                first_name = tutor_name.split(", ")[1]
                last_name = tutor_name.split(", ")[0]

                # Process and format date values
                logged_25_hours_level_1 = process_date(row[28])
                level_1_complete = process_date(row[30])
                logged_25_hours_level_2 = process_date(row[60])
                level_2_complete = process_date(row[62])

                # Calculate tutor's level
                level = calculate_tutor_level(row[30], row[62])

                # Extract relevant columns
                email = row[1]
                date_hired = row[2]
                level_1_hours = row[26]
                level_1_hours_in_person = row[27]
                level_2_hours = row[58]
                level_2_hours_in_person = row[59]

                # Create a list with tutor entry data
                Tutor.objects.create(
                    first_name = first_name, 
                    last_name = last_name, 
                    email = email, 
                    date_hired = date_hired, 
                    level = level, 
                    level_1_hours = level_1_hours,
                    level_1_hours_in_person = level_1_hours_in_person, 
                    logged_25_hours_level_1 = logged_25_hours_level_1, 
                    level_1_completion_date = level_1_complete, 
                    level_2_hours = level_2_hours,
                    level_2_hours_in_person = level_2_hours_in_person, 
                    logged_25_hours_level_2 = logged_25_hours_level_2, 
                    level_2_completion_date = level_2_complete)

            current_row += 1

def process_date(date_str):
    '''
    Processes a date string in CSV format and converts it to "yyyy-mm-dd" format.

    Args:
        date_str (str): A date string in CSV format (e.g., "mm/dd/yy" or "mm/dd/yyyy").

    Returns:
        str: The processed date in "yyyy-mm-dd" format.
    '''
    if date_str and date_str != "N/A":
        try:
            return datetime.strptime(date_str, "%m/%d/%y").strftime("20%y-%m-%d")
        except:
            return datetime.strptime(date_str, "%m/%d/%Y").strftime("20%y-%m-%d")
    else:
        return None

def calculate_tutor_level(level_1, level_2):
    '''
    Calculates the tutor's level based on level 1 and level 2 completion status.

    Args:
        level_1 (str): Level 1 completion status.
        level_2 (str): Level 2 completion status.

    Returns:
        int: The tutor's level (0, 1, or 2).
    '''
    if level_1 != "N/A" and level_2:
        return 2
    if level_1 != "N/A" and not level_2:
        return 1
    if level_1 == "N/A" and not level_2:
        return 0


# Fills Takes Table
def parse_takes(file):
    '''
    Parses a CSV file and populates the Takes table with data.

    Parameters:
        - file (str): The path to the CSV file to be parsed.

    This function reads a CSV file containing information about courses taken by tutors and populates the Takes table in the database.

    The CSV file is expected to have specific columns, and the function processes these columns to extract information about tutors, courses, semesters, and dates.

    The resulting data is structured with the following columns:
    - ID: A unique identifier for each entry.
    - Name: The name of the tutor taking the course.
    - Course: The name of the course.
    - Semester: The semester in which the course was taken.
    - Date: The date when the course was taken.

    Note: This function currently prints the entries but should be updated to save them to the database.

    Args:
        file (str): The path to the CSV file.

    Returns:
        None
    '''
    # Define the indices of the columns you want to select (0, 3 - 25, 31 - 57)
    columns_to_select_indices = [0] + [i for i in range(3, 26)] + [i for i in range(31, 58)]

    with open(file, 'r', newline='') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)

        # Initialize a counter for the current row
        current_row = 1

        # Initialize a unique ID for each entry
        ID = 1 #tutor_instance = Tutor.objects.get(id = id)

        for row in csv_reader:
            if current_row == 3:
                # For row 3, generate a class list and header row
                class_list = [row[i] for i in columns_to_select_indices]

            if current_row > 3 and current_row < 115:
                name = row[0]
                class_num = 0

                for i in columns_to_select_indices:
                    if i != 0 and row[i]:
                        if " and " in row[i]:
                            dates = row[i].split(" and ")
                        elif " &" in row[i]:
                            dates = row[i].split(" &")
                        else:
                            dates = row[i].split(" & ")

                        for date in dates:
                            date = date.strip()

                            if date != "Pre-Update Certified 05/11/2022":
                                sem = date.split(" ")[0]
                                date = date.split(" ")[1]
                            else:
                                sem = "Pre-Update Certified"
                                date = "05/11/2022"

                            # Reverse Date
                            date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")

                            #columns_to_select = [ID if name != "McCannon, Michael" else -1] + [name] + [class_list[class_num]] + [sem] + [date]
                            Takes.objects.create(
                                tutor = ID,
                                course = class_list[class_num],
                                semester = sem,
                                date = date
                            )

                            
                    class_num += 1

                ID = ID + 1 #if name != "McCannon, Michael" else ID

            current_row += 1

# Fills Course Table
def parse_course(file):
    '''
    Parses a CSV file and populates the Course table with data.

    Parameters:
        - file (str): The path to the CSV file to be parsed.

    This function reads a CSV file containing course information and populates the Course table in the database.

    The CSV file is expected to have specific columns, and the function processes these columns to extract course information.

    The course information includes:
    - Course Name
    - Course Type (e.g., Basics, Communication, Learning & Study Techniques, Ethics & Equality, Electives)
    - Course Level (1 or 2)

    Note: This function currently prints course entries but should be updated to save them to the database.

    Args:
        file (str): The path to the CSV file.

    Returns:
        None
    '''
    columns_to_select_indices = [i for i in range(3, 26)] + [i for i in range(31, 58)]

    with open(file, 'r', newline='') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)

        current_row = 1

        # Iterate through the CSV rows
        for row in csv_reader:
            # Check if this is the row containing course information
            if current_row == 3:
                # Iterate through the selected columns
                for i in columns_to_select_indices:
                    if i < 31:
                        level = 1
                    else:
                        level = 2

                    # Determine the course type based on column ranges
                    type = determine_course_type(i)

                    name = row[i]

                    Course.objects.create(
                        name = name,
                        level = level,
                        subject = type
                    )

                # Exit the loop after processing the course information row
                break
            else:
                current_row += 1

def determine_course_type(column_index):
    '''
    Determines the course type based on the column index.

    Args:
        column_index (int): The index of the column in the CSV file.

    Returns:
        str: The course type (e.g., Basics, Communication, Learning & Study Techniques, Ethics & Equality, Electives).
    '''
    if column_index in range(3, 7) or column_index in range(31, 37):
        return "Basics"
    elif column_index in range(7, 11) or column_index in range(37, 43):
        return "Communication"
    elif column_index in range(11, 17) or column_index in range(43, 49):
        return "Learning & Study Techniques"
    elif column_index in range(17, 20) or column_index in range(49, 53):
        return "Ethics & Equality"
    elif column_index in range(20, 26) or column_index in range(53, 58):
        return "Electives"


# Fills InPersonTrainingSession and TotalTrainingSession Table
def parse_training_session(file):
    '''
    Parses a CSV file containing training session information and populates the InPersonTrainingSession and TotalTrainingSession tables with data.

    Parameters:
        - file (str): The path to the CSV file to be parsed.

    This function reads a CSV file containing training session records and determines whether the records should be added to the InPersonTrainingSession or TotalTrainingSession table based on the file name. It then populates the appropriate table with the data.

    The CSV file is expected to have specific columns, including the tutor's name, the date of the training session, and the training time in hours and minutes.

    If the file name contains "In-Person," the data is added to the InPersonTrainingSession table, and if not, it's added to the TotalTrainingSession table.

    Args:
        file (str): The path to the CSV file.

    Returns:
        None
    '''
    current_row = 1

    with open(file, 'r', newline='') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if current_row > 1:
                name = row[0]
                date = file.split(' ')[0]
                training_time = row[1]

                if "In-Person" in file:
                    InPersonTrainingSession.objects.create(
                        sub_topic = name,
                        date = date,
                        training_time = training_time
                    )
                else:
                    TotalTrainingSession.objects.create(
                        sub_topic = name,
                        date = date,
                        training_time = training_time
                    )
            
            current_row += 1

def count_courses():
    course_update_queries = '''
    UPDATE CertTracApp_tutor
    SET number_basic_courses_completed_level_1 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Basics'
                AND CertTracApp_course.level = 1
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_basic_courses_completed_level_2 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Basics'
                AND CertTracApp_course.level = 2
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_communication_courses_completed_level_1 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Communication'
                AND CertTracApp_course.level = 1
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_communication_courses_completed_level_2 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Communication'
                AND CertTracApp_course.level = 2
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_learningstudytechinque_courses_completed_level_1 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Learning & Study Techniques'
                AND CertTracApp_course.level = 1
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_learningstudytechinque_courses_completed_level_2 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Learning & Study Techniques'
                AND CertTracApp_course.level = 2
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_ethicsequality_courses_completed_level_1 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Ethics & Equality'
                AND CertTracApp_course.level = 1
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_ethicsequality_courses_completed_level_2 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Ethics & Equality'
                AND CertTracApp_course.level = 2
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_elective_courses_completed_level_1 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Electives'
                AND CertTracApp_course.level = 1
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );

    UPDATE CertTracApp_tutor
    SET number_elective_courses_completed_level_2 = (
        SELECT COUNT(DISTINCT course_name)  -- Use COUNT DISTINCT to count unique course names
        FROM (
            SELECT CertTracApp_course.name AS course_name
            FROM CertTracApp_takes
            JOIN CertTracApp_course ON CertTracApp_takes.course = CertTracApp_course.name
            WHERE 
                CertTracApp_takes.tutor = CertTracApp_tutor.id
                AND CertTracApp_course.subject = 'Electives'
                AND CertTracApp_course.level = 2
            GROUP BY course_name  -- Group by course name to count each unique course only once
        ) AS unique_courses
    );
    '''
    cursor = connection.cursor()
    queries = course_update_queries.split(';')
    for query in queries:
        with connection.cursor() as cursor:
            cursor.execute(query)

class Command(BaseCommand):
    help = 'Parses CSV Files to Populate Database'

    def handle(self, *args, **kwargs):
        #Do these first as they have no foreign keys
        parse_tutors(main_csv_file)
        parse_course(main_csv_file)

        #Takes foreign key Tutor and Course
        #Session foreign key to Course
        parse_takes(main_csv_file)
        for csv_file in training_sessions:
            parse_training_session(csv_file)
        count_courses()

