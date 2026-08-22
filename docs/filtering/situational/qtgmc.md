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

The other QTGMC modes work similarly:

```py
# Repair a badly deinterlaced progressive clip
repaired = QTempGaussMC().repair(clip2)

# Remove shimmering from a progressive clip
deshimmered = QTempGaussMC().deshimmer(clip3)
```

By default, `deinterlace()` will perform double-rate deinterlacing, i.e. generate a unique frame for every field of your input clip, hence resulting in twice as many output frames as input frames.
To perform single-rate deinterlacing, pass `fps_divisor=2` to the `motion_blur` stage (see below for an explanation of how to pass parameters):

```py
deinterlaced = QTempGaussMC().motion_blur(fps_divisor=2).deinterlace(clip)
```

## Configuring

QTGMC consists of several stages. Extremely roughly, they are

1. Create a naively bobbed and strongly temporally blurred clip to run motion analysis on.
1. Bob the input clip with a high-quality spatial deinterlacer like NNEDI3 or EEDI3.
1. Use the computed motion vectors to refine the spatially deinterlaced clip further.

For a more detailed explanation of the algorithm, refer to the [documentation](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsdeinterlace/qtgmc/)
You can access some of the intermediate clips produced during this pipeline to more precisely check what QTGMC is doing and what effects your parameters have:

```py
qtgmc = QTempGaussMC()
deinterlaced, graph = qtgmc.deinterlace(clip, return_graph=True)

clip.set_output(0)

graph.draft.set_output(1)
graph.prefilter.set_output(2)
graph.denoise.set_output(3)
graph.bob_input.set_output(4)
graph.bobbed.set_output(5)
graph.basic.set_output(6)
graph.final.set_output(7)
graph.motion_blur.set_output(8)

deinterlaced.set_output(9)
```

Refer to the [docstrings](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsdeinterlace/qtgmc/#vsdeinterlace.qtgmc.QTempGaussMC.basic_output) for each of these variables for explanations of their roles.

Each of these stages can be configured in great detail.
There are two ways to pass settings to QTGMC. The first is to use the configuration methods for each of the individual stages:

```py
from vsaa import EEDI3
from vsdenoise import MVToolsPreset

qtgmc = QTempGaussMC()
qtgmc.prefilter(tr=3)                                                         # Configure the prefilter stage to use a higher temporal radius
qtgmc.analyze(blksize=32, preset=MVToolsPreset.HQ_SAD | dict(chroma=False))   # Configure the motion analysis stage to use a larger block size and not check chroma
qtgmc.basic(tr=3, bobber=EEDI3(alpha=0.25, beta=0.3))                         # Configure the basic stage to use EEDI3 as a bobber and a temporal radius of 3
qtgmc.source_match(iterations=1)                                              # Enable the source match stage with 1 iteration
# etc.
# Note that these are example settings to illustrate how to set various kinds of parameters.
# Their values should not be blindly copied.

deinterlaced = qtgmc.deinterlace(clip)


# Or, alternatively, all in one line:

deinterlaced = QTempGaussMC().prefilter(tr=3).analyze(blksize=32, preset=MVToolsPreset.HQ_SAD | dict(chroma=False)).basic(tr=3, bobber=EEDI3(alpha=0.25, beta=0.3)).source_match(iterations=1).deinterlace(clip)
```

The [docstrings](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsdeinterlace/qtgmc/#vsdeinterlace.qtgmc.QTempGaussMC) of each of these stage configuration methods contain detailed explanations of all the possible parameters. If you are migrating from AviSynth or havsfunc's QTGMC, you can refer to [this mapping](https://gist.github.com/Ichunjo/76c96f1130c9e9f972de956f40571e54) for how parameter names in these QTGMC implementations map to vs-jetpack's parameter names.

The second way to pass settings is to pass all of them when constructing the `QTempGaussMC` method by prefixing each stage's parameter with the stage's name (separated by two underscores):

```py
from vsaa import EEDI3

deinterlaced = QTempGaussMC(prefilter__tr=3, analyze__blksize=32, analyze__preset=MVToolsPreset.HQ_SAD | dict(chroma=False), basic__tr=3, basic__bobber=EEDI3(alpha=0.25, beta=0.3), source_match__iterations=1).deinterlace(clip)
```

This can be useful when you want to collect a group of args into a "preset" that you can then pass to multiple different QTGMC calls:

```py

from vsaa import EEDI3

my_qtgmc_settings = dict(prefilter__tr=3, analyze__blksize=32, analyze__preset=MVToolsPreset.HQ_SAD | dict(chroma=False), basic__tr=3, basic__bobber=EEDI3(alpha=0.25, beta=0.3), source_match__iterations=1)

deinterlaced1 = QTempGaussMC(**my_qtgmc_settings).deinterlace(clip1)
deinterlaced2 = QTempGaussMC(**my_qtgmc_settings, final__thsad=192).deinterlace(clip2)
```

## Reusing

Once you have a configured `QTempGaussMC` instance, you can also use it to process more than one clip:

```py
qtgmc = QTempGaussMC()
# set some parameters 

deinterlaced = qtgmc.deinterlace(clip1)
repaired = qtgmc.repair(clip2)
```

You can also access the MVTools instance used by your QTGMC call using `graph.mv` (and hence its computed vectors using `graph.mv.vectors`) if you want to reuse them elsewhere.
