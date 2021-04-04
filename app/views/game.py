from typing import Optional, Tuple

from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, current_app, session

from app import FileGameGateway
from app.domain.game import Game
from app.game.player_game import PlayerGame
from app.game.prepare import Prepare
from app.views.forms import JoinForm

bp = Blueprint('game', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    session.permanent = True
    form = JoinForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            return __join(form=form)
        except Prepare.JoinUnsuccessful:
            return abort(400)
    if request.method == 'GET':
        game = __restore_existing()
        if game:
            return redirect(url_for('game.game', code=game.code))
        else:
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


def __join(form: JoinForm):
    if 'code' in session or 'player_id' in session or 'spectator' in session:
        return redirect(url_for('game.index'))
    prepare = __make_prepare()
    game, player = prepare.join(player_name=form.name.data, code=form.code.data)
    session['code'] = game.code
    session['player_id'] = player.id
    return redirect(url_for('game.game', code=game.code))


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


@bp.route('/game/<string:code>')
def game(code: str):
    is_player = 'player_id' in session
    is_spectator = 'spectator' in session
    has_code = 'code' in session
    if (is_player or is_spectator) and has_code and session['code'] == code:
        prepare = __make_prepare()
        try:
            game = prepare.current(code=code)
            return __render_game(game=game, is_player=is_player, is_spectator=is_spectator)
        except Exception:
            return __reset_to_index()
    return __reset_to_index()


def __render_game(game: Game, is_player: bool, is_spectator: bool):
    player = None
    if is_player:
        player = next(i for i in game.players if i.id == session['player_id'])
    players_list = None
    if is_spectator:
        players_list = ', '.join(list(map(lambda p: p.name, game.players)))
    return render_template(
        'game.html',
        game=game,
        player=player,
        players_list=players_list,
        is_spectator=is_spectator,
        is_player=is_player)


@bp.route('/create', methods=['GET'])
def create():
    session.permanent = True
    enter = Prepare(gateway=FileGameGateway(dir=current_app.instance_path))
    game = enter.create()
    session['spectator'] = True
    session['code'] = game.code
    return redirect(url_for('game.game', code=game.code))


@bp.route('/game/<string:code>/start')
def start(code: str):
    if 'spectator' in session and session['code'] == code:
        gateway = FileGameGateway(dir=current_app.instance_path)
        game = gateway.existing(code=code)
        gateway.start(game=game)
        return redirect(url_for('game.game', code=code))
    return abort(403)


@bp.route('/game/<string:code>/add/<int:number>')
def add_number(code: str, number: int):
    gateway = FileGameGateway(dir=current_app.instance_path)
    game = gateway.existing(code=code)
    player = next(i for i in game.players if i.id == session['player_id'])
    player_game = PlayerGame(player=player, game=game, gateway=gateway)
    player_game.add_number(number=number)
    return redirect(url_for('game.game', code=code))


@bp.route('/game/<string:code>/restart')
def restart(code: str):
    if 'spectator' in session and session['code'] == code:
        gateway = FileGameGateway(dir=current_app.instance_path)
        game = gateway.existing(code=code)
        gateway.restart(game=game)
        return redirect(url_for('game.game', code=code))
    return abort(403)


@bp.route('/game/<string:code>/finish')
def finish(code: str):
    if 'spectator' in session and session['code'] == code:
        gateway = FileGameGateway(dir=current_app.instance_path)
        game = gateway.existing(code=code)
        gateway.finish(game=game)
        return __reset_to_index()
    abort(403)


def __reset_to_index():
    __clear_session()
    return redirect(url_for('game.index'))


def __clear_session():
    session.pop('spectator', None)
    session.pop('code', None)
    session.pop('player_id', None)


def __make_prepare() -> Prepare:
    return Prepare(gateway=FileGameGateway(dir=current_app.instance_path))