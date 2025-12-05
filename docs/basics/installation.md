# Setup and First Steps

This page explains how to install VapourSynth and the JET packages,
as well as how to properly set up your code editor and previewer.
If you know what you're doing, you can skip or modify any of the steps listed here,
but if you run into issues this should be a fairly foolproof way to get things working again.

<!-- If you're using Linux, it's very strongly recommended to use Arch Linux or a derivative, -->
<!-- as that is the only distribution that provides sufficiently many of the required programs -->
<!-- and plugins as packages or via the AUR. -->
<!-- On other distributions you risk a great amount of pain compiling a ton of programs and plugins manually. -->
<!-- The rest of this page will assume that Linux users use Arch Linux. -->

## Getting a Clean Slate

If you're on Linux, you can probably skip this step.

If you have VapourSynth or any version of Python installed, uninstall them.
Also delete any leftover directories like

- `%APPDATA%/VapourSynth`
- `%APPDATA%/Python`
- `%LOCALAPPDATA%/Programs/VapourSynth`
- `%LOCALAPPDATA%/Programs/Python`

on Windows.

## Installing Python and VapourSynth

=== "Windows"
    Check the [VapourSynth documentation](http://www.vapoursynth.com/doc/installation.html)
    to find out the latest Python version currently supported by VapourSynth,
    and install it from the [Python website](https://www.python.org/downloads/).
    At the time of writing, that's Python 3.12.

    !!! warning
        Make sure to install Python to PATH!
        This is not strictly necessary,
        but will make your life a lot easier.
        During installation, this will be
        the "Add Python to environment variables" option.

    Then, download the latest [GitHub release](https://github.com/vapoursynth/vapoursynth/releases)
    of VapourSynth and install it.

    Unless you want to risk running into issues, install the installer versions (not the portable ones)
    and select "Install for this user only" when asked.

=== "Linux"
    !!! warning "This section is incomplete!"

        This section is a stub.
        You can help us
        by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-guide?tab=readme-ov-file#contributing).

    Install Python and VapourSynth using your package manager.
    Also install `vsgenstubs`. <!-- (`vapoursynth-tools-genstubs-git` on the AUR) -->

## Installing VapourSynth Plugins

VapourSynth itself only provides a frame server,
i.e. the ability to load plugins and use them to process audio and video.
The meat of the VapourSynth ecosystem lies in these plugins,
which need to be installed separately.

If you ever want to run a VapourSynth script or call some function and get an error message like

`No attribute with the name bs exists. Did you mistype a plugin namespace or forget to install a plugin?`,

this means that you need to install the mentioned plugin, in this case `bs` (which is short for bestsource).

=== "Windows"
    On Windows, plugins are installed using VSRepo.
    Open a terminal and run `vsrepo.py available` to list all installable plugins.
    To install a plugin (e.g. `bs`), run `vsrepo.py install bs`.
    You can install multiple plugins at once to save time, e.g. `vsrepo.py install bs lsmas`.

    !!! bug "Note"
        VSRepo can be finnicky depending on your configuration and file associations.
        (TODO figure out some foolproof method to call it or fix it upstream)
        If you run into issues running vsrepo, try using a different terminal (cmd or PowerShell)
        or calling it as `vsrepo` or `python -m vsrepo` rather than `vsrepo.py`.
        If all else fails, you can manually navigate to the folder VSRepo is in
        (usually `%localappdata%/Programs/VapourSynth/vsrepo`), open a terminal there,
        and run `python vsrepo.py` with your arguments.
        Alternatively, you can also try [VSRepoGUI](https://github.com/theChaosCoder/VSRepoGUI).

=== "Linux"
    !!! warning "This section is incomplete!"

        This section is a stub.
        You can help us
        by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-guide?tab=readme-ov-file#contributing).

    <!-- Install plugins using your package manager, e.g. `vapoursynth-plugin-bestssource` on Arch Linux. -->
    <!-- A few plugins are available in the official repositories, but for most of them you'll need to use the AUR. -->

    <!-- After you've installed a plugin, run `vsgenstubs4` to generate function stubs for the installed plugins, -->
    <!-- which will help your language server. -->

To start out, install the following plugins:

- `bs` and `lsmas`, to load audio and video
- `akarin`, `vszip` and `fmtc` which may be needed by vs-preview.

## Installing the JET Packages

The JET python packages build on top of the existing plugin ecosystem to provide

- More convenient and Pythonic wrapper functions around various plugins
- More complex filtering functions which combine functions of various plugins
  to achieve various filtering goals
- vs-preview, a previewer for VapourSynth with plugin support and many useful features for encoders.

To install it, open a terminal and run:

`pip install vsjetpack vspreview`

To update your JET packages, you can run `pip install --upgrade vsjetpack vspreview`.

??? info "Migrating from `vsjet`"

    If you previously used `vsjet` to install and update JET packages,
    you can use the following commands to migrate:
    ```
    pip uninstall stgpytools vstools vspyplugin vskernels vsexprtools vsrgtools vsmasktools vsaa vsscale vsdenoise vsdehalo vsdeband vsdeinterlace vssource vspreview vsjet -y
    pip install vsjetpack vspreview
    ```

Linux users may need to create a virtualenv to install the packages or try their luck with `pipx`.
<!-- On Arch Linux, you can use the [`vapoursynth-plugin-vsjetpack`](https://aur.archlinux.org/packages/vapoursynth-plugin-vsjetpack) and [`vapoursynth-preview`](https://aur.archlinux.org/packages/vapoursynth-preview) AUR packages. -->

## Installing your Code Editor

You're now ready to use JET packages with VapourSynth.
However, it's strongly recommended to also install a code editor or IDE,
in order to benefit from a Python language server to see available plugins, functions, documentation, etc.
The simplest choice is VS Code:

- Install VS Code from [its download page](https://code.visualstudio.com/download)
- Follow the [vs-preview documentation](https://github.com/Jaded-Encoding-Thaumaturgy/vs-preview/blob/master/docs/installation/install_vscode.rst)
  to configure VS Code to work with VapourSynth and vs-preview.

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

Then, open this file in vs-preview.
If you've correctly set up VS Code, you should be able to just press F5.
Otherwise, you can also open a terminal in your script's directory and run `vspreview myscript.vpy`.

You should see vs-preview open and display your video.

## A few further First Steps

With this, you've learned how to install everything you need.
The following will explain a few basic first steps if this is your first time using VapourSynth or vs-preview.

### Getting Comfortable with vs-preview

If you've followed the instructions above, you should now have vs-preview opened and should be able to preview your video file.
Here are a few things you can try out:

-   Press Space to play or pause
-   Click around in the timeline bar below the video display to step around the video
-   Ctrl+Scroll to zoom and Click+Drag to pan around the displayed image
-   Click the "Pipette" button at the bottom and look at the values at the bottom changing while you move your mouse around the image.
-   Click the "Benchmark" button at the bottom and click "Run" to find out how fast your VapourSynth script runs.
    At the moment, your script just loads a video, so it should be fairly fast,
    but in the future your scripts might contain more complex filtering, and knowing how fast or slow your filtering is will be more important.
-   Click the "Comp" button at the bottom and click "Start Upload".
    Once the upload is done, find the box containing a `slow.pics` link and press the button next to it to copy that link to your clipboard.
    Open that link in your browser: You'll get a `slow.pics` comparison of random frames in your video.
    If your script has multiple outputs, the comparison will show all output nodes.
-   Move your mouse to the very right of vs-preview's window and drag the bar there to the left.
    This opens the plugins panel, which contains one tab for each vs-preview plugin.
    First, open the "Frame Props" tab and have a look at the values there.

    Then, open the "Split Planes" tab.
    This shows the individual planes of your video.
    For your average video clip, this will consist of one luma plane and two chroma planes with half the width and height.
    You can press Ctrl+A to unlock the split planes view,
    which will allow you to freely zoom and pan around in the view like you would on the normal video.

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

Then press Ctrl+R to reload vs-preview.

!!! warning "Note"
    Reloading vs-preview in-place with Ctrl+R uses dark magic and can occasionally break with certain complex scripts.
    If you run into issues with reloading, the foolproof way is always to close and reopen vs-preview.

If you open the drop-down at the bottom left of vs-preview,
you should now see two output nodes you can switch between.
The first is your video, the second is a slightly blurred version of your video.
You can also press the 1 and 2 keys to switch between them (which is the recommended method since it's much faster).

### Going JET

The above example code only used standard VapourSynth functions; except for vs-preview we didn't use any JET packages.
But even in such a simple script, JET packages can save you a bit of work.
Let's see how this script could be modified:

```py
from vstools import core, set_output

clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")
blurred = core.std.BoxBlur(clip)

set_output(clip)
set_output(blurred)
```

Let's go over the differences:

1. The top lines are different.
   While standard VapourSynth scripts start with the incantations `import vapoursynth as vs` and `core = vs.core`,
   the JET way is `from vstools import core, set_output` (possibly followed by further imports).
   This is not a big difference, but it does cut down the boilerplate to one line.
2. We no longer need to give numbers to `set_output`.
   When using `clip.set_output`, you need to give `set_output` a number to specify what output node the given clip should be.
   When you want to add another node at the start, you'd need to update the numbers of all following output nodes, which can be annoying.
   The `set_output` function in vs-tools automatically numbers nodes based on the order they're output in.
3. Nodes are automatically named.
   If you open the above script in vs-preview, you'll see that the dropdown in the bottom left now contains the names `clip` and `blurred`
   instead of `Video Node 1` and `Video Node 2`, matching how the clips were called in our script.
   If you were to upload a comparison to slow.pics, the images in the comparison would also be labeled like this.

We can also name nodes manually by passing another argument to `set_output`:

```py
set_output(clip, "Source")
set_output(blurred, "Blurred")
```

If you wanted to, you could also replace the `BoxBlur` call with a JET wrapper:

```py
from vstools import core, set_output
from vsrgtools import box_blur

clip = core.lsmas.LWLibavSource("C:/Path/to/my/file.mkv")
blurred = box_blur(clip)

set_output(clip, "Source")
set_output(blurred, "Blurred")
```

Whether you want to do this or not is a matter of taste.
The advantage of writing `core.std.BoxBlur` explicitly is that
you see exactly what plugin is called and don't need to worry about understanding the Python wrapper.
On the other hand, a wrapper like `box_blur` may have more features
(e.g. here `box_blur` allows specifying a different radius for every plane, which `core.std.BoxBlur` doesn't allow out-of-the-box`)
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

Don't be surprised if vs-preview takes a long time to open now.
This is necessary in order for BestSource to be accurate.
The second time you open the same video, it will be much faster.

LWLibavSource is still fine when you want to quickly look through some video,
but as soon as you want to do any kind of actual encoding,
it's recommended to use BestSource.
