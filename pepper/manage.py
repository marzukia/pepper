import argparse
import shutil
from livereload import Server, shell
import os

from pepper.builder.functions import build_site, compile_default_sass, create_new_site

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
        create_new_site(arg)
        build_path = os.path.join(arg, "build")
        if os.path.isdir(build_path):
            shutil.rmtree(build_path)
        build_site(arg)

    if command == "server":
        server = Server()
        server.watch(f"{arg}/*.toml", shell(f"python -m pepper.manage build {arg}"))
        server.watch(f"{arg}/content/", shell(f"python -m pepper.manage build {arg}"))
        server.watch(f"{arg}/static/", shell(f"python -m pepper.manage build {arg}"))
        server.watch(f"{arg}/templates/", shell(f"python -m pepper.manage build {arg}"))
        server.serve(root=f"{arg}/build")

    if command == "dev-server":
        server = Server()
        current_dir = os.path.abspath(os.path.dirname(__file__))

        def copy_html():
            shutil.copytree(
                os.path.join("pepper", "builder", "default", "layout"),
                os.path.join(arg, "templates", "default", "layout"),
                dirs_exist_ok=True,
            )

        def compile_and_copy_css():
            compile_default_sass()
            shutil.copytree(
                os.path.join("pepper", "builder", "default", "static", "css"),
                os.path.join(arg, "build", "css"),
                dirs_exist_ok=True,
            )

        server.watch("pepper/builder/default/static/scss/*.scss", compile_and_copy_css)
        server.watch("pepper/builder/default/layout/*.html", copy_html)
        server.watch(f"{arg}/*.toml", shell(f"python -m pepper.manage build {arg}"))
        server.watch(f"{arg}/content/", shell(f"python -m pepper.manage build {arg}"))
        server.serve(root=f"{arg}/build")
