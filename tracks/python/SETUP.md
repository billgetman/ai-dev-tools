# Python Track Setup

## Requirements

- Python 3.10+
- Deepgram API key
- ~500MB disk for dependencies and test data

## Install

```bash
cd tracks/python
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install deepgram-sdk pandas numpy python-Levenshtein pytest pytest-asyncio httpx aiosqlite
```

Optional for visualization:
```bash
pip install matplotlib plotly dash prometheus-client
```

## Deepgram API Key

1. Sign up at [console.deepgram.com/signup](https://console.deepgram.com/signup) (free tier: $200 credit)
2. Create API key
3. Create `.env` file:
```bash
DEEPGRAM_API_KEY=your_api_key_here
```
4. Add `.env` to `.gitignore`

Test:
```python
from deepgram import DeepgramClient
import os

api_key = os.getenv("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(api_key)
response = deepgram.listen.prerecorded.v("1").transcribe_url(
    {"url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"}
)
print(response["results"]["channels"][0]["alternatives"][0]["transcript"])
```

## Test Data

### Audio Files

Use Deepgram's sample files:
```python
SAMPLE_URLS = [
    "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav",
    "https://static.deepgram.com/examples/nasa-spacewalk-interview.wav"
]
```

Or place your own in `tracks/python/test_data/audio/` (WAV, MP3, FLAC, OGG).

### Ground Truth Transcripts

Create `tracks/python/test_data/ground_truth.json`:
```json
[
  {
    "audio_url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav",
    "transcript": "Yeah. Life moves pretty fast. If you don't stop and look around once in a while, you could miss it.",
    "duration_seconds": 6.5
  }
]
```

## Directory Structure

```
tracks/python/
├── .env
├── venv/
├── test_data/
│   └── ground_truth.json
├── greenfield/
│   └── python_greenfield.md
└── brownfield/
    ├── python_brownfield.md
    └── benchmark_nightmare.py  # Create before demo
```

## Create Brownfield Starting Code

Before demo, create `benchmark_nightmare.py` with the terrible code described in `brownfield/python_brownfield.md`. This is the 1000-line mess participants will refactor.
