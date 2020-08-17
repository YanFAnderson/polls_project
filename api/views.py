from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Question
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer, AvailableSerializer


class PollListView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        polls = Poll.objects.all()
        serialized = PollSerializer(polls, many=True).data
        return Response({"polls": serialized}, status=status.HTTP_200_OK)


class PollAddView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Created successfully"}, status.HTTP_200_OK)


class PollEditView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.data:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        if "start_date" in request.data:
            return Response("start_date can't be edit", status=status.HTTP_400_BAD_REQUEST)
        saved_poll = Poll.objects.get(id=request.data["id"])
        serializer = PollSerializer(instance=saved_poll, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Updated successfully"}, status.HTTP_200_OK)


class PollDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.data:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        poll = Poll.objects.get(id=request.data["id"])
        print(poll)
        poll.delete()
        return Response({"success": "Deleted successfully"}, status.HTTP_200_OK)


class QuestionListView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "poll_id" not in request.data:
            return Response("Please, specify the poll_id", status=status.HTTP_400_BAD_REQUEST)
        questions = Question.objects.filter(poll__id=request.data["poll_id"])
        serialized = QuestionSerializer(questions, many=True).data
        return Response({"questions": serialized}, status.HTTP_200_OK)


class QuestionAddView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Created successfully"}, status.HTTP_200_OK)


class QuestionEditView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.data:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        saved_question = Question.objects.get(id=request.data["id"])
        serializer = QuestionSerializer(instance=saved_question, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Updated successfully"}, status.HTTP_200_OK)


class QuestionDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.data:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.get(id=request.data["id"])
        for value in question.values.all():
            value.delete()
        question.delete()
        return Response({"success": "Deleted successfully"}, status.HTTP_200_OK)


class AnswerAddView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        answer = AnswerSerializer(data=request.data)
        if answer.is_valid(raise_exception=True):
            poll = Poll.objects.get(id=request.data["poll"])
            if not poll:
                return Response("Incorrect poll id", status=status.HTTP_400_BAD_REQUEST)
            question = poll.questions.get(id=request.data["question"])
            if not question:
                return Response("Incorrect question id", status=status.HTTP_400_BAD_REQUEST)
            serialized = QuestionSerializer(question).data
            if serialized["type"] == "TYPE_SINGLE_CHOICE" or "TYPE_MULTIPLE_CHOICE":
                for value_id in request.data["values_answer"]:
                    if not question.values.filter(id=value_id):
                        return Response("Incorrect values", status=status.HTTP_400_BAD_REQUEST)
            if serialized["type"] == "TYPE_TEXT" and request.data["text"] is "":
                return Response("Please, fill the answer", status=status.HTTP_400_BAD_REQUEST)
            if serialized["type"] == "TYPE_SINGLE_CHOICE" and len(request.data["values_answer"]) > 1:
                return Response("Please, choose one value", status=status.HTTP_400_BAD_REQUEST)
            answer.save()
        return Response({"success": "Created successfully"}, status.HTTP_200_OK)


class AnswerListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "user_id" not in request.data:
            return Response("Please, specify the user_id", status=status.HTTP_400_BAD_REQUEST)
        polls = Poll.objects.all().filter(questions__answer__user_id=request.data["user_id"])
        serialized = PollSerializer(polls, many=True).data
        return Response({"answers": serialized}, status=status.HTTP_200_OK)


class PollAvailableView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        polls = Poll.objects.all()
        serialized = AvailableSerializer(polls, many=True).data
        return Response({"polls": serialized}, status=status.HTTP_200_OK)
