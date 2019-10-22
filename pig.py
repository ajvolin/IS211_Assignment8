#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pig.py: IS 211 Assignment 8."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

# Imports
import sys
import argparse
import random
import time
from queue import Queue

class Players(object):
    """This class is used to track the players for a game of Pig.

    The attributes of this class are protected as they should not
    be accessed or set directly. This is ensures the integrity
    of the game.

    Attributes:
        _players (Queue): The players queue.
        _current_player (Player): The currently dequeued player.
    """

    def __init__(self, players):
        """ 
        The constructor for Players class. 

        Parameters: 
            players (Queue): The queue holding the players. 
        """

        self._players = players
        self._current_player = players.get()

    def get_current_player(self):
        """ 
        The getter for the _current_player attribute.

        Returns:
            (Player): The current player.
        """

        # Return the current player
        return self._current_player

    def get_next_player(self):
        """ 
        A method to get the next player in the Players queue.

        Returns:
            (Player): The current player.
        """

        # Add the current player back to the end of the queue
        self._players.put(self._current_player)
        # Get the next player from the queue and return it
        self._current_player = self._players.get()
        return self._current_player

    def get_players(self):
        """ 
        The getter for the _players attribute.

        Returns:
            (list): The players in the queue.
        """

        # Append the current player to the list and return it
        players_list = list(self._players.queue)
        players_list.append(self._current_player)
        return players_list


class Player(object):
    """This class is used to store details about a player.

    The attributes of this class are protected as they should not
    be accessed or set directly. This is ensures the integrity
    of the game.

    Attributes:
        _name (str): The player's name.
        _score (int): The player's total score.
        _current_score (int): The player's score for the current turn.
        _rolls (int): The player's number of rolls.
        _last_roll (int): The player's last roll.
    """

    def __init__(self, name):
        """ 
        The constructor for Player class. 

        Parameters: 
            name (string): The player's name.
        """

        self._name = name.strip()
        self._total_score = 0
        self._current_score = 0
        self._total_rolls = 0
        self._last_roll = 0

    def get_name(self):
        """ 
        The getter for the _name attribute.

        Returns:
            (strings): The player's name.
        """
        
        # Return the player's name
        return self._name

    def get_total_score(self):
        """ 
        The getter for the _total_score attribute.

        Returns:
            (int): The player's total score.
        """

        # Return the player's total score
        return self._total_score

    def get_current_score(self):
        """ 
        The getter for the _current_score attribute.

        Returns:
            (int): The player's current turn score.
        """

        # Return the player's current turn score
        return self._current_score

    def get_total_rolls(self):
        """ 
        The getter for the _total_rolls attribute.

        Returns:
            (int): The player's number of rolls.
        """

        # Return the player's rolls
        return self._total_rolls

    def get_last_roll(self):
        """ 
        The getter for the _last_roll attribute.

        Returns:
            (int): The player's last roll.
        """

        # Return the player's last roll
        return self._last_roll

    def update_total_rolls(self):
        """ 
        Method to increment the _total_rolls attribute.
        """

        # Incremene the attribute by 1
        self._total_rolls += 1

    def update_turn_score(self, score):
        """ 
        Method to increment the _current_score attribute.

        Parameters: 
            score (int): The amount to increment the current score by.
        """

        # Increment the attribute by the passed value
        self._current_score += score

    def update_last_roll(self, roll):
        """ 
        Method to increment the _last_roll attribute.

        Parameters: 
            score (int): The player's last roll.
        """

        # Increment the attribute by the passed value
        self._last_roll = roll

    def reset_turn_stats(self):
        """ 
        Method to reset the _current_score attribute.
        """

        # Set the attribute value to 0
        self._current_score = 0

    def commit_score(self):
        """ 
        Method to increment the _total_score and _total_rolls attributes.
        """

        # Update the player's total score and total roll count
        self._total_score += self._current_score

    def request_action(self):
        """ 
        Method to return the player's desired action.

        Returns:
            (str): The player's desired action.
        """

        # Return the player's input
        return input("Enter 'r' to roll the die, or 'h' to hold. What you you like to do? ")


class ComputerPlayer(Player):
    """This class is used to store details about a computer player.

    This class is a subclass of Player.

    Attributes:
        _name (str): The player's name.
        _score (int): The player's total score.
        _current_score (int): The player's score for the current turn.
        _rolls (int): The player's number of rolls.
        _last_roll (int): The player's last roll.
    """
    
    def request_action(self):
        """ 
        Method to return the computer player's desired action.

        Returns:
            (str): The computer player's desired action.
        """

        # Determine the computer player's desired action
        action = "r" if self._current_score < min(25, (100 - (self._total_score + self._current_score))) else "h"
        # Return the action
        return action


class PlayerFactory:
    """This class is used to get the correct player type."""

    def get_player(self, player_name, player_type):
        """
        Returns the correct player type based on argument value
        set on the command line.

        Parameters: 
            player_name (str): The player's name.
            player_type (str): The type of player.

        Returns:
            (Player) or (ComputerPlayer)
        """

        # Return correct player class
        if player_type == "human":
            return Player(player_name)
        if player_type == "computer":
            return ComputerPlayer(player_name)


class Die(object):
    """This class is used to generate a die for a game."""

    def __init__(self):
        """ 
        The constructor for Player class. 

        Seeds the random generator with 0.
        """

        # Set the seed to 0
        random.seed(0)

    def roll(self):
        """ 
        Method to 'roll' the die.

        Returns:
            (int): The result of the 'roll', an integer between 1 and 6
        """

        # Return a random integer between 1 and 6
        return random.randint(1, 6)


class Game(object):
    """This class is used to run a game of Pig.

    The attributes of this class are protected as they should not
    be accessed or set directly. Additionally, most functions of
    this class are protected to prevent manipulation of the game.
    This is ensures the integrity of the game.

    Attributes:
        _players (Players): The instantiated players for this game.
        _die (Die): The die instantiated for this game.
        _active_turn (bool): Whether or not the game is in active turn.
        _end_game (bool): Whether or not the game has ended.
    """

    def __init__(self, players):
        """ 
        The constructor for Game class.

        Instantiates the players and die for the current game.

        Parameters: 
            players (Queue): The players queue for the current game.
        """

        # Instantiate a Players object with the players queue
        self._players = Players(players)
        # Instantiate the Die to be used for the current game
        self._die = Die()
        # Track the game status
        self._active_turn = True
        self._end_game = False

    def start(self):
        """The method to start the current game."""

        # Call the protected _turn method to start the game
        self._turn()

    def _accounce_winner(self):
        """The method to announce the winner."""

        winner = sorted(((player.get_name(), player.get_last_roll(), player.get_total_score())
                       for player in self._players.get_players()),
                             key=lambda player: (player[1]),
                             reverse=True)[0]

        print("\n\nCongratulations {}, you rolled a {} and your total score is {}. You won the game!"
                              .format(winner[0], winner[1], winner[2]))

    def _game_over(self):
        """
            The method to run at the end of the current game.

            Prints a leaderboard with the scores and number of
            rolls for each of the current game's players.
        """

        # Get the players and create the leaderboard tuple
        leaderboard = ((player.get_name(), player.get_total_score(), player.get_total_rolls())
                       for player in self._players.get_players())

        print("\nLEADERBOARD\n")
        # Print leaderboard header border
        print("+-{:<32}-+-{:>10}-+-{:>10}-+".format("-"*32, "-"*10, "-"*10))
        # Print the leaderboard header
        print("| {:<32} | {:>10} | {:>10} |".format(
            'Player', 'Score', '# of Rolls'))
        # Sort by highest scores first and print the details
        for player in sorted(leaderboard,
                             key=lambda player: (player[1]),
                             reverse=True):
            # Print the cell separators
            print("|-{:<32}-+-{:>10}-+-{:>10}-|".format("-"*32, "-"*10, "-"*10))
            # Print the player's details
            print("| {:<32} | {:>10} | {:>10} |".format(
                player[0], player[1], player[2]))

        # Print leaderboard footer border
        print("+-{:<32}-+-{:>10}-+-{:>10}-+".format("-"*32, "-"*10, "-"*10))

    def _play(self, player):
        """
        The method to control a player's turn.

        Parameters: 
            player (Player): The player who's turn it is.
        """

        # Request the current player's desired action
        action = player.request_action()

        # Player chose to roll
        if action == "r":
            # Roll the die and add to roll total for the turn
            roll = self._die.roll()
            player.update_total_rolls()
            player.update_last_roll(roll)
            # If the player rolls 1, reset the current
            # score and commit the current rolls count
            # to the player's Player object, and exit
            # the loop.
            if roll == 1:
                player.reset_turn_stats()
                player.commit_score()
                print("Ouch {}, you rolled a {} and lost all points you accumulated during this turn. Your score for this turn is {}. Your total score is {}.".format(
                    player.get_name(), roll, player.get_current_score(), player.get_total_score()))
                self._active_turn = False
            # If the player rolled other than a 1, update the
            # current score to the value of the roll, check
            # to see if the player's total is >= 100 and end
            # the game, otherwise ask the player for their
            # next action
            else:
                player.update_turn_score(roll)
                if (player.get_current_score() + player.get_total_score()) >= 100:
                    player.commit_score()
                    player.reset_turn_stats()
                    self._end_game, self._active_turn = True, False
                else:
                    print("Nice {}! You rolled a {}. Your current score for this turn is {}. Your total score is {}".format(
                            player.get_name(),
                            roll,
                            player.get_current_score(),
                            player.get_current_score() + player.get_total_score()
                        )
                    )
        # Player chose to hold, commit their current score and
        # roll count to their Player object and exit the loop
        elif action == "h":
            player.commit_score()
            print("{}, you held. Your score for this turn is {}. Your total score is {}.".format(
                player.get_name(), player.get_current_score(), player.get_total_score()))
            player.reset_turn_stats()
            self._active_turn = False
        # The player entered an invalid action
        else:
            print("You entered an invalid action.")

    def _turn(self, next_player=False):
        """
        The method to control player turns.

        Parameters: 
            next_player (bool): Used to decide if the next player
                                should be called to play. Defaults
                                to False.
        """

        # Get the player for the current turn
        player = self._players.get_current_player(
        ) if not next_player else self._players.get_next_player()

        # Reset the _active_turn attribute to True
        self._active_turn = True

        # Let the players know who's turn it is
        print("\n{}, it's your turn. Your current score is {}".format(
            player.get_name(), player.get_total_score()))

        # Keep the current player's turn until they roll a 1,
        # win the game, or hold.
        while self._active_turn and not self._end_game:
            self._play(player)

        # Check to see if the game is over, if not go to the next player,
        # otherwise call the protected _game_over function to trigger the
        # leaderboard display
        if not self._end_game:
            self._turn(True)
        else:
            self._accounce_winner()
            self._game_over()


class TimedGame(Game):
    """This class is used to run a timed game of Pig.

    Inherits from the Game class

    Attributes:
        _players (Players): The instantiated players for this game.
        _die (Die): The die instantiated for this game.
        _active_turn (bool): Whether or not the game is in active turn.
        _end_game (bool): Whether or not the game has ended.
        _end_time (time): The time the game was started.
    """

    def start(self):
        """The method to start the current game."""
        # Call the protected _turn method to start the game
        self._end_time = time.time() + 60
        self._turn()

    def _accounce_winner(self):
        """The method to announce the winner."""
        
        if self._end_time < time.time():
            winner = sorted(((player.get_name(), player.get_last_roll(), player.get_total_score())
                       for player in self._players.get_players()),
                             key=lambda player: (player[1]),
                             reverse=True)[0]

            print("\n\nCongratulations {}, you had the highest score of {} before time ran out. You won the game!"
                              .format(winner[0], winner[2]))
        else:
            super()._accounce_winner()

    def _play(self, player, time_left):
        """
        The method to control a player's turn.
        
        Prints the time left in the game and then calls
        the parent _play method.

        Parameters: 
            player (Player): The player who's turn it is.
        """

        print("There are {} seconds left in this game.".format(time_left))
        super()._play(player)

    def _turn(self, next_player=False):
        """
        The method to control player turns.

        Parameters: 
            next_player (bool): Used to decide if the next player
                                should be called to play. Defaults
                                to False.
        """
        # Get the player for the current turn
        player = self._players.get_current_player(
        ) if not next_player else self._players.get_next_player()

        # Reset the _active_turn attribute to True
        self._active_turn = True

        # Let the players know who's turn it is
        print("\n{}, it's your turn. Your current score is {}".format(
            player.get_name(), player.get_total_score()))

        # Keep the current player's turn until they roll a 1,
        # win the game, hold, or the time has expired
        while self._active_turn and not self._end_game and time.time() < self._end_time:
            self._play(player, round(self._end_time - time.time(), 0))

        if time.time() >= self._end_time:
            self._end_game = True
            self._active_turn = False

        # Check to see if the game is over, if not go to the next player,
        # otherwise call the protected _game_over function to trigger the
        # leaderboard display
        if not self._end_game:
            self._turn(True)
        else:
            self._accounce_winner()
            self._game_over()


class TimedGameProxy(Game):
    """This class is used to get the correct game type.
    
    Attributes:
        _players (Players): The instantiated players for this game.
        _game (Game): The instantiated game.
    """

    def __init__(self, players):
        """ 
        The constructor for TimedGameProxy class.

        Parameters: 
            players (Queue): The players queue for the current game.
        """

        self._players = players
        self._game = None

    def start(self, timed):
        """
        The method to start the game.

        Parameters:
            timed (bool): Whether or not the game is timed.
        """

        if timed:
            self._game = TimedGame(self._players)
        else:
            self._game = Game(self._players)
       
        self._game.start()


def main():
    """The method that runs when the program is executed."""

    # Setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1',
                        help='Player 1 type, computer or human.',
                        type=str
                        )
    parser.add_argument('--player2',
                        help='Player 2 type, computer or human.',
                        type=str
                        )
    parser.add_argument('--timed',
                        action='store_true',
                        help='Whichever player has the most points after one minute wins the game.'
                        )
    args = parser.parse_args()

    # Check for required arguments and correct values
    if not args.player1 and not args.player2:
        print("The --player1 and --player2 arguments are required. Valid types are computer or human. Please try again.")
        sys.exit()

    if not args.player1.lower() == "computer" and not args.player1.lower() == "human":
        print("You entered an invalid player type for player1. Valid types are computer or human. Please try again.")
        sys.exit()

    if not args.player2.lower() == "computer" and not args.player2.lower() == "human":
        print("You entered an invalid player type for player2. Valid types are computer or human. Please try again.")
        sys.exit()

    # Create a queue for the players
    players = Queue()

    # Ask for player names if they are human
    player1_name = "Computer [Player 1]" if args.player1.lower() == "computer" \
        else input("What is Player 1's name? ")

    player2_name = "Computer [Player 2]" if args.player2.lower() == "computer" \
        else input("What is Player 2's name? ")

    # Use PlayerFactory to get correct player classes and add to players queue
    players.put(PlayerFactory().get_player(player1_name, args.player1.lower()))
    players.put(PlayerFactory().get_player(player2_name, args.player2.lower()))

    # Use GameFactory to get correct game class and start the game
    TimedGameProxy(players).start(args.timed)

    # Exit the program after the game is over
    sys.exit()


if __name__ == '__main__':
    main()
