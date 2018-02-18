"""entry point for drawing program
"""
from .command_runner import CommandRunner


def main():
    runner = CommandRunner()
    should_exit = False
    while not should_exit:
        try:
            command_line = input('enter command: ')
            result = runner.run_command(command_line)
            if isinstance(result, str):
                print(result)
            elif isinstance(result, tuple):
                should_exit = result[1]
                print(result[0])
        except Exception as err:
            print('Unhandled exception happened')
            raise
