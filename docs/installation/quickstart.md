# Quickstart

!!! warning "Stub"
    This page is a [stub][wikipedia-stubs].
    You can help by [expanding it][contributing].

    ??? question "How can I help?"
        MacOS and Linux users can help by adding and verifying information
        on how to install the dependencies on their respective operating systems.

These are quickstart instructions to get you started immediately.

!!! warning
    Only follow these instructions if you're already familiar with Python
    or installing packages yourself.
    If you're new,
    we suggest following the [standard installation guide](standard.md) instead.

## Pre-installation

It may be a good idea to get a clean slate before continuing.

??? example "Removing existing installations"
    !!! question "When to do this"
         If you're a programmer,
         you might want to keep your existing Python installation,
         but if you're not and you want to start fresh,
         this step is recommended.

    Prior to (re-)installing Vapoursynth,
    make sure to remove any existing installations.

    This means deleting the following directories:

    === ":fontawesome-brands-windows: Windows"

        - `%APPDATA%/VapourSynth`
        - `%APPDATA%/Python`
        - `%LOCALAPPDATA%/Programs/VapourSynth`
        - `%LOCALAPPDATA%/Programs/Python`

    === ":fontawesome-brands-apple: macOS"

        - `~/Library/Application Support/VapourSynth`
        - `~/Library/Application Support/Python`
        - `~/Library/Python`

    === ":fontawesome-brands-linux: Linux"

        - `~/.config/VapourSynth`

## Installation

Installing JET and its dependencies is pretty straightforward.

!!! example "Installation steps"
    === ":fontawesome-brands-windows: Windows"
        1. Install the latest version of Python from the [Python website][python-download].<br>
           Make sure to select the option to "_Add Python to PATH_"!

        2. Download the [latest GitHub release][vapoursynth-release] for Vapoursynth.

        3. Install JET using pip:

           ```bash
           $ pip install vsjet
           ```

    === ":fontawesome-brands-apple: macOS"
        4. Install Python using Homebrew.

           ```bash
           $ brew install python
           ```

        5. Install Vapoursynth using Homebrew.

           ```bash
           $ brew install vapoursynth
           ```

        6. Install JET using pip:

           ```bash
           $ pip install vsjet
           ```

    === ":fontawesome-brands-linux: Linux"
        === "Debian"
            1. Add the [deb-multimedia repository][deb-multimedia] to your system
               by following the instructions on their site.

            2. Ensure your package manager is up to date:

               ```bash
               $ sudo apt update && sudo apt upgrade
               ```

            3. Install Python:

               ```bash
               $ sudo apt install python3 python3-pip python3-virtualenv
               ```

            4. Install Vapoursynth:

               ```bash
               $ sudo apt install vapoursynth
               ```

            5. Install JET using pip:

               ```bash
               $ pip install vsjet
               ```

        === "Arch"
            === "pacman"
                1. Ensure your package manager is up to date:

                   ```bash
                   $ sudo pacman -Syu
                   ```

                2. Install Python:

                   ```bash
                   $ sudo pacman -S python python-pip
                   ```

                3. Install Vapoursynth:

                   ```bash
                   $ sudo pacman -S vapoursynth
                   ```

                4. Install JET using the `vapoursynth-plugin-vsjet-meta-git` AUR package:

                   ```bash
                   $ sudo pacman -S vapoursynth-plugin-vsjet-meta-git
                   ```

            === "yay"
                1. Install Python:

                   ```bash
                   $ yay -S python python-pip python-virtualenv
                   ```

                2. Install Vapoursynth:

                   ```bash
                   $ sudo pacman -S vapoursynth
                   ```

                3. Install JET using the `vapoursynth-plugin-vsjet-meta-git` AUR package:

                   ```bash
                   $ yay -S vapoursynth-plugin-vsjet-meta-git
                   ```

Verify the installation by running the following commands in a terminal:

```bash
$ vspipe --version
```

```bash
$ python
>>> from vapoursynth import core
>>> str(core)
'VapourSynth Video Processing Library\nCopyright (c) 2012-2024 Fredrik Mellbin\n\tCore R70\n\tAPI R4.1\n\tAPI R3.6\n\tOptions: -\n\tNumber of Threads: 32\n\tMax Cache Size: 4096\n'
```

[//]: # (stubs)
[contributing]: https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing
[wikipedia-stubs]: https://en.wikipedia.org/wiki/Wikipedia:Stubs

[//]: # (programs and other urls)
[python-download]: https://www.python.org/downloads/
[vapoursynth-release]: https://github.com/vapoursynth/vapoursynth/releases
[deb-multimedia]: https://www.deb-multimedia.org/