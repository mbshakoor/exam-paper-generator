from django.urls import include, path
from . import views

app_name = "teacher"
urlpatterns = [
    path('fetchMetadata', views.PaperMetadeta.as_view(), name="fetch_metadata"),
    path('fetchHistory', views.Papers.as_view(), name="fetch_history"),
    path('fetchChapters', views.Chapters.as_view(), name="fetch_chapters"),
    path('fetchQuestionsFromLib', views.LibraryQuestions.as_view(), name="fetch_questions_from_lib"),
    path('addQuestionsToLib', views.LibraryQuestions.as_view(), name="add_questions_tp_lib"),
    path('fetchQuestionsFromPaper', views.PaperQuestions.as_view(), name="fetch_questions_from_paper"),
    path('addQuestionsToPaper', views.PaperQuestions.as_view(), name="add_questions_to_paper"),
    path('deleteQuestionsFromPaper', views.PaperQuestions.as_view(), name="delete_questions_from_paper"),
]
