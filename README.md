# MiniORM 

## Overview

MiniORM is a very simple ORM (Object-Relational Mapping) library inspired by the functionality of more comprehensive ORMs like those found in Odoo and Django. It is designed for educational purposes to help understand how ORMs abstract database calls, simplifying interactions with databases for developers.

### Supported Database

- SQLite (for simplicity and ease of use)

```python
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


print(person1.name)
person1.name="Daviti"
person1.save()
print(person1.name)


# Create instances of Enrollment
enrollment1 = Enrollment(student=person1.id, course=course1.id)
enrollment2 = Enrollment(student=person1.id, course=course2.id)
enrollment3 = Enrollment(student=person2.id, course=course1.id)

enrollment1.save()
enrollment2.save()
enrollment3.save()


print(course1.enrolled_students)

search_course = Course.search([('name', '=', 'Mathematics')])
print(search_course)

```

## Features

MiniORM currently supports the following features:

- [x] **Automatic Database Table Creation Based on Models:** Automatically creates database tables for defined models, eliminating the need for manual SQL table creation.
- [x] **Create New Record:** Provides functionality to create new records in the database directly from model instances.
- [x] **Update Record:** Allows updating existing records in the database with new values.
- [x] **Search Record:** Enables searching for records in the database based on criteria defined in queries.
- [x] **Many-to-One (ForeignKey) Relationships:** Supports Many-to-One relationships, allowing models to reference other models via foreign keys.
- [x] **One-to-Many Relationships:** Enables defining One-to-Many relationships between models, facilitating the representation of inverse relationships.
- [ ] **Deleting Records:** (Future feature) Will allow deletion of records from the database.
- [ ] **Many-to-Many Relationships:** (Future feature) Plans to support Many-to-Many relationships between models.

- [ ] Validations 

## How to Use

1. **Define Models:** Start by defining your models, inheriting from a base class provided by MiniORM. Define your fields and relationships in the model.
2. **Initialize Database:** Use MiniORM to initialize your database connection, specifying your SQLite database file.
3. **Automatic Table Creation:** Upon initialization, MiniORM will automatically create tables for your models if they do not exist.
4. **CRUD Operations:** Utilize MiniORM's methods to create, read, update, and (in the future) delete records.


