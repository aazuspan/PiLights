from backend.visualizations.Trails.GenericTrail import GenericTrail


class GreenTrail(GenericTrail):
    name = 'Green Trail'
    description = 'A light trail with a white head and green trail.'
    hide = False

    head_color = (200, 255, 200)
    tail_color = (0, 255, 100)
    fill_color = (0, 15, 5)
    trail_length = 15
    delay_ms = 45
