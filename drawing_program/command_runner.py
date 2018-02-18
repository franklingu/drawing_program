"""Run commands
"""
from .commands import (
    CreateCanvasCommand, DrawLineCommand, DrawRectangleCommand,
    BucketFillCommand, QuitCommand,
)
from .utils import (
    InvalidInputException, UnknownCommandException, UserExitException
)


class CommandRunner(object):
    """\CommandRunner"""

    def __init__(self, *args, **kwargs):
        super(CommandRunner, self).__init__()
        self.state = None
        self.commands = []
        self.command_factory = {
            CreateCanvasCommand.COMMAND: CreateCanvasCommand,
            DrawLineCommand.COMMAND: DrawLineCommand,
            DrawRectangleCommand.COMMAND: DrawRectangleCommand,
            BucketFillCommand.COMMAND: BucketFillCommand,
            QuitCommand.COMMAND: QuitCommand,
        }

    def run_command(self, command_line, *args, **kwargs):
        try:
            cmd, *rest = command_line.split()
        except (ValueError, AttributeError):
            return 'Unknown command: {}'.format(command_line)
        try:
            cmd_cls = self.command_factory[cmd]
        except KeyError:
            return 'Unknown command: {}'.format(command_line)
        try:
            cmd_ins = cmd_cls(self.state, command_line)
            new_state = cmd_ins.do()
        except InvalidInputException as err:
            return str(err)
        except UnknownCommandException as err:
            return str(err)
        except UserExitException as err:
            return str(err), True
        self.state = new_state
        self.commands.append(cmd_ins)
        return self.state_repr

    @property
    def state_repr(self):
        if self.state is None:
            return ''
        wrap_line = ''.join(['-'] * (len(self.state[0]) + 2))
        res = [wrap_line]
        for row in self.state:
            res.append('|' + ''.join(row) + '|')
        res.append(wrap_line)
        return '\n'.join(res)
