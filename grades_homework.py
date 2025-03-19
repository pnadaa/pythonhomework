import json
import os.path
import time
from os import remove
input_error = "there was an input error, discard the results"

# GOALS: ADD GRADES, SAVE GRADES INTO A JSON, DO CALCULATIONS BASED OFF THE GRADES. input and stuff and whatever i am so confusedddddd
# might be good to save the grades into a dictionary ??? or an array i guess
# YIPPEEEE

#HOMEWORK TASK 
#store my uni grades: course code + mark 
#extension: order course by best to worst mark 
#average mark

# → after it has shown everything, you can enter the course code and it will show what mark you’ve got
def newline():
    print("")
def pause(duration):
    time.sleep(duration)

def initialise_and_load(user):
    """Loads grades from the json file being used to store the data. If the json file does not exist or is empty, return an empty dictionary.
    """
    grades = {}
    grades.update(load_grades(user))
    return grades

def load_grades(user):
    """
    Gets grades from the json file, if the file does not exist yet, return an empty dictionary.
    """
    # If the file exists, return the json data
    if os.path.exists(user) == True:
        return load_file(user)
    # Else, return an empty array.
    return {}

def load_file(user):
    """
    Loads the json file and returns the grades stored. If there is a formatting error in the json file, return an empty dictionary.
    """
    try:   
        file = open(user, "r")
        file_content = file.read()
        content = json.loads(file_content)
        file.close
        return content
    except json.decoder.JSONDecodeError:
        return {}

def write_file(content, user):
    """
    Writes any content parsed into this function into the json file.
    """
    stringcontent = json.dumps(content)
    file = open(user, 'w')
    file.write(stringcontent)
    file.close





async def view_grades(grades, message, usage):
    """
    Prints all currently saved grades in the order in which they were saved.
    Contains a check to ensure the space between the course and mark is consistent
    """
    existing_grades = check_for_grades(grades)
    marks = ""

    if check_for_grades(grades) == False:
        await message.reply("There aren't any courses saved yet.")
        return
    i = 0
    for n in grades:
        course_code = list(grades)[i]
        # spaces is to ensure that the spacing between the couse code and mark is consistent when printed out. Max len course code = 10
        spaces = 10 - len(course_code)
        marks+=(f"{list(grades)[i]}: {spaces * " "}{grades[f"{course_code}"]}\n")
        i = i + 1
    if usage == 0:
        await message.reply(f"Here are your courses in the order you entered them:\n```{marks}```")
    if usage == 1:
        await message.reply(f"Here are your courses from best to worst:\n```{marks}```")


def check_for_grades(grades):
    """
    Checks for whether or not there are any grades already saved. Returns False if there aren't any grades saved.
    """
    if len(grades) == 0:
        return False


async def add_grades(content, message, user):
    """
    This function breaks the >add grades mark input into components and saves the input into the respective json.
    Checks for whether or not the mark input is a valid number
    """
    grades_dict = {}
    course_code = content.split(" ")[1]
    course_code = course_code.upper()
    course_grade = content.split(" ")[2]
    input_error = False
    try:
        course_grade = float(course_grade)
    except (TypeError, ValueError):
        await message.reply("Please enter a number for the grade! Your mark has not been saved")
        input_error = True
    if input_error == False:
        # Store the course and grade into grades_dict
        grades_dict[f"{course_code}"] = course_grade
        k = 0
        saved_courses = list(grades_dict)[k]
        # Spaces ensures that the spacing between the course and the mark is consistent when printed
        spaces = 10 - len(saved_courses)
        await message.reply(f"Grades saved!\n{saved_courses}: {spaces * " "}{grades_dict[f"{saved_courses}"]}")
    old_grades = {}
    #Load existing grades from the json and add new grades to the old grades
    old_grades = initialise_and_load(user)
    new_grades = grades_dict
    old_grades.update(new_grades)
    write_file(old_grades, user)




def calculate_average(grades):
    """
    Calculates the average of the stored grades
    """
    if check_for_grades(grades) == False:
        return
    i = 0
    total = 0
    for x in range(len(grades)):
        marks = list(grades)[i]
        total = total + grades[f"{marks}"]
        i = i + 1
    average = total/len(grades)
    return [average,i]
    

async def rank_grades(grades,message):
    """
    Sorts the stored grades from best to worse and prints the sorted dict using the existing view_grades function.
    """
    if check_for_grades(grades) == False:
        await message.reply("There aren't any courses saved yet.")
        return
    # This sorting solution was found on stackoverflow here: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_grades = dict(sorted(grades.items(), key = lambda item: item[1], reverse = True))
    # Passes on the 1 classifier to view_grades. This is used to determine which explaination message is printed in view_grades. 
    await view_grades(sorted_grades,message,1)

async def get_mark(grades, course_code, message):
    """
    Checks whether it is possible to access the typed in course, replies the mark if it is successful.
    """
    if check_for_grades(grades) == False:
        await message.reply("There aren't any courses saved yet.")
        return
    try:
        mark = grades[f"{course_code}"]
        await message.reply(f"Your grade for {course_code} is {mark}")
    except (ValueError, TypeError, KeyError):
        await message.reply("That course was not found.")

async def delete_all(message,user):
    """
    Deletes all data for the specified user
    """
    if os.path.exists(user) == True:
        os.remove(user)
        await message.reply("Results have been deleted.")
        return True
    else:
        await message.reply("Results have been deleted.")
        return True


### Below are functions which are not used for the discord bot grades code.

# def exit():
#     print("Thank you for using the rat course service!")
#     newline()
#     return False


# if __name__ == "__grades_logger__":
#     grades_logger()




# def select_function(grades):
#     """
#     The main function of this program. It asks the user for a selection and forwards it to the relevent process.
#     """
    
#     newline()
#     print("Select a number below to start!")
#     print(">1: View all existing grades")
#     print(">2: Add new grades")
#     print(">3: View the average of your grades")
#     print(">4: Show your grades from best to worst")
#     print(">5: Show the mark for a particular course")
#     print(">6: Clear all my saved results")    
#     print(">7: Quit")
#     newline()
#     selection = input_text("Please select an option: ")
#     if content.startswith(">1"):
#         if check_for_grades(grades) == False:
#             return
#         print("Here are your courses in the order you entered them:")
#         view_grades(grades)
#         newline()
#     elif content.startswith(">2"):
#         #First loads previous grades into old_grades and recently added grades from add_grades() into new_grades
#         #Then adds new_grades into the old_grades dictionary and writes to grades.json
#         old_grades = grades
#         new_grades = add_grades()
#         old_grades.update(new_grades)
#         write_file(old_grades)
#         newline()
#     elif content.startswith(">3"):
#         calculate_average(grades)
#         newline()
#     elif content.startswith(">4"):
#         rank_grades(grades)
#         newline()
#     elif content.startswith(">5"):
#         get_mark(grades)
#         newline()
#     elif content.startswith(">6"):
#         # Checks for whether or not the delete_all function is successfully run.
#         # If the delete_all function proceeds successfully, returns False. This is for the main while True loop
#         # If False is returned, the main loop reinitialises the grades, since the previous onces have been wiped.
#         if delete_all() == True:
#             return False
#         newline()
#     elif content.startswith(">7"):
#         # exit() always returns False. Kept it this way if anything needs to be changed in the future
#         response = exit()
#         if response == False:
#             quit()
#     else:
#         print("You did not choose from the options. Please try again\n")
#         pause(1)

# def grades_logger():
#     grades = initialise_grades()
#     while True:
#         if select_function(grades) == False:
#             grades = initialise_grades()
#         pause(0.75)


# def changes_saved(grades_dict):
#     """
#     Prints out all the grades stored for addition. Typically run at the end of add_grades().
#     """
#     k = 0
#     newline()
#     print("Saved your provided courses:")
#     # Similar in logic to view_grades()
#     for n in grades_dict:
#         saved_courses = list(grades_dict)[k]
#         k = k + 1
#         spaces = 10 - len(saved_courses)
#         print(f"{saved_courses}: {spaces * " "}{grades_dict[f"{saved_courses}"]}")

# def input_text(explanatory_text):
#     """
#     The function used throughout the program for any input the user makes. The provided explanatory text is what is shown before the input.
#     """
#     selection = str(input(f"{explanatory_text}"))
#     return selection