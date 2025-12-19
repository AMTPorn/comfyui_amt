from .text_utils import AMTStringDeduplication, AMTReplaceAndMaybeDropString, AMTMultiConditionRegexReplace, AMTCountTagsInDirectory, AMTEmbedTagFrequencySafetensors

NODE_CLASS_MAPPINGS = {
    "AMTStringDeduplication": AMTStringDeduplication,
    "AMTReplaceAndMaybeDropString": AMTReplaceAndMaybeDropString,
    "AMTMultiConditionRegexReplace": AMTMultiConditionRegexReplace,
    "AMTCountTagsInDirectory": AMTCountTagsInDirectory,
    "AMTEmbedTagFrequencySafetensors": AMTEmbedTagFrequencySafetensors,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AMTStringDeduplication": "String Deduplication",
    "AMTReplaceAndMaybeDropString": "Replace and Maybe Drop String",
    "AMTMultiConditionRegexReplace": "Multi Condition Regex Replace",
    "AMTCountTagsInDirectory": "Count Tags in directory",
    "AMTEmbedTagFrequencySafetensors": "Embed tags information in safetensors",
}