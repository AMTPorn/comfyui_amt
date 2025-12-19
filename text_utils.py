import os
import sys
import re
import random
from pathlib import Path
from .helpers.tag_counter import (
    build_tag_frequency_tree,
    embed_tag_frequency_in_safetensors,
)
from .helpers.windows_linux import (
    normalize_path,
)
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
            "Seed": ("INT", {"default": 0}),
        }
    }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "replace"

    def replace(self, String, Regex, ReplaceWith, DropChance, Seed):
        # Clamp drop chance just in case
        drop_chance = max(0, min(100, DropChance))

        # Local RNG derived from seed
        rng = random.Random(Seed)

        def replacer(match):
            roll = rng.randint(1, 100)
            if roll <= drop_chance:
                return ""
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
                "Logic": ("STRING", {"default": "AND", "choices": ["AND", "OR"]}),
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
        Logic,
        Condition_1,
        Condition_2,
        Condition_3,
        Condition_4,
        Condition_5,
    ):
        conditions = [
            Condition_1,
            Condition_2,
            Condition_3,
            Condition_4,
            Condition_5,
        ]

        # Determine if replacement should occur
        if Logic == "AND":
            do_replace = all(conditions) if conditions else False
        elif Logic == "OR":
            do_replace = any(conditions) if conditions else False
        else:
            do_replace = False  # fallback safe

        def process_one(s):
            if not do_replace:
                return s
            return re.sub(Regex, ReplaceWith, s)

        if isinstance(String, list):
            return ([process_one(s) for s in String],)
        else:
            return (process_one(String),)

class AMTCountTagsInDirectory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "DirectoryPath": ("STRING", {"default": ""}),
                "Trigger": ("ANY", {"default": None}),  # any upstream value forces execution
                "Seed": ("INT", {"default": 0}),  # dummy input to force execution
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TagSummary",)
    FUNCTION = "count"
    OUTPUT_NODE = True

    def count(self, DirectoryPath, Trigger, Seed):
        DirectoryPath = normalize_path(DirectoryPath)

        if not os.path.isdir(DirectoryPath):
            return ("❌ Invalid directory path",)

        tag_tree = build_tag_frequency_tree(DirectoryPath)
        total = tag_tree.get("total", {})

        if not total:
            return ("⚠️ No tags found",)

        total_tags = sum(total.values())
        unique_tags = len(total)

        sorted_tags = sorted(
            total.items(), key=lambda x: x[1], reverse=True
        )

        lines = [
            f"📊 Total tags: {total_tags}",
            f"🏷 Unique tags: {unique_tags}",
            "",
            "All tags (sorted by frequency):",
        ]

        for tag, count in sorted_tags:
            lines.append(f"{tag}: {count}")

        text = "\n".join(lines)

        return (text,)

class AMTEmbedTagFrequencySafetensors:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SafetensorsPath": ("STRING", {"default": ""}),
                "CaptionDirectory": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OutputSafetensors",)
    FUNCTION = "embed"
    OUTPUT_NODE = True

    def embed(self, SafetensorsPath, CaptionDirectory):
        SafetensorsPath = normalize_path(SafetensorsPath)
        CaptionDirectory = normalize_path(CaptionDirectory)

        if not os.path.isfile(SafetensorsPath):
            return ("❌ Safetensors file not found",)

        if not os.path.isdir(CaptionDirectory):
            return ("❌ Caption directory not found",)

        output_path = SafetensorsPath

        embed_tag_frequency_in_safetensors(
            safetensors_path=SafetensorsPath,
            tag_freq_dict=build_tag_frequency_tree(CaptionDirectory),
            output_path=output_path,
        )

        return (output_path,)