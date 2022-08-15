import json
from typing import Optional

from flask import Blueprint, redirect, url_for, current_app, session, request, abort

from app import FileGameGateway
from app.domain.game import Game
from app.game.player_game import PlayerGame
from app.game.prepare import Prepare

api = Blueprint('game_api', __name__, url_prefix='/api/')


@api.after_request
def middleware_for_response(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


def register_error_handlers(app):
    app.errorhandler(400)(bad_request)
    app.errorhandler(403)(forbidden)
    app.errorhandler(404)(not_found)
    app.errorhandler(500)(internal_error)


def bad_request(error):
    return \
        json.dumps({'message': 'Запрос был так себе, если честно...'}), \
        400,\
        {'content-type': 'application/json'}


def forbidden(error):
    return \
        json.dumps({'message': 'Не-не-не, это делать нельзя.'}), \
        403, \
        {'content-type': 'application/json'}


def not_found(error):
    return \
        json.dumps({'message': 'Что-то я не вижу таких. Может, ошибся?'}), \
        404, \
        {'content-type': 'application/json'}


def internal_error(error):
    return \
        json.dumps({'message': 'Ай блин. Ну написали мы фигню, да, что теперь поделаешь?'}), \
        500, \
        {'content-type': 'application/json'}


@api.route('/game/new', methods=['POST'])
def new_game():
    session.permanent = True
    enter = Prepare(gateway=FileGameGateway(dir=current_app.instance_path))
    game = enter.create()
    session['spectator'] = True
    session['code'] = game.code
    return __render_game(game=game, is_player=False, is_spectator=True)


@api.route('/game/join', methods=['POST'])
def join_game():
    if 'code' in session or 'player_id' in session or 'spectator' in session:
        return __render_game(
            game=__restore_existing(),
            is_player='player_id' in session,
            is_spectator='spectator' in session)
    prepare = __make_prepare()
    body = json.loads(request.data)
    try:
        game, player = prepare.join(player_name=body['name'], code=body['code'])
        session['code'] = game.code
        session['player_id'] = player.id
        return __render_game(game=__restore_existing(), is_player=True, is_spectator=False)
    except Exception as e:
        return __not_found(message=f'invalid code {e} {request}')


@api.route('/game/start', methods=['POST'])
def start_game():
    body = json.loads(request.data)
    code = body['code']

    if 'spectator' in session and session['code'] == code:
        gateway = FileGameGateway(dir=current_app.instance_path)
        game = gateway.existing(code=code)
        gateway.start(game=game)

        return redirect(url_for('game.game', code=code))

    return abort(403)


@api.route('/game/<string:code>', methods=['GET', 'PUT', 'DELETE'])
def game(code: str):
    if request.method == 'PUT':
        body = json.loads(request.data)
        if 'player_id' in session and body['action'] == 'add':
            gateway = FileGameGateway(dir=current_app.instance_path)
            game = gateway.existing(code=code)
            player = next(i for i in game.players if i.id == session['player_id'])
            player_game = PlayerGame(player=player, game=game, gateway=gateway)
            player_game.add_number(number=body['number'])

            return {}, 204

        if 'spectator' in session and session['code'] == code and body['action'] == 'restart':
            gateway = FileGameGateway(dir=current_app.instance_path)
            game = gateway.existing(code=code)
            gateway.restart(game=game)

            return __render_game(game=game, is_player=False, is_spectator=True)

        return abort(403)

    if request.method == 'DELETE':
        if 'spectator' in session and session['code'] == code:
            gateway = FileGameGateway(dir=current_app.instance_path)
            game = gateway.existing(code=code)
            gateway.finish(game=game)

            return {}, 204

        return abort(403)

    if request.method == 'GET':
        is_player = 'player_id' in session
        is_spectator = 'spectator' in session
        has_code = 'code' in session

        if (is_player or is_spectator) and has_code and session['code'] == code:
            prepare = __make_prepare()
            try:
                game = prepare.current(code=code)
                return __render_game(game=game, is_player=is_player, is_spectator=is_spectator)
            except Exception:
                return __not_found(message=f'game with code {code} not found')

        return __not_found(message='game not joined')

    return abort(405)


def __restore_existing() -> Optional[Game]:
    if 'code' not in session:
        return None
    if 'player_id' in session or 'spectator' in session:
        try:
            prepare = __make_prepare()
            game = prepare.current(session['code'])
            return game
        except Exception:
            __clear_session()
            return None
    return None


def __render_game(game: Game, is_player: bool, is_spectator: bool):
    player = None
    if is_player:
        player = next(i for i in game.players if i.id == session['player_id'])
    return \
        json.dumps({
            'code': game.code,
            'players': [p.name for p in game.players] if is_spectator else [player.name],
            'is_spectator': is_spectator,
            'is_started': game.started
        }), \
        200,\
        {'content-type': 'application/json'}


def __not_found(message: str):
    __clear_session()
    return \
        json.dumps({
            'error': 'not_found',
            'message': message
        }), \
        404, \
        {'content-type': 'application/json'}


def __clear_session():
    session.pop('spectator', None)
    session.pop('code', None)
    session.pop('player_id', None)


def __make_prepare() -> Prepare:
    return Prepare(gateway=FileGameGateway(dir=current_app.instance_path))