import json
from kagenda import config, speech
from trello import TrelloClient


class Credentials:
    __slots__ = ['board', 'key', 'token']

    def __init__(self, parsed_creds):
        self.board = parsed_creds['trello']['board']
        self.key = parsed_creds['trello']['key']
        self.token = parsed_creds['trello']['token']


def get_credentials(path='credentials.json'):
    with open(path, 'rt') as credentials:
        parsed_creds = json.loads(credentials.read())
        return Credentials(parsed_creds)


class Todo:
    def __init__(self, card):
        self.name = card.name
        self.due = card.due_date

        if self.due:
            self.due = self.due.astimezone(config.LOCAL_TZ)

    def string(self):
        s = '+ ' + self.name
        if self.due:
            s += ' (due ' + self.due.strftime('%Y-%m-%d') + ')'
        return s

    def text(self):
        s = self.name
        if self.due:
            s += ', due ' + speech.day_to_text(self.due)
        return s + '.'


class TodoList:
    def __init__(self, cards):
        self.cards = [Todo(card) for card in cards]

    def string(self):
        return '\n'.join([card.string() for card in self.cards])

    def text(self):
        return '\n'.join([card.text() for card in self.cards])

    def __len__(self):
        return len(self.cards)

def get_todo_list(path='credentials.json'):
    creds = get_credentials(path)
    client = TrelloClient(api_key=creds.key, api_secret=creds.token)
    board = client.get_board(creds.board)
    lists = board.all_lists()

    cards = None
    for list in lists:
        if list.name == 'TODO':
            cards = list.list_cards()

    return TodoList(cards)
