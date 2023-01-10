import os.path
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class UI:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        SCREEN_WIDTH = 1200
        SCREEN_HEIGHT = 750
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.screen.fill((34, 139, 34))
        print(pygame.font.get_fonts())
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.card_images = {}
        for suit in ['c', 'd', 'h', 's']:
            for value in range(1, 14):
                key_card = str(value) + suit
                self.card_images[key_card] = pygame.image.load(os.path.join('res', key_card + '.png'))

    def render(self, betting_round):
        y = 50
        x = 150
        for i in range(len(betting_round.deal.game.players)):
            player = betting_round.deal.game.players[i]
            player_deal = betting_round.deal.player_deal_states[i]
            player_round = betting_round.player_round_states[i]
            player_name_surface = self.font.render(player.name, True, (0, 0, 0))
            self.screen.fill((34, 139, 34))
            self.screen.blit(player_name_surface, (0, y))
            self.screen.blit(self.card_images[
                                 self.card_to_dictionary_key(betting_round.deal.player_deal_states[i].hand[0])], (x, y))
            self.screen.blit(self.card_images[
                                 self.card_to_dictionary_key(betting_round.deal.player_deal_states[i].hand[1])],
                             (x + 100, y))
            player_stack_surface = self.font.render(str(player.stack), True, (0, 0, 0))
            player_folded_surface = self.font.render(str(player_deal.folded), True, (0, 0, 0))
            player_current_bet_surface = self.font.render(str(player_round.total_bet), True, (0, 0, 0))
            self.screen.blit(player_stack_surface, (350, y))
            self.screen.blit(player_folded_surface, (450, y))
            self.screen.blit(player_current_bet_surface, (550, y))
            y += 125
        pygame.display.update()
        pygame.event.get()

    @staticmethod
    def card_to_dictionary_key(card):
        return str(card.value) + card.suit


    def button(pygame.sprite.Sprite)
        def __init__(self):
            super(button, self).__init__()
            self.surf = pygame.Surface((75, 25))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect()

            def on_button_click():
                event.type
                user_event == 'f'




