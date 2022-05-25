from teacher.models import *
from user.models import *


class PaperSerializer:
    data = None

    def __init__(self, paper):
        data = {
            "id": paper.id,
            "title": paper.title,
            "teacher-id": paper.teacher_id,
            "date-generated": paper.date_generated,
            "status": paper.status,
        }


class ChapterSerializer:
    data = None

    def __init__(self, chapter):
        data = {
            "id": chapter.id,
            "title": chapter.title,
            "subject-id": chapter.subject_id,
        }


class LibraryQuestionSerializer:
    data = None

    def __init__(self, question):
        data = {
            "id": question.id,
            "title": question.title,
            "is-inaequo-lib": question.organization.id == 1,
            "type": question.type,
            "file-path": question.file_path,
            "subject-id": question.subject_id,
            "marks": question.marks,
        }


class QuestionSerializer:
    data = None

    def __init__(self, question):
        data = {
            "id": question.id,
            "title": question.title,
            "is-inaequo-lib": question.organization.id == 1,
            "type": question.type,
            "subject-id": question.subject_id,
            "file-path": question.file_path,
            "marks": question.marks,
        }
