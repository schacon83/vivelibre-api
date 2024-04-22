from cerberus import Validator
from flask import Blueprint, jsonify, Response, abort, request
from sqlalchemy.exc import IntegrityError

from src.models import school

school_api = Blueprint('school_api', __name__)


@school_api.route(
    '/school/courses/<int:course_id>/students/<int:student_id>',
    methods=['post']
)
def post_course_student(course_id, student_id):
    with school.current_session() as session:
        course = session.query(school.Course).filter_by(
            course_id=course_id
        ).first()
        if not course:
            abort(404, description='Course not found')
        student = session.query(school.Student).filter_by(
            student_id=student_id
        ).first()
        if not student:
            abort(404, description='Student not found')

        course_student = school.CourseStudent(
            course_id=course_id,
            student_id=student_id
        )
        session.add(course_student)
        try:
            session.commit()
        except IntegrityError:
            abort(409, description='Student already registered in the course')

    return Response(status=200)


@school_api.route(
    '/school/courses/<int:course_id>/students',
    methods=['get']
)
def get_course_students(course_id):
    with school.current_session() as session:
        course = session.query(school.Course).filter_by(
            course_id=course_id
        ).first()
        if not course:
            abort(404, description='Course not found')

    return jsonify([student.to_json() for student in course.students])


@school_api.route(
    '/school/students/<int:student_id>/courses',
    methods=['get']
)
def get_student_courses(student_id):
    with school.current_session() as session:
        student = session.query(school.Student).filter_by(
            student_id=student_id
        ).first()
        if not student:
            abort(404, description='Student not found')

    return jsonify([course.to_json() for course in student.courses])


@school_api.route(
    '/school/students',
    methods=['get']
)
def get_students():
    v = Validator(
        {
            'career': {
                'type': 'string',
                'required': False
            }
        }
    )

    args = request.args.to_dict()
    if not v.validate(args):
        abort(422, description=v.errors)

    career = args.get('career')

    with school.current_session() as session:
        query = session.query(school.Student)
        if career:
            query = query.filter_by(career=career)
        students = query.all()

    return jsonify([student.to_json() for student in students])


@school_api.route(
    '/school/professors',
    methods=['get']
)
def get_professors():
    v = Validator(
        {
            'min_age': {
                'type': 'integer',
                'required': False,
                'coerce': to_integer
            },
            'max_age': {
                'type': 'integer',
                'required': False,
                'coerce': to_integer
            }
        }
    )

    args = request.args.to_dict()
    if not v.validate(args):
        abort(422, description=v.errors)

    args = v.document
    min_age = args.get('min_age')
    max_age = args.get('max_age')

    with school.current_session() as session:
        query = session.query(school.Professor)
        if min_age:
            query = query.filter(school.Professor.age >= min_age)
        if max_age:
            query = query.filter(school.Professor.age <= max_age)
        professors = query.all()

    return jsonify([professor.to_json() for professor in professors])


@school_api.route(
    '/school/courses',
    methods=['get']
)
def get_courses():
    with school.current_session() as session:
        courses = session.query(school.Course).all()

    return jsonify([course.to_json() for course in courses])


@school_api.route(
    '/school/logs',
    methods=['get']
)
def get_logs():
    with school.current_session() as session:
        logs = session.query(school.Log).all()

    return jsonify([log.to_json() for log in logs])


def to_integer(value):
    try:
        return int(value)
    except ValueError:
        return None
