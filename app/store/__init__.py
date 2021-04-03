import os
import string
import random
from pathlib import Path
from typing import Optional

from app.domain.game import Game
from app.domain.game_gateway import GameGateway
from app.domain.player import Player


class FileGameGateway(GameGateway):

    def __init__(self, dir: os.path):
        self.dir = dir

    def create(self) -> Game:
        game = Game(code=self._generate_code(), started=False, exp_seq=[], seq=[], players=[])
        path = self.make_filepath(code=game.code)
        path.write_text(game.json())
        return game

    def start(self, game: Game):
        numbers = random.sample(range(1, 100), len(game.players) * 3)
        game.exp_seq = sorted(numbers)
        chunks = self._chunks(numbers, 3)
        for p, c in zip(game.players, chunks):
            p.all_numbers = c
        game.started = True
        self.update(game=game)

    def _chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def restart(self, game: Game):
        self.start(game=game)

    def finish(self, game: Game):
        os.remove(self.make_filepath(code=game.code).absolute())

    def existing(self, code: str) -> Optional[Game]:
        return Game.parse_file(self.make_filepath(code=code))

    def make_filepath(self, code: str) -> Path:
        return Path(self.dir, code + '.json')

    def _generate_code(self) -> str:
        return str(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))

    def update(self, game: Game):
        path = self.make_filepath(code=game.code)
        path.write_text(game.json())
