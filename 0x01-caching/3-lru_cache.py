#!/usr/bin/env python3
"""
LRUCache module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.lru_order = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update the LRU order
                self.lru_order.remove(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the least recently used item (LRU algorithm)
                lru_key = self.lru_order.pop(0)
                del self.cache_data[lru_key]
                print("DISCARD: {}".format(lru_key))
            self.cache_data[key] = item
            self.lru_order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        # Update the LRU order
        self.lru_order.remove(key)
        self.lru_order.append(key)
        return self.cache_data[key]
