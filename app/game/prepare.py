import uuid
from typing import Optional

from app.domain.game import Game
from app.domain.game_gateway import GameGateway
from app.domain.player import Player


class Prepare:

    class StartUnsuccessful(Exception):
        pass

    class JoinUnsuccessful(Exception):
        pass

    def __init__(self, gateway: GameGateway):
        self.gateway = gateway

    def current(self, code: str) -> Optional[Game]:
        return self.gateway.existing(code=code)

    def create(self) -> Game:
        try:
            game = self.gateway.create()
            return game
        except Exception as e:
            print(e)
            raise Prepare.StartUnsuccessful()

    def join(self, player_name: str, code: str) -> (Game, Player):
        game = self.gateway.existing(code=code)
        if next(p for p in game.players if p.name == player_name):
            raise Prepare.JoinUnsuccessful()
        player = Player(id=uuid.uuid4(), name=player_name, all_numbers=[], used_numbers=[])
        if game.started:
            raise Prepare.JoinUnsuccessful()
        game.players.append(player)
        self.gateway.update(game=game)
        return game, player
