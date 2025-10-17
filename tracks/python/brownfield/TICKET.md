# TICKET: Refactor Deepgram Benchmark Tool

**ID**: PERF-5621
**Priority**: Critical
**File**: `brownfield/benchmark_nightmare.py`

## Context

Jupyter notebook converted to Python script by intern. Has been calculating wrong metrics in production for months. Takes 10 minutes to process 100 files. Should take 30 seconds.

## Current Issues

1. **Three broken WER implementations** - All calculate different wrong values
2. **Global variables everywhere** - 20+ globals modified throughout
3. **Synchronous processing** - Processing files one by one
4. **Pandas abuse** - Using iterrows, at[], copying DataFrames repeatedly
5. **No real API calls** - Using simulated responses

## Quick Analysis

```python
# Current WER calculation (WRONG):
def calculate_wer_broken(reference, hypothesis):
    ref_words = reference.split(' ')
    hyp_words = hypothesis.split(' ')
    diff_count = 0
    for i in range(min(len(ref_words), len(hyp_words))):
        if ref_words[i] != hyp_words[i]:
            diff_count += 1
    return diff_count / len(ref_words) * 100

# Should use Levenshtein distance:
# WER = (S + D + I) / N
# where S=substitutions, D=deletions, I=insertions, N=reference length
```

## Requirements

1. **Fix WER calculation** - Use proper Levenshtein distance (jiwer library or implement correctly)

2. **Add async processing** - Use asyncio/httpx for concurrent API calls

3. **Remove globals** - Use classes or proper function parameters

4. **Optimize pandas** - Vectorized operations, no iterrows

5. **Real Deepgram integration** - Actually call the API

## Key Refactoring Tasks

- Replace 3 broken WER functions with one correct implementation
- Convert `process_audio_file_sync` → `async process_audio_file`
- Replace globals with a `BenchmarkSession` class
- Use `pandas.apply()` instead of `iterrows()`
- Batch API calls with `asyncio.gather()`
- Add proper error handling and retries
- Remove redundant DataFrame copies

## Performance Targets

- 100 files in < 30 seconds (from 10 minutes)
- Memory usage < 100MB (from 500MB+)
- Accurate WER calculation (± 0.1% of ground truth)

## Definition of Done

- [ ] One correct WER implementation using Levenshtein
- [ ] Async processing with concurrency limit
- [ ] No global variables
- [ ] Vectorized pandas operations
- [ ] Real Deepgram API calls
- [ ] 20x performance improvement

## Hints

- `jiwer.wer()` or implement edit distance with dynamic programming
- `async with httpx.AsyncClient() as client:`
- `df['wer'] = df.apply(lambda row: calculate_wer(row['ref'], row['hyp']), axis=1)`
- `asyncio.gather(*[process(url) for url in urls])`
- Use `deepgram-sdk` properly with async context managers

---

*The intern who wrote this is now a senior engineer. The code remains.*