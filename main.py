from model import Game, Player
from UI import UI

players = [Player('Adrian'), Player('Zach'), Player('Aditya')]
ui = UI()
game = Game(players, ui)


game.play_game()






