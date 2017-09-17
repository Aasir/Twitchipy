from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import twitch_audio


def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')

@view_config(renderer='json')
def getSongInfo(request):
    print('Song Request')
    channel = request.matchdict['channel']
    ret = twitch_audio.getTwitchStream(channel)
    if ret['channelExists'] is True:
        ret = twitch_audio.getSongID()

    return ret


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('twitchChannel', '/{channel}')
        config.add_view(getSongInfo, route_name='twitchChannel', renderer='json')
        app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 6543, app)
        server.serve_forever()
