'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import eval7, random, statistics, math

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        print('works :)')
        pass

    def handle_new_round(self, game_state, round_state, active):
        
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        #previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        #opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        #continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        hr = eval7.HandRange("22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 93s+, 84s+, 74s+, 64s+, 54s, 43s, A2o+, K2o+, Q3o+, J5o+, T6o+, 96o+, 86o+, 76o") #stores all possible hands in the given range (edit the argument of HandRange with desired range)
        randnum = random.random()
        if street == 0:
            for hand in hr: #hand is of the form ((a,b),c) where (a,b) is your dealt hand, and c is the probability that you would play with that hand (i.e 0<c<1 corresponds to a mixed strategy)
                if hand[0] == (eval7.Card(my_cards[0]),eval7.Card(my_cards[1])): 
                    if randnum <= hand[1]:
                        if CallAction in legal_actions:
                            return CallAction()
                        else:
                            return CheckAction()
                    else:
                        return FoldAction()
            return FoldAction()
        else:
            score_list = [] 
            print(score_list)
            for hand in hr:
                score = eval7.evaluate([hand[0][0],hand[0][1]] + [eval7.Card(y) for y in board_cards]) #this evaluates the strength of your current hand including cards on the board
                score_list.append(score)
            my_cards_score = eval7.evaluate([eval7.Card(y) for y in my_cards] + [eval7.Card(y) for y in board_cards])
            if my_cards_score >= statistics.median(score_list): #only runs if your hand is better than the median hand in your range
                if CallAction in legal_actions:
                    return CallAction()
                elif RaiseAction in legal_actions:
                    min_raise, max_raise = round_state.raise_bounds()
                    return RaiseAction(str(max(min_raise,min(max_raise, math.floor((my_contribution + opp_contribution)/2))))) #raises to half of the current pot if legal, and bet as much as possible otherwise
        if CheckAction in legal_actions:  # check-call
            return CheckAction()
        return FoldAction()


if __name__ == '__main__':
    run_bot(Player(), parse_args())