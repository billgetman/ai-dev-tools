#!/usr/bin/env python3
"""
Reference implementations for correct WER calculation and async processing.
This shows the RIGHT way to do things (vs the brownfield code).
"""

import asyncio
import time

# Note: Real implementation would use pandas and numpy
# This is simplified to avoid dependencies


def calculate_wer_correct(reference: str, hypothesis: str) -> float:
    """
    Calculate Word Error Rate using Levenshtein distance.

    WER = (Substitutions + Deletions + Insertions) / Total Words in Reference

    This is a simplified implementation. For production, use the jiwer library.
    """
    ref_words = reference.lower().split()
    hyp_words = hypothesis.lower().split()

    # Dynamic programming for Levenshtein distance
    # Create 2D array for dynamic programming
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]

    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i-1] == hyp_words[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion = d[i][j-1] + 1
                deletion = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    wer = d[len(ref_words)][len(hyp_words)] / max(len(ref_words), 1)
    return wer * 100  # Return as percentage


# Example showing the difference
def demonstrate_wer_calculation():
    """Show why the brownfield calculation is wrong."""

    reference = "the quick brown fox"
    hypothesis = "a quick brown foxes"

    # Wrong way (from brownfield code)
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    wrong_wer = sum(1 for r, h in zip(ref_words, hyp_words) if r != h) / len(ref_words) * 100

    # Right way
    correct_wer = calculate_wer_correct(reference, hypothesis)

    print(f"Reference: '{reference}'")
    print(f"Hypothesis: '{hypothesis}'")
    print(f"Wrong WER (position-based): {wrong_wer:.1f}%")
    print(f"Correct WER (Levenshtein): {correct_wer:.1f}%")
    print(f"Actual errors: 1 substitution ('the'→'a'), 1 substitution ('fox'→'foxes')")


# Async example (simplified)
async def process_audio_file_async(url: str, client=None) -> dict:
    """Example of async processing for API calls."""
    # Simulate API call with sleep
    await asyncio.sleep(0.1)  # In reality, this would be an API call

    return {
        "url": url,
        "transcript": "Sample transcript",
        "duration": 10.5
    }


async def process_batch_async(urls: list) -> list:
    """Process multiple URLs concurrently."""
    # Create tasks for all URLs
    tasks = [process_audio_file_async(url) for url in urls]

    # Process concurrently with gather
    results = await asyncio.gather(*tasks)

    return results


# Pandas vectorization example (conceptual)
def demonstrate_pandas_concept():
    """Show the concept of efficient pandas operations."""

    print("\nPandas Anti-patterns (conceptual):")
    print("SLOW (iterrows):")
    print("  for index, row in df.iterrows():")
    print("      df.at[index, 'wer'] = calculate_wer(row['ref'], row['hyp'])")
    print("")
    print("FAST (vectorized):")
    print("  df['wer'] = df.apply(lambda row: calculate_wer(row['ref'], row['hyp']), axis=1)")
    print("")
    print("Performance difference: ~10-100x faster with vectorization")


if __name__ == "__main__":
    print("=== WER Calculation Demo ===")
    demonstrate_wer_calculation()

    print("\n=== Async Processing Demo ===")
    urls = [f"http://example.com/audio{i}.wav" for i in range(10)]

    # Run async example
    results = asyncio.run(process_batch_async(urls))
    print(f"Processed {len(results)} files concurrently")

    print("\n=== Pandas Vectorization Concepts ===")
    demonstrate_pandas_concept()