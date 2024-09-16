# Installing Vapoursynth and JET

!!! info "Stub"
    This page is a [stub](https://en.wikipedia.org/wiki/Wikipedia:Stubs).
    You can help by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing).

!!! warning "User skill level"
    This guide is written assuming the user
    has absolutely zero Vapoursynth or Python experience
    and is starting fresh,
    as many Vapoursynth users are not programmers.
    If you are looking for the quickstart guide,
    you can find it [here](./quickstart.md).

This page explains how to install both VapourSynth and JET,
as well as how to set up your code editor and previewer.

We will be going over the following steps:

- Installing requirements
- Setting up your code editor

## Prerequisite knowledge

To follow this guide,
you should have a basic understanding of a couple of things.

### Terminal

If you're using Windows,
it's recommended to use Windows Terminal
with cmd or [git bash](https://git-scm.com/downloads) shell
as the default profile.

If you're a PowerShell user,
you may need to change a number of commands shown here
to make them work with PowerShell.

The terminal will be used a lot,
so it's recommended you get comfortable with it as soon as possible.
For a basic introduction,
see [this guide](https://www.freecodecamp.org/news/command-line-for-beginners/).

### Code blocks

  In this guide, as well as on other pages,
  you may find blocks like this:

  ```
  Some random text here
  ```

  This is also known as a "code block",
  and will contain pieces of code.

  If you see a code block like this:

  ```bash
  $ some_command
  ```

  This means you should run the command in your terminal (without the `$`).


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
               <p class="admonition-title">Question</p>
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
    === "Windows"
        !!! danger "Windows Store"
            Avoid installing Python from the Windows Store.
            The store version can have compatibility issues
            with certain packages and tools.

        1. Check the [Vapoursynth documentation](http://www.vapoursynth.com/doc/installation.html)
            to find out the latest Python version currently supported by Vapoursynth.
            At the time of writing, that's _Python 3.12_.

        2. Install that version or a newer version from the [Python website](https://www.python.org/downloads/).<br>
            Make sure to select the option to "_Add Python to PATH_"!

        3. Once you've downloaded the installer,
        run it and click on "Install Now".<br>

    === "macOS"
        Install Python using Homebrew.

        ```bash
        $ brew install python
        ```

    === "Linux"
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
    === "Windows"
        !!! warning "Installer versions"
            Unless you know what you're doing,
            you should avoid using the portable versions,
            as this can complicate things.

        1. Download the [GitHub release](https://github.com/vapoursynth/vapoursynth/releases)
        of VapourSynth that is tagged as "Latest".

        2. Run the installer and select "Install for this user only" if asked.

    === "macOS"
        Install Vapoursynth using Homebrew.

        ```bash
        $ brew install vapoursynth
        ```

    === "Linux"

        === "Debian"

            1. The Vapoursynth is available in the [deb-multimedia repository](https://www.deb-multimedia.org/).
            Follow the instructions on their site to add the repository to your system.
            3. Update your package manager:
            ```bash
            sudo apt update
            ```

            4. Install Vapoursynth:
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
you can verify that everything is working by running the following commands in a terminal:

```bash
$ vspipe --version
```

## Installing JET

The JET python packages build on top of the existing plugin ecosystem
to provide more convenient and complex functionality.
It adds, among other things:

- More convenient and Pythonic wrapper functions around various plugins.
- More complex filtering functions which combine functions of various plugins
  to achieve various filtering goals.
- `vs-preview`, a previewer for VapourSynth with plugin support and many useful features for encoders.
- Many helper functions and classes for developing Vapoursynth packages.

!!! example "Installing JET"
    === "Windows"
        1. Install JET using pip:

        ```bash
        $ pip install vsjet
        ```

    === "macOS"
        1. Install JET using pip:

        ```bash
        $ pip install vsjet
        ```

    === "Linux"
        === "Debian"
            !!! info "Stub"
                This page is a [stub](https://en.wikipedia.org/wiki/Wikipedia:Stubs).
                You can help by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing).

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
                3. Install the JET meta package:

                ```bash
                yay -S vapoursynth-plugin-vsjet-meta-git
                ```

### Updating JET

!!! example "Updating JET"
    === "Windows"
        === "Stable"
            1. You can update the JET packages using the following command:

            ```bash
            $ vsjet
            ```

        === "Nightly"
            !!! danger "Nightly version"
                Nightly/latest versions are not always stable.
                They may contain bugs or other issues that could cause problems.<br>
                If you run into issues,
                you can follow the "Stable" instructions again to roll back to a stable version.

            1. If you want to install the nightly version,
            you can use the following command:

            ```bash
            $ vsjet latest
            ```

            This will install the latest bleeding-edge versions of every JET package.

    === "macOS"
        === "Stable"
            1. You can update the JET packages using the following command:

            ```bash
            $ vsjet
            ```

        === "Nightly"
            !!! danger "Nightly version"
                Nightly/latest versions are not always stable.
                They may contain bugs or other issues that could cause problems.<br>
                If you run into issues,
                you can follow the "Stable" instructions again to roll back to a stable version.

            1. If you want to install the nightly version,
            you can use the following command:

            ```bash
            $ vsjet latest
            ```

            This will install the latest bleeding-edge versions of every JET package.

    === "Linux"
        === "Debian"
            !!! info "Stub"
                This page is a [stub](https://en.wikipedia.org/wiki/Wikipedia:Stubs).
                You can help by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing).

        === "Arch"
            !!! info "Stub"
                This page is a [stub](https://en.wikipedia.org/wiki/Wikipedia:Stubs).
                You can help by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing).

## Code editor

TODO

### Installing VSCode

TODO

### Setting up VSCode

TODO

## Installing plugins

TODO
