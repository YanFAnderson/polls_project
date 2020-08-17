from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    description = models.CharField(max_length=255, blank=True, null=False)

    class Meta:
        app_label = "api"


class Question(models.Model):
    poll = models.ForeignKey("Poll", related_name="questions", on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255, null=False)

    TYPE_CHOICES = [
        ('TYPE_TEXT', 'Text'),
        ('TYPE_SINGLE_CHOICE', 'Single choice'),
        ('TYPE_MULTIPLE_CHOICE', 'Multiple choice')
    ]

    type = models.CharField(max_length=55, choices=TYPE_CHOICES, default='TEXT', null=False, blank=False)
    values = models.ManyToManyField("Value", related_name="values", null=True, blank=True)

    class Meta:
        app_label = "api"


class Answer(models.Model):
    poll = models.ForeignKey("Poll", related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", related_name="answer", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False, blank=True)
    user_id = models.IntegerField(null=False, blank=False)
    values_answer = models.ManyToManyField("Value", related_name="values_answer")

    class Meta:
        app_label = "api"


class Value(models.Model):
    value = models.CharField(max_length=55, null=False, blank=False)

    class Meta:
        app_label = "api"
