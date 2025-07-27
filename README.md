# Create subtitles

Creates subtitles for audio using open AI or faster whisper models. Users can choose the models and other parameters based on the quality they are looking for.

Requirements:

    Python 3.13

    numpy >= 1.20, < 2.0

    srt

    faster-whisper

Setup:

```
python3.13 -m venv myenv

source myenv/bin/activate

pip install -r requirements.txt

python UI.py

```