from bottle import run, get, hook, response, route, get, static_file, request
from config import API_PORT, IMAGES_SOURCE
from utils.middlewares import authenticate
from webapis import user, news, potin, group


@hook('after_request')
def enableCORSGenericRoute():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, PATCH, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'


@route('/', method='OPTIONS')
@route('/<path:path>', method='OPTIONS')
def option_handler(path=None):
    return


@get('/images/<path:path>')
def get_image(path=None):
    if not path:
        return
    return static_file(path, root=IMAGES_SOURCE)


if __name__=='__main__':
    run(host='0.0.0.0', port=API_PORT, debug=False, reloader=True)
