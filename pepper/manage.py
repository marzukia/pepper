import argparse
import threading
import os

from pepper.builder.functions import build_site, create_new_site
from pepper.server.watcher import run_watcher
from pepper.server.runner import app


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

if command == "build":
    build_site(arg)

if command == "server":
    watcher_thread = threading.Thread(target=run_watcher)
    watcher_thread.start()
    os.environ["app_name"] = arg
    app.run(debug=True)
    watcher_thread.join()
