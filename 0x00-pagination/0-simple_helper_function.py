#!/usr/bin/env python3
"""Pagination
"""
from typing import Tuple


def index_range(page, page_size):
    """ Calculate the start and end indices based on the page and page size
    """
    start = (page - 1) * page_size
    end = start + page_size

    return start, end
