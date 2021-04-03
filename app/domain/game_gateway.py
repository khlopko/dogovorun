from typing import Optional

from app.domain.game import Game
from app.domain.player import Player


class GameGateway:

    def create(self) -> Game:
        pass

    def join(self, code: str, player: Player) -> Game:
        pass

    def start(self, game: Game):
        pass

    def restart(self, game: Game):
        pass

    def finish(self, game: Game):
        pass

    def existing(self, code: str) -> Optional[Game]:
        pass

    def update(self, game: Game):
        pass
