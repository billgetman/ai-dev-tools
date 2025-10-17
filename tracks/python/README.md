# Python Track: Deepgram QA & Observability

## Track Structure

Build a quality assurance platform for Deepgram's speech-to-text API:

1. **Greenfield: "The Deepgram Observatory"** - Monitoring and testing framework from scratch
2. **Brownfield: "The Benchmark Nightmare"** - Refactor a terrible benchmarking tool

Connection: Greenfield builds the infrastructure, brownfield refactors the analysis tool that plugs into it.

## Challenges

**Greenfield**
Phase 1 → Basic API wrapper logging to SQLite
Phase 2 → Add WER calculation and metrics
Phase 3 → Multi-model A/B testing
Phase 4 → Distributed monitoring with dashboards

**Brownfield**
Phase 1 → Understand and extract WER logic
Phase 2 → Vectorize and optimize (100x speedup target)
Phase 3 → Add async processing
Phase 4 → Real-time streaming mode

## Prerequisites

- Python 3.10+
- Deepgram API key
- Basic audio files for testing
- Ground truth transcripts

See [SETUP.md](./SETUP.md) for installation.

## Target Time

20-25 minutes total with AI assistance (hours without).

## Success Criteria

- API calls logged with latency and cost metrics
- WER calculated correctly (matches known benchmarks)
- Multi-model comparison working
- Benchmark tool processes 1000 files in seconds
- Real-time dashboard shows streaming metrics

## Performance & Correctness Notes

### WER Calculation Problem

The brownfield code calculates WER incorrectly:

```python
# WRONG (current code):
def calculate_wer_broken(reference, hypothesis):
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    diff_count = sum(1 for r, h in zip(ref_words, hyp_words) if r != h)
    return diff_count / len(ref_words) * 100

# Example: "the cat sat" vs "a cat sits"
# Wrong method: 2/3 = 66.7% (just counts different positions)
# Correct WER: 2/3 = 66.7% (1 substitution, 1 substitution, via Levenshtein)
```

Correct WER uses Levenshtein distance: `WER = (S + D + I) / N`
- S = substitutions, D = deletions, I = insertions, N = reference word count

### Sync vs Async Performance

Current code processes files sequentially:
```python
# SLOW (10 minutes for 100 files):
for url in urls:
    result = process_audio_file_sync(url)  # Blocks for ~6 seconds each

# FAST (30 seconds for 100 files):
async def process_all():
    tasks = [process_audio_file(url) for url in urls]
    return await asyncio.gather(*tasks)  # Process concurrently
```

### Pandas Anti-patterns

```python
# SLOW (iterrows):
for index, row in df.iterrows():
    df.at[index, 'wer'] = calculate_wer(row['ref'], row['hyp'])

# FAST (vectorized):
df['wer'] = df.apply(lambda row: calculate_wer(row['ref'], row['hyp']), axis=1)

# Or even better with numpy for numeric operations:
df['normalized'] = df['value'].values / df['value'].max()
```

### Performance Impact

- 10 files: ~60 seconds (sync) vs ~6 seconds (async)
- 100 files: ~600 seconds (sync) vs ~30 seconds (async)
- 1000 files: ~6000 seconds (sync) vs ~120 seconds (async with rate limiting)

See `test_data/wer_reference.py` for correct implementations.
