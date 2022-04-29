from pepper.markdown.classes import MarkdownDirectory, MarkdownFile
from pepper.markdown.functions import map_directory_markdown_files

import os
from typing import List, Union, Dict


def build_content(
    content: List[Union[Dict[MarkdownDirectory, MarkdownFile], MarkdownFile]]
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
                        target.write(content.html)


def build_site(target_site: str):
    content = map_directory_markdown_files(f"{target_site}/content")
    for c in content:
        build_content(c)
