from .text_utils import AMTStringDeduplication, AMTReplaceAndMaybeDropString, AMTMultiConditionRegexReplace

NODE_CLASS_MAPPINGS = {
    "AMTStringDeduplication": AMTStringDeduplication,
    "AMTReplaceAndMaybeDropString": AMTReplaceAndMaybeDropString,
    "AMTMultiConditionRegexReplace": AMTMultiConditionRegexReplace,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AMTStringDeduplication": "String Deduplication",
    "AMTReplaceAndMaybeDropString": "Replace and Maybe Drop String",
    "AMTMultiConditionRegexReplace": "Multi Condition Regex Replace"
}