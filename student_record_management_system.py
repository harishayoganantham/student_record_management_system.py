"""
STUDENT RECORD MANAGEMENT SYSTEM
Task 2 - File-based student record management

Features:
1. Add student
2. View all students
3. Search student
4. Update student
5. Delete student
6. Performance report
7. Save and load records using a JSON file

Pass rule: PASS when every subject mark is 40 or above.
Records are loaded from students.json when the program starts and saved
automatically whenever records are added, updated, or deleted.
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.json")
PASS_MARK = 40


def load_records():
    """Load student records from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            print("Warning: The data file format is invalid. Starting with no records.")
            return []

        return records

    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load records: {error}")
        return []


def save_records(students):
    """Save all student records to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError as error:
        print(f"Could not save records: {error}")
        return False


def get_marks():
    """Read a comma-separated list of marks and validate the values."""
    while True:
        raw_marks = input("Marks (comma-separated): ").strip()

        try:
            marks = [float(value.strip()) for value in raw_marks.split(",")]
            if not marks:
                raise ValueError
            if any(mark < 0 or mark > 100 for mark in marks):
                print("Each mark must be between 0 and 100.")
                continue
            return marks
        except ValueError:
            print("Enter valid marks separated by commas, for example: 78,85,72")


def get_attendance():
    """Read and validate attendance percentage."""
    while True:
        try:
            attendance = float(input("Attendance (%): ").strip())
            if 0 <= attendance <= 100:
                return attendance
            print("Attendance must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def calculate_average(student):
    """Calculate the average mark for one student."""
    marks = student.get("marks", [])
    return sum(marks) / len(marks) if marks else 0.0


def get_result(student):
    """Return PASS if all subject marks meet the pass mark."""
    marks = student.get("marks", [])
    return "PASS" if marks and all(mark >= PASS_MARK for mark in marks) else "FAIL"


def find_student_indices(students, name):
    """Find all matching student names, ignoring letter case."""
    return [
        index for index, student in enumerate(students)
        if student["name"].casefold() == name.casefold()
    ]


def choose_student(students, indices):
    """Choose a record when more than one student has the same name."""
    if len(indices) == 1:
        return indices[0]

    print("More than one student has that name:")
    for number, index in enumerate(indices, start=1):
        student = students[index]
        print(f"{number}. {student['name']} - {student['department']}")

    while True:
        try:
            choice = int(input("Choose record number: "))
            if 1 <= choice <= len(indices):
                return indices[choice - 1]
            print("Select a number from the list.")
        except ValueError:
            print("Enter a valid number.")


def add_student(students):
    """Collect details and add a new student."""
    print("\nADD STUDENT")
    name = input("Student Name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Student Name: ").strip()

    department = input("Department: ").strip()
    while not department:
        print("Department cannot be empty.")
        department = input("Department: ").strip()

    marks = get_marks()
    attendance = get_attendance()

    students.append({
        "name": name,
        "department": department,
        "marks": marks,
        "attendance": attendance
    })

    if save_records(students):
        print("Student added successfully.")


def view_students(students):
    """Display all saved student records."""
    print("\nSTUDENT RECORDS")
    print("-" * 55)

    if not students:
        print("No student records found.")
        return

    for number, student in enumerate(students, start=1):
        print(f"\nStudent {number}")
        print(f"Name: {student['name']}")
        print(f"Department: {student['department']}")
        print(f"Marks: {', '.join(str(mark) for mark in student['marks'])}")
        print(f"Average: {calculate_average(student):.1f}%")
        print(f"Attendance: {student['attendance']:.1f}%")


def search_student(students):
    """Search for a student by exact name, ignoring letter case."""
    print("\nSEARCH STUDENT")
    name = input("Search: ").strip()
    matches = find_student_indices(students, name)

    if not matches:
        print("Student not found.")
        return

    index = choose_student(students, matches)
    student = students[index]

    print("\nStudent Found")
    print("-" * 20)
    print(f"Name: {student['name']}")
    print(f"Department: {student['department']}")
    print(f"Average: {calculate_average(student):.1f}%")
    print(f"Attendance: {student['attendance']:.1f}%")


def update_student(students):
    """Update the details of an existing student."""
    print("\nUPDATE STUDENT")
    name = input("Enter the student name to update: ").strip()
    matches = find_student_indices(students, name)

    if not matches:
        print("Student not found.")
        return

    index = choose_student(students, matches)
    student = students[index]

    print("Enter the new details.")
    new_name = input(f"Student Name [{student['name']}]: ").strip()
    new_department = input(
        f"Department [{student['department']}]: "
    ).strip()

    print("Enter new marks:")
    new_marks = get_marks()
    new_attendance = get_attendance()

    if new_name:
        student["name"] = new_name
    if new_department:
        student["department"] = new_department
    student["marks"] = new_marks
    student["attendance"] = new_attendance

    if save_records(students):
        print("Student updated successfully.")


def delete_student(students):
    """Delete a student record after confirmation."""
    print("\nDELETE STUDENT")
    name = input("Enter the student name to delete: ").strip()
    matches = find_student_indices(students, name)

    if not matches:
        print("Student not found.")
        return

    index = choose_student(students, matches)
    student = students[index]
    confirmation = input(
        f"Delete {student['name']}? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        removed = students.pop(index)
        if save_records(students):
            print(f"{removed['name']} deleted successfully.")
    else:
        print("Delete cancelled.")


def performance_report(students):
    """Display averages, results and the highest-performing student."""
    print("\nPERFORMANCE REPORT")
    print("-" * 55)

    if not students:
        print("No student records available.")
        return

    for student in students:
        print(
            f"{student['name']} | Average: {calculate_average(student):.1f}% "
            f"| Result: {get_result(student)}"
        )

    top_student = max(students, key=calculate_average)
    class_average = sum(
        calculate_average(student) for student in students
    ) / len(students)

    print("\nClass Summary")
    print(f"Total Students: {len(students)}")
    print(f"Average of Student Averages: {class_average:.1f}%")
    print(
        f"Top Performer: {top_student['name']} "
        f"({calculate_average(top_student):.1f}%)"
    )


def main():
    """Run the menu-driven student record management system."""
    students = load_records()
    print("Student Record Management System")
    print(f"{len(students)} record(s) loaded.")

    while True:
        print("\nChoose an option:")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Performance Report")
        print("7. Save Records")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            performance_report(students)
        elif choice == "7":
            if save_records(students):
                print("Records saved successfully.")
        elif choice == "8":
            save_records(students)
            print("Records saved. Thank you!")
            break
        else:
            print("Invalid option. Please choose from 1 to 8.")


if __name__ == "__main__":
    main()
