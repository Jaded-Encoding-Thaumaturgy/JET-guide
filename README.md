A template with a bunch of plugins and theming pre enabled.<br>
Also includes a workflow that will automatically build and publish the site when anything gets pushed to the master/main branch.<br>
You should obviously make sure that you have github pages on your repo set up.

## How to run

`pip install mkdocs-material mkdocstrings[python] pymdown-extensions`<br>
`mkdocs serve` to host it locally with hot-reload

## How to configure

Please check out these links.<br>

https://squidfunk.github.io/mkdocs-material/setup/ <br>
https://www.mkdocs.org/getting-started/#adding-pages

If you want to host this on a custom domain make sure to create a `CNAME` file in the ./docs directory and put your domain in there.<br>
Like it was done [here](https://github.com/Vodes/muxtools-doc/blob/master/docs/CNAME).