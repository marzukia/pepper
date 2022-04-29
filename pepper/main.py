import os
import sys

from jinja2 import Environment, PackageLoader
from pepper.builder.functions import build_site

from pepper.markdown.functions import map_directory_markdown_files

target_site = "example"

directory = os.getcwd()
sys.path.insert(0, directory)

env = Environment(loader=PackageLoader(target_site))

template = env.get_template("base.html")
content = map_directory_markdown_files(f"{target_site}/content")

build_site(target_site)
