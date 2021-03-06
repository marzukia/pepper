import shutil

from jinja2 import Environment, FileSystemLoader
import toml
from pepper.markdown.classes import (
    BuildContext,
    MarkdownDirectory,
    MarkdownFile,
    TreeItem,
)
from pepper.markdown.functions import map_directory_markdown_files

from inspect import getsourcefile
import os
import sass

from typing import Any, List, NewType, Union, Dict


ContentMap = NewType(
    "ContentMap", List[Union[Dict[MarkdownDirectory, MarkdownFile], MarkdownFile]]
)
TreeMap = NewType("TreeMap", List[Union[TreeItem, List[TreeItem]]])


def load_config(target_site: str):
    config_path = os.path.join(target_site, "config.toml")
    with open(config_path, "r") as config_file:
        config = toml.loads(config_file.read())
        config["app_name"] = target_site
    return config


def build_content(
    content: ContentMap,
    context: Dict[str, Any],
) -> None:
    app_name = context.config.get("app_name")
    template_dir = os.path.join(app_name, "templates", "default")
    env = Environment(loader=FileSystemLoader(template_dir))

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
                    filepath = filepath.replace("_index.html", "index.html")
                    with open(filepath, "w") as target:
                        template = env.get_template("index.html")
                        target.write(template.render(**context.as_dict()))


def build_page(
    file: MarkdownFile,
    parent: MarkdownDirectory = None,
    tree: TreeMap = None,
    config: Any = None,
) -> None:
    context = BuildContext(file=file, parent=parent, tree=tree, config=config)
    build_content(content=file, context=context)


def build_nested_directory(
    folder: dict, tree: TreeMap = None, config: Any = None
) -> None:
    for directory, children in folder.items():
        for child in children:
            if type(child) == dict:
                build_nested_directory(folder=child, tree=tree, config=config)
            else:
                build_page(file=child, parent=directory, tree=tree, config=config)


def build_tree(content: ContentMap):
    tree = []
    for item in content:
        if type(item) == dict:
            directory = list(item.keys()).pop()
            tree_item = TreeItem(
                filepath=directory.filename, title=directory.meta.title
            )
            tree.append(tree_item)
            for value in item.values():
                nested_tree = build_tree(value)
                tree.append(nested_tree)
        else:
            if "_index" not in item.filename:
                tree_item = TreeItem(filepath=item.filename, title=item.meta.title)
                tree.append(tree_item)
    return tree


def build_site(target_site: str) -> None:
    build_path = os.path.join(target_site, "build")
    if os.path.isdir(build_path):
        shutil.rmtree(build_path)

    content_path = os.path.join(target_site, "content")
    content = map_directory_markdown_files(content_path)
    tree = build_tree(content)

    config = load_config(target_site)

    for item in content:
        if type(item) == dict:
            build_nested_directory(folder=item, tree=tree, config=config)
        else:
            build_page(file=item, tree=tree, config=config)

    static_srcs = [
        os.path.join(target_site, "templates", "default", "static"),
        os.path.join(target_site, "static"),
    ]
    static_dst = os.path.join(target_site, "build")

    for static_src in static_srcs:
        shutil.copytree(static_src, static_dst, dirs_exist_ok=True)


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
    shutil.copytree(
        default_dir, os.path.join(site_dir, "templates", "default"), dirs_exist_ok=True
    )


def compile_default_sass():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    default_theme_path = os.path.join(current_dir, "default")
    sass_path = os.path.join(default_theme_path, "static", "scss")
    sass_files = os.listdir(sass_path)
    css_path = os.path.join(default_theme_path, "static", "css", "styles.css")

    sass_string = ""
    for sass_file in sass_files:
        sass_file_path = os.path.join(sass_path, sass_file)
        with open(sass_file_path, "r") as sass_file:
            data = sass_file.read()
            sass_string += "\n" + data + "\n"

    compiled_sass = sass.compile(string=sass_string)

    with open(css_path, "w") as css_file:
        css_file.write(compiled_sass)
