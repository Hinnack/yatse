from django import template
from yatse.models import boards

register = template.Library()

class board_list(template.Node):
    def render(self, context):
        user = context.get('request').user
        if user.is_authenticated():
            context['boards'] = boards.objects.filter(c_user=user, active_record=True)
        else:
            context['boards'] = []
        return ''

def do_board_list(parser, token):
    return board_list()

register.tag('board_list', do_board_list)

def multiply(value, arg):
    return value*arg

register.filter('multiply', multiply)
