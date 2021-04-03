from app.domain.game import Game
from app.domain.game_gateway import GameGateway
from app.domain.player import Player


class PlayerGame:

    def __init__(self, player: Player, game: Game, gateway: GameGateway):
        self.player = player
        self.game = game
        self.gateway = gateway

    def add_number(self, number: int):
        player_has_that_number = self.player.all_numbers.__contains__(number)
        game_has_that_number = self.game.exp_seq.__contains__(number)
        if not (self.game.started or player_has_that_number or game_has_that_number):
            return
        if self.player.used_numbers.__contains__(number) or len(self.player.used_numbers) == 3:
            return
        self.game.seq.append(number)
        self.player.used_numbers.append(number)
        self.gateway.update(game=self.game)
