import json
import os
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, event
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, mapper

from src.api import app
from src.api import settings as st

db = SQLAlchemy(app)


class CourseStudent(db.Model):
    __tablename__ = 'courses_students'

    course_id = Column(
        'course_id', Integer,
        ForeignKey('courses.course_id'), primary_key=True
    )
    student_id = Column(
        'student_id', Integer,
        ForeignKey('students.student_id'), primary_key=True
    )


class Course(db.Model):
    __tablename__ = 'courses'

    course_id = Column('course_id', Integer, primary_key=True)
    name = Column('name', String)
    duration = Column('duration', String)
    professor_id = Column(
        'professor_id', Integer, ForeignKey('professors.professor_id')
    )
    professor = relationship(
        'Professor',
        back_populates='courses',
        lazy='subquery'
    )
    students = relationship(
        'Student',
        secondary=CourseStudent.__table__,
        lazy='joined',
        viewonly=True
    )

    def __str__(self):
        return (
            f"This is the course {self.name}. "
            f"It is taught by professor {self.professor.name}"
        )

    def to_json(self):
        return {
            'course_id': self.course_id,
            'name': self.name,
            'duration': self.duration,
            'professor': self.professor.to_json()
        }


class Professor(db.Model):
    __tablename__ = 'professors'

    professor_id = Column('professor_id', Integer, primary_key=True)
    name = Column('name', String)
    age = Column('age', Integer)
    specialty = Column('specialty', String)
    courses = relationship(
        'Course',
        back_populates='professor',
        lazy='subquery'
    )

    def __str__(self):
        return (
            f"Hi, I'm the professor {self.name}, "
            f"I am {self.age} years old and "
            f"I teach {', '.join([c.name for c in self.courses])}"
        )

    def to_json(self):
        return {
            'professor_id': self.professor_id,
            'name': self.name,
            'age': self.age,
            'specialty': self.specialty,
        }


class Student(db.Model):
    __tablename__ = 'students'

    student_id = Column('student_id', Integer, primary_key=True)
    name = Column('name', String)
    age = Column('age', Integer)
    career = Column('degree', String)
    courses = relationship(
        'Course',
        secondary=CourseStudent.__table__,
        lazy='joined',
        viewonly=True
    )

    def __str__(self):
        return (
            f"Hi, my name is {self.name}, "
            f"I am {self.age} years old and I study {self.career}"
        )

    def to_json(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "career": self.career
        }


class Log(db.Model):
    __tablename__ = 'log'

    log_id = Column('log_id', Integer, primary_key=True)
    table_name = Column('table_name', String)
    operation = Column('operation', String)
    record_id = Column('record_id', Integer)
    old_values = Column('old_values', String)
    new_values = Column('new_values', String)
    timestamp = Column('timestamp', DateTime, default=datetime.now)

    def to_json(self):
        return {
            "log_id": self.log_id,
            "table_name": self.table_name,
            "operation": self.operation,
            "record_id": self.record_id,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "timestamp": self.timestamp
        }


def log_changes(mapper, connection, target):
    # Listener que captura los eventos que se producen en la bbdd
    # y los almancena en la tabla logs
    if isinstance(target, Log):
        return
    session = Session.object_session(target)
    if session and session.transaction is not None:
        table_name = target.__table__.name
        if hasattr(target, '__modified__'):
            operation = 'UPDATE'
            record_id = target.id
            old_values = {
                c.name: getattr(target, c.name)
                for c in target.__table__.columns
            }
            new_values = {
                c.name: getattr(target, c.name)
                for c in target.__table__.columns
            }
        elif hasattr(target, '__deleted__'):
            operation = 'DELETE'
            record_id = target.id
            old_values = {
                c.name: getattr(target, c.name)
                for c in target.__table__.columns
            }
            new_values = None
        else:
            operation = 'INSERT'
            record_id = None
            old_values = None
            new_values = {
                c.name: getattr(target, c.name)
                for c in target.__table__.columns
            }
        log_entry_values = {
            'table_name': table_name,
            'operation': operation,
            'record_id': record_id,
            'old_values': json.dumps(old_values) if old_values else None,
            'new_values': json.dumps(new_values) if new_values else None
        }
        connection.execute(Log.__table__.insert().values(log_entry_values))


def _initialize_data(session):
    # Inicializa la bbdd con la información de /jsons/school.json
    with open(os.path.join(st.INPUTS_PATH, st.SCHOOL_JSON_FILENAME), 'r') as f:
        data = json.load(f)

    session.bulk_insert_mappings(Student, data['students'])
    session.bulk_insert_mappings(Professor, data['professors'])
    session.bulk_insert_mappings(Course, data['courses'])
    session.commit()


with app.app_context():
    db.create_all()
    _initialize_data(db.session)
    Session = sessionmaker(bind=db.engine)

current_session = scoped_session(Session)
# Se asocia el listener para los eventos en bbdd
event.listen(mapper, 'after_insert', log_changes)
event.listen(mapper, 'after_update', log_changes)
event.listen(mapper, 'after_delete', log_changes)
