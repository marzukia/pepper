from pepper.markdown.classes import MarkdownFile

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("example"))

template = env.get_template("base.html")

file = MarkdownFile("example/content/article.md")

print(template.render(file=file))
