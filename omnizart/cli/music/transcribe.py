# pylint: disable=C0303,W1401

from functools import partial

import click

from omnizart.music import app

click.option = partial(click.option, show_default=True)


@click.command()
@click.argument("input_audio", type=click.Path(exists=True))
@click.option(
    "-m",
    "--model-path",
    help="Path to the pre-trained model for transcription",
    type=click.Path(exists=True),
)
@click.option("-o", "--output", help="Path to output the MIDI file", default="./", type=click.Path(writable=True))
def transcribe(input_audio, model_path, output):
    """Transcribe a single audio and output as a MIDI file.

    This will output a MIDI file with the same name as the given audio, except the
    extension will be replaced with '.mid'.

    \b
    Example Usage
    $ omnizart music transcribe \ 
        example.wav \ 
        --model-path path/to/model \ 
        --output example.mid
    """
    app.transcribe(input_audio, model_path, output=output)


def process_doc():
    # Some dirty work for preserving and converting the docstring inside the decorated
    # function into .rst format.
    doc = transcribe.__doc__
    doc = doc.replace("\b", "").replace("    ", "").replace("--", "        --")

    code_block = "\n.. code-block:: bash\n\n"
    doc = doc.replace("$", f"{code_block}    $")

    return doc


__doc__ = process_doc()