from backend.visualizations.Trails.GenericTrail import GenericTrail


class FireTrail(GenericTrail):
    name = 'Fire trail'
    description = 'A light trail with a red head and orange tail.'
    hide = False

    head_color = (255, 100, 0)
    tail_color = (200, 100, 0)
    fill_color = (15, 5, 0)
    trail_length = 15
    delay_ms = 45
