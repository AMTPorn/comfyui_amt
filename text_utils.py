import os
import sys
import re
import random
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

class AMTReplaceAndMaybeDropString:
    @classmethod
    def INPUT_TYPES(s):
        return {
        "required": {
            "String": ("STRING", {"default": ""}), # input string
            "Regex": ("STRING", {"default": ""}), # regex to search for
            "ReplaceWith": ("STRING", {"default": ""}), # string to replace with
            "DropChance": ("INT", {"default": 0, "min": 0, "max": 100}),
        }
    }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "replace"

    def replace(self, String, Regex, ReplaceWith, DropChance):
        # Clamp drop chance just in case
        drop_chance = max(0, min(100, DropChance))

        def replacer(match):
            roll = random.randint(1, 100)
            if roll <= drop_chance:
                return ""  # dropped
            return ReplaceWith

        def process_one(s):
            return re.sub(Regex, replacer, s)

        # Handle ComfyUI batching
        if isinstance(String, list):
            return ([process_one(s) for s in String],)
        else:
            return (process_one(String),)

class AMTMultiConditionRegexReplace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "String": ("STRING", {"default": ""}),
                "Regex": ("STRING", {"default": ""}),
                "ReplaceWith": ("STRING", {"default": ""}),
            },
            "optional": {
                "Condition_1": ("BOOLEAN", {"default": True}),
                "Condition_2": ("BOOLEAN", {"default": True}),
                "Condition_3": ("BOOLEAN", {"default": True}),
                "Condition_4": ("BOOLEAN", {"default": True}),
                "Condition_5": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "replace"

    def replace(
        self,
        String,
        Regex,
        ReplaceWith,
        Condition_1,
        Condition_2,
        Condition_3,
        Condition_4,
        Condition_5,
    ):
        conditions = [
            c for c in [
                Condition_1,
                Condition_2,
                Condition_3,
                Condition_4,
                Condition_5,
            ]
        ]

        all_true = all(conditions) if conditions else False

        def process_one(s):
            if not all_true:
                return s
            return re.sub(Regex, ReplaceWith, s)

        if isinstance(String, list):
            return ([process_one(s) for s in String],)
        else:
            return (process_one(String),)