
class SchemdrawElementManifest:
    def __init__(self, element_class, constructor_args, other_anchors, start_coord, end_coord, has_length) -> None:
        self.element_class = element_class
        self.constructor_args = constructor_args
        self.other_anchors = other_anchors
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.has_length = has_length

 