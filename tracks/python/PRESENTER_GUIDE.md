# Python Track Presenter Guide

Target time: 20-25 minutes

## Part 1: Greenfield (10-12 min)

### Phase 1: Basic Wrapper (0-3 min)

Prompt AI:
```
Create a Python wrapper around the Deepgram SDK that logs all API calls to SQLite.
Track: timestamp, model, duration, latency, response code, cost.
Use asyncio. Store in 'monitoring.db'.
```

Context: `greenfield/python_greenfield.md`, SETUP.md, .env setup

Expected: `greenfield/deepgram_monitor.py` with DeepgramMonitor class, SQLite schema, async transcription method.

Test:
```python
from deepgram_monitor import DeepgramMonitor

monitor = DeepgramMonitor()
result = await monitor.transcribe_url("https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav")
```

### Phase 2: WER Calculation (3-6 min)

Prompt AI:
```
Add WER calculation. Load ground truth from test_data/ground_truth.json.
Calculate WER using Levenshtein distance. Handle text normalization (lowercase, punctuation).
Store WER in database.
```

Context: Current code, test_data structure, WER = (insertions + deletions + substitutions) / total_words

Expected: `calculate_wer()` function, text normalization, updated schema.

### Phase 3: Multi-Model Comparison (6-9 min)

Prompt AI:
```
Add compare_models() function. Transcribe same audio with multiple models (nova-2, nova-3, base).
Run in parallel with asyncio.gather. Return comparison showing latency, cost, WER for each.
```

Context: Current code, Deepgram model docs

Expected: `compare_models()` async function, parallel execution, comparison output.

### Phase 4: Quick Dashboard (9-12 min)

Prompt AI:
```
Add generate_report() that reads monitoring database and creates summary:
average WER by model, latency percentiles, total cost. Export to JSON or print table.
```

Expected: Report generation function, summary statistics.

## Part 2: Brownfield (10-13 min)

### Phase 1: Understand & Extract (0-3 min)

Prompt AI:
```
Analyze brownfield/benchmark_nightmare.py. What does it calculate? What's broken?
Extract and fix the WER calculation. Create clean wer_calculator.py module with proper
Levenshtein distance. Handle text normalization.
```

Context: `benchmark_nightmare.py`, brownfield spec

Expected: `wer_calculator.py` with correct WER implementation.

Verify:
```python
assert calculate_wer("hello world", "hello world") == 0.0
assert calculate_wer("hello world", "hello earth") == 0.5
```

### Phase 2: Vectorize (3-6 min)

Prompt AI:
```
Refactor benchmark_nightmare.py to be fast. Remove redundant dataframe copies.
Vectorize operations instead of loops with .iloc. Create clean benchmark.py.
```

Context: `benchmark_nightmare.py`, `wer_calculator.py`

Expected: `benchmark.py`, vectorized pandas operations, no redundant copies.

Performance test:
```python
%timeit old_benchmark(results_df)  # ~10 seconds
%timeit new_benchmark(results_df)  # ~0.1 seconds
```

### Phase 3: Add Async (6-10 min)

Prompt AI:
```
Add async batch processing to benchmark.py. Process multiple audio files through Deepgram
in parallel with rate limiting (max 10 concurrent). Show progress.
```

Expected: Async batch function, rate limiting with semaphore, progress tracking.

### Phase 4: Real-time Streaming (10-13 min)

Prompt AI:
```
Add streaming mode. Evaluate transcriptions as they stream in via WebSocket.
Calculate WER on partial results. Live updates.
```

Expected: Streaming evaluation function, WebSocket integration, partial WER calculation.

## Context Layering

Give AI information incrementally:
1. Start: Challenge spec only
2. Add: Previous code files as created
3. Provide: Docs links when needed
4. Show: Sample data structures

Don't give everything at once.

## Common Issues

**API Rate Limiting**: Reduce concurrent requests, add exponential backoff
**WER > 1.0**: Check text normalization, verify with known examples
**Slow generation**: Break into smaller pieces, ask for specific functions first

## Success Criteria

Greenfield:
- [ ] API wrapper logging to SQLite
- [ ] Accurate WER calculation
- [ ] Multi-model comparison working
- [ ] Basic metrics reporting

Brownfield:
- [ ] Clean WER extraction
- [ ] 100x+ performance improvement proven
- [ ] Async batch processing working
- [ ] Streaming mode functional

Done in ~20-25 minutes.
