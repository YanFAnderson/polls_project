from rest_framework import serializers

from .models import Poll, Question, Value, Answer


class ValueSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    value = serializers.CharField(max_length=55)

    class Meta:
        model = Value

    def create(self, validated_data):
        return Value.objects.create(**validated_data)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())
    text = serializers.CharField(max_length=255, allow_null=False, allow_blank=True)

    TYPE_CHOICES = [
        ('TYPE_TEXT', 'Text'),
        ('TYPE_SINGLE_CHOICE', 'Single choice'),
        ('TYPE_MULTIPLE_CHOICE', 'Multiple choice')
    ]

    type = serializers.ChoiceField(choices=TYPE_CHOICES, allow_null=False, allow_blank=False)
    values = ValueSerializer(required=True, many=True)

    class Meta:
        model = Question

    def create(self, validated_data):
        values_data = validated_data.pop('values')
        values = []
        for value_data in values_data:
            values.append(Value.objects.create(**value_data).id)
        question = Question.objects.create(**validated_data)
        question.values.set(values)
        return question

    def update(self, instance, validated_data):
        instance.poll = validated_data.get("poll", instance.poll)
        instance.text = validated_data.get("text", instance.text)
        instance.type = validated_data.get("type", instance.type)
        if "values" in validated_data:
            for value in instance.values.all():
                value.delete()
            values_data = validated_data.pop('values')
            values = []
            for value_data in values_data:
                values.append(Value.objects.create(**value_data).id)
            instance.values.set(values)
        instance.save()
        return instance


class AnswerSerializer(serializers.Serializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    text = serializers.CharField(max_length=255, allow_null=False, allow_blank=True)
    values_answer = serializers.PrimaryKeyRelatedField(queryset=Value.objects.all(), many=True)
    user_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = Answer

    def create(self, validated_data):
        values = validated_data.pop("values_answer")
        answer = Answer.objects.create(**validated_data)
        answer.values_answer.set(values)
        return answer


class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=120, allow_null=False, allow_blank=False)
    start_date = serializers.DateField(allow_null=False)
    end_date = serializers.DateField(allow_null=False)
    description = serializers.CharField(max_length=255, allow_null=False, allow_blank=True)
    questions = QuestionSerializer(many=True, required=False, read_only=True)
    answers = AnswerSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Poll

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class AvailableSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
