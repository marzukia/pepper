import shutil

from jinja2 import Environment, FileSystemLoader
from pepper.markdown.classes import MarkdownDirectory, MarkdownFile
from pepper.markdown.functions import map_directory_markdown_files

from inspect import getsourcefile
import os

from typing import Any, List, Union, Dict

cwd = os.getcwd()
app_name = os.environ["app_name"]
template_dir = os.path.join(cwd, app_name, "templates", "default")
env = Environment(loader=FileSystemLoader(template_dir))


def build_content(
    content: List[Union[Dict[MarkdownDirectory, MarkdownFile], MarkdownFile]],
    context: Dict[str, Any],
) -> None:
    if type(content) != MarkdownFile:
        key = list(content.keys()).pop()
        content = content[key]
        for c in content:
            build_content(c)
    else:
        src_path = content.filepath
        build_path = src_path.replace("content", "build")
        paths = build_path.split("/")

        checked = []
        for path in paths:
            checked.append(path)
            filepath = os.path.join(*checked)

            if not os.path.exists(filepath):
                if ".md" not in filepath:
                    os.mkdir(filepath)
                else:
                    filepath = filepath.replace(".md", ".html")
                    with open(filepath, "w") as target:
                        template = env.get_template("index.html")
                        target.write(template.render(**context))


def build_site(target_site: str) -> None:
    print("Content change, rebuilding site...")
    content = map_directory_markdown_files(f"{target_site}/content")
    for c in content:
        context = {"content": c.html, "meta": c.meta, "tree": content}
        build_content(c, context)


def create_new_site(site_dir: str) -> None:
    directories = ["content", "static"]

    if not os.path.exists(site_dir):
        os.makedirs(site_dir)

    for directory in directories:
        target_path = os.path.join(site_dir, directory)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    source_path = os.path.abspath(getsourcefile(lambda: 0))
    default_dir = os.path.join(os.path.dirname(source_path), "default")
    shutil.copytree(default_dir, os.path.join(site_dir, "templates", "default"))
