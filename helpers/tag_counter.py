import os
import json
from collections import defaultdict

from safetensors import safe_open
from safetensors.torch import save_file
import torch


def parse_tags_from_line(line):
    return [tag.strip() for tag in line.split(",") if tag.strip()]


def count_tags_in_directory(directory):
    tag_freq = defaultdict(int)

    for filename in os.listdir(directory):
        if filename.lower().endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        for tag in parse_tags_from_line(line):
                            tag_freq[tag] += 1
            except Exception as e:
                print(f"[AMT] Skipping {filepath}: {e}")

    return dict(tag_freq)


def build_tag_frequency_tree(root_dir):
    all_tag_data = {}

    def is_hidden(path):
        return os.path.basename(path).startswith(".")

    if any(
        f.lower().endswith(".txt")
        for f in os.listdir(root_dir)
        if os.path.isfile(os.path.join(root_dir, f))
    ):
        all_tag_data["__ROOT__"] = count_tags_in_directory(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.normpath(dirpath) == os.path.normpath(root_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            continue

        if is_hidden(dirpath):
            continue

        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        if any(f.lower().endswith(".txt") for f in filenames):
            all_tag_data[os.path.basename(dirpath)] = count_tags_in_directory(dirpath)

    total_freq = defaultdict(int)
    ss_tag_frequency = {}

    for key, freq in all_tag_data.items():
        if key != "__ROOT__":
            ss_tag_frequency[key] = freq
        for tag, count in freq.items():
            total_freq[tag] += count

    ss_tag_frequency["total"] = dict(total_freq)
    return ss_tag_frequency


def embed_tag_frequency_in_safetensors(
    safetensors_path,
    tag_freq_dict,
    output_path=None,
):
    if output_path is None:
        output_path = safetensors_path

    with safe_open(safetensors_path, framework="pt", device="cpu") as f:
        metadata = f.metadata() or {}
        tensors = {key: f.get_tensor(key) for key in f.keys()}

    metadata["ss_tag_frequency"] = json.dumps(
        tag_freq_dict, ensure_ascii=False
    )

    save_file(tensors, output_path, metadata=metadata)