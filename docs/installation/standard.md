# Installing Vapoursynth and JET

!!! info
    This page is a [stub](https://en.wikipedia.org/wiki/Wikipedia:Stubs).
    You can help by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing).

This page explains how to install both VapourSynth and JET,
as well as how to set up your code editor and previewer.

We will be going over the following steps:

- Installing requirements
- Setting up your code editor

## Prerequisite knowledge

!!! warning "User skill level"
    This guide is written assuming the user has absolutely zero prior Vapoursynth or Python experience
    and is starting fresh,
    as many Vapoursynth users are not programmers.
    If you are a programmer,
    you may skip some of the steps (including this one)
    or find out more about the prerequisites
    by reading the [Vapoursynth documentation](http://www.vapoursynth.com/doc/installation.html).

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

!!! example "Removing existing installations"

    === "Windows"
        !!! question
            It's unknown how necessary this step is.
            If you're a programmer,
            you might want to keep your existing Python installation,
            but if you're not and you want to start fresh,
            this step is recommended.

        Prior to (re-)installing Vapoursynth,
        make sure to remove any existing installations.

        This means deleting the following directories:

        - `%APPDATA%/VapourSynth`
        - `%APPDATA%/Python`
        - `%LOCALAPPDATA%/Programs/VapourSynth`
        - `%LOCALAPPDATA%/Programs/Python`

    === "Linux"
        !!! info "Stub"
            This page is a [stub](https://en.wikipedia.org/wiki/Wikipedia:Stubs).
            You can help by [expanding it](https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing).

## Installation

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

        ```sh
        brew install python
        ```

    === "Linux"
        === "Debian"
            1. Ensure your package manager is up to date:
            ```sh
            sudo apt update && sudo apt upgrade
            ```

            2. Install Python:
            ```sh
            sudo apt install python3 python3-pip python3-virtualenv
            ```

        === "Arch"
            === "pacman"

                1. Ensure your package manager is up to date:
                ```sh
                sudo pacman -Syu
                ```

                2. Install Python:
                ```sh
                sudo pacman -S python python-pip python-virtualenv
                ```

            === "yay"
                ```sh
                yay -S python python-pip python-virtualenv
                ```

After installation,
you can verify that everything is working by running the following commands in a terminal:

```sh
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

        ```sh
        brew install vapoursynth
        ```

    === "Linux"

        === "Debian"

            1. The Vapoursynth is available in the [deb-multimedia repository](https://www.deb-multimedia.org/).
            Follow the instructions on their site to add the repository to your system.
            3. Update your package manager:
            ```sh
            sudo apt update
            ```

            4. Install Vapoursynth:
            ```sh
            sudo apt install vapoursynth
            ```

        === "Arch"
            === "pacman"

                1. Ensure your package manager is up to date:
                ```sh
                sudo pacman -Syu
                ```

                2. Install Vapoursynth:
                ```sh
                sudo pacman -S vapoursynth
                ```

            === "yay"
                1. Install Vapoursynth:

                ```sh
                yay -S vapoursynth
                ```

After installation,
you can verify that everything is working by running the following commands in a terminal:

```sh
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

=== "Windows"
    To install it, open a terminal and run:

    ```bash
    $ pip install vsjet
    ```

=== "macOS"
    To install it, open a terminal and run:

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
            ```sh
            sudo pacman -Syu
                ```

            2. Install the JET meta package:
            ```sh
            sudo pacman -S vapoursynth-plugin-vsjet-meta-git
            ```

        === "yay"
            1. Install the JET meta package:

            ```sh
            yay -S vapoursynth-plugin-vsjet-meta-git
            ```

### Updating JET

=== "Windows"
    === "Stable"
        You can update the JET packages using the following command:

        ```bash
        $ vsjet
        ```

    === "Nightly"
        !!! danger "Nightly version"
            Nightly/latest versions are not always stable.
            They may contain bugs or other issues that could cause problems.<br>
            If you run into issues,
            you can follow the "Stable" instructions again to roll back to a stable version.

        If you want to install the nightly version,
        you can use the following command:

        ```bash
        $ vsjet latest
        ```

        This will install the latest bleeding-edge versions of every JET package.

=== "macOS"
    === "Stable"
        You can update the JET packages using the following command:

        ```bash
        $ vsjet
        ```

    === "Nightly"
        !!! danger "Nightly version"
            Nightly/latest versions are not always stable.
            They may contain bugs or other issues that could cause problems.<br>
            If you run into issues,
            you can follow the "Stable" instructions again to roll back to a stable version.

        If you want to install the nightly version,
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

## Installing your IDE

TODO
