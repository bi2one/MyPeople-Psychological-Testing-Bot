# -*- coding: utf-8 -*-
from wordbot.models import Survey, Question, Answer, Result, AnswerLog, ResultLog
from pprint import pprint 

def base_state(action_manager, buddy_id, content, *arguments):
    action_table = {
        u'ㄷㅇㅁ': 'help',
        u'도움말': 'help',
        u'ㅁㄹ': 'survey_list',
        u'목록': 'survey_list',
        u'ㅅㅈ': 'start',
        u'시작': 'start',
        }
        
    next_state = base_state
    if is_integer(arguments[0]):
        target_map = action_manager.get_user_data_value(buddy_id, 'survey_map', dict())
        target = target_map.get(arguments[0], arguments[0])
        arguments = ['ㅅㅈ', target]
        action = 'start'
    else:
        action = action_table.get(arguments[0], 'help')
    
    if action == 'help':
        next_state = help_state(action_manager, buddy_id, content, *arguments)
    elif action == 'survey_list':
        next_state = survey_list_state(action_manager, buddy_id, content, *arguments)
    elif action == 'start':
        next_state = start_question_state(action_manager, buddy_id, content, *arguments)
    return next_state
        
def help_state(action_manager, buddy_id, content, *arguments):
    # show help message
    message = '<심리테스트 도움말>\n\n'
    message += '초성만 입력해도 작동합니다.\n\n'
    message += '"도움말", "ㄷㅇㅁ"은 같습니다.\n\n'
    message += '* 테스트 목록 보기\n'
    message += '  "목록"\n\n'
    message += '* 테스트 시작하기\n'
    message += '  "시작 [테스트 번호]"\n'
    message += '  "[테스트 번호]"\n\n'
    message += '* 도움말\n'
    message += '  "도움말"'
    action_manager.bot_manager.send_message(buddy_id, message);
    return base_state

def survey_list_state(action_manager, buddy_id, content, *arguments):
    surveys = Survey.objects.all()
    if len(surveys) <= 0:
        action_manager.bot_manager.send_message(buddy_id, '등록된 설문지가 없습니다.')
    else:
        message = '**심리테스트 목록**'
        index = 0
        survey_map = dict()
        for survey in surveys:
            index += 1
            validity = '공사중'
            if survey.is_valid:
                validity = '사용가능'
            message += '\n%s. %s\n(%s)' % (index, survey.name.encode('utf-8'), validity)
            survey_map[index] = survey.pk
        action_manager.set_user_data_value(buddy_id, 'survey_map', survey_map)
        action_manager.bot_manager.send_message(buddy_id, message)
    return base_state

def start_question_state(action_manager, buddy_id, content, *arguments):
    if len(arguments) < 2 or not is_integer(arguments[1]):
        next_state = help_state(action_manager, buddy_id, content, *arguments)
    else:
        survey_id = int(arguments[1])
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            action_manager.bot_manager.send_message(buddy_id,
                                                    '설문지가 없습니다. 번호를 확인하세요')
            return survey_list_state(action_manager, buddy_id, content, *arguments)
        if not survey.is_valid:
            action_manager.bot_manager.send_message(buddy_id,
                                                    '아직 작업중인 설문지입니다. 다른 설문지를 시작하세요.')
            return survey_list_state(action_manager, buddy_id, content, *arguments)
        
        # initialize values
        question_ids = [x.pk for x in survey.question_set.all()]
        action_manager.set_user_data_value(buddy_id, 'survey_id', survey_id)
        action_manager.set_user_data_value(buddy_id, 'questions', question_ids)
        action_manager.set_user_data_value(buddy_id, 'total_weight', 0)
        if len(question_ids) <= 0:
            action_manager.bot_manager.send_message(buddy_id, '**심리테스트**\n심리테스트 내용이 없습니다. 설문을 종료합니다.')
            next_state = base_state
        else:
            message = '**심리테스트**'
            message += '\n%s\n%s' % (survey.name.encode('utf-8'),
                                     survey.description.encode('utf-8'))
            message += '\n\n1. 시작\n2. 취소'
            action_manager.bot_manager.send_message(buddy_id, message)
            next_state = confirm_question_state
    return next_state

def confirm_question_state(action_manager, buddy_id, content, *arguments):
    action_table = {
        '1': 'confirm',
        '2': 'cancel',
        }
    action = action_table.get(arguments[0], 'help')
    if action == 'confirm':
        return pop_question_state(action_manager, buddy_id, content, *arguments)
    elif action == 'cancel':
        action_manager.bot_manager.send_message(buddy_id, '취소합니다.')
        return help_state(action_manager, buddy_id, content, *arguments)
    else:
        action_manager.bot_manager.send_message(buddy_id, '다음중 하나를 입력하세요.\n\n1. 시작\n2. 취소')
        return confirm_question_state

def pop_question_state(action_manager, buddy_id, content, *arguments):
    # 문제 프린팅
    next_state = question_state
    question_ids = action_manager.get_user_data_value(buddy_id, 'questions', list())
    if len(question_ids) <= 0:
        action_manager.bot_manager.send_message(buddy_id, '잘못된 state 접근')
        next_state = base_state
    else:
        question_id = question_ids[0]
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            action_manager.bot_manager.send_message(buddy_id, '질문이 없네요?')
            return help_state(action_manager, buddy_id, content, *arguments)
        answers = question.answer_set.all()
        message = '* %s' % (question.content.encode('utf-8'))
        for answer in answers:
            message += '\n%s. %s' % (answer.sequence, answer.content.encode('utf-8'))
        action_manager.bot_manager.send_message(buddy_id, message)
        next_state = question_state
    return next_state

def question_state(action_manager, buddy_id, content, *arguments):
    # 답변 받기, 종료.
    action_table = {
        u'ㄴㄱ': 'exit',
        u'나가': 'exit',
        u'exit': 'exit',
        u'ㄷㅇㅁ': 'question_help',
        u'도움말': 'question_help',
        }
    next_state = question_state
    if is_integer(arguments[0]):
        action = 'answer'
    else:
        action = action_table.get(arguments[0], 'question_help')
        
    if action == 'exit':
        action_manager.bot_manager.send_message(buddy_id,
                                                '진행중인 테스트를 종료합니다.')
        next_state = help_state(action_manager, buddy_id, content, *arguments)
    elif action == 'question_help':
        next_state = question_help_state(action_manager, buddy_id, content, *arguments)
    elif action == 'answer':
        next_state = answer_state(action_manager, buddy_id, content, *arguments)
    return next_state

def answer_state(action_manager, buddy_id, content, *arguments):
    # 답변 받아 결과를 뿌리거나 다시 question_state이동
    next_state = question_state
    sequence = int(arguments[0])
    questions = action_manager.get_user_data_value(buddy_id, 'questions', list())
    if len(questions) <= 0:
        action_manager.bot_manager.send_message(buddy_id,
                                                '잘못된 접근입니다. 처음으로 돌아갑니다.')
        next_state = base_state
    else:
        question = Question.objects.get(pk=questions[0])
        answer = question.answer_set.get(sequence=sequence)
        total_weight = action_manager.get_user_data_value(buddy_id, 'total_weight', 0)
        action_manager.set_user_data_value(buddy_id, 'total_weight', total_weight + answer.weight)
        questions = questions[1:]
        action_manager.set_user_data_value(buddy_id, 'questions', questions)
        
        if len(questions) <= 0:
            # show result
            next_state = show_result_state(action_manager, buddy_id, content, *arguments)
        else:
            next_state = pop_question_state(action_manager, buddy_id, content, *arguments)
    return next_state

def show_result_state(action_manager, buddy_id, content, *arguments):
    total_weight = action_manager.get_user_data_value(buddy_id, 'total_weight', -1)
    survey_id = action_manager.get_user_data_value(buddy_id, 'survey_id', -1)
    if total_weight == -1 or survey_id == -1:
        action_manager.bot_manager.send_message(buddy_id,
                                                '잘못된 접근입니다. 처음으로 돌아갑니다.')
    else:
        survey = Survey.objects.get(pk=survey_id)
        results = survey.result_set.filter(weight_start__lte=total_weight, weight_end__gte=total_weight)
        message = '**심리테스트 결과**'
        if len(results) <= 0:
            message += '\n현재 가중치: %s' % total_weight
            results = survey.result_set.all()
            for result in results:
                message += '\n\n%s<=(가중치)<=%s\n%s' % (result.weight_start,
                                                         result.weight_end,
                                                         result.description.encode('utf-8'))
        else:
            for result in results:
                message += '\n\n%s' % result.description.encode('utf-8')
                
        if survey.result_help_description:
            message += '\n\n----------------\n%s' % survey.result_help_description.encode('utf-8')

        action_manager.bot_manager.send_message(buddy_id, message)
    return base_state

def question_help_state(action_manager, buddy_id, content, *arguments):
    message = '<심리테스트 문제 도움말>\n\n'
    message += '초성만 입력해도 작동합니다.\n\n'
    message += '"도움말", "ㄷㅇㅁ"은 같습니다.\n\n'
    message += '답변 번호 입력시 다음으로 넘어갑니다.\n\n'
    message += '* 진행중인 문제와 도움말\n'
    message += '  "도움말"\n\n'
    message += '* 심리테스트 중지\n'
    message += '  "exit"\n'
    message += '  "나가"'
    
    action_manager.bot_manager.send_message(buddy_id, message)
    # action_manager.bot_manager.send_message(buddy_id, '현재 진행중인 질문입니다.')
    return pop_question_state(action_manager, buddy_id, content, *arguments)

def is_integer(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
