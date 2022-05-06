from typing import Any, Tuple, List, Union
import re
import yaml
import mistune

meta_rx = re.compile(r"(?:[-]{3,}\n)((?:.|\n)*)(?:[-]{3,}\n)")
key_rx = re.compile(r"[a-zA-Z0-9_-]*(?=:)")


class MarkdownFileMeta:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MarkdownFile:
    meta: MarkdownFileMeta
    html: str
    filepath: str
    filename: str

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = "/".join(filepath.split("/")[2:]).replace(".md", ".html")
        self.filename = "/" + self.filename
        self.meta, self.html = self.parse_file()

    def load_meta(self, md_str: str) -> MarkdownFileMeta:
        meta = meta_rx.search(md_str)

        if meta:
            meta = meta.group(1)
            meta = yaml.load(meta, Loader=yaml.FullLoader)

            return MarkdownFileMeta(**meta)

    def parse_file(self) -> Tuple[MarkdownFileMeta, str]:
        with open(self.filepath, "r") as md_file:
            md_str = md_file.read()
            meta = self.load_meta(md_str)
            body_str = meta_rx.sub("", md_str)
            converted = mistune.html(body_str)

        return (meta, converted)


class MarkdownDirectory(MarkdownFile):
    def parse_file(self) -> Tuple[MarkdownFileMeta, str]:
        self.filepath += "/_index.md"
        return super().parse_file()


class TreeItem:
    def __init__(self, filepath: str, title: str):
        self.filepath = filepath
        self.title = title


class BuildContext:
    html: str
    parent: MarkdownDirectory = None
    meta: MarkdownFileMeta
    tree: List[Union[TreeItem, List[TreeItem]]] = None
    config: Any = None

    def __init__(
        self,
        file: MarkdownFileMeta,
        parent: MarkdownDirectory,
        tree: List[Union[TreeItem, List[TreeItem]]],
        config: Any,
        **kwargs
    ):
        self.html = file.html
        self.meta = file.meta
        self.parent = parent
        self.tree = tree
        self.config = config

        for key, value in kwargs.items():
            setattr(self, key, value)

    def as_dict(self):
        return self.__dict__
