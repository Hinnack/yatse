from django import template
from yatse.models import Server

register = template.Library()

class server_list(template.Node):
    def render(self, context):
        user = context.get('request').user
        if user.is_authenticated():
            context['server'] = Server.objects.filter(active_record=True)
        else:
            context['server'] = []
        return ''

def do_server_list(parser, token):
    return server_list()

register.tag('server_list', do_server_list)
