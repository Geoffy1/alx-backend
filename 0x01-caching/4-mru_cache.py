#!/usr/bin/env python3
"""
MRUCache module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Move the key to the most recently used position (MRU algorithm)
                self.cache_data.pop(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the most recently used item (MRU algorithm)
                mru_key = next(reversed(self.cache_data))
                del self.cache_data[mru_key]
                print("DISCARD: {}".format(mru_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        # Move the key to the most recently used position (MRU algorithm)
        item = self.cache_data.pop(key)
        self.cache_data[key] = item
        return item
