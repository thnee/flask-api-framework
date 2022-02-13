from pallets_sphinx_themes import ProjectLink, get_version


project = "Flask-API-Framework"
copyright = "2022, Mattias Lindvall"
author = "Mattias Lindvall"
release, version = get_version("Flask-API-Framework")

extensions = [
    "pallets_sphinx_themes",
]

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("PyPI", "https://pypi.org/project/Flask-API-Framework/"),
        ProjectLink("Source", "https://github.com/thnee/flask-api-framework/"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
html_static_path = ["_static"]
html_logo = "logo.png"
html_title = f"Flask-API-Framework Documentation ({version})"
html_show_sourcelink = False
