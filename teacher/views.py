import base64
import json
import os

import docx as docx
from braces.views import CsrfExemptMixin
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from .models import *
from user.models import *
from django.contrib.auth.models import User, Group, Permission

from inaequo_server import response_codes
from . import serializers
import time


#####################
#
# Utility functions
#
#####################


current_time_in_ms = lambda: int(round(time.time() * 1000))

def get_title_from_doc(doc):
    title = ""
    for paragraph in doc.paragraphs:
        if len(title) > 90:
            break
        title += f"{paragraph.text[:90-len(title)]}"
    return title


##############
#
# API CALLS
#
##############


class PaperMetadeta(APIView):
    def get(self, request, format=None):
        boards = None
        levels = None
        classes = None
        subjects = None
        terms = None

        response = {
            "boards": [{
                "id": 1,
                "name": "Karachi",
                "levels": [{
                    "id": 1,
                    "name": "1",
                    "classes": [{
                        "id": 1,
                        "name": "11",
                        "subjects": [{
                            "id": 1,
                            "name": "Computer",
                        }, {
                            "id": 2,
                            "name": "Math",
                        }],
                    }, {
                        "id": 2,
                        "name": "12",
                        "subjects": [{
                            "id": 3,
                            "name": "Physics",
                        }, {
                            "id": 4,
                            "name": "Chemistry",
                        }],
                    }],
                }, {
                    "id": 2,
                    "name": "2",
                    "classes": [{
                        "id": 3,
                        "name": "11",
                        "subjects": [{
                            "id": 5,
                            "name": "English",
                        }, {
                            "id": 6,
                            "name": "Urdu",
                        }],
                    }, {
                        "id": 4,
                        "name": "12",
                        "subjects": [{
                            "id": 7,
                            "name": "Islamiyat",
                        }, {
                            "id": 8,
                            "name": "History",
                        }],
                    }],
                }],
            }, {
                "id": 2,
                "name": "Sindh",
                "levels": [{
                    "id": 3,
                    "name": "1",
                    "classes": [{
                        "id": 5,
                        "name": "11",
                        "subjects": [{
                            "id": 9,
                            "name": "Computer",
                        }, {
                            "id": 10,
                            "name": "Math",
                        }],
                    }, {
                        "id": 6,
                        "name": "12",
                        "subjects": [{
                            "id": 11,
                            "name": "Physics",
                        }, {
                            "id": 12,
                            "name": "Chemistry",
                        }],
                    }],
                }, {
                    "id": 4,
                    "name": "2",
                    "classes": [{
                        "id": 7,
                        "name": "11",
                        "subjects": [{
                            "id": 13,
                            "name": "English",
                        }, {
                            "id": 14,
                            "name": "Urdu",
                        }],
                    }, {
                        "id": 8,
                        "name": "12",
                        "subjects": [{
                            "id": 15,
                            "name": "Islamiyat",
                        }, {
                            "id": 16,
                            "name": "History",
                        }],
                    }],
                }],
            }],
            "terms": [{
                "id": 1,
                "name": "Mid",
            }, {
                "id": 2,
                "name": "Final",
            }],
            "response-code": response_codes.SUCCESSFUL,
        }

        return JsonResponse(response)


class Papers(APIView):
    def get(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        date_from = data.get("date-from", None)
        date_to = data.get("date-to", None)
        subject_id = data.get("subject-id", None)
        teacher_id = data.get("teacher-id", None)

        papers = Paper.objects.filter(organization_id__in=[1, organization.id])  # 1 is id of Inaqeuo by default

        if date_from:
            papers = papers.filter(created_on__gte=date_from)

        if date_to:
            papers = papers.filter(created_on__lte=date_to)

        if subject_id:
            papers = papers.filter(subect_id=subject_id)

        if teacher_id:
            papers = papers.filter(teacher_id=teacher_id)

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "papers": [serializers.PaperSerializer(paper).data for paper in papers.all()],
            "papers-approved": papers.filter(status="approved").count(),
            "papers-pending": papers.filter(status="pending").count(),
            "papers-rejected": papers.filter(status="rejected").count(),
        }

        return JsonResponse(response)


class Chapters(APIView):
    def get(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        board_id = data.get("board-id", None)
        level_id = data.get("level-id", None)
        class_id = data.get("class-id", None)
        subject_id = data.get("subject-id", None)

        chapters = Chapter.objects

        if board_id:
            chapters = chapters.filter(subject__school_class__level__board_id=board_id)

        if level_id:
            chapters = chapters.filter(subject__school_class__level_id=level_id)

        if class_id:
            chapters = chapters.filter(subject__school_class_id=class_id)

        if subject_id:
            chapters = chapters.filter(subject_id=subject_id)

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "chapters": [serializers.ChapterSerializer(chapter).data for chapter in chapters.all()],
        }

        return JsonResponse(response)


class LibraryQuestions(CsrfExemptMixin, APIView):
    # Fetch questions from library
    def get(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        board_id = data.get("board-id", None)
        level_id = data.get("level-id", None)
        class_id = data.get("class-id", None)
        subject_id = data.get("subject-id", None)
        chapter_ids = data.get("chapter-ids", None)
        question_type = data.get("question-type", None)

        questions = Question.objects.filter(organization_id__in=[1, organization.id])
        if board_id:
            questions = questions.filter(subject__school_class__level__board_id=board_id)
        else:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'board_id' not found",
            }
            return JsonResponse(response)

        if level_id:
            questions = questions.filter(subject__school_class__level_id=level_id)
        if class_id:
            questions = questions.filter(subject__school_class_id=class_id)
        if subject_id:
            questions = questions.filter(subject_id=subject_id)
        if chapter_ids:
            questions = questions.filter(chapters__in=chapter_ids)
        if question_type:
            questions = questions.filter(type=question_type)

        serialized_questions = []
        for question in questions.all():
            serialized_question = serializers.LibraryQuestionSerializer(question).data
            serialized_question["current-paper"] = request.user.profile.current_paper_id in [x.id for x in question.paper_set.all()]
            serialized_questions.append(serialized_question)

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "questions": serialized_questions,
        }

        return JsonResponse(response)

    # Add questions to library
    def post(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization
        serialized_questions = []

        # Data validation
        questions = data.get("questions", None)

        if not questions:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'questions' not found, empty list, or invalid",
            }
            return JsonResponse(response)

        for question in questions:
            title = question.get("question-title", None)
            if title is None:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'question.question-title' not found, or invalid",
                }
                return JsonResponse(response)

            title = question.get("question-title", None)
            if title is None:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'question.question-title' not found, or invalid",
                }
                return JsonResponse(response)

            title_is_not_provided = not title

            type = question.get("question-type", None)
            if type is None:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'question.question-type' not found, or invalid",
                }
                return JsonResponse(response)

            subject_id = question.get("subject-id", None)
            if subject_id is None:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'question.subject-id' not found, or invalid",
                }
                return JsonResponse(response)

            chapter_ids = question.get("chapters-ids", None)
            if not chapter_ids:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'question.chapter_ids' not found, empty or invalid",
                }
                return JsonResponse(response)

            file_str_64 = question.get("question-file", None)
            if file_str_64 is None:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'question.question-file' not found, or invalid",
                }
                return JsonResponse(response)

            file_str = base64.b64decode(file_str_64)
            file_name = f"{current_time_in_ms()}{title}.docx"
            rel_path = f"/static/data_files/{file_name}"
            abs_path = f"{os.path.abspath('')}/inaequo_server{rel_path}"

            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as file:
                file.write(file_str)

            docx_file = docx.Document(abs_path)
            if title_is_not_provided:
                title = get_title_from_doc(docx_file)

            question = Question.objects.create(
                title=title,
                description=type,
                organization=organization,
                subject_id=subject_id,
                chapter_id=chapter_ids,
                file_path=rel_path,
            )
            question.chapters.add(chapter_ids)
            question.save()
            serialized_questions.append(
                serializers.QuestionSerializer(question).data
            )

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "questions": serialized_questions,
        }
        return JsonResponse(response)

    # Delete questions from library
    def delete(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        questions = data.get("questions", None)

        if not questions:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'questions' not found, empty list, or invalid",
            }
            return JsonResponse(response)

        question_ids = [question.get("id", None) for question in questions]

        if any(x in question_ids for x in ["", None]):  # Check if question_ids doesn't contain all valid ids (no None or empty)
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "One or more 'id' in 'questions' is empty, None, or invalid",
            }
            return JsonResponse(response)

        question_objs = Question.objects.filter(id__in=question_ids).all()

        if question_objs.count() is not len(question_ids):  # If any provided question does not exist in the database
            response = {
                "response-code": response_codes.ITEM_DOES_NOT_EXIST,
                "error": "One or more objects mapped to 'id' in 'questions' does not exist in the database.",
            }
            return JsonResponse(response)

        if question_objs.filter(organization_id=1).count() > 0:  # If given questions contains an Inaequo question
            response = {
                "response-code": response_codes.ACCESS_DENIED,
                "error": "One or more objects mapped to 'id' in 'questions' can not be modified.",
            }
            return JsonResponse(response)

        serialized_questions = [serializers.QuestionSerializer(question).data for question in question_objs]

        question_objs.delete()

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "questions": serialized_questions,
        }
        return JsonResponse(response)


class PaperQuestions(CsrfExemptMixin, APIView):
    # Fetch questions from paper
    def get(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        paper_id = data.get("paper_id", None)

        paper = Paper.objects.filter(id__in=[1, organization.id])
        if paper_id:
            paper = paper.filter(id=paper_id).first()
            if paper:
                questions = paper.questions
            else:
                response = {
                    "response-code": response_codes.ITEM_DOES_NOT_EXIST,
                    "error": "Provided paper_id does not map to a corresponding Paper related to this organization",
                }
                return JsonResponse(response)
        else:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'paper_id' not found",
            }
            return JsonResponse(response)

        serialized_questions = []
        for question in questions.all():
            serialized_question = serializers.QuestionSerializer(question).data
            serialized_question["current-paper"] = request.user.profile.current_paper_id in [x.id for x in question.paper_set.all()]
            serialized_questions.append(serialized_question)

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "questions": serialized_questions,
        }

        return JsonResponse(response)

    # Add questions to paper
    def post(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        paper_id = data.get("paper-id", None)
        questions = data.get("questions", None)

        if paper_id is None:
            paper = user.profile.current_paper
        elif not paper_id:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'paper-id' not found or invalid",
            }
            return JsonResponse(response)
        else:
            paper = Paper.objects.filter(organization_id__in=[1, organization.id], id=paper_id).first()
            if not paper:
                response = {
                    "response-code": response_codes.ITEM_DOES_NOT_EXIST,
                    "error": "Provided paper_id does not map to a corresponding Paper related to this organization",
                }
                return JsonResponse(response)

        if not questions:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'questions' not found, empty list, or invalid",
            }
            return JsonResponse(response)

        serialized_questions = []
        for question in questions:
            if not question.id:
                response = {
                    "response-code": response_codes.INVALID_KEY,
                    "error": "Required parameter 'id' in list 'questions' not found",
                }
                return JsonResponse(response)
            question = Question.objects.filter(id=question.id).all()
            paper.questions.add(question)
            serialized_questions.push(serializers.QuestionSerializer(question).data)

        paper.save()

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "paper-id": paper.id,
            "questions": serialized_questions,
        }
        return JsonResponse(response)

    # Delete questions from paper
    def delete(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        paper_id = data.get("paper-id", None)
        questions = data.get("questions", None)

        if paper_id is None:
            paper = user.profile.current_paper
        elif not paper_id:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'paper-id' not found or invalid",
            }
            return JsonResponse(response)
        else:
            paper = Paper.objects.filter(organization_id__in=[1, organization.id], id=paper_id).first()
            if not paper:
                response = {
                    "response-code": response_codes.ITEM_DOES_NOT_EXIST,
                    "error": "Provided paper_id does not map to a corresponding Paper related to this organization",
                }
                return JsonResponse(response)

        if not questions:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'questions' not found, empty list, or invalid",
            }
            return JsonResponse(response)

        question_ids = [question.get("id", None) for question in questions]

        if any(x in question_ids for x in ["", None]):  # Check if question_ids doesn't contain all valid ids (no None or empty)
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "One or more 'id' in 'questions' is empty, None, or invalid",
            }
            return JsonResponse(response)

        question_objs = paper.questions.filter(id__in=question_ids).all()

        if question_objs.count() is not len(question_ids):  # If any provided question does not exist in the paper
            response = {
                "response-code": response_codes.ITEM_DOES_NOT_EXIST,
                "error": "One or more objects mapped to 'id' in 'questions' does not exist in the paper.",
            }
            return JsonResponse(response)

        serialized_questions = [serializers.QuestionSerializer(question).data for question in question_objs]

        paper.questions.remove(question_objs)
        paper.save()

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "paper-id": paper.id,
            "questions": serialized_questions,
        }
        return JsonResponse(response)


class QuestionFile(APIView):
    # View question (file)
    def get(self, request, format=None):
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        organization = profile.organization

        # Data validation
        question_id = data.get("question-id", None)

        if not question_id:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'question-id' not found",
            }
            return JsonResponse(response)

        question = Question.objects.filter(id=question_id).first()

        if not question:
            response = {
                "response-code": response_codes.INVALID_KEY,
                "error": "Required parameter 'question-id' not found",
            }
            return JsonResponse(response)

        # Getting file from file path of question object
        abs_path = f"{os.path.abspath('')}/inaequo_server{question.file_path}"

        with open(abs_path, "r") as f:
            file_str = f.read()

        file_str_64 = base64.b64encode(file_str)

        response = {
            "response-code": response_codes.SUCCESSFUL,
            "question-id": question_id,
            "question-text": file_str_64,
        }

        return JsonResponse(response)


def submit_paper_to_reviewer(request):

    return JsonResponse({})


def generate_papers(request):  # To accept papers
    return JsonResponse({})


def reject_paper(request):
    return JsonResponse({})
