from vsmuxtools import Setup, mux

setup = Setup("01")

mux(
    video_hevc.to_track(name="Vodes Encode", lang="jpn", default=True),
    audio.to_track("Japanese 2.0 (Amazon)", "jpn", True),
    subtitle.to_track("English (CR)", "en", True),
    *fonts,  # The * is necessary to unpack the list into multiple "tracks"
    chapters
)
