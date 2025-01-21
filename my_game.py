#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod
import io
import platform
from typing import Callable, Any
from io import BufferedIOBase, StringIO
from pathlib import Path
import argparse, asyncio, os, re, sys

import discord
from PIL import Image, ImageDraw, ImageFont

# You can add game constants here, like a board size for example

# Default Timeouts :
TIMEOUT_LENGTH = 1  # sec
DISCORD_TIMEOUT = 60  # sec

WIDTH = 10
HEIGHT = 10

CELL_SIZE = 50 # pixels
SIDE_OFFSET = 20

# Usefull emojis :
EMOJI_NUMBERS = ("0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣")
EMOJI_COLORS = ("🟠", "🔴", "🟡", "🟢", "🔵", "🟣", "🟤", "⚪️", "⚫️")
CODE_COLORS = ("ff6723", "f8312f", "fcd53f", "00d26a", "0074ba", "8d65c5", "6d4534", "ffffff", "000000")
CODE_COLORS = dict(zip(EMOJI_COLORS, ('#'+col for col in CODE_COLORS)))

# what is the type of a valid move or a valid input (when it has a specific format) to use in typing
ValidMove = Any
ValidInput = str

# input and output functions types
InputFunction = Callable[
    ..., str
]  # function asking a discord player to make a move, returns the discord answer
OutputFunction = Callable[
    [str], None
]  # function called when an AI wants to "talk" to discord, the argument being the message


class Player(ABC):

    ofunc = None

    def __init__(self, no: int, name: str = None, **kwargs):
        """The abstract Player constructor

        Args:
            no (int): player number/id
            name (str, optional): The player name. Defaults to None.
        """
        # You can add any number of kwargs you want that will be passed in the discord command for your game

        self.no = no

        # These can be altered to give personnality to your game display (with emojis for example)
        self.icon = self.no
        self.name = name
        self.rendered_name = None

    @abstractmethod
    async def start_game(self, no, w, h, p_pos):
        self.alive = True
        self.no = no
        self.w = w
        self.h = h
        self.p_pos = p_pos
        self.pos = p_pos[self.no]
        await Player.print(f"{self} is ready!")

    @abstractmethod
    async def lose_game(self):
        await Player.print(f"{self} is eliminated")

    async def ask_move(
        self, *args, **kwargs
    ) -> tuple[ValidMove, None] | tuple[None | str]:
        pass

    @abstractmethod
    async def tell_move(self, move: ValidInput):
        pass

    async def tell_other_players(self, players: list[Player], move: ValidInput):
        for other_player in players:
            if self != other_player and other_player.alive:
                await other_player.tell_move(move)

    @staticmethod
    async def sanithize(
        userInput: str, **kwargs
    ) -> tuple[ValidMove, None] | tuple[None | str]:
        """Parses raw user input text into an error message or a valid move

        Args:
            userInput (`str`): the raw user input text

        Returns:
            `tuple[ValidMove, None] | tuple[None | str]`
        """
        # You can add any number of kwargs you want
        # that will be necessary to parse the input
        # (like the game board for example),
        # just remember to pass them when calling this method.

        if userInput == "stop":
            # When a human player (or an AI, who knows) wants to abandon.
            return None, "user interrupt"

        # Here, you can process your userInput,
        # try to get all wrong input cases out as errors
        # to make sure your game doesn't break.
        moves = ("up", "down", "left", "right", "ready")
        if userInput not in moves:
            await Player.print(f"invalid move: {userInput}")
            return None, "invalid move"

        processed_input: ValidMove = userInput

        return processed_input, None

    @staticmethod
    async def print(output: StringIO | str, send_discord=True, end="\n"):
        if isinstance(output, StringIO):
            text = output.getvalue()
            output.close()
        else:
            text = output + end
        print(text, end="")
        if Player.ofunc and send_discord:
            if len(text) < 300:
                await Player.ofunc(text)
            else:
                # Create a blank image with white background
                img = Image.new("RGB", (WIDTH * CELL_SIZE + 2*SIDE_OFFSET, HEIGHT * CELL_SIZE + 2*SIDE_OFFSET), color="#313338")
                draw = ImageDraw.Draw(img)

                radius = CELL_SIZE//2*0.7

                # Draw the grid
                for y, line in enumerate(text.split("\n")):
                    for x, char in enumerate(line):
                        draw.circle(((x+0.5)*CELL_SIZE + SIDE_OFFSET, (y+0.5)*CELL_SIZE + SIDE_OFFSET), radius, CODE_COLORS[char])

                fp = io.BytesIO()
                img.save(fp, format="PNG")
                fp.seek(0)
                file = discord.File(fp=fp, filename="board.png")
                await Player.ofunc(file=file)

    def __str__(self):
        return self.rendered_name


class Human(Player):

    def __init__(
        self, no: int, name: str = None, ifunc: InputFunction = None, **kwargs
    ):
        """The human player constructor
        Let ifunc be None to get terminal input (for a local game)

        Args:
            no (`int`): player number/id
            name (`str`, optional): The player name. Defaults to None.
            ifunc (`InputFunction`, optional): The input function. Defaults to None.
        """
        super().__init__(no, name, **kwargs)
        self.ifunc = ifunc

        # Here you can personnalize human players name specifically
        self.rendered_name = (
            f"{self.name} {self.icon}" if name else f"Player {self.icon}"
        )

    async def start_game(self, *args, **kwargs):
        await super().start_game(*args, **kwargs)

    async def lose_game(self):
        await super().lose_game()

    # Don't forget to replace <**kwargs> with the arguments necessary for parsing the input
    async def ask_move(self, *args, **kwargs):
        await super().ask_move(*args, **kwargs)
        # You can customize your message asking for a move here :
        await Player.print(f"Awaiting {self}'s move : ", end="")
        try:
            user_input = await self.input()
        except asyncio.TimeoutError:
            await Player.print(
                f"User did not respond in time (over {DISCORD_TIMEOUT}s)"
            )
            return None, "timeout"
        # This is where the kwargs are usefull :
        return await Human.sanithize(user_input, **kwargs)

    async def tell_move(self, move: ValidInput):
        return await super().tell_move(move)

    async def input(self):
        if self.ifunc:
            user_input = await asyncio.wait_for(
                self.ifunc(self.name), timeout=DISCORD_TIMEOUT
            )
            await Player.print(user_input, send_discord=False)
            return user_input
        else:
            return input()


class AI(Player):

    @staticmethod
    def prepare_command(progPath: str | Path):
        """Prepares the command to start the AI

        Args:
            progPath (`str` | `Path`): the path to the program

        Raises:
            Exception: File not found error

        Returns:
            `str`: the command to start the AI
        """
        path = Path(progPath)
        if not path.is_file():
            raise FileNotFoundError(f"File {progPath} not found\n")

        match path.suffix:
            case ".py":
                if platform.system() == "Windows":
                    return f"python {progPath}"
                else:
                    return f"python3 {progPath}"
            case ".js":
                return f"node {progPath}"
            case ".class":
                return f"java -cp {os.path.dirname(progPath)} {os.path.splitext(os.path.basename(progPath))[0]}"
            case _:
                return f"./{progPath}"

    def __init__(self, no: int, prog_path: str, discord: bool, **kwargs):
        """The AI player constructor

        Args:
            no (int): player number/id
            prog_path (str): AI's program path
            discord (bool): if it is instantiated through discord to associate the user tag
        """
        super().__init__(no, Path(prog_path).stem, **kwargs)
        self.prog_path = prog_path
        self.command = AI.prepare_command(self.prog_path)

        # Once again, you can personnalize how the AI player will be called during the game here
        if discord:
            # if it's through discord, self.name should be the discord user's ID
            self.rendered_name = f"<@{self.name}>'s AI {self.icon}"
        else:
            self.rendered_name = f"AI {self.icon} ({self.name})"

    async def drain(self):
        return
        if self.prog.stdin.transport._conn_lost:
            self.prog.stdin.close()
            self.prog.stdin = asyncio.subprocess.PIPE
        else:
            await self.prog.stdin.drain()

    async def start_game(self, *args, **kwargs):
        # You can specify here what parameters are required to start a game for an AI player.
        # For example : board size, number of players...
        await super().start_game(*args, **kwargs)
        cmd = AI.prepare_command(self.prog_path)
        self.prog = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        if self.prog.stdin:
            # Here, write the NORMALIZED message you'll send to the AIs for them to start the game.
            # This is what this method's kwargs are for, the AI will need
            self.prog.stdin.write(f"{self.w} {self.h}\n".encode())
            self.prog.stdin.write(f"{len(self.p_pos)} {self.no+1}\n".encode())

            for i, pos in enumerate(self.p_pos):
                self.prog.stdin.write(f"{pos[0]} {pos[1]}\n".encode())

            await self.drain()

            pass
    async def lose_game(self):
        await super().lose_game()

    # Don't forget to replace <**kwargs> with the arguments necessary for parsing the input
    async def ask_move(
        self, debug: bool = True, **kwargs
    ) -> tuple[tuple[int, int] | None, str | None]:
        await super().ask_move(**kwargs)
        try:
            while True:
                if not self.prog.stdout:
                    return None, "communication failed"
                progInput = await asyncio.wait_for(
                    self.prog.stdout.readuntil(), TIMEOUT_LENGTH
                )
                # progInput = await self.read_until_delimiter(self.prog.stdout, TIMEOUT_LENGTH)

                if not isinstance(progInput, bytes):
                    continue
                progInput = progInput.decode().strip()

                if progInput.startswith("Traceback"):
                    output = StringIO()
                    if debug:
                        print(file=output)
                        print(progInput, file=output)
                        progInput = self.prog.stdout.read()
                        if isinstance(progInput, bytes):
                            print(progInput.decode(), file=output)
                        await Player.print(output)
                    return None, "error"

                if progInput.startswith(">"):
                    # Any bot can write lines starting with ">" to debug in local.
                    # It is recommended to remove any debug before playing
                    # against other players to avoid reverse engineering!
                    if debug:
                        await Player.print(f"{self} {progInput}")
                else:
                    break

            # You can customize the message all bots will send to announce their moves here :
            await Player.print(f"{self}'s move : {progInput}")

        except (asyncio.TimeoutError, asyncio.exceptions.IncompleteReadError) as e:
            await Player.print(f"AI did not respond in time (over {TIMEOUT_LENGTH}s)")
            return None, "timeout"

        # This is where the kwargs are usefull :
        return await AI.sanithize(progInput, **kwargs)

    async def tell_move(self, move: ValidInput):
        if self.prog.stdin:
            # The AIs should keep track of who's playing themselves.
            self.prog.stdin.write(f"{move}\n".encode())
            await self.drain()

    async def stop_game(self):
        try:
            self.prog.terminate()
            await self.prog.wait()
        except ProcessLookupError:
            pass


# Here is a place to define functions useful for your game, typically:
#  - checking for a win or a draw,
#  - drawing the grid in terminal or in discord
#  - processing a move
#  - ...


class MoveError(Exception):
    pass


class Board:
    def __init__(self, w: int, h: int, p_pos: list[int]):
        self.w = w
        self.h = h
        self.p_pos = list(p_pos)
        self.grid = [[0 for _ in range(w)] for _ in range(h)]
        for i, pos in enumerate(p_pos):
            x, y = pos
            self.grid[y][x] = i + 1

    def get_delta(self, move: str) -> tuple[int, int]:
        moves = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        out = moves.get(move, None)
        if not out:
            raise ValueError("Invalid move")
        return out

    def move(self, i: int, move: ValidMove):
        try:
            dx, dy = self.get_delta(move)
        except ValueError:
            raise ValueError("Invalid move")

        if not (0 <= i < len(self.p_pos)):
            raise ValueError("Invalid player")

        x, y = self.p_pos[i]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.w and 0 <= ny < self.h):
            raise MoveError("Out of bounds")

        if self.grid[ny][nx] != 0:
            raise MoveError("Collision")

        self.grid[ny][nx] = i + 1
        self.p_pos[i] = (nx, ny)

    def display(self):
        out = StringIO()
        for y in range(self.h):
            for x in range(self.w):
                out.write(EMOJI_COLORS[self.grid[y][x]])
            out.write("\n")
        out.seek(0)
        return out


async def game(
    players: list[Human | AI], p_pos: list[int], w: int, h: int, debug: bool, **kwargs
) -> tuple[list[Human | AI], Human | AI | None, dict]:
    """The function handling all the game logic.
    Once again, you can add as many kwargs as you need.
    Note that you can return anything you need that will be treated in `main()` after the specified args.

    Args:
        players (`list[Human | AI]`): The list of players
        debug (`bool`): _description_

    Returns:
        `tuple[list[Human | AI], Human | AI | None, dict, ...]`: A whole bunch of game data to help display and judge the result
    """

    nb_players = len(players)
    alive_players = nb_players
    errors = {}  # This is for logging and debugginf purposes
    starters = (
        player.start_game(turn, w, h, p_pos) for turn, player in enumerate(players)
    )
    await asyncio.gather(*starters)
    turn = 0
    winner = None

    # Initialize general game objects here, like the board
    board = Board(w, h, p_pos)

    # game loop
    while alive_players >= 2:
        i = turn % nb_players
        player = players[i]

        if not player.alive:
            # It is essential to notify of a player "death" so that AIs can skip their turn.
            # Replace `None` by a NORMALIZED simple value signifying an incorrect move.
            await player.tell_other_players(players, f"death {i}")

        else:
            await Player.print(f"Turn {turn} : player {player}")
            await Player.print(board.display())  # Render the grid for the player here

            # player input
            user_input, error = None, None
            while not user_input:
                # Don't forget to give the kwargs necessary for an AI (or a player) to understand what's asked
                user_input, error = await player.ask_move(debug, **kwargs)
                if isinstance(player, AI) or error in ("user interrupt", "timeout"):
                    break

            # saving eventual error
            if not user_input:
                await player.lose_game()
                errors[player] = error
                player.alive = False
                alive_players -= 1
                # It is essential to notify of a player "death" so that AIs can skip their turn.
                # Replace `None` by a NORMALIZED simple value signifying an incorrect move.
                await player.tell_other_players(players, f"death {i}")

            else:
                # Apply the user_input to the game here, it already went through sanithization so it is a ValidMove
                # You'll also need to convert to a ValidInput to notify all the AIs of the played move
                try:
                    board.move(i, user_input)
                except MoveError as e:
                    await player.lose_game()
                    errors[player] = error
                    player.alive = False
                    alive_players -= 1
                    await player.tell_other_players(players, f"death {i}")
                except ValueError as e:
                    raise  # Should not happen

                await player.tell_other_players(players, f"move {i} {user_input}")

                # Check for wins or draw here.
                # Any end must break the `while alive_players >= 2`.
                # Do this step early to avoid an infinite loop!

                # Nothing to do here for snake

        turn += 1

    if alive_players == 1:
        # nobreak
        # winner = [player for player in players if player.alive][0]
        winner = next(player for player in players if player.alive)

    enders = (player.stop_game() for player in players if isinstance(player, AI))
    await asyncio.gather(*enders)

    # You can add extra returned stuff here, like the final board and other stuff
    return players, winner, errors


async def main(
    raw_args: str = None,
    ifunc: InputFunction = None,
    ofunc: OutputFunction = None,
    discord=False,
):
    # these arguments should not be messed with because that's how the discord bot works

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "prog", nargs="*", help="AI program to play the game ('user' to play yourself)"
    )
    parser.add_argument(
        "-g",
        "--grid",
        type=int,
        nargs=2,
        default=[WIDTH, HEIGHT],
        metavar=("WIDTH", "HEIGHT"),
        help="size of the grid",
    )
    parser.add_argument(
        "-p",
        "--players",
        type=int,
        default=2,
        metavar="NB_PLAYERS",
        help="number of players (if more players than programs are provided, the other ones will be filled as real players)",
    )
    parser.add_argument(
        "-P",
        "--pos",
        type=int,
        nargs=2,
        action="append",
        metavar=("X", "Y"),
        help="initial position of a player",
    )
    parser.add_argument(
        "-s", "--silent", action="store_true", help="only show the result of the game"
    )
    parser.add_argument(
        "-n",
        "--nodebug",
        action="store_true",
        help="do not print the debug output of the programs",
    )
    # Add here any extra argument you need to define the game (board size for example)

    args = parser.parse_args(raw_args)
    width, height = args.grid
    p_pos = args.pos

    Player.ofunc = ofunc
    players = []
    ai_only = True
    pattern = re.compile(r"^\<\@[0-9]{18}\>$")
    for i, name in enumerate(args.prog):
        if name == "user":
            players.append(Human(i))  # Add extra arguments extracted from `args`
            ai_only = False
        elif pattern.match(name):
            players.append(
                Human(i, name, ifunc)
            )  # Add extra arguments extracted from `args`
            ai_only = False
        else:
            players.append(
                AI(i, name, discord)
            )  # Add extra arguments extracted from `args`

    while len(players) < args.players:
        players.append(Human(len(players)))  # Add extra arguments extracted from `args`
        ai_only = False

    if p_pos is None:
        p_pos = [(0, 0), (width - 1, height - 1), (0, height - 1), (width - 1, 0)][
            : len(players)
        ]

    origin_stdout = sys.stdout
    if args.silent:
        if not ai_only:
            output = StringIO("Game cannot be silent since humans are playing")
            tmp = output.getvalue()
            await Player.print(output)
            raise Exception(tmp)
        if discord:
            Player.ofunc = None
        else:
            sys.stdout = open(os.devnull, "w")

    players, winner, errors = await game(
        players, p_pos, width, height, not args.nodebug
    )  # Add extra arguments extracted from `args`

    if args.silent:
        sys.stdout = origin_stdout
        Player.ofunc = ofunc
    else:
        # print whatever you want when not silent, often the final board
        ...
    ...  # another place to display things

    return (
        players,
        winner,
        errors,
    )  # this should not be messed with because that's how the discord bot works


if __name__ == "__main__":
    asyncio.run(main())
