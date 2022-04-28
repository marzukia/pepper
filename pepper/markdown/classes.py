import re

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

    def __init__(self, filepath):
        self.filepath = filepath
        self.meta, self.html = self.parse_file()

    def load_meta(self, md_str):
        meta = meta_rx.search(md_str)

        if meta:
            meta = meta.group(1)
            meta = meta.replace("\n", ",")

            key_matches = key_rx.findall(meta)

            for match in filter(lambda x: len(x) > 0, key_matches):
                target = f"{match}:"
                replacement = f'"{match}":'
                meta = meta.replace(target, replacement)

            enclosed = "{" + meta + "}"

            return MarkdownFileMeta(**eval(enclosed))

    def parse_file(self):
        with open(self.filepath, "r") as md_file:
            md_str = md_file.read()
            meta = self.load_meta(md_str)
            body_str = meta_rx.sub("", md_str)
            converted = mistune.html(body_str)
        return (meta, converted)
