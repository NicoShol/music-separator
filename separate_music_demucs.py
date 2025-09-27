import argparse

import librosa
import torchaudio
import torch
from demucs.apply import apply_model
from demucs.pretrained import get_model
import os


def separate_music(input_file: str, output_dir: str):
    """
    Separates a music file into its components using Demucs.
    """
    model = get_model(name="htdemucs")
    wav, sr = librosa.load(input_file, sr=None, mono=False)
    wav = torch.from_numpy(wav)
    ref = wav.mean(0)
    wav = (wav - ref.mean()) / ref.std()
    sources = apply_model(model, wav[None], device="cpu", progress=True, num_workers=0)[
        0
    ]
    sources = sources * ref.std() + ref.mean()

    output_full_path = output_dir + "/" + os.path.splitext(os.path.basename(input_file))[0] + "/"
    if not os.path.exists(output_full_path):
        os.makedirs(output_full_path)

    for source_idx, source in enumerate(sources):
        stem_name = model.sources[source_idx]
        output_path = os.path.join(output_full_path, f"{stem_name}.wav")
        torchaudio.save(output_path, source.cpu(), sr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Separate music into components")
    parser.add_argument("input_file", type=str, help="Path to the input music file")
    parser.add_argument(
        "output_dir", type=str, help="Directory to save separated tracks"
    )
    args = parser.parse_args()

    separate_music(args.input_file, args.output_dir)
