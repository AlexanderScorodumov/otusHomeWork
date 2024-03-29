from time import sleep
import unittest
from unittest.mock import Mock, patch
import homework8 as main
import concurrent.futures


class TestExceptionHandlers(unittest.TestCase):
    def test_GameCommand(self):       
        self.movableMock = Mock(main.Movable)
        self.movableMock.GetPosition.return_value = [1, 1]
        self.movableMock.GetVelocity.return_value = [2, 2]
        self.game = main.GameCommand(gameId=1)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.game.Execute)
            interpretCommand = main.InterpretCommand(gameId="1", objectId="1", operationId="Move", args="None")
            self.game.objects = {"1": self.movableMock}
            main.IoC.Resolve(main.Command, "Scopes.Current", "1").Execute()
            main.IoC.Resolve(None, "EventQueue", interpretCommand)
            sleep(1)
            self.game.gameQueue = None
            assert self.movableMock.GetPosition.call_count == 1
            assert self.movableMock.GetVelocity.call_count == 1
            assert self.movableMock.SetPosition.call_count == 1