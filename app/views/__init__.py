from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, current_app, session
from wtforms import Form, StringField, validators

from app import FileGameGateway
from app.game.player_game import PlayerGame
from app.game.prepare import Prepare

bp = Blueprint('game', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = JoinForm(request.form)
    enter = Prepare(gateway=FileGameGateway(dir=current_app.instance_path))
    if request.method == 'POST' and form.validate():
        game, player = enter.join(player_name=form.name.data, code=form.code.data)
        session['code'] = game.code
        session['player_id'] = player.id
        flash('Game Joined! Wait for the beginning!')
        return redirect(url_for('game.game', code=game.code))
    if request.method == 'GET':
        if 'code' not in session:
            return render_template('index.html', form=form)
        if 'player_id' in session or 'spectator' in session:
            try:
                game = enter.current(session['code'])
                return redirect(url_for('game.game', code=game.code))
            except:
                __clear_session()
                return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@bp.route('/game/<string:code>')
def game(code: str):
    is_spectator = 'spectator' in session
    is_player = 'player_id' in session
    if (is_player or is_spectator) and session['code'] == code:
        enter = Prepare(gateway=FileGameGateway(dir=current_app.instance_path))
        try:
            game = enter.current(code=code)
            player = None
            if is_player:
                player = next(i for i in game.players if i.id == session['player_id'])
            return render_template(
                'game.html',
                game=game,
                player=player,
                is_spectator=is_spectator,
                is_player=is_player)
        except:
            __clear_session()
            return redirect(url_for('game.index'))
    abort(404)


@bp.route('/create', methods=['GET'])
def create():
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
    abort(403)


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
        return redirect(url_for('game.index'))


@bp.route('/game/<string:code>/finish')
def finish(code: str):
    if 'spectator' in session and session['code'] == code:
        gateway = FileGameGateway(dir=current_app.instance_path)
        game = gateway.existing(code=code)
        gateway.finish(game=game)
        __clear_session()
        return redirect(url_for('game.index'))
    abort(404)


def __clear_session():
    session.pop('spectator', None)
    session.pop('code', None)
    session.pop('player_id', None)


class JoinForm(Form):
    name = StringField('Имя', [validators.Length(min=3, max=25)])
    code = StringField('Код Игры', [validators.Length(min=10, max=10)])
