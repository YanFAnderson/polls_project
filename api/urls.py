from django.urls import path

from .views import PollListView, PollAddView, QuestionListView, QuestionAddView, AnswerAddView, AnswerListView, \
    PollAvailableView, PollEditView, QuestionEditView, PollDeleteView, QuestionDeleteView

urlpatterns = [
    path('poll/list', PollListView.as_view()),
    path('poll/add', PollAddView.as_view()),
    path('question/list', QuestionListView.as_view()),
    path('question/add', QuestionAddView.as_view()),
    path('answer/add', AnswerAddView.as_view()),
    path('answer/list', AnswerListView.as_view()),
    path('poll/available', PollAvailableView.as_view()),
    path('poll/edit', PollEditView.as_view()),
    path('question/edit', QuestionEditView.as_view()),
    path('poll/delete', PollDeleteView.as_view()),
    path('question/delete', QuestionDeleteView.as_view()),
]
