# -*- coding: utf-8 -*-
from django.db import models
from mypeoplebot import settings

# Create your models here.
class OAuthToken(models.Model):
    consumer_key = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)

class BotInfo(models.Model):
    oauth_token = models.ForeignKey(OAuthToken)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    callback = models.CharField(max_length=255, default=settings.BOT_CALLBACK_URL)
    profile_image = models.ImageField(upload_to='bot_info/profile_images/')

class Survey(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    result_help_description = models.TextField(null=True)

    @property
    def is_valid(self):
        questions = self.question_set.all()
        # check question
        if len(questions) <= 0:
            return False
        # check answer
        if len([question for question in questions if len(question.answer_set.all()) <= 0]) > 0:
            return False
        return True

    def test_create(self):
        self.question_set.all().delete()
        self.result_set.all().delete()
        test1 = self.question_set.create(content='test1??')
        test2 = self.question_set.create(content='test2??')
        test3 = self.question_set.create(content='test3??')
        test1.make_normal_answer_set()
        test2.make_normal_answer_set()
        test3.make_normal_answer_set()
        self.result_set.create(weight_end=5, description='낮은 숫자만 찍었고만')
        self.result_set.create(weight_start=6, weight_end=10, description='중간 숫자만 찍었고만')
        self.result_set.create(weight_start=11, description='높은 숫자만 찍었고만')

class Question(models.Model):
    survey = models.ForeignKey(Survey)
    content = models.CharField(max_length=255, null=True)

    def make_normal_answer_set(self):
        self.answer_set.all().delete()
        self.answer_set.create(content='매우 그렇다', weight=5)
        self.answer_set.create(content='다소 그렇다', weight=4)
        self.answer_set.create(content='보통이다', weight=3)
        self.answer_set.create(content='그렇지 않다', weight=2)
        self.answer_set.create(content='아주 그렇지 않다', weight=1)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    sequence = models.IntegerField(default=1)
    content = models.CharField(max_length=255, null=True)
    weight = models.IntegerField()

    class Meta:
        ordering = ['sequence', 'id']

    def save(self, *args, **kwargs):
        if not self.sequence or self.sequence == 1:
            answers = Answer.objects.filter(question = self.question).order_by('-sequence')
            if len(answers) <= 0:
                self.sequence = 1
            else:
                self.sequence = answers[0].sequence + 1
        return super(Answer, self).save(*args, **kwargs)

class Result(models.Model):
    survey = models.ForeignKey(Survey)
    code = models.CharField(max_length=255, null=True)
    weight_start = models.IntegerField(null=True)
    weight_end = models.IntegerField(null=True)
    description = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if self.weight_start is None:
            self.weight_start = -1000
        if self.weight_end is None:
            self.weight_end = 1000
        return super(Result, self).save(*args, **kwargs)

class AnswerLog(models.Model):
    buddy_id = models.CharField(max_length=255)
    answer = models.ForeignKey(Answer)
    pub_date = models.DateTimeField(auto_now_add=True)

class ResultLog(models.Model):
    buddy_id = models.CharField(max_length=255)
    result = models.ForeignKey(Result)
    pub_date = models.DateTimeField(auto_now_add=True)

# ############################################################
class Deck(models.Model):
    buddy_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
class Card(models.Model):
    deck = models.ForeignKey(Deck)
    side1 = models.TextField()
    side2 = models.TextField()
    tag = models.CharField(max_length=255, null=True)

    status = models.CharField(max_length=255) # normal, trash, know, dontknow
    flip_status = models.BooleanField(default=True)

    @property
    def front_side(self):
        if self.flip_status:
            return side1
        else:
            return side2

    @property
    def back_side(self):
        if self.flip_status:
            return side2
        else:
            return side1
        
class Status(models.Model):
    buddy_id = models.CharField(max_length=255, unique=True)
    deck = models.ForeignKey(Deck, null=True)
