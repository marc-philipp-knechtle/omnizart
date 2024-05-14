import os
from typing import Optional
from tqdm import tqdm

import click

from omnizart.cli import silence_tensorflow
from omnizart.cli.common_options import add_common_options, COMMON_TRANSCRIBE_OPTIONS
from omnizart.utils import LazyLoader

vocal = LazyLoader("vocal", globals(), "omnizart.vocal")


@click.command()
@add_common_options(COMMON_TRANSCRIBE_OPTIONS)
def transcribe(input_audio: Optional[str] = None, model_path: Optional[str] = None, output: str = "./",
               input_directory: Optional[str] = None):
    """Transcribe a single audio or complete directory and output as a MIDI file.

    This will output a MIDI file with the same name as the given audio, except the
    extension will be replaced with '.mid'.
    """
    silence_tensorflow()
    if input_directory is not None:
        files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
        for file in tqdm(files):
            file_path = os.path.join(input_directory, file)
            vocal.app.transcribe(file_path, model_path, output=output)
            os.remove(file_path)
    elif input_audio is not None:
        vocal.app.transcribe(input_audio, model_path, output=output)
    else:
        raise RuntimeError("Either input audio or input directory has to be specified")
