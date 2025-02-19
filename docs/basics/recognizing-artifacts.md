# Recognizing Artifacts

!!! warning "Not a Filtering Guide"

    This page focuses on identifying artifacts
    rather than providing detailed filtering solutions.
    For specific filtering techniques,
    refer to the relevant pages
    in the filtering section of this guide,
    which will be linked throughout
    where applicable.

As a video encoder,
you will inevitably encounter artifacts in your video.
These are flaws in the source material,
and your job
is to fix them
if possible,
or at least
to make them less noticeable.
No video is perfect,
but with a little bit of finesse,
a lot of problems
can be suppressed
or even entirely eliminated.

## Types of Artifacts

Most artifacts
can be broadly categorized
into two distinct
yet closely related types:

1. **Mastering defects**
2. **Authoring defects**

!!! warning "Defect Categories Are Not Absolute"

    While certain artifacts
    tend to appear more frequently
    during specific stages of production,
    any type of defect
    can potentially occur
    at any point in the process.

    For example,
    poor deinterlacing
    is commonly associated with authoring,
    but a studio might also apply it
    during mastering
    or send deinterlaced masters
    to a distributor.
    Similarly,
    compression artifacts
    typically arise during authoring,
    but can also be present
    in the master
    if it was poorly archived
    or transmitted.

    Be flexible in your understanding
    of where an artifact may have originated from,
    as the same visual artifact
    may require different solutions
    depending on its origin!

### Mastering defects

Mastering defects are imperfections
inherent to the master
of video content.
These typically arise from technical limitations
in the production studio's software and equipment
during the anime production and mastering process.
While many mastering defects
are inherent to the original production,
some may be introduced later
through subpar remastering efforts.

Common mastering defects include:

- Low-quality upscales
- Aliasing in computer-generated 3D content
- Excessive artificial sharpening
- Visible banding in gradients due to limited bit depth
- Orphan fields introduced in telecined content

### Authoring defects

Authoring defects are flaws
introduced into the source material
during the authoring process,
such as Blu-ray/DVD authoring,
poor analog-to-digital transfers,
or compression for streaming platforms.
These artifacts commonly originate
from the encoding process
and various authoring tools
used by distribution companies
and streaming services.
As a result,
these defects may appear
on some releases but not others,
even for the same shows.

Common authoring defects include:

- Heavy quantization (a.k.a. compression) artifacts
- Improper colorspace conversion
- Lowpass filtering
- Poor deinterlacing or IVTC

## Trade-offs

A common misconception
among both new encoders
and those unfamiliar with encoding
is that every single artifact
_must_ be fixed.
This is far from the case.
Each filter applied to a video
comes with its own costs and trade-offs,
and it's crucial to understand
when leaving an artifact unfixed
may be preferable to
introducing new problems
through aggressive filtering.
Nearly every single filter
has the potential
to degrade video quality
in some way.

There are some exceptions
to this general rule,
particularly with filters
that perform the _mathematical inverse_
of a known operation.
A prime example is _descaling_,
which [reverses the upscaling process](../filtering/descaling/descaling.md)
to remove artifacts
introduced during upscaling,
while allowing you to re-upscale the image
using a much better algorithm.
However, even these "inverse" filters
will cause issues if misapplied,
and come with their own limitations
and requirements.

When deciding whether to apply filtering,
you should carefully weigh the benefits
against any potential drawbacks.
If you're confident
the pros outweigh the cons,
then proceed with the filter.
But if you're uncertain
about potential side effects,
it's often better to either
skip the filter entirely
or thoroughly [compare the results](../misc/comparison.md)
to ensure the trade-offs
are worthwhile.

## Frame Composition

Before you can effectively identify
and address artifacts,
it's essential to understand
the fundamental components
that make up a frame.
Different regions within a frame
have distinct characteristics
that make them more or less susceptible
to specific types of artifacts.

The following sections break down
the key regions you'll encounter
and how they interact
with various artifacts.
By learning to recognize
these distinct areas,
you'll be better equipped to:

1. Identify where artifacts
   are most likely to appear
2. Understand why certain artifacts
   occur in specific regions
3. Make informed decisions
   about trade-offs
   in your filtering choices

!!! example "Different types of regions of a frame"

    ![Screenshot of Hibiki from The iDOLM@STER](./img/artifacts/imas-frame.png)

It's recommended
you open this image
in a new tab
and zoom in on it
to get a better look
at the different regions.

### Flat Areas

Flat areas are regions in a frame
characterized by low-frequency components
and minimal pixel-to-pixel variations.
These areas tend to have very subtle color
and brightness transitions,
if any at all.

Due to their uniform nature,
flat areas are particularly susceptible
to artifacts like banding,
blocking,
and quantization noise.

Common examples include:

- Solid colored backgrounds (e.g., title cards, UI elements)
- Clear, cloudless skies
- Smooth surfaces like walls, skin, or polished materials
- Uniform gradients (e.g., lighting transitions, shadows)
- Out-of-focus backgrounds ([bokeh](https://en.wikipedia.org/wiki/Bokeh))

### Hard Edges

Hard edges encompass any sharp,
clearly defined transitions
between different regions in an image.
These edges provide high contrast
between objects and their surroundings.

Hard edges are high-frequency information,
and are therefore particularly susceptible
to compression artifacting,
as well as artifacting
that results from poor upscaling,
such as ringing, aliasing, and blurring.

Common examples include:

- Character line-art
- Text and subtitles
- Sharp boundaries between objects in the background
- Geometric shapes and patterns
- Architectural features like window frames or building edges
- Strong shadow boundaries

### Textures

Textures are more complex
and can contain a mix of high-frequency
and low-frequency information.
This makes it difficult
to target them specifically
without introducing unwanted detail loss.

Textures are often found in:

- Complex patterns like wallpaper or floors
- Natural elements like wood, stone, or fabric
- Detailed backgrounds like foliage or water

### Dithering

Dithering is a technique
used to help prevent banding
and other color break-ups
during compression.
This is not an artifact
in and of itself,
but it can be difficult
to immediately recognize
the difference between dithering and textures,
and dithering and compression noise.
The big thing
that usually sets them apart
is the noise structure.
Dithering is usually random,
while textures are usually structured.
Noise can still be somewhat random
both spatially and temporally,
but usually has a discernible structure.

The [colors of noise](https://en.wikipedia.org/wiki/Colors_of_noise) applied for dithering
will impact the noise structure
as well as which frequencies
they are most visible in.
Some colors will be more difficult to get rid of,
and may require leaving alone.
In almost all cases,
you will want to try to match
the original noise color
when redithering
at the end of your filtering script.

| Noise Color  | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| White noise  | Equal intensity at all frequencies                              |
| Blue noise   | Concentrates energy in higher frequencies, perceptually uniform |
| Violet noise | Intensity increases with frequency                              |
| Pink noise   | Intensity decreases with frequency                              |
| Brown noise  | Intensity decreases more steeply with frequency                 |

## Spatial vs. Temporal

Artifacts can appear either spatially,
temporally,
or as a combination of both:

- **Spatially**
   (static,
   easily visible in a single frame)
- **Temporally**
   (dynamic,
   visible only in motion)

Spatial artifacts are visible
when looking at a single frame,
and generally stay static
from frame to frame.
These include things like:

- Banding in gradients
- Ringing around edges
- Aliasing
- Blurring from poor upscaling

Temporal artifacts only become visible
when watching the video in motion.
Common examples include:

- Shimmering
- Flickering
- Motion judder
- Interlacing

Temporal artifacts are more difficult to fix
and will require motion compensation
to some extent,
which is also rather expensive
in terms of processing power.

## Artifacts

!!! warning "Not Exhaustive"

    This list covers artifacts
    you are likely to encounter,
    but is **_not_** exhaustive.
    Many artifacts
    can manifest in different ways
    or combine characteristics
    of multiple categories
    (for example,
    poor upscaling can cause blurring,
    aliasing,
    and ringing).
    When diagnosing issues,
    focus on understanding
    the underlying causes
    rather than strict categorization.

### Banding

!!! example "Frame with banding"

    !!! info "Exposure"

        This frame has additional exposure
        applied to it
        to help make the banding more visible
        in the marked region.

    ![Frame with heavy banding from Hayate no Gotoku!](./img/artifacts/hayate-banding.png)

Banding is one of
the most prevalent artifacts
in digital video.
It appears as visible "steps" or bands
in what should be smooth gradients,
such as in skies,
shadows,
or other areas
with color transitions.
This artifact occurs
when there isn't enough precision
to represent subtle color
and brightness variations smoothly.
There are two main causes:

1. The video was encoded
   with an insufficient bit depth,
   meaning there aren't enough distinct values
   to represent smooth gradients.
2. During production,
   processing was done
   at a low bit depth,
   introducing banding
   that gets "baked in"
   to the final output.

Most modern production workflows
use 16-bit color precision
during editing
and VFX work.
For final distribution,
this is usually reduced to 10-bit,
which is generally sufficient
for most content.
However,
most consumer video content
is further reduced to 8-bit color,
which only allows 256 distinct values
per color channel.
This significant reduction
in color precision
often makes banding visible,
especially in scenes
with subtle gradients
and darker areas of the image[^banding-video].

[^banding-video]: Tom Scott's [Why dark video is a terrible mess](https://www.youtube.com/watch?v=h9j89L8eQQk)
    goes into more detail
    on why this happens.

| Bit Depth | Colors Per Channel |
| --------- | ------------------ |
| 16-bit    | 65536              |
| 10-bit    | 1024               |
| 8-bit     | 256                |

The process
to fix this
is called "debanding".
Additional dithering is usually
applied after
to preserve the gradient
during the encoding stage.

#### Chroma banding

In some cases,
banding may be more noticeable
in the chroma planes
than in the luma plane.
This is because
the chroma planes
are often compressed
more heavily than the luma plane.

!!! example "Frame with chroma banding"

    <!-- TODO: Get frame from Slow Start -->

    ![]()

### Aliasing

Aliasing is a sawtooth-like artifact
that occurs on hard edges.
It is caused by a lack of high-frequency information,
and is often a sign of poor upscaling
or a lack of proper line smoothing.

There are four common causes
of aliasing:

1. Poor upscaling algorithms
2. Poor (3D) rendering
3. Binarized line art that wasn't smoothed
4. Stylistic choices

#### Poor upscaling algorithms

Poor upscaling algorithms are the most common source
of aliasing artifacts.
When an image is upscaled,
the algorithm must create new pixels
to fill in the gaps.
Most basic algorithms
struggle to handle sharp transitions smoothly,
resulting in jagged edges
and stair-stepping patterns.

!!! example "Frame with aliasing"

    <!-- TODO: Get a frame -->

    ![]()

#### Poor (3D) rendering

Poor rendering can cause aliasing
in the same way
that poor upscaling can.
3D rendered content especially
is prone to aliasing
when the rendering process
lacks sufficient anti-aliasing.
This is particularly noticeable
on high-contrast edges
and fine geometric details.

!!! example "Frame with aliasing"

    <!-- TODO: Get a frame -->

    ![]()

Non-poor 3D rendering
is common in western cartoons,
resulting in an overall very jagged look.

!!! example "Frame with aliasing"

    <!-- TODO: Get a frame from Generator Rex -->

    ![]()

#### Binarized line art that wasn't smoothed

During animation production,
frames are _binarized_
to create clean, sharp lines
for the coloring process.
This step is normally followed by
line smoothing to prevent aliasing.
However,
if this smoothing step is skipped,
the resulting lines will still be aliased.

!!! example "Frame with aliasing"

    <!-- TODO: Get a frame -->

    ![]()

#### Stylistic choices

Modern animation sometimes employs
deliberately jagged or pixelated lines
as a stylistic element.
These artistic choices are usually obvious
and should be preserved rather than "fixed"
through anti-aliasing.

!!! example "Frame with intentionally jagged lines"

    <!-- TODO: Get a frame from Occultic;Nine or Granblue Fantasy -->

    ![]()

### Ringing

#### Lowpass filters

### Noise

#### DCT noise

#### Grain

### Blocking

### Range compression/expansion

#### Luma overflow/underflow

### Interlacing

#### Combing

#### Orphan Fields

### Shimmering

### Cross-conversion

### Blending

### Dimming

### Point-scaled chroma

### Chroma shift

### Chroma bleed

### Rainbowing

### Dotcrawl

#### Double composite

### IRE units

### Scanning defects

<!-- TODO: Use that example from ToHeart2's Nozomi or ADV edit -->

### Cel degradation
