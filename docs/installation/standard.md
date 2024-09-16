# Standard setup

!!! warning "Stub"
    This page is a [stub][wikipedia-stubs].
    You can help by [expanding it][contributing]

!!! info "User experience"
    This guide is written with the assumption that the user
    has absolutely zero Vapoursynth or Python experience
    and is starting fresh.
    If you're already semi-experienced,
    you may want the [quickstart guide][quickstart] instead.

This page explains how to install both Vapoursynth and JET,
as well as how to set up your code editor and previewer.

We will be going over the following steps:

- Installing requirements
- Installing JET packages
- Setting up a code editor/IDE
- Installing Vapoursynth plugins

## Prerequisite knowledge

To follow this guide,
you should have a basic understanding of a couple of things:

### Terminal

If you're using Windows,
it's recommended to use Windows Terminal
with cmd or [git bash][git-bash] shell
as the default profile.

If you're a PowerShell user,
you may need to change a number of commands shown here
to make them work with PowerShell.

The terminal will be used a lot,
so it's recommended you get comfortable with it as soon as possible.
For a basic introduction,
see [this guide][terminal-guide].

### Code blocks

  In this guide, as well as on other pages,
  you may find blocks like this:

  ```python
  src = source("PATH")
  ```

  This is known as a "code block",
  and will contain pieces of code.
  You will find these a lot in our guides.

  If you see a code block like this with a `$` sign:

  ```bash
  $ vspipe --version
  ```

  This means you should run the command in your terminal (without the `$`).

  If you see a code block like these with a `>>>` sign:

  ```python
  >>> str(core)
  ```

  ```python
  >>> def some_function():
  ...     return ''
  ```

  This means you should run the code in your Python interpreter (without the `>>>` or `...`).

## Pre-installation

It's not uncommon to have to (re-)install Vapoursynth or Python at some point,
or to have to upgrade to a new version.
When doing this,
you may run into issues.

If you encounter issues,
it may be a good idea
to get a clean slate before continuing.

<details class="example">
    <summary>Removing existing installations</summary>
       <div class="tab-content">
           <div class="admonition question">
               <p class="admonition-title">Necessity</p>
               <p>It's unknown how necessary this step is.
               If you're a programmer,
               you might want to keep your existing Python installation,
               but if you're not and you want to start fresh,
               this step is recommended.</p>
           </div>

           <p>
             Prior to (re-)installing Vapoursynth,
             make sure to remove any existing installations.
           </p>

           <p>
            This means deleting the following directories:
           </p>

           <ul>
               <li><code>%APPDATA%/VapourSynth</code></li>
               <li><code>%APPDATA%/Python</code></li>
               <li><code>%LOCALAPPDATA%/Programs/VapourSynth</code></li>
               <li><code>%LOCALAPPDATA%/Programs/Python</code></li>
           </ul>
       </div>
</details>

## Installing dependencies

Installing Vapoursynth is pretty straightforward,
but does require a bit of setup.

### Installing Python

!!! note
    If you already have a working installation
    of the latest supported Python version,
    you can skip this step.

!!! example "Installing Python"
    === ":fontawesome-brands-windows: Windows"
        !!! danger "Windows Store"
            Avoid installing Python from the Windows Store.
            The store version can have compatibility issues
            with certain packages and tools.

        1. Check the [Vapoursynth documentation][vapoursynth-doc]
            to find out the latest Python version currently supported by Vapoursynth.
            At the time of writing, that's _Python 3.12_.

        2. Install that version or a newer version from the [Python website][python-download].<br>
            Make sure to select the option to "_Add Python to PATH_"!

        3. Once you've downloaded the installer,
        run it and click on "Install Now".<br>

    === ":fontawesome-brands-apple: MacOS"
        Install Python using Homebrew.

        ```bash
        $ brew install python
        ```

    === ":fontawesome-brands-linux: Linux"
        === "Debian"
            1. Ensure your package manager is up to date:
            ```bash
            $ sudo apt update && sudo apt upgrade
            ```

            2. Install Python:
            ```bash
            $ sudo apt install python3 python3-pip python3-virtualenv
            ```

        === "Arch"
            === "pacman"

                1. Ensure your package manager is up to date:
                ```bash
                sudo pacman -Syu
                ```

                2. Install Python:
                ```bash
                sudo pacman -S python python-pip python-virtualenv
                ```

            === "yay"
                1. Install Python:

                ```bash
                yay -S python python-pip python-virtualenv
                ```

After installation,
you can verify that everything is working by running the following commands in a terminal:

```bash
$ python --version
$ pip --version
```

### Installing Vapoursynth

Vapoursynth is the backbone of JET's processing functionality.
It's a frame server that allows you to load plugins
and use them to process audio and video.

!!! example "Installing Vapoursynth"
    === ":fontawesome-brands-windows: Windows"
        !!! warning "Installer versions"
            Unless you know what you're doing,
            you should avoid using the portable versions,
            as this can complicate things.

        1. Download the [GitHub release][vapoursynth-release]
        of Vapoursynth that is tagged as "Latest".

        2. Run the installer and select "Install for this user only" if asked.

    === ":fontawesome-brands-apple: MacOS"
        1. Install Vapoursynth using Homebrew.

        ```bash
        $ brew install vapoursynth
        ```

    === ":fontawesome-brands-linux: Linux"

        === "Debian"

            1. The Vapoursynth is available in the [deb-multimedia repository][deb-multimedia].
            Follow the instructions on their site to add the repository to your system.
            2. Update your package manager:
            ```bash
            sudo apt update
            ```

            3. Install Vapoursynth:
            ```bash
            sudo apt install vapoursynth
            ```

        === "Arch"
            === "pacman"

                1. Ensure your package manager is up to date:
                ```bash
                sudo pacman -Syu
                ```

                2. Install Vapoursynth:
                ```bash
                sudo pacman -S vapoursynth
                ```

            === "yay"
                1. Install Vapoursynth:

                ```bash
                yay -S vapoursynth
                ```

After installation,
you can verify that everything is working by running the following command in a terminal:

```bash
$ vspipe --version
```

```bash
$ python
>>> from vapoursynth import core
>>> str(core)
'VapourSynth Video Processing Library\nCopyright (c) 2012-2024 Fredrik Mellbin\n\tCore R70\n\tAPI R4.1\n\tAPI R3.6\n\tOptions: -\n\tNumber of Threads: 32\n\tMax Cache Size: 4096\n'
```

## Installing JET packages

The JET python packages build on top of the existing plugin ecosystem
to provide more convenient and complex functionality.
It adds, among other things:

- More convenient and Pythonic wrapper functions around various plugins.
- More complex filtering functions which combine functions of various plugins
  to achieve various filtering goals.
- `vs-preview`, a previewer for Vapoursynth with plugin support and many useful features for encoders.
- Many helper functions and classes for developing Vapoursynth packages.

### Installing the core package

!!! example "Installing JET packages"

    !!! info "Available packages"
        Not every JET package is included in the installer.
        These missing packages are often still in the basic development phase,
        or otherwise not ready for use.

        For a list of all packages that will be installed,
        see the [vs-jet requirements][vsjet-requirements].

    === ":fontawesome-brands-windows: Windows"
        1. Install JET using pip:

        ```bash
        $ pip install vsjet
        ```

    === ":fontawesome-brands-apple: MacOS"
        1. Install JET using pip:

        ```bash
        $ pip install vsjet
        ```

    === ":fontawesome-brands-linux: Linux"
        === "Debian"
            !!! warning "Stub"
                This page is a [stub][wikipedia-stubs].
                You can help by [expanding it][contributing]

        === "Arch"
            You can install the packages using the `vapoursynth-plugin-vsjet-meta-git` AUR package.

            === "pacman"

                1. Ensure your package manager is up to date:

                   ```bash
                   sudo pacman -Syu
                   ```

                2. Install the JET meta package:

                   ```bash
                   sudo pacman -S vapoursynth-plugin-vsjet-meta-git
                   ```

            === "yay"
                1. Install the JET meta package:

                ```bash
                yay -S vapoursynth-plugin-vsjet-meta-git
                ```

### Updating packages

!!! example "Updating JET packages"
    === ":octicons-tag-24: Stable"
        <details class="note">
            <summary>Developer support</summary>
            <div class="tab-content">
                <br>
                Due to how often JET packages are updated,
                only the nightly version receives developer support.
                If you run into any issues with the stable version,
                try updating to the nightly version
                to see if your issue has already been fixed.
             </div>
        </details>
        Stable versions are built from tagged releases
        of every JET package's git repository.

        They aim to be free of major issues,
        and are recommended for most users.

        === ":fontawesome-brands-windows: Windows"
            1. You can update the JET packages using the following command:

            ```bash
            $ vsjet
            ```

        === ":fontawesome-brands-apple: MacOS"
            1. You can update the JET packages using the following command:

            ```bash
            $ vsjet
            ```

        === ":fontawesome-brands-linux: Linux"
            === "Debian"
                !!! warning "Stub"
                    This page is a [stub][wikipedia-stubs].
                    You can help by [expanding it][contributing]

            === "Arch"
                !!! warning "Stub"
                    This page is a [stub][wikipedia-stubs].
                    You can help by [expanding it][contributing]

    === ":octicons-moon-24: Nightly"
        !!! danger "Nightly version"
            Nightly versions are not always stable.
            They may contain bugs or other issues that could cause problems.<br>
            If you run into issues,
            you can follow the "Stable" instructions again to roll back to a stable version.

        Nightly (or more often called "latest") versions are built from the latest commit
        on the main branch of every JET package's git repository.
        These will be bleeding-edge versions,
        and include the latest features
        as well as potentially breaking changes
        or bugs that have not been fixed yet.

        To install the latest versions of individual packages,
        you must install each separately.<br>
        Be extremely mindful of the web of dependencies if you're doing this.

        A list of all package repositories can be found [here][vsjet-python-repositories].

        === ":fontawesome-brands-windows: Windows"
            1. If you want to install the nightly version,
            you can use the following command:

            ```bash
            $ vsjet latest
            ```

        === ":fontawesome-brands-apple: MacOS"
            1. If you want to install the nightly version,
            you can use the following command:

            ```bash
            $ vsjet latest
            ```

        === ":fontawesome-brands-linux: Linux"
            === "Debian"
                !!! warning "Stub"
                    This page is a [stub]().
                    You can help by [expanding it][contributing]

            === "Arch"
                !!! warning "Stub"
                    This page is a [stub][wikipedia-stubs].
                    You can help by [expanding it][contributing].

## Code editor

In order to edit Vapoursynth scripts,
you will need an integrated development environment (IDE).
This will give you useful tools
like a code editor,
a built-in terminal,
syntax highlighting,
and more.

We will also go over how to set up a simple previewer for your scripts
using `vspreview`.

<details class="warning">
    <summary>Other previewers</summary>
    <p>
        JET only officially supports and recommends `vspreview` as the primary previewer.
    </p>

    <p>
        While alternative previewers like <i>vsedit</i> exist,
        they often lack the comprehensive feature set,
        active maintenance,
        and up-to-date compatibility
        that vspreview offers.
    </p>

    <p>
        For the best experience and full compatibility
        with JET's ecosystem,
        we strongly advise using vspreview for your
        Vapoursynth script previewing needs.
    </p>
</details>

### Installing an IDE

There are a couple of IDEs you can choose from.
We recommend using [VSCode][vscode].

<details class="info">
    <summary>Using other IDEs</summary>
      <p>
        While we recommend VSCode for its ease of use and extensive features,
        you're free to use any IDE of your preference.
        The key features to look for in an IDE for Vapoursynth scripting and development are:
      </p>

      <ol>
        <li>An integrated terminal</li>
        <li>The ability to set up custom hotkeys for external commands</li>
      </ol>

      <p>
        External command support is particularly important for convenience,
        as it enables you to quickly preview your scripts
        without opening up a terminal window each time.
      </p>

      <p>
        If your preferred IDE offers these capabilities,
        feel free to use it and skip the VSCode setup instructions in the following sections.
        Just ensure you configure your chosen IDE to work effectively with Vapoursynth scripts.
      </p>
</details>

!!! example "Installing VSCode"
    === ":fontawesome-brands-windows: Windows"
        1. Download the installer from the [VSCode website][vscode]
        2. Run the installer and follow the instructions.

    === ":fontawesome-brands-apple: MacOS"
        3. Download the installer from the [VSCode website][vscode]
        4. Run the installer and follow the instructions.

    === ":fontawesome-brands-linux: Linux"
        === "Debian"
            1. Download the installer from the [VSCode website][vscode]
            2. Run the installer and follow the instructions.

        === "Arch"
            === "pacman"
                1. Ensure your package manager is up to date:

                   ```bash
                   sudo pacman -Syu
                   ```

                2. Install VSCode:

                   ```bash
                   sudo pacman -S code
                   ```

            === "yay"
                1. Install VSCode:

                ```bash
                yay -S visual-studio-code-bin
                ```

### Setting up VSCode

#### Associating `.vpy` files

If you have not done so already,
make sure you install the [Python extension][vscode-python] for VSCode.

`.vpy` is the file extension commonly used for Vapoursynth scripts.
However, IDEs will not automatically associate this file extension with Python.

To fix this,
you can create a custom file association in VSCode.

!!! info "`.ppy` files"
    `.ppy` files are the file extension commonly used for vspreview plugin scripts.

!!! example "Associating `.vpy` files"
     1. Open the Command Palette (with the keyboard shortcut `F1`).
     2. Search for "Preferences: Open Settings (JSON)" and select it.
     3. Add the following line to the JSON settings and save the file:

     ```json
     "files.associations": {
         "*.vpy": "python",
         "*.ppy": "python"
     }
     ```

#### Configuring the launch file

To easily preview your Vapoursynth scripts,
we will configure a launch file.

!!! example "Configuring the launch file"
    === ":material-microsoft-visual-studio-code: Global launch file"
        1. Open the Command Palette (with the keyboard shortcut `F1`).
        2. Search for "Preferences: Open Keyboard Shortcuts (JSON)" and select it.
        3. Add the following line to the JSON settings and save the file.<br>
           You can change the "key" to whichever keybind you prefer.

        ```json
        // Binding for previewing a Vapoursynth filterchain using vs-preview
        {
            "key": "F5",
            "command": "workbench.action.terminal.sendSequence",
            "args": {
                "text": "python -m vspreview \"${file}\"\u000D"
            },
            "when": "resourceExtname == '.py' || resourceExtname == '.vpy'",
            "description": "Preview a Vapoursynth script with vspreview"
        }
        ```

    === ":octicons-terminal-16: Local launch file"
        !!! warning
            This method requires you to run the setup command for every new project.
            For ease of use, we strongly advise setting a global launch file instead.

        4. Open a terminal in your project directory.
        5. Run the following command:

        ```bash
        $ vspreview --vscode-setup
        ```

## Installing plugins

!!! info "Packages vs. Plugins"
     Plugins are not the same as packages!

     If a file has the `.py` extension,
     it's a Python package.
     Python packages must be imported
     in order to be used.<br>
     Plugins are external DLLs
     that are automatically loaded by Vapoursynth.

Vapoursynth by itself is only a frame server,
and only a handful of basic plugins are included by default.
The meat of the Vapoursynth ecosystem lies in third- (and sometimes first)-party plugins,
which must be installed separately.

JET packages depend on a number of plugins,
and will attempt to call them if possible.
If a plugin is not found,
it may throw an error like:

```bash
Python exception: No attribute with the name bs exists. Did you mistype a plugin namespace or forget to install a plugin?
```

In this error, `bs` is the plugin that is missing,
and stands for `BestSource`.

!!! info "Plugin namespaces"
    Plugin namespaces help distinguish between plugins with the same name.
    This is useful for differentiating between implementations,
    but the namespace by itself may not be enough to go on.

    If you can't find a specific plugin,
    feel free to ask for help in the [JET Discord server][discord].

!!! example "Installing plugins"
    === ":octicons-terminal-16: Terminal"
        === ":fontawesome-brands-windows: Windows"
            !!! warning "Running into issues with VSRepo"
                VSRepo can be finicky depending on your configuration and file associations.
                If you run into issues,
                you can try using a different terminal,
                or calling it as `python -m vsrepo` or `vsrepo.py`.

                If all else fails,
                you can either go to the VSRepo directory (`%LOCALAPPDATA%/Programs/VapourSynth/vsrepo`),
                open a terminal there,
                and run `python vsrepo.py` from there,
                or try installing the plugin [manually](#__tabbed_19_2).

            On Windows,
            plugins are installed using VSRepo.

            1. Open a terminal.
            2. Update the plugin list:

            ```bash
            $ vsrepo update
            ```

            3. Install the plugin you need using the following command:

            ```bash
            $ vsrepo install plugin_name
            ```

            You can also install multiple plugins at once:

            ```bash
            $ vsrepo install plugin_name1 plugin_name2 plugin_name3
            ```

        === ":fontawesome-brands-apple: MacOS"
            !!! warning "Stub"
                This page is a [stub][wikipedia-stubs].
                You can help by [expanding it][contributing]

        === ":fontawesome-brands-linux: Linux"
            === "Debian"
                !!! warning "Stub"
                    This page is a [stub][wikipedia-stubs].
                    You can help by [expanding it][contributing]

            === "Arch"
                === "pacman"
                    !!! danger "Package availability"
                        Very few plugins are available in the official repositories.<br>
                        You will have to install the plugins from the AUR,
                        or build them from source.

                === "yay"
                    1. Find the plugin you want to install on the [AUR][aur-vs-plugins].
                    2. Install the plugin using the following command:

                    ```bash
                    yay -S vapoursynth-plugin-plugin-name
                    ```
    === ":octicons-tools-16: Manual installation"
        === ":fontawesome-brands-windows: Windows"
            Vapoursynth plugins are stored in the `plugins` and `plugins64` subdirectory
            of the Vapoursynth installation directory.

            To manually install a plugin,
            grab the plugin DLL and place it in the `plugins` or `plugins64` directory.

        === ":fontawesome-brands-apple: MacOS"
            !!! warning "Stub"
                This page is a [stub][wikipedia-stubs].
                You can help by [expanding it][contributing]

        === ":fontawesome-brands-linux: Linux"

            === "Debian"

                !!! warning "Stub"
                    This page is a [stub][wikipedia-stubs].
                    You can help by [expanding it][contributing]

            === "Arch"

                !!! warning "Stub"
                    This page is a [stub][wikipedia-stubs].
                    You can help by [expanding it][contributing]

[//]: # (stubs)
[contributing]: https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing
[wikipedia-stubs]: https://en.wikipedia.org/wiki/Wikipedia:Stubs

[//]: # (programs and other urls)
[quickstart]: ./quickstart.md
[vsjet-python-repositories]: https://github.com/orgs/Jaded-Encoding-Thaumaturgy/repositories?q=language%3APython
[vsjet-requirements]: https://github.com/Jaded-Encoding-Thaumaturgy/vs-jet/blob/master/requirements.txt

[//]: # (programs and other urls)
[python-download]: https://www.python.org/downloads/
[vapoursynth-doc]: http://www.vapoursynth.com/doc/installation.html
[vapoursynth-release]: https://github.com/vapoursynth/vapoursynth/releases
[deb-multimedia]: https://www.deb-multimedia.org/
[git-bash]: https://gitforwindows.org/
[terminal-guide]: https://www.freecodecamp.org/news/command-line-for-beginners/
[vscode]: https://code.visualstudio.com/download
[vscode-python]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[aur-vs-plugins]: https://aur.archlinux.org/packages?O=0&SeB=nd&K=vapoursynth-plugin&outdated=&SB=p&SO=d&PP=50&submit=Go

[//]: # (other)
[discord]: https://discord.gg/XTpc6Fa9eB
