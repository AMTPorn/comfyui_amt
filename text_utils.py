import os
import sys
from pathlib import Path

class AMTStringDeduplication:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Deduplicate provided string(s).", "multiline": True}),
            },
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "deduplicate"

    def deduplicate(self, prompt):
        # Split by comma, strip whitespace, remove empty
        items = [item.strip() for item in prompt.split(',') if item.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_items = []
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)
        
        deduplicated_prompt = ', '.join(unique_items)
        
        return (deduplicated_prompt,)


