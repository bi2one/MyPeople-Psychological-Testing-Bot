# -*- coding: utf-8 -*-
import oauthmodule, ujson, redis
from mypeoplebot import settings
from wordbot.models import Deck, OAuthToken, BotInfo, Status, \
     Survey, Question, Answer, Result, AnswerLog, ResultLog
from mind_states import base_state, question_state, confirm_question_state
from pprint import pprint

class OAuthManager(object):
    def __init__(self, request, consumer_key=settings.consumer_key, consumer_secret=settings.consumer_secret):
        self.request = request
        self.consumer_key = consumer_key
        try:
            self.token = OAuthToken.objects.get(consumer_key=consumer_key)
        except OAuthToken.DoesNotExist:
            self.token = None
        self.oauth = oauthmodule.OAuth(consumer_key, consumer_secret)

    def has_access_token(self):
        return self.token.access_token is not None
    
    def create_request_token(self):
        request_token = self.oauth.request_token(settings.request_token_url,
                                                 settings.oauth_callback_url)
        self.request.session['consumer_key'] = self.consumer_key
        self.request.session['request_token'] = request_token.to_string()
        redirect_url = self.oauth.request_authorize_user(request_token,
                                                         settings.authorization_url,
                                                         settings.oauth_callback_url)
        return redirect_url
    
    def create_access_token(self, verifier_code):
        request_token_string =  self.request.session['request_token']
        consumer_key = self.request.session['consumer_key']
        if not self.token:
            self.token = OAuthToken()
        self.token.consumer_key = consumer_key
        self.token.access_token = self.oauth.request_access_token(request_token_string,
                                                                  verifier_code,
                                                                  settings.access_token_url)
        self.token.save()
    
    def access_resource(self, request_parameters, resource_url, files=None):
        if self.has_access_token():
            return self.oauth.access_resource(self.token.access_token, request_parameters, resource_url, files)
        else:
            raise Exception('access token is empty.')

class BotManager(object):
    def __init__(self, request):
        self.oauth_manager = OAuthManager(request)
        self.bot_info, created = BotInfo.objects.get_or_create(oauth_token=self.oauth_manager.token)

    def register(self, bot_name=settings.BOT_NAME, callback=settings.BOT_CALLBACK_URL):
        return self.oauth_manager.access_resource(dict(botName = bot_name,
                                                       receiveUrl = callback),
                                                  settings.pb_register_url)
    def update(self, name, status='', callback=settings.BOT_CALLBACK_URL, file='', save_db=True):
        files = None
        if file:
            files = dict(file = file)
        result_json = self.oauth_manager.access_resource(dict(name = name,
                                                              status = status,
                                                              callback = callback),
                                                         settings.pb_edit_url,
                                                         files=files)
        result = ujson.loads(result_json)
        if save_db and result['code'] == '200':
            self.bot_info.name = name
            self.bot_info.status = status
            self.bot_info.callback = callback
            if file:
                self.bot_info.profile_image.save("%s_%s" % (self.bot_info.pk, file._name),
                                                 file)
            self.bot_info.save()
        return result_json

    def send_message(self, buddy_id, content, request_count=1):
        result_json = self.oauth_manager.access_resource(dict(buddyId = buddy_id,
                                                              content = content),
                                                         settings.pb_buddy_send_url)
        result = ujson.loads(result_json)
        if result['code'] != '200' and request_count <= 5:
            return self.send_message(buddy_id, content, request_count + 1)
        else:
            return result_json

    def perform_action(self, request):
        action = request.POST.get('action')
        getattr(ActionManager(self), action)(request)

    def perform_action_mind(self, request):
        action = request.POST.get('action')
        getattr(MindActionManager(self), action)(request)

class MindActionManager(object):
    def __init__(self, bot_manager):
        self.bot_manager = bot_manager
        self.red = settings.redis_store

    def get_user_data(self, buddy_id):
        data = self.red.get(buddy_id)
        if data:
            return ujson.loads(data)
        else:
            return dict()

    def get_user_data_value(self, buddy_id, key, default):
        return self.get_user_data(buddy_id).get(key, default)

    def set_user_data(self, buddy_id, data):
        self.red.set(buddy_id, ujson.dumps(data))

    def set_user_data_value(self, buddy_id, key, value):
        data = self.get_user_data(buddy_id)
        data[key] = value
        self.set_user_data(buddy_id, data)

    def sendFromMessage(self, request):
        buddy_id = request.POST.get('buddyId')
        content = request.POST.get('content')
        arguments = [x.strip() for x in ' '.join(content.split()).split(' ')]
        
        user_data = self.get_user_data(buddy_id)

        print 'state log *********'
        state = globals().get(user_data.get('state'), base_state)
        print 'current state::: %s' % state.__name__
        next_state = state(self, buddy_id, content, *arguments)
        user_data = self.get_user_data(buddy_id)
        user_data['state'] = next_state.__name__
        print 'next state::: %s' % user_data.get('state')
        pprint(self.get_user_data(buddy_id))
        self.set_user_data(buddy_id, user_data)
        
class ActionManager(object):
    functions = {
        u'ㅅㅌ': 'show_status',         # v
        u'상태': 'show_status',         # v
        u'ㅁㄹ': 'read_deck',           # v
        u'목록': 'read_deck',           # v
        u'ㄱㅅ': 'read_deck',           # v
        u'검색': 'read_deck',           # v
        u'ㅊㄱ': 'create_card',         # v
        u'추가': 'create_card',         # v
        u'ㅋㄷ': 'read_card',           # 
        u'카드': 'read_card',           # 
        u'ㅁㄹㅊㄱ': 'create_deck',     # v
        u'목록추가': 'create_deck',     # v
        u'ㅈㅇ': 'delete_deck',         # v
        u'지워': 'delete_deck',         # v
        u'ㅈㅇㄱ': 'delete_deck',       # v
        u'지우기': 'delete_deck',       # v
        u'ㅅㅇ': 'select_deck',         # v
        u'사용': 'select_deck',         # v
        u'h': 'help',                   # v
        u'H': 'help',                   # v
        u'ㅗ': 'help',                  # v
        u'ㄷㅇ': 'help',                # v
        u'ㄷㅇㅁ': 'help',              # v
        u'도움말': 'help',              # v
        }
    
    def __init__(self, bot_manager):
        self.bot_manager = bot_manager
        
    def sendFromMessage(self, request):
        buddy_id = request.POST.get('buddyId')
        # status = Status.objects.get_or_create(buddy_id=buddy_id)
        content = request.POST.get('content')
        arguments = [x.strip() for x in content.split('.')]
        getattr(self, self.functions.get(arguments[0], 'invalid_param_f'))(buddy_id,
                                                                           content,
                                                                           *arguments)
        # self.bot_manager.send_message(buddy_id, 'dfasfd')

    def select_deck(self, buddy_id, content, *arguments):
        if len(arguments) <= 1 or not is_integer(arguments[1]) \
               or len(Deck.objects.filter(pk=int(arguments[1]))) <= 0:
            self.send_usage(buddy_id, '사용 . [항목번호]')
            return
        deck_id = int(arguments[1])
        status, created = Status.objects.get_or_create(buddy_id=buddy_id)
        status.deck = Deck.objects.get(pk=deck_id)
        status.save()
        self.send_status_message(buddy_id, '**사용선택 완료**', status=status)

    def delete_deck(self, buddy_id, content, *arguments):
        if len(arguments) <= 1 or not is_integer(arguments[1]):
            self.send_usage(buddy_id, '지워 . [항목번호]')
            return 
        status, created = Status.objects.get_or_create(buddy_id=buddy_id)
        deck_id = int(arguments[1])
        # if status.deck.pk == deck_id:
        #     status.deck = None
        #     status.save()
        Deck.objects.filter(pk=int(arguments[1])).delete()
        self.send_status_message(buddy_id, '**지우기 완료**')

    def create_card(self, buddy_id, content, *arguments):
        if len(arguments) < 3:
            self.send_usage(buddy_id, '추가 . [앞면내용] . [뒷면내용]')
            return 
            
        status, created = Status.objects.get_or_create(buddy_id=buddy_id)
        if not status.deck:
            self.send_usage(buddy_id, '꾸러미를 선택하세요.')
            self.read_deck(buddy_id, content, *arguments)
            return 
            
        side1 = arguments[1]
        side2 = arguments[2]
        status.deck.card_set.create(side1=side1,
                                    side2=side2,
                                    status='normal')
        self.bot_manager.send_message(buddy_id, '**카드 추가 완료**')

    def show_status(self, buddy_id, content, *arguments):
        self.send_status_message(buddy_id, '**내 상태 표시**')

    def read_deck(self, buddy_id, content, *arguments):
        decks = Deck.objects.filter(buddy_id=buddy_id)

        if len(decks) <= 0:
            self.bot_manager.send_message(buddy_id, '꾸러미가 없습니다.')
            return

        return_content = '**검색 결과**'
        for deck in decks:
            return_content += '\n%3s | %s' % (deck.pk, deck.name.encode('utf-8'))
        return_content += '\n* 지우려면 "지워 . [항목번호]"'
        return_content += '\n* 사용하려면 "사용 . [항목번호]"'
            
        self.bot_manager.send_message(buddy_id, return_content)

    def send_status_message(self, buddy_id, front_msg='', rear_msg='', status=None):
        if status is None:
            status, created = Status.objects.get_or_create(buddy_id=buddy_id)

        if status.deck is None:
            body = '선택한 꾸러미: 없음'
        else:
            body = '선택한 꾸러미: %s' % status.deck.name.encode('utf-8')
            body += '\n설명: %s' % status.deck.description.encode('utf-8')

        if front_msg:
            message = front_msg + '\n'
        message += body
        if rear_msg:
            message += '\n' + rear_msg
        self.bot_manager.send_message(buddy_id, message)

    def create_deck(self, buddy_id, content, *arguments):
        if len(arguments) != 3:
            self.invalid_param_f(buddy_id, content, *arguments)
        name = arguments[1]
        desc = arguments[2]
        
        if len(Deck.objects.filter(name=name)) > 0:
            self.bot_manager.send_message(buddy_id, '이미 중복된 이름이 있습니다.')
            return 
        deck = Deck.objects.create(buddy_id=buddy_id, name=name, description=desc)
        status, created = Status.objects.get_or_create(buddy_id=buddy_id)
        status.deck = deck
        status.save()
        self.send_status_message(buddy_id, front_msg='꾸러미를 만들었습니다.', status=status)

    def invalid_param_f(self, buddy_id, content, *arguments):
        print arguments
        print self.bot_manager.send_message(buddy_id, content)

    def send_usage(self, buddy_id, content):
        self.bot_manager.send_message(buddy_id, '사용법: %s' % content)

    def help(self, buddy_id, content, *arguments):
        self.bot_manager.send_message(buddy_id, 'help: ')


def is_integer(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
