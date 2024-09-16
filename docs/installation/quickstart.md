# Quickstart

These are quickstart instructions to get you started immediately.
Only follow these if you're already familiar with Vapoursynth.

## Pre-installation

It may be a good idea to get a clean slate before continuing.

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

## Installation

Installing JET and its dependencies is pretty straightforward.

!!! example "Installation steps"
    === ":fontawesome-brands-windows: Windows"
        1. Install that version or a newer version from the [Python website](https://www.python.org/downloads/).<br>
            Make sure to select the option to "_Add Python to PATH_"!

        2. Download the [latest GitHub release](https://github.com/vapoursynth/vapoursynth/releases) for Vapoursynth.

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
            1. Add the [deb-multimedia repository](https://www.deb-multimedia.org/) to your system
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