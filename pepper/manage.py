import argparse
from livereload import Server, shell
import os

from pepper.builder.functions import build_site, create_new_site

parser = argparse.ArgumentParser(
    description="Pepper static site generator command line utility tool",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

command_parser = parser.add_argument(
    "command", help="[build, server, new]", nargs=2, default="."
)

parser.add_argument("-f", "--filepath", help="[build] Source for Pepper project")
parser.add_argument("-o", "--output", help="[build] Ouput for Pepper build")


if __name__ == "__main__":
    args = parser.parse_args()
    command = args.command
    command, arg = command

    os.environ["app_name"] = arg

    if command == "new":
        create_new_site(arg)

    if command == "build":
        build_site(arg)

    if command == "server":
        server = Server()
        server.watch(f"{arg}/content/", shell(f"python -m pepper.manage build {arg}"))
        server.watch(f"{arg}/static/", shell(f"python -m pepper.manage build {arg}"))
        server.watch(f"{arg}/templates/", shell(f"python -m pepper.manage build {arg}"))
        server.serve(root=f"{arg}/build")
