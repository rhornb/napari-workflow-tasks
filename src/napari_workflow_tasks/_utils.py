#!/usr/bin/env python3
import logging
from typing import Optional

import numpy as np
from ngio import Roi

from napari.utils.notifications import show_info

def create_roi_from_bbox(data: np.ndarray, roi_id: Optional[int]= None):
    """Create roi_table roi from 2D bounding box coordinates.

    Parameters
    ----------
    data : (N, 2) array
        Points around which the box is created.
    roi_id : int, optional
        ID to assign to the roi name.

    Returns
    -------
    roi_crop : Roi
    """
    top_left = np.min(data, axis=(0))
    bottom_right = np.max(data, axis=(0))
    
    y, x = top_left[1], top_left[2]
    x_length = bottom_right[2] - top_left[2]
    y_length = bottom_right[1] - top_left[1]
    
    if roi_id is not None:
        name = f"FOV_{roi_id}"
    else:
        name = "FOV_1"
    
    roi_crop = Roi(x=x, y=y, x_length=x_length, y_length=y_length, name=name)
    return roi_crop

class NapariHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        show_info(log_entry)

