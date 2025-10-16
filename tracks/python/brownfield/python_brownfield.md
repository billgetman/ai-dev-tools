Brownfield: "The Benchmark Nightmare"
1000-line Jupyter notebook converted to .py for evaluating Deepgram models

```python
# Actual nightmare fuel:
import pandas as pd
import json
from deepgram import Deepgram

# Load test results
results_nova2 = pd.read_json('nova2_results.json')
results_nova3 = pd.read_json('nova3_results.json')
results_nova2_copy = results_nova2.copy()
results_backup = results_nova3.copy()
results_final = results_nova2.copy()
results_final_v2 = results_nova3.copy()

# Calculate WER (incorrectly implemented)
for i in range(len(results_nova2)):
    reference = results_nova2.iloc[i]['ground_truth']
    hypothesis = results_nova2.iloc[i]['transcript']
    # ... 50 lines of buggy string comparison
    # Doesn't handle case sensitivity, punctuation, or calculate proper WER

# Synchronous API calls blocking everything
for audio_file in audio_files:
    result = dg.transcription.sync_prerecorded(...)  # Blocks for seconds
    # ... more processing

# 800 more lines of:
# - Redundant dataframe operations
# - Nested loops where vectorization would work
# - No error handling whatsoever
# - Hardcoded file paths everywhere
# - Memory leaks with large files
```

**Phase 1: Understand and extract**
- Decode the WER calculation logic
- Identify bugs
- Extract reusable comparison functions
- Proper Levenshtein distance implementation
- Text normalization (case, punctuation, numbers)

**Phase 2: Optimize**
- Vectorize pandas operations
- Remove redundant data copies
- Fix O(n²) string comparisons
- Target: 100x speedup

**Phase 3: Add async processing**
- Test 1000 audio files in parallel
- Rate limiting and backpressure handling
- Progress tracking

**Phase 4: Real-time streaming**
- Evaluate transcriptions as they stream in
- Calculate WER on partial results
- Live dashboard updates