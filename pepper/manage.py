import argparse

from pepper.builder.functions import create_new_site


parser = argparse.ArgumentParser(
    description="Pepper static site generator command line utility tool",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

command_parser = parser.add_argument(
    "command", help="[build, server, new]", nargs=2, default="."
)

parser.add_argument("-f", "--filepath", help="[build] Source for Pepper project")
parser.add_argument("-o", "--output", help="[build] Ouput for Pepper build")

args = parser.parse_args()
command = args.command
command, arg = command

if command == "new":
    create_new_site(arg)
