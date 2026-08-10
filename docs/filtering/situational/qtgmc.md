# QTGMC

QTGMC (Quick Temporal Gaussian Motion Compensated) is an advanced algorithm for deinterlacing interlaced video or repairing progressive material.

!!! warning "When to use QTGMC"
    QTGMC is a filter for *deinterlacing* footage. Not all footage that is
    "interlaced" (in the sense that it contains combed frames)
    should be *deinterlaced*.
    In many cases, the combed footage is actually *telecined*, in which case
    deinterlacing it is incorrect and destructive. Read the guide on [field-based video](fieldbased.md)
    for how to differentiate between interlaced telecined footage.

## Basic Usage

The simplest possible QTGMC call is the following:

```py
from vsdeinterlace import QTempGaussMC

# load your interlaced clip
# clip = ...

deinterlaced = QTempGaussMC().deinterlace(clip)

# then proceed to output your deinterlaced clip or filter it further.
# clip.set_output()
```

## Debugging

QTGMC consists of several stages. Extremely roughly, they are

1. Create a naively bobbed and strongly temporally blurred clip to run motion analysis on.
1. Bob the input clip with a high-quality spatial deinterlacer like NNEDI3 or EEDI3.
1. Use the computed motion vectors to refine the spatially deinterlaced clip further.

For a more detailed explanation of the algorithm, refer to the [documentation](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsdeinterlace/qtgmc/) or the [Avisynth wiki](http://avisynth.nl/index.php/QTGMC).

You can access some of the intermediate clips produced during this pipeline to more precisely check what QTGMC is doing and what effects your parameters have:

```py
qtgmc = QTempGaussMC()
deinterlaced = qtgmc.deinterlace(clip)

clip.set_output(0)

qtgmc.draft.set_output(1)
qtgmc.prefilter_output.set_output(2)
qtgmc.denoise_output.set_output(3)
qtgmc.input.set_output(4)
qtgmc.bobbed.set_output(5)
qtgmc.basic_output.set_output(6)
qtgmc.final_output.set_output(7)
qtgmc.motion_blur_output.set_output(8)

deinterlaced.set_output(9)
```

You can also access the used MVTools instance using `qtgmc.mv` (and hence its computed vectors using `qtgmc.mv.vectors`) if you want to reuse them elsewhere.

Refer to the [docstrings](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsdeinterlace/qtgmc/#vsdeinterlace.qtgmc.QTempGaussMC.basic_output) for each of these variables for explanations of their roles.

## Configuring

Each of QTGMC's stages can be configured in great detail.
There are two ways to pass settings to QTGMC. The first is to use the configuration methods for each of the individual stages:

```py
from vsaa import EEDI3

qtgmc = QTempGaussMC()
qtgmc.prefilter(tr=3)                                     # Configure the prefilter stage to use a higher temporal radius
qtgmc.analyze(blksize=32)                                 # Configure the motion analysis stage to use a larger block size
qtgmc.basic(tr=3, bobber=EEDI3(alpha=0.25, beta=0.3))     # Configure the basic stage to use EEDI3 as a bobber and a temporal radius of 3
# etc.
# Note that these are example settings that should not be blindly copied.

deinterlaced = qtgmc.deinterlace(clip)


# Or, alternatively, all in one line:

deinterlaced = QTempGaussMC().prefilter(tr=3).analyze(blksize=32).basic(tr=3, bobber=EEDI3(alpha=0.25, beta=0.3)).deinterlace(clip)
```

The docstrings of these stage configuration methods contain explanations of all the possible parameters.

The second way to pass settings is to pass all of them when constructing the `QTempGaussMC` method by prefixing each stage's parameter with the stage's name:

```py
from vsaa import EEDI3

deinterlaced = QTempGaussMC(prefilter_tr=3, analyze_blksize=32, basic_tr=3, basic_bobber=EEDI3(alpha=0.25, beta=0.3)).deinterlace(clip)
```

This can be useful when you want to collect a group of args into a "preset" that you can then pass to multiple different QTGMC calls:

```py

from vsaa import EEDI3

my_qtgmc_settings = {prefilter_tr=3, analyze_blksize=32, basic_tr=3, basic_bobber=EEDI3(alpha=0.25, beta=0.3)}

deinterlaced1 = QTempGaussMC(**my_qtgmc_settings).deinterlace(clip1)
deinterlaced2 = QTempGaussMC(**my_qtgmc_settings, final_thsad=192).deinterlace(clip2)

```

## Reusing

Once you have a configured `QTempGaussMC` instance, you can also use it to process more than one clip:

```py
qtgmc = QTempGaussMC()
# set some parameters 

deinterlaced = qtgmc.deinterlace(clip1)
repaired = qtgmc.repair(clip2)
```
