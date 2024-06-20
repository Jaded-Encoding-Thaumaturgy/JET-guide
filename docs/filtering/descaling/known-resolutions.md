# A List of Known Native Resolutions

It can be difficult
to determine the native resolution
of an anime.
Many encoders
have already done
a lot of research themselves,
and this page documents the found results.

!!! danger "Attention"
    Our knowledge on descaling
    is ever-improving.
    Some of these findings may be inaccurate
    and outdated!
    Take them with a grain of salt,
    and do your due diligence.
    Verify everything yourself
    before applying a descale
    to your encode!

This table contains
the following information:

1. The show name,
   with a link to its AniDB page.
   Seasons are separated
   into their own rows.
   This may extend
   to certain specials too.
2. The known native resolutions
   and kernels.
   This may be a list
   of multiple resolutions
   with additional information.
   in certain cases
   If a kernel is unknown,
   "unknown" will be written down instead.
3. A confidence rating
   on whether this show
   is descaleable
   with current known tools
   and techniques.
4. Additional notes
   and information.

## Known Native Resolutions

| Anime name                                                                     | Native Resolution(s)/Kernel                            | Descaleable? | Notes                                                                                                       |
| ------------------------------------------------------------------------------ | ------------------------------------------------------ | ------------ | ----------------------------------------------------------------------------------------------------------- |
| [Blue Archive the Animation](https://anidb.net/anime/17834)                    | 1280x720 (Bilinear)<br>1920x1080\*                     | Yes          | OP and ED are 1920x1080                                                                                     |
| [Gakkou Gurashi!](https://anidb.net/anime/10697)                               | 1280x720 (Lanczos 3-taps)<br>1280x720 (BicubicSharp)\* | Yes          | BicubicSharp on frames with overlays                                                                        |
| [Hayate no Gotoku!](https://anidb.net/anime/4917)                              | 1280x720? (Unknown)                                    | No           | HDCAM master                                                                                                |
| [Kubikiri Cycle: Aoiro Savant to Zaregotozukai](https://anidb.net/anime/12116) | 1279.67...x719.67... (FFmpegBicubic)                   | Yes          | Match centers model                                                                                         |
| [Kuzu no Honkai](https://anidb.net/anime/11998)                                | 1280x720 (Lanczos 3-taps)<br>1280x720 (BicubicSharp)\* | Yes          | BicubicSharp on frames with overlays                                                                        |
| [Toaru Majutsu no Index](https://anidb.net/anime/5975)                         | 1280x720 (Bilinear)<br>1440x1080 (Bilinear)            | Yes\*        | HDCAM master, can be descaled to 720 vertically, but only 1440 horizontally, and requires multiple descales |
