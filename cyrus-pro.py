import os
import sys
import socket
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import ANSI

# اگر خروجی به ترمینال واقعی نرود، رنگ‌ها خاموش می‌شوند
USE_COLOR = sys.stdout.isatty()

RESET = "\033[0m"
CYAN = "\033[38;5;45m"
GOLD = "\033[38;5;220m"


def c(code, text):
    if USE_COLOR:
        return code + text + RESET
    return text


class SystemCompleter(Completer):

    def __init__(self):
        super().__init__()
        self.commands = set()

        for directory in os.environ.get("PATH", "").split(os.pathsep):
            if not os.path.isdir(directory):
                continue
            try:
                for name in os.listdir(directory):
                    path = os.path.join(directory, name)
                    if os.path.isfile(path) and os.access(path, os.X_OK):
                        self.commands.add(name)
            except (PermissionError, OSError):
                pass

        self.commands = sorted(self.commands)

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for command in self.commands:
            if command.startswith(word):
                yield Completion(command, start_position=-len(word))
class CommandLexer(Lexer):
    def lex_document(self, document):
        def get_line(lineno):
            line = document.lines[lineno]

            if not line.strip():
                return line

            parts = line.split()
            if not parts:
                return line

            command = parts[0]

            # دستورات رایج لینوکس
            commands = {
                "ls", "cd", "pwd", "mkdir", "rmdir",
                "cp", "mv", "rm", "touch", "cat",
                "less", "more", "head", "tail",
                "grep", "find", "locate",
                "sudo", "apt", "apt-get",
                "python", "python3", "pip", "pip3",
                "nano", "vim", "nvim",
                "clear", "echo", "printf",
                "whoami", "id", "uname",
                "chmod", "chown",
                "ps", "kill", "top", "htop",
                "ip", "ping", "curl", "wget",
                "ssh", "scp",
                "tar", "zip", "unzip",
                "git", "systemctl",
                "ifconfig", "netstat", "ss"
            }

            if command in commands:
                start = line.find(command)

                return [
                    ("class:command", line[:start]),
                    ("class:command", command),
                    ("", line[start + len(command):])
                ]

            return line

        return get_line

class KouroshTerminal:

    def __init__(self):
        self.running = True

        style = Style.from_dict({
            "user": "bold #00FF00",
            "host": "bold #FF0000",
            "path": "bold #00AFFF",
            "arrow": "bold #00FF00",
            "command": "bold #00AFFF",
        })

        self.session = PromptSession(
            completer=SystemCompleter(),
            complete_while_typing=True,
            style=style,
            lexer=CommandLexer()
        )

        # نام کاربر و hostname واقعی، مثل ترمینال کالی
        self.user = os.environ.get("USER") or os.environ.get("LOGNAME") or "kali"
        self.host = socket.gethostname() or "kali"

    def _banner_text(self):
        if USE_COLOR:
            return (
                CYAN + "╔══════════════════════════════════════════════╗\n" +
                CYAN + "║" + GOLD + "           KOUROUSH-E BOZORG" + CYAN + "             ║\n" +
                CYAN + "║" + GOLD + "                کوروش بزرگ" + CYAN + "                 ║\n" +
                CYAN + "╠══════════════════════════════════════════════╣\n" +
                CYAN + "║" + "           PERSIAN TERMINAL" + "               ║\n" +
                CYAN + "║" + "       Ancient Iran • Modern Terminal" + "       ║\n" +
                CYAN + "╚══════════════════════════════════════════════╝" + RESET
            )
        return (
            "╔══════════════════════════════════════════════╗\n"
            "║           KOUROUSH-E BOZORG             ║\n"
            "║                کوروش بزرگ                 ║\n"
            "╠══════════════════════════════════════════════╣\n"
            "║           PERSIAN TERMINAL               ║\n"
            "║       Ancient Iran • Modern Terminal       ║\n"
            "╚══════════════════════════════════════════════╝"
        )

    def banner(self):
        text = self._banner_text()
        if USE_COLOR:
            print_formatted_text(ANSI(text))
        else:
            print(text)
        print()

    def _short_path(self):
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        if cwd == home:
            return "~"
        if cwd.startswith(home + os.sep):
            return "~" + cwd[len(home):]
        return cwd

    def run(self):
        self.banner()

        while self.running:
            try:
                short = self._short_path()

                prompt = [
                    ("class:user", "┌──(" + self.user),
                    ("class:host", "㉿" + self.host),
                    ("", ")-["),
                    ("class:path", short),
                    ("", "]\n"),
                    ("class:arrow", "└─$ "),
                ]

                command = self.session.prompt(prompt).strip()

                if not command:
                    continue

                lower = command.lower()

                if lower in ("exit", "quit", "خروج"):
                    self.running = False
                    continue

                if lower in ("clear", "پاک"):
                    os.system("clear" if os.name == "posix" else "cls")
                    continue

                result = os.system(command)

                if result != 0:
                    print(c("\033[31m", f"خطا - Code: {result}"))

            except KeyboardInterrupt:
                print(c(GOLD, "^C"))

            except EOFError:
                print()
                break

            except Exception as error:
                print(c("\033[31m", f"خطا: {error}"))


def main():
    KouroshTerminal().run()


if __name__ == "__main__":
    main()
