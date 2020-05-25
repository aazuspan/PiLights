from backend.visualizations.Trails.GenericTrail import GenericTrail


class Comet(GenericTrail):
    name = 'Comet'
    description = 'A light trail with a white head and blue tail.'
    hide = False

    head_color = (255, 255, 255)
    tail_color = (255, 0, 255)
    fill_color = (0, 0, 15)
    trail_length = 15
    delay_ms = 45
