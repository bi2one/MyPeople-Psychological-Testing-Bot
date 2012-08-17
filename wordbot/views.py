# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from mypeoplebot import settings
from pbutils.oauthmanager import OAuthManager, BotManager
from wordbot.forms import BotUpdateForm, CreateSurveyForm, CreateQuestionForm, CreateAnswerForm, CreateResultForm
from wordbot.models import BotInfo, Survey, Question, Answer, Result
from pprint import pprint
import ujson

@csrf_exempt
def home(request):
    if request.method == 'POST':
        return callback(request)
    manager = OAuthManager(request)
    surveys = Survey.objects.all()
    return render_to_response('home.html',
                              dict(surveys=surveys,
                                   token = manager.token),
                              context_instance=RequestContext(request))

def oauth_callback(request):
    manager = OAuthManager(request)
    manager.create_access_token(request.GET['oauth_verifier'])
    messages.info(request, "토큰 발급 완료")
    return HttpResponseRedirect('/')

def get_token(request):
    return HttpResponseRedirect(OAuthManager(request).create_request_token())

def bot_create(request):
    manager = BotManager(request)
    messages.info(request, "등록 메시지: %s" % manager.register())
    return HttpResponseRedirect('/')

def bot_update(request):
    manager = BotManager(request)
    if request.method == 'POST':
        form = BotUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].encode('utf-8')
            status = form.cleaned_data['status'].encode('utf-8')
            file = form.cleaned_data['file']
            callback = form.cleaned_data['callback']

            result_json = manager.update(name, status, callback, file)
            result = ujson.loads(result_json)
            if result['code'] == '200':
                messages.info(request, "업데이트 완료 %s" % result_json);
                return HttpResponseRedirect('/')
            else:
                messages.info(request, '요청실패: %s' % result_json)
    else:
        form = BotUpdateForm(initial=dict(name = manager.bot_info.name,
                                          status = manager.bot_info.status,
                                          callback = manager.bot_info.callback))
        
    return render_to_response('bot_update.html',
                              dict(form = form),
                              context_instance = RequestContext(request))

def add_question(request):
    survey_id = request.GET.get('survey_id')
    survey = Survey.objects.get(pk=survey_id)
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            survey.question_set.create(content=content)
            messages.info(request, 'Question 등록 완료')
    else:
        form = CreateQuestionForm()
    return render_to_response('add_question.html',
                              dict(form=form,
                                   survey=survey),
                              context_instance = RequestContext(request))

def add_answer(request):
    question_id = request.GET.get('question_id')
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = CreateAnswerForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            weight = form.cleaned_data['weight']
            question.answer_set.create(content=content, weight=weight)
            messages.info(request, 'Answer 등록 완료')
            return HttpResponseRedirect('/add_answer/?question_id=%s' % question_id)
    else:
        form = CreateAnswerForm()
    return render_to_response('add_answer.html',
                              dict(question=question,
                                   form=form),
                              context_instance = RequestContext(request))

def add_result(request):
    survey_id = request.GET.get('survey_id')
    survey = Survey.objects.get(pk=survey_id)
    if request.method == 'POST':
        form = CreateResultForm(request.POST)
        if form.is_valid():
            weight_start = form.cleaned_data['weight_start']
            weight_end = form.cleaned_data['weight_end']
            description = form.cleaned_data['description']
            
            survey.result_set.create(weight_start=weight_start,
                                     weight_end=weight_end,
                                     description=description)
            messages.info(request, 'Result 등록 완료')
            return HttpResponseRedirect('/add_result/?survey_id=%s' % survey_id)
    else:
        form = CreateResultForm()
    return render_to_response('add_result.html',
                              dict(survey=survey,
                                   form=form),
                              context_instance = RequestContext(request))

def add_basic_answer(request):
    question_id = request.GET.get('question_id')
    question = Question.objects.get(pk=question_id)
    question.make_normal_answer_set()
    messages.info(request, '기본 답변 추가 완료')
    return HttpResponseRedirect('/add_answer/?question_id=%s' % question_id)

def remove_survey(request):
    survey_id = request.GET.get('survey_id')
    Survey.objects.get(pk=survey_id).delete()
    messages.info(request, 'Survey 지우기 성공')
    return HttpResponseRedirect('/')

def remove_result(request):
    result_id = request.GET.get('result_id')
    Result.objects.get(pk=result_id).delete()
    messages.info(request, 'Result 지우기 성공')
    return HttpResponseRedirect('/add_result/?survey_id=%s' % request.GET.get('survey_id'))


def remove_answer(request):
    answer_id = request.GET.get('answer_id')
    Answer.objects.get(pk=answer_id).delete()
    messages.info(request, 'Answer 지우기 성공')
    return HttpResponseRedirect('/add_answer/?question_id=%s' % request.GET.get('question_id'))


def remove_question(request):
    question_id = request.GET.get('question_id')
    Question.objects.get(pk=question_id).delete()
    messages.info(request, 'Question 지우기 성공')
    return HttpResponseRedirect('/add_question/?survey_id=%s' % request.GET.get('survey_id'))

def add_survey(request):
    survey_id = request.GET.get('survey_id', None)
    if request.method == 'POST':
        form = CreateSurveyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            result_help_description = form.cleaned_data['result_help_description']
            if survey_id:
                survey = Survey.objects.get(pk=survey_id)
                survey.name = name
                survey.description = description
                survey.result_help_description = result_help_description
                survey.save()
            else:
                survey = Survey.objects.create(name=name,
                                               description=description,
                                               result_help_description=result_help_description)
            messages.info(request, 'Survey등록 완료')
            return HttpResponseRedirect('/add_question/?survey_id=%s' % survey.pk)
    else:
        if survey_id:
            survey = Survey.objects.get(pk=survey_id)
            form = CreateSurveyForm(initial=dict(name=survey.name,
                                                 description=survey.description,
                                                 result_help_description=survey.result_help_description))
        else:
            form = CreateSurveyForm()
    return render_to_response('add_survey.html',
                              dict(form = form,
                                   survey_id=survey_id),
                              context_instance = RequestContext(request))
    
@csrf_exempt
def test(request):
    manager = BotManager(request)
    return HttpResponse(manager.update('testname', 'teststatus5', file=open('/Users/excgate/Desktop/2.png', 'r'), save_db=False))

def callback(request):
    manager = BotManager(request)
    result = manager.perform_action_mind(request)
    return HttpResponse('')
# def callback(request):
#     manager = BotManager(request)
#     result = manager.perform_action(request)
    
#     return HttpResponse('')
