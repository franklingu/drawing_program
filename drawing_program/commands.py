"""Built in commands
"""
from copy import deepcopy
from abc import ABC

from .utils import (
    InvalidInputException, UserExitException
)


class BaseCommand(ABC):
    """Base class for command"""
    COMMAND = None

    def __init__(self, state, command, *args, **kwargs):
        super(BaseCommand, self).__init__()
        self.prev_state = None
        self.done = False
        self.state = deepcopy(state)
        self.command = command

    def do(self, *args, **kwargs):
        self.prev_state = self.state
        self.state = self.do_execute(*args, **kwargs)
        self.done = True
        return self.state

    def do_execute(self, *args, **kwargs):
        raise NotImplementedError

    def undo(self, *args, **kwargs):
        if not self.done:
            raise InvalidInputException('Cannot undo not-yet-executed command')
        self.done = False
        return self.prev_state

    def redo(self, *args, **kwargs):
        if self.done:
            raise InvalidInputException('Cannot redo already-executed command')
        self.done = True
        return self.state


class CreateCanvasCommand(BaseCommand):
    """Implement create-canvas command"""
    COMMAND = 'C'

    def do_execute(self, *args, **kwargs):
        try:
            _, width, length = self.command.split()
            width = int(width)
            length = int(length)
        except (AttributeError, ValueError):
            raise InvalidInputException(
                'Invalid input format: {}'.format(self.command)
            )
        if width < 1 or length < 1:
            raise InvalidInputException(
                'Invalid canvas specified: {}'.format(self.command)
            )
        return [[' '] * width for _ in range(length)]


class DrawLineCommand(BaseCommand):
    """Implement create-canvas command"""
    COMMAND = 'L'

    def do_execute(self, *args, **kwargs):
        if self.state is None:
            raise InvalidInputException(
                'Invalid initialization: {}'.format(self.command)
            )
        try:
            _, x1, y1, x2, y2 = self.command.split()
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
        except (AttributeError, ValueError):
            raise InvalidInputException(
                'Invalid input format: {}'.format(self.command)
            )
        if x1 != x2 and y1 != y2:
            raise InvalidInputException(
                'Invalid input: {} -- not a line'.format(self.command)
            )
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if (x1 < 1 or x2 > len(self.state[0]) or
                y1 < 1 or y2 > len(self.state)):
            raise InvalidInputException(
                'Invalid line: {} -- overflowed'.format(self.command)
            )
        new_state = deepcopy(self.state)
        x1, y1, x2, y2 = x1 - 1, y1 - 1, x2 - 1, y2 - 1
        if x1 == x2:
            for y in range(y1, y2 + 1):
                new_state[y][x1] = 'x'
        else:
            for x in range(x1, x2 + 1):
                new_state[y1][x] = 'x'
        return new_state


class DrawRectangleCommand(BaseCommand):
    """Implement create-canvas command"""
    COMMAND = 'R'

    def do_execute(self, *args, **kwargs):
        if self.state is None:
            raise InvalidInputException(
                'Invalid initialization: {}'.format(self.command)
            )
        try:
            _, x1, y1, x2, y2 = self.command.split()
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
        except (AttributeError, ValueError):
            raise InvalidInputException(
                'Invalid input format: {}'.format(self.command)
            )
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if (x1 < 1 or x2 > len(self.state[0]) or
                y1 < 1 or y2 > len(self.state)):
            raise InvalidInputException(
                'Invalid rectangle: {} -- overflowed'.format(self.command)
            )
        new_state = deepcopy(self.state)
        x1, y1, x2, y2 = x1 - 1, y1 - 1, x2 - 1, y2 - 1
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if x == x1 or x == x2 or y == y1 or y == y2:
                    new_state[y][x] = 'x'
        return new_state


class BucketFillCommand(BaseCommand):
    """Implement create-canvas command"""
    COMMAND = 'B'

    def do_execute(self, *args, **kwargs):
        if self.state is None:
            raise InvalidInputException(
                'Invalid initialization: {}'.format(self.command)
            )
        try:
            _, x, y, color = self.command.split()
            x = int(x)
            y = int(y)
        except (AttributeError, ValueError):
            raise InvalidInputException(
                'Invalid input format: {}'.format(self.command)
            )
        if (x < 1 or x > len(self.state[0]) or
                y < 1 or y > len(self.state)):
            raise InvalidInputException(
                'Invalid point: {} -- overflowed'.format(self.command)
            )
        if self.state[y][x] != ' ':
            raise InvalidInputException(
                'Invalid point: {} -- not fillable'.format(self.command)
            )
        if len(color) != 1:
            raise InvalidInputException(
                'Invalid color: {}'.format(self.command)
            )
        new_state = deepcopy(self.state)
        x, y = x - 1, y - 1
        visited = set()
        dests = [(x, y)]
        while len(dests) > 0:
            dest_x, dest_y = dests.pop(0)
            if (dest_x, dest_y) in visited:
                continue
            if dest_x < 0 or dest_x >= len(new_state[0]):
                continue
            if dest_y < 0 or dest_y >= len(new_state):
                continue
            visited.add((dest_x, dest_y))
            if new_state[dest_y][dest_x] != ' ':
                continue
            new_state[dest_y][dest_x] = color
            dests.append((dest_x - 1, dest_y))
            dests.append((dest_x + 1, dest_y))
            dests.append((dest_x, dest_y - 1))
            dests.append((dest_x, dest_y + 1))
        return new_state


class QuitCommand(BaseCommand):
    """"""
    COMMAND = 'Q'

    def do_execute(self, *args, **kwargs):
        raise UserExitException('Thanks for using the program')
