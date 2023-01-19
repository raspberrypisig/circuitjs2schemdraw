from schemdraw.elements import Element2Term, Element
from schemdraw import Segment, SegmentCircle, SegmentArrow
import math

gap = (math.nan, math.nan)

total_width = 1.0
#total_width = 1.0
total_height = 1.5
arrow_height = 0.7
arrow_bottom = arrow_height
drain_to_gate = total_width / 2.0
gate_to_source = drain_to_gate
drain_to_source = drain_to_gate + gate_to_source
lead_length = (total_width - drain_to_source)/2.0
drain_x = 0.0
gate_x = drain_x + drain_to_gate
source_x = drain_x + drain_to_source
half_leg = 0.1
gate_gap = 0.3

class PChannelMOSFET(Element):
    ''' P-type Field Effect Transistor which extends
        source/drain leads to the desired length

        Args:
            bulk: Draw bulk contact

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *d, bulk: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        '''
        self.segments.append(Segment([(0.0, -y_offset), (1.1, -y_offset), gap, (1.6, -y_offset), (3.0, -y_offset)]))
        self.segments.append(Segment([(1.1, -y_offset), (1.1, -arrow_bottom) ]))
        self.segments.append(Segment([(1.0, -arrow_bottom), (1.2, -arrow_bottom) ]))
        self.segments.append(Segment([(1.6, -y_offset), (1.6, -arrow_bottom) ]))
        self.segments.append(Segment([(1.5, -arrow_bottom), (1.7, -arrow_bottom) ]))        
        self.segments.append(Segment([(2.1, -y_offset), (2.1, -arrow_bottom) ]))
        self.segments.append(Segment([(2.0, -arrow_bottom), (2.2, -arrow_bottom) ])) 
        '''
        self.segments.append(Segment([(drain_x, 0.0),(drain_x,-arrow_bottom), gap, (gate_x, 0.0), (source_x, 0.0)]))        
        self.segments.append(Segment([(drain_x - half_leg, -arrow_bottom), (drain_x + half_leg, -arrow_bottom) ]))
        self.segments.append(Segment([(gate_x, -arrow_bottom), (gate_x, 0.0) ], arrow=">"))
        self.segments.append(Segment([(gate_x - half_leg, -arrow_bottom), (gate_x + half_leg, -arrow_bottom) ]))
        self.segments.append(Segment([(source_x, 0.0), (source_x, -arrow_bottom) ]))
        self.segments.append(Segment([(source_x - half_leg, -arrow_bottom), (source_x + half_leg, -arrow_bottom) ]))                
        self.segments.append(Segment([(drain_x + half_leg, -arrow_bottom - gate_gap), (source_x - half_leg, -arrow_bottom - gate_gap)]))
        self.segments.append(Segment([(gate_x, -arrow_bottom - gate_gap), (gate_x, -total_height)]))

        self.anchors['isource'] = (total_width, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (gate_x, total_height)
        self.params['lblloc'] = 'right'
        #if bulk:
        #    self.segments.append(Segment([(fetl+fetw/2, 0), (fetl+fetw/2, fetw)],
        #                                 arrow='->', arrowwidth=.2))
        #    self.anchors['bulk'] = (fetl+fetw/2, 0)
    
    
    '''
    def _place_anchors(self, start, end):
        super()._place_anchors(start, end)
        self.anchors['source'] = self.anchors['end']
        self.anchors['drain'] = self.anchors['start']
        if self._userparams.get('reverse', False):
            self.anchors['source'] = self.anchors['start']
            self.anchors['drain'] = self.anchors['end']
    '''
