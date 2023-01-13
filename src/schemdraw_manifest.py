
class SchemdrawElementManifest:
    def __init__(self, element_class, constructor_args, other_anchors, end_coord) -> None:
        self.element_class = element_class
        self.constructor_args = constructor_args
        self.other_anchors = other_anchors
        self.end_coord = end_coord

 