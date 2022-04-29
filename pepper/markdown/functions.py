from pepper.markdown.classes import MarkdownDirectory, MarkdownFile
from typing import List, Dict, Union
import os


def map_directory_markdown_files(
    directory_path: str,
) -> List[Union[MarkdownFile, Dict[MarkdownDirectory, MarkdownFile]]]:
    files = os.listdir(directory_path)
    tree = []
    for filepath in files:
        path = os.path.join(directory_path, filepath)
        if os.path.isdir(path):
            filepath = MarkdownDirectory(path)
            tree.append({filepath: map_directory_markdown_files(path)})
        else:
            if filepath != "_index.md" and ".md" in filepath:
                file = MarkdownFile(path)
                tree.append(file)
    return tree
