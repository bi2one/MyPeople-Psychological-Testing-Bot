# -*- coding: utf-8 -*-
from django import forms
from mypeoplebot import settings

class BotUpdateForm(forms.Form):
    name = forms.CharField(label='닉네임', required=True, error_messages={'required': '닉네임을 입력해주세요.'})
    status = forms.CharField(label='상태 메시지', required=False)
    file = forms.ImageField(label='프로필 사진', help_text='png, jpg, gif만 가능', required=False)
    callback = forms.URLField(label='callback url', initial=settings.BOT_CALLBACK_URL, error_messages={'invalid': '올바른 url이 아닙니다.'}, required=False)

    def clean_callback(self):
        super(BotUpdateForm, self).clean()
        callback = self.cleaned_data['callback']
        if len(callback.strip()) == 0:
            return settings.BOT_CALLBACK_URL
        else:
            return callback.strip()
        
class CreateSurveyForm(forms.Form):
    name = forms.CharField(label='이름', required=True, error_messages={'required': '이름을 입력하세요.' })
    description = forms.CharField(label='설명', required=False, widget=forms.Textarea)
    result_help_description = forms.CharField(label='최종결과 보조설명', required=False, widget=forms.Textarea)

class CreateQuestionForm(forms.Form):
    content = forms.CharField(label='질문')

class CreateAnswerForm(forms.Form):
    content = forms.CharField(label='답변내용', required=True, error_messages={'required': '답변내용을 입력하세요.'})
    weight = forms.IntegerField(label='가중치', required=True, error_messages={'required': '가중치를 입력하세요.'})

class CreateResultForm(forms.Form):
    weight_start = forms.IntegerField(label='종합 가중치 시작', required=True, error_messages={'required': '가중치 범위를 입력하세요.'})
    weight_end = forms.IntegerField(label='종합 가중치 끝', required=True, error_messages={'required': '가중치 범위를 입력하세요.'})
    description = forms.CharField(label='종합결과', required=True, widget=forms.Textarea, error_messages={'required': "종합결과를 입력하세요."})
