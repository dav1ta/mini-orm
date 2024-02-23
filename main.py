import fields
from orm import Model

class People(Model):
    name = fields.Char()
    age = fields.Int()
    is_student = fields.Boolean()
    bio = fields.Text()

class Course(Model):
    name = fields.Char()
    enrolled_students = fields.One2many('Enrollment', 'course')


class Enrollment(Model):
    student = fields.Many2one(People)
    course = fields.Many2one(Course)

# Create instances of People and Course
person1 = People(name="Dato", age=22, is_student=True, bio="I am a student.")
person2 = People(name="Alice", age=25, is_student=True, bio="I am also a student.")
course1 = Course(name="Mathematics")
course2 = Course(name="Physics")

# Saving instances
person1.save()
person2.save()
course1.save()
course2.save()

# Create instances of Enrollment
enrollment1 = Enrollment(student=person1.id, course=course1.id)
enrollment2 = Enrollment(student=person1.id, course=course2.id)
enrollment3 = Enrollment(student=person2.id, course=course1.id)

enrollment1.save()
enrollment2.save()
enrollment3.save()

# # Retrieving related courses for a person
# person1_courses = [enrollment.course for enrollment in Enrollment._instances if enrollment.student == person1]
# print(f"{person1.name}'s courses: {[course.name for course in person1_courses]}")

# # Retrieving enrolled people in a course
# course1_people = [enrollment.student for enrollment in Enrollment._instances if enrollment.course == course1]
# print(f"People enrolled in {course1.name}: {[person.name for person in course1_people]}")
print(course1.enrolled_students)

# a = Course.search([('name', '=', 'Mathematics')])
# print(a,"gg")
