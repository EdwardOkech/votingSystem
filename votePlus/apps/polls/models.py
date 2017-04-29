from django.db import models


class Question(models.Model):
    """
    this model stores our questions dataset
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    """
    A question's choice mapping model
    """
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)





