# Quickstart

These are quickstart instructions to get you started immediately.
Only follow these if you're already familiar with Vapoursynth.

## Pre-installation

It may be a good idea to get a clean slate before continuing.

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

=== "Windows"
      1. Install that version or a newer version from the [Python website](https://www.python.org/downloads/).<br>
          Make sure to select the option to "_Add Python to PATH_"!

      2. Download the [latest GitHub release](https://github.com/vapoursynth/vapoursynth/releases) for Vapoursynth.

      3. Install JET:
      ```bash
      $ pip install vsjet
      ```

=== "macOS"
      1. Install Python using Homebrew.

      ```sh
      brew install python
      ```

      2. Download the [latest GitHub release](https://github.com/vapoursynth/vapoursynth/releases) for Vapoursynth.

      3. Install JET:
      ```bash
      $ pip install vsjet
      ```
