# Setup and First Steps

This page explains how to install VapourSynth and the JET packages,
as well as how to properly set up your code editor and previewer.
If you know what you're doing, you can skip or modify any of the steps listed here,
but if you run into issues this should be a fairly foolproof way to get things working again.

As of VapourSynth R74, everything is installed through `pip` (or `uv`),
including VapourSynth itself and most plugins.
No separate installers or plugin managers are needed anymore.

## Getting a Clean Slate

If you never used VapourSynth before R74, or you're on Linux, you can probably skip this step.

If you previously installed VapourSynth using the Windows installer (R73 or earlier),
uninstall it before proceeding.
As of R74, plugins are stored inside the VapourSynth Python package,
and **no plugins will be loaded from the previous locations**,
so leftovers from an old installation will only cause confusion.
Also delete any leftover directories like

- `%APPDATA%/VapourSynth`
- `%LOCALAPPDATA%/Programs/VapourSynth`

on Windows.

## Installing Python

VapourSynth requires Python 3.12 or later.
As of R74, a single VapourSynth wheel works on all supported Python versions,
so you can simply install the latest stable Python release.

=== "Windows"
    Install Python from the [Python website](https://www.python.org/downloads/).

    !!! warning
        Make sure to install Python to PATH!
        This is not strictly necessary,
        but will make your life a lot easier.
        During installation, this will be
        the "Add Python to environment variables" option.

=== "Linux"
    Install Python 3.12 or later using your package manager.
    It's recommended to create a virtual environment to install VapourSynth
    and the JET packages into, since most distributions do not allow
    installing packages with `pip` system-wide:

    ```sh
    python -m venv ~/.venvs/vapoursynth
    source ~/.venvs/vapoursynth/bin/activate
    ```

    You'll need to activate this virtual environment (the second command)
    in every new terminal session in which you want to use VapourSynth.

## Installing VapourSynth

As of R74, VapourSynth is installed with pip on all platforms.
Open a terminal and run:

```
pip install vapoursynth
vapoursynth config
```

The second command downloads and sets up the VapourSynth core library.
On Windows, update the Visual Studio Redistributable if the command tells you to.

Optionally, you can also run:

- `vapoursynth register-install` to set the `VSSCRIPT_PATH` environment variable,
  which allows other applications (e.g. media players and encoding GUIs) to find VapourSynth.
- (Windows only) `vapoursynth register-legacy-install` to write installation information
  to the registry, so that applications not yet aware of the R74+ install method still work.

To verify that everything works, open a Python prompt (run `python`) and type:

```py
from vapoursynth import core
print(str(core))
```

You should see the VapourSynth version printed, e.g. `VapourSynth Video Processing Library ... Core R77`.

## Installing the JET Packages

The JET Python packages build on top of the existing plugin ecosystem to provide

- More convenient and Pythonic wrapper functions around various plugins
- More complex filtering functions which combine functions of various plugins
  to achieve various filtering goals

As of vs-jetpack v2, the VapourSynth plugins that these functions rely on
are themselves distributed as Python packages
and can be installed automatically alongside `vsjetpack` using *extras*.
The simplest option is the `full` extra, which pulls in all CPU-based plugins:

=== "Windows"
    ```
    pip install vsjetpack[full]
    ```

    If you have an NVIDIA GPU, you can additionally install the GPU-accelerated plugins:

    ```
    pip install vsjetpack[full,nvidia] `
        --extra-index-url https://pypi.nvidia.com/ `
        --extra-index-url https://jaded-encoding-thaumaturgy.github.io/vs-wheels/simple
    ```

=== "Linux / macOS"
    Some plugins distribute their wheels through VSWheels of PyPI,
    so you need to add it with `--extra-index-url`:

    ```sh
    pip install vsjetpack[full] \
        --extra-index-url https://jaded-encoding-thaumaturgy.github.io/vs-wheels/simple
    ```

    If you have an NVIDIA GPU, you can additionally install the GPU-accelerated plugins:

    ```sh
    pip install vsjetpack[full,nvidia] \
        --extra-index-url https://pypi.nvidia.com/ \
        --extra-index-url https://jaded-encoding-thaumaturgy.github.io/vs-wheels/simple
    ```

If you don't want all plugins, there are more granular extras
like `source`, `denoise` or `deinterlace`,
as well as `amd`, `cl` and `vulkan` extras for non-NVIDIA GPUs.
See the [vs-jetpack documentation](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/#installation)
for the full breakdown and the platforms each extra supports.

To update your JET packages later, run the same command with `--upgrade` added.

??? info "Using uv instead of pip"
    If you manage your projects with [uv](https://docs.astral.sh/uv/),
    you can add `vsjetpack` to your `pyproject.toml` instead:

    ```sh
    uv add vsjetpack[full,nvidia] \
        --index https://jaded-encoding-thaumaturgy.github.io/vs-wheels/simple \
        --index https://pypi.nvidia.com/ \
        --index-strategy unsafe-best-match
    ```

    You may want to add the following setting to your `pyproject.toml` for later use:

    ```toml
    [tool.uv]
    index-strategy = "unsafe-best-match"
    ```

    If you don't want to use `unsafe-best-match` as the index strategy,
    you'll have to explicitly pin packages to indices via `tool.uv.sources`,
    like [vs-jetpack's own pyproject.toml](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jetpack/blob/main/pyproject.toml) does.
    See [this discussion](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jetpack/discussions/336)
    for details.

## Installing Additional VapourSynth Plugins

The `vsjetpack` extras cover everything the JET packages themselves need,
but you may occasionally want a plugin that isn't included.
If you ever run a VapourSynth script and get an error message like

`No attribute with the name foo exists. Did you mistype a plugin namespace or forget to install a plugin?`,

this means that you need to install the mentioned plugin.

Many plugins are now published on PyPI (or [VSWheels](https://github.com/Jaded-Encoding-Thaumaturgy/vs-wheels))
and can be installed with pip, e.g. `pip install vapoursynth-bestsource`.

For plugins without a Python package, you can still use VSRepo,
which is now installed separately: `pip install vsrepo`, then `vsrepo install <plugin>`.

If you need to use a manually downloaded native plugin, keep its native file in a
location of your choice and load it explicitly with `core.std.LoadPlugin()`.
Alternatively, you can also set the `VAPOURSYNTH_EXTRA_PLUGIN_PATH` environment variable
to an additional plugin directory.

## Installing VSView

[VSView](https://jaded-encoding-thaumaturgy.github.io/vs-view/) is the JET previewer for VapourSynth:
it lets you open scripts, videos or images in one interface,
making it easy to preview, inspect and compare sources.
It is the modern replacement for the older vs-preview.

Install it together with the recommended plugins:

```
pip install vsview[recommended]
```

You can also use `vsview[full]` to install all plugins,
or plain `vsview` for a minimal installation.

To launch it, just run `vsview`,
or open files directly:

```
vsview myscript.vpy video.mkv
```

## Installing your Code Editor

You're now ready to use the JET packages with VapourSynth.
However, it's strongly recommended to also install a code editor or IDE,
in order to benefit from a Python language server to see available plugins, functions, documentation, etc.
The simplest choice is VS Code:

- Install VS Code from [its download page](https://code.visualstudio.com/download)
- Install the Python extension from the Extensions panel
- If you installed VapourSynth into a virtual environment,
  select it as your Python interpreter
  (Ctrl+Shift+P, "Python: Select Interpreter")
- Associate `.vpy` files with Python by adding the following to your `settings.json`:

  ```json
  "files.associations": {
      "*.vpy": "python"
  }
  ```

You can then open your scripts in VSView from VS Code's integrated terminal
by running `vsview yourscript.vpy`.

## Opening your First File

With everything set up, it's time to open your first video in VapourSynth.
Start by finding your favorite video file, and copy its path (e.g. `C:/Path/to/my/file.mkv`).
Then, make a file called `myscript.vpy`, and open it (for example in VS Code).
Write the following into it:

```py
import vapoursynth as vs
core = vs.core

clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")

clip.set_output(0)
```

Where, obviously, you should replace the path with the path to your own video file.

!!! note "Note"
    This example uses the `lsmas.LWLibavSource` source filter because of its faster indexing.
    For any kind of more serious work, `bs.VideoSource` is recommended,
    since only that filter can fully guarantee accurate seeking.

Then, open this file in VSView by opening a terminal in your script's directory and running:

```
vsview myscript.vpy
```

You should see VSView open and display your video.

## A few further First Steps

With this, you've learned how to install everything you need.
The following will explain a few basic first steps if this is your first time using VapourSynth or VSView.

### Getting Comfortable with VSView

If you've followed the instructions above, you should now have VSView opened and should be able to preview your video file.
Here are a few things you can try out:

-   Press Space to play or pause
-   Click around in the timeline bar below the video display to step around the video
-   Ctrl+Scroll to zoom and Click+Drag to pan around the displayed image
-   Look at the sidebar on the left: each open workspace (script, video, or image) is represented by an icon.
    Right-click an icon to access workspace-specific actions such as reloading the script.
-   Explore the tool docks and panels via the "View" menu,
    which provide features like frame props inspection and comparisons.
-   Move your mouse to the very right of the window and drag the bar there to the left.
    This opens the plugins panel, which contains one tab for each VSView plugin.

For a full tour of the interface, see the
[VSView usage documentation](https://jaded-encoding-thaumaturgy.github.io/vs-view/usage/overview/).

### A Second Output Node

Now, let's do some actual filtering.
Add two lines to the bottom of your VapourSynth script, so that it looks as follows:

```py
import vapoursynth as vs
core = vs.core

clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")

clip.set_output(0)

blurred = core.std.BoxBlur(clip)

blurred.set_output(1)
```

Then press Ctrl+R to reload VSView.

You should now see two output nodes you can switch between.
The first is your video, the second is a slightly blurred version of your video.
You can also press the 1 and 2 keys to switch between them (which is the recommended method since it's much faster).

### Going JET

The above example code only used standard VapourSynth functions; except for VSView we didn't use any JET packages.
But even in such a simple script, JET packages can save you a bit of work.
Let's see how this script could be modified:

```py
from vstools import core
from vsview import set_output

clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")
blurred = core.std.BoxBlur(clip)

set_output(clip)
set_output(blurred)
```

Let's go over the differences:

1. The top lines are different.
   While standard VapourSynth scripts start with the incantations `import vapoursynth as vs` and `core = vs.core`,
   the JET way is `from vstools import core` and `from vsview import set_output` (possibly followed by further imports).
   This is not a big difference, but it does cut down the boilerplate.
2. We no longer need to give numbers to `set_output`.
   When using `clip.set_output`, you need to give `set_output` a number to specify what output node the given clip should be.
   When you want to add another node at the start, you'd need to update the numbers of all following output nodes, which can be annoying.
   The `set_output` function in VSView automatically numbers nodes based on the order they're output in.
3. Nodes are automatically named.
   If you open the above script in VSView, you'll see that the output nodes are now named `clip` and `blurred`
   instead of `Video Node 1` and `Video Node 2`, matching how the clips were called in our script.

We can also name nodes manually by passing another argument to `set_output`:

```py
set_output(clip, "Source")
set_output(blurred, "Blurred")
```

If you wanted to, you could also replace the `BoxBlur` call with a JET wrapper:

```py
from vstools import core
from vsrgtools import box_blur
from vsview import set_output

clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")
blurred = box_blur(clip)

set_output(clip, "Source")
set_output(blurred, "Blurred")
```

Whether you want to do this or not is a matter of taste.
The advantage of writing `core.std.BoxBlur` explicitly is that
you see exactly what plugin is called and don't need to worry about understanding the Python wrapper.
On the other hand, a wrapper like `box_blur` may have more features
(e.g. here `box_blur` allows specifying a different radius for every plane, which `core.std.BoxBlur` doesn't allow out-of-the-box)
and be easier to use.

### Using a Better Source Filter

Finally, I need to talk about the line

```py
clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")
```

This is the line that loads your video using the `lsmas` plugin.
The `LWLibavSource` video source is very reliable for most videos you'll encounter,
but it's not infallible.
When jumping around the video, it's possible for such source filters to sometimes return the wrong frame,
which can render your encodes unusable.
To avoid this, the source filter BestSource is recommended.
In exchange for needing a long time to process when opening a video for the first time,
this filter ensures perfect seeking accuracy in audio and video.
You can call it using

```py
clip = core.bs.VideoSource("C:/Path/to/my/file.mkv", showprogress=True)
```

Don't be surprised if VSView takes a long time to open now.
This is necessary in order for BestSource to be accurate.
The second time you open the same video, it will be much faster.

LWLibavSource is still fine when you want to quickly look through some video,
but as soon as you want to do any kind of actual encoding,
it's recommended to use BestSource.
