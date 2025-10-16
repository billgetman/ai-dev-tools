#!/usr/bin/env python3
"""
DEEPGRAM BENCHMARK TOOL v1.0 - DO NOT MODIFY - WORKS PERFECTLY
Last updated: 2023 by intern
Note: Converted from Jupyter notebook benchmark_analysis_FINAL_v2_ACTUALLY_FINAL.ipynb
"""

import pandas as pd
import numpy as np
import json
import time
import os
import sys
from deepgram import DeepgramClient, PrerecordedOptions
import requests
from datetime import datetime
import random
import copy

# GLOBAL VARIABLES - DO NOT CHANGE
RESULTS_NOVA2 = None
RESULTS_NOVA3 = None
RESULTS_NOVA2_COPY = None
RESULTS_NOVA3_COPY = None
RESULTS_BACKUP = None
RESULTS_FINAL = None
RESULTS_FINAL_V2 = None
RESULTS_TEMP = None
TEMP_DF = None
TEMP_DF2 = None
WORKING_DF = None
ALL_RESULTS = []
ERROR_COUNT = 0
SUCCESS_COUNT = 0
TOTAL_COUNT = 0
WER_SCORES = []
WER_SCORES_BACKUP = []
API_KEY = os.getenv("DEEPGRAM_API_KEY", "test_key_123")

# Constants that aren't really constant
MAX_RETRIES = 3  # but we actually retry 5 times
TIMEOUT = 30  # seconds but we ignore this
BATCH_SIZE = 10  # but we process one at a time anyway

def load_test_data():
    """Load test data from multiple sources with no error handling."""
    global RESULTS_NOVA2, RESULTS_NOVA3, RESULTS_NOVA2_COPY, RESULTS_BACKUP, RESULTS_FINAL

    try:
        # Try to load from files that might not exist
        RESULTS_NOVA2 = pd.read_json('../test_data/nova2_results.json')
    except:
        # Create fake data if file doesn't exist
        RESULTS_NOVA2 = pd.DataFrame({
            'id': ['test_' + str(i) for i in range(100)],
            'transcript': ['This is test transcript number ' + str(i) for i in range(100)],
            'ground_truth': ['This is test transcript number ' + str(i) for i in range(100)],
            'model': ['nova-2'] * 100,
            'wer': [0.0] * 100,
            'duration': [random.random() * 10 for _ in range(100)],
            'timestamp': [datetime.now().isoformat()] * 100
        })

    # Make multiple copies for no reason
    RESULTS_NOVA2_COPY = RESULTS_NOVA2.copy()
    RESULTS_BACKUP = RESULTS_NOVA2.copy()
    RESULTS_FINAL = RESULTS_NOVA2.copy()

    # Create Nova3 data by copying Nova2 and changing model name
    RESULTS_NOVA3 = RESULTS_NOVA2.copy()
    for i in range(len(RESULTS_NOVA3)):
        RESULTS_NOVA3.iloc[i]['model'] = 'nova-3'  # Inefficient row-by-row update

    print(f"Loaded {len(RESULTS_NOVA2)} Nova2 results")
    print(f"Loaded {len(RESULTS_NOVA3)} Nova3 results")
    print(f"Total memory usage: {sys.getsizeof(RESULTS_NOVA2) * 5} bytes")  # Wrong calculation

def calculate_wer_broken(reference, hypothesis):
    """
    Calculate WER incorrectly - just counts different words.
    This is completely wrong but we use it everywhere.
    """

    # Convert to strings in case they're not
    ref_str = str(reference)
    hyp_str = str(hypothesis)

    # Don't handle case or punctuation properly
    ref_words = ref_str.split(' ')
    hyp_words = hyp_str.split(' ')

    # Just count how many words are different (completely wrong WER calculation)
    diff_count = 0
    for i in range(min(len(ref_words), len(hyp_words))):
        if ref_words[i] != hyp_words[i]:
            diff_count += 1

    # Add extra words (also wrong)
    diff_count += abs(len(ref_words) - len(hyp_words))

    # Calculate WER (incorrectly)
    if len(ref_words) == 0:
        return 100.0  # Should return 0 or handle edge case

    wer = diff_count / len(ref_words)
    return wer * 100  # Return as percentage inconsistently

def calculate_wer_also_broken(ref, hyp):
    """Another broken WER calculation that's slightly different."""
    # Duplicate implementation with small differences
    words1 = ref.lower().split()  # This one handles case!
    words2 = hyp.split()  # But inconsistently

    errors = 0
    for w1, w2 in zip(words1, words2):
        if w1 != w2:
            errors = errors + 1  # Could just use +=

    return errors / max(len(words1), 1)  # Different denominator

def calculate_wer_third_version(reference_text, hypothesis_text):
    """Yet another WER implementation because why not."""
    # This one strips punctuation but only some of it
    import string
    ref = reference_text.replace(',', '').replace('.', '')
    hyp = hypothesis_text  # Forgot to strip punctuation from hypothesis

    ref_tokens = ref.split()
    hyp_tokens = hyp.split()

    # Use set difference (completely wrong for WER)
    ref_set = set(ref_tokens)
    hyp_set = set(hyp_tokens)
    diff = ref_set.symmetric_difference(hyp_set)

    return len(diff) / len(ref_set) if ref_set else 0

def process_audio_file_sync(audio_url, model="nova-2"):
    """Process audio file synchronously, blocking everything."""
    global ERROR_COUNT, SUCCESS_COUNT, TOTAL_COUNT

    TOTAL_COUNT = TOTAL_COUNT + 1

    print(f"Processing file {TOTAL_COUNT}: {audio_url}")

    # Create client every time instead of reusing
    client = DeepgramClient(API_KEY)

    # Retry logic that doesn't work properly
    for retry in range(5):  # Said 3 retries but do 5
        try:
            # Make synchronous call
            time.sleep(random.random())  # Random delay for no reason

            options = PrerecordedOptions(
                model=model,
                smart_format=True,  # Random options
                utterances=True,
                punctuate=True,
                profanity_filter=False
            )

            # This would actually need to be async but we're calling it sync
            # Just simulate a response
            start_time = time.time()

            # Simulate API call with random success
            if random.random() > 0.1:  # 90% success rate
                response = {
                    "results": {
                        "channels": [{
                            "alternatives": [{
                                "transcript": f"Sample transcript for {audio_url}",
                                "confidence": random.random(),
                                "words": []
                            }]
                        }]
                    }
                }
                end_time = time.time()

                SUCCESS_COUNT += 1

                # Extract transcript in the most convoluted way
                transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]

                # Calculate metrics
                latency = end_time - start_time

                # Store in multiple places
                result = {
                    "url": audio_url,
                    "model": model,
                    "transcript": transcript,
                    "latency": latency,
                    "timestamp": datetime.now().isoformat(),
                    "retry_count": retry,
                    "success": True
                }

                ALL_RESULTS.append(result)

                # Also store in dataframe (duplicate storage)
                new_row = pd.DataFrame([result])
                global RESULTS_FINAL
                RESULTS_FINAL = pd.concat([RESULTS_FINAL, new_row], ignore_index=True)

                return result

            else:
                raise Exception("Random failure")

        except Exception as e:
            print(f"Error on retry {retry}: {e}")
            ERROR_COUNT = ERROR_COUNT + 1
            time.sleep(retry * 2)  # Exponential backoff but wrong

    # If all retries failed
    return {"error": "Failed after 5 retries", "url": audio_url}

def batch_process_files_inefficiently(audio_urls, model="nova-2"):
    """Process multiple files one by one instead of in parallel."""
    results = []

    print(f"Starting batch processing of {len(audio_urls)} files...")
    print(f"Estimated time: {len(audio_urls) * 5} seconds")  # Wrong estimate

    # Process sequentially
    for i, url in enumerate(audio_urls):
        print(f"\n{'='*50}")
        print(f"Processing {i+1}/{len(audio_urls)}")
        print(f"{'='*50}\n")

        result = process_audio_file_sync(url, model)
        results.append(result)

        # Update global dataframes unnecessarily
        update_all_dataframes()

        # Save intermediate results repeatedly
        save_results_multiple_times()

    return results

def update_all_dataframes():
    """Update all global dataframes redundantly."""
    global RESULTS_NOVA2, RESULTS_NOVA3, RESULTS_NOVA2_COPY, RESULTS_BACKUP

    # Copy data around for no reason
    RESULTS_NOVA2_COPY = RESULTS_NOVA2.copy()
    RESULTS_BACKUP = pd.concat([RESULTS_NOVA2, RESULTS_NOVA3])

    # Sort multiple times
    RESULTS_NOVA2 = RESULTS_NOVA2.sort_values('timestamp')
    RESULTS_NOVA2 = RESULTS_NOVA2.sort_values('model')
    RESULTS_NOVA2 = RESULTS_NOVA2.sort_values('timestamp')  # Sort again?

def save_results_multiple_times():
    """Save results to multiple formats redundantly."""
    global RESULTS_FINAL

    # Save as JSON
    RESULTS_FINAL.to_json('results_final.json')

    # Save as CSV
    RESULTS_FINAL.to_csv('results_final.csv')

    # Save as pickle
    RESULTS_FINAL.to_pickle('results_final.pkl')

    # Save backup
    RESULTS_FINAL.to_json('results_final_backup.json')

    # Save another backup
    RESULTS_FINAL.to_json('results_final_backup_v2.json')

def calculate_all_wer_scores():
    """Calculate WER scores using all three broken implementations."""
    global RESULTS_FINAL, WER_SCORES

    WER_SCORES = []

    # Use inefficient iterrows
    for index, row in RESULTS_FINAL.iterrows():
        transcript = row['transcript']
        ground_truth = row.get('ground_truth', transcript)  # Use transcript if no ground truth

        # Calculate WER three different ways
        wer1 = calculate_wer_broken(ground_truth, transcript)
        wer2 = calculate_wer_also_broken(ground_truth, transcript)
        wer3 = calculate_wer_third_version(ground_truth, transcript)

        # Average them (why?)
        avg_wer = (wer1 + wer2 + wer3) / 3

        WER_SCORES.append({
            'index': index,
            'wer_v1': wer1,
            'wer_v2': wer2,
            'wer_v3': wer3,
            'wer_avg': avg_wer
        })

        # Update the dataframe in place (inefficient)
        RESULTS_FINAL.at[index, 'wer_v1'] = wer1
        RESULTS_FINAL.at[index, 'wer_v2'] = wer2
        RESULTS_FINAL.at[index, 'wer_v3'] = wer3
        RESULTS_FINAL.at[index, 'wer_avg'] = avg_wer

def generate_comparison_report():
    """Generate a comparison report with tons of redundant calculations."""
    global RESULTS_NOVA2, RESULTS_NOVA3, RESULTS_FINAL

    print("\n" + "="*100)
    print("DEEPGRAM MODEL COMPARISON REPORT")
    print("="*100 + "\n")

    # Calculate the same metrics multiple times
    nova2_mean_wer = RESULTS_NOVA2['wer'].mean()
    nova2_avg_wer = sum(RESULTS_NOVA2['wer']) / len(RESULTS_NOVA2['wer'])  # Same as mean
    nova2_average = np.average(RESULTS_NOVA2['wer'])  # Also the same

    print(f"Nova-2 Mean WER: {nova2_mean_wer}")
    print(f"Nova-2 Avg WER: {nova2_avg_wer}")
    print(f"Nova-2 Average WER: {nova2_average}")

    # Do the same for Nova-3
    nova3_mean_wer = RESULTS_NOVA3['wer'].mean()
    nova3_avg_wer = sum(RESULTS_NOVA3['wer']) / len(RESULTS_NOVA3['wer'])
    nova3_average = np.average(RESULTS_NOVA3['wer'])

    print(f"\nNova-3 Mean WER: {nova3_mean_wer}")
    print(f"Nova-3 Avg WER: {nova3_avg_wer}")
    print(f"Nova-3 Average WER: {nova3_average}")

    # Calculate percentiles inefficiently
    print("\n" + "-"*50)
    print("PERCENTILES")
    print("-"*50)

    for p in [10, 25, 50, 75, 90, 95, 99]:
        nova2_p = np.percentile(RESULTS_NOVA2['wer'], p)
        nova3_p = np.percentile(RESULTS_NOVA3['wer'], p)
        print(f"P{p}: Nova-2={nova2_p:.2f}, Nova-3={nova3_p:.2f}")

    # Create comparison dataframe
    comparison = pd.DataFrame({
        'Metric': ['Mean', 'Median', 'Std', 'Min', 'Max'],
        'Nova-2': [
            RESULTS_NOVA2['wer'].mean(),
            RESULTS_NOVA2['wer'].median(),
            RESULTS_NOVA2['wer'].std(),
            RESULTS_NOVA2['wer'].min(),
            RESULTS_NOVA2['wer'].max()
        ],
        'Nova-3': [
            RESULTS_NOVA3['wer'].mean(),
            RESULTS_NOVA3['wer'].median(),
            RESULTS_NOVA3['wer'].std(),
            RESULTS_NOVA3['wer'].min(),
            RESULTS_NOVA3['wer'].max()
        ]
    })

    print("\n" + "-"*50)
    print("COMPARISON TABLE")
    print("-"*50)
    print(comparison)

    # Save comparison multiple times
    comparison.to_csv('comparison.csv')
    comparison.to_json('comparison.json')
    comparison.to_html('comparison.html')

def visualize_results_badly():
    """Create visualizations but don't actually show them."""
    try:
        import matplotlib.pyplot as plt

        # Create figure but don't show it
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))

        # Plot 1: WER distribution (but data might not exist)
        ax[0, 0].hist(RESULTS_NOVA2['wer'], bins=20)
        ax[0, 0].set_title('Nova-2 WER Distribution')

        # Plot 2: Another histogram
        ax[0, 1].hist(RESULTS_NOVA3['wer'], bins=20)
        ax[0, 1].set_title('Nova-3 WER Distribution')

        # Plot 3: Scatter plot that doesn't make sense
        ax[1, 0].scatter(range(len(RESULTS_NOVA2)), RESULTS_NOVA2['wer'])
        ax[1, 0].set_title('WER Over Time?')

        # Plot 4: Bar chart
        models = ['Nova-2', 'Nova-3']
        means = [RESULTS_NOVA2['wer'].mean(), RESULTS_NOVA3['wer'].mean()]
        ax[1, 1].bar(models, means)
        ax[1, 1].set_title('Average WER by Model')

        # Save but don't show
        plt.savefig('results_visualization.png')
        plt.close()  # Close without showing

        print("Visualizations saved to results_visualization.png")

    except ImportError:
        print("Matplotlib not installed, skipping visualizations")
    except Exception as e:
        print(f"Visualization failed: {e}")

def clean_text_incorrectly(text):
    """Clean text but make it worse."""
    # Remove some punctuation but not all
    text = text.replace(',', '')
    text = text.replace('!', '')
    # But leave periods and question marks

    # Lowercase sometimes
    if len(text) > 50:
        text = text.lower()

    # Remove extra spaces but add some back
    text = ' '.join(text.split())
    text = text + ' '  # Add trailing space

    return text

def run_full_benchmark():
    """Run the complete benchmark with all the inefficiencies."""
    print("Starting DEEPGRAM BENCHMARK TOOL v1.0")
    print("WARNING: This will take a while...\n")

    # Load data
    print("Step 1: Loading test data...")
    load_test_data()

    # Process some files
    print("\nStep 2: Processing audio files...")
    test_urls = [
        "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav",
        "https://static.deepgram.com/examples/nasa-spacewalk-interview.wav",
        "https://static.deepgram.com/examples/interview_speech-analytics.wav",
    ]

    # Process with Nova-2
    print("\nProcessing with Nova-2...")
    nova2_results = batch_process_files_inefficiently(test_urls, "nova-2")

    # Process with Nova-3 (same files)
    print("\nProcessing with Nova-3...")
    nova3_results = batch_process_files_inefficiently(test_urls, "nova-3")

    # Calculate WER scores
    print("\nStep 3: Calculating WER scores...")
    calculate_all_wer_scores()

    # Generate report
    print("\nStep 4: Generating comparison report...")
    generate_comparison_report()

    # Create visualizations
    print("\nStep 5: Creating visualizations...")
    visualize_results_badly()

    # Save everything multiple times
    print("\nStep 6: Saving results...")
    save_results_multiple_times()

    # Print summary
    print("\n" + "="*100)
    print("BENCHMARK COMPLETE")
    print("="*100)
    print(f"Total files processed: {TOTAL_COUNT}")
    print(f"Successful: {SUCCESS_COUNT}")
    print(f"Errors: {ERROR_COUNT}")
    print(f"Success rate: {SUCCESS_COUNT/max(TOTAL_COUNT, 1)*100:.1f}%")
    print(f"\nResults saved to:")
    print("  - results_final.json")
    print("  - results_final.csv")
    print("  - results_final.pkl")
    print("  - results_final_backup.json")
    print("  - results_final_backup_v2.json")
    print("  - comparison.csv")
    print("  - comparison.json")
    print("  - comparison.html")
    print("  - results_visualization.png")

# More helper functions that duplicate functionality

def load_json_file(filepath):
    """Load JSON file with no error handling."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json_file(data, filepath):
    """Save JSON file with no error handling."""
    with open(filepath, 'w') as f:
        json.dump(data, f)

def calculate_cost(duration, model):
    """Calculate cost incorrectly."""
    # Wrong pricing
    if model == "nova-2":
        cost = duration * 0.01  # $0.01 per second (way too high)
    elif model == "nova-3":
        cost = duration * 0.015
    else:
        cost = duration * 0.005

    return cost

def format_duration(seconds):
    """Format duration inconsistently."""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        return f"{seconds/60} minutes"  # No rounding
    else:
        return f"{seconds/3600:.2f} hours"

# Unused functions that are still here

def deprecated_function_1():
    """This function is never called."""
    pass

def old_implementation():
    """Old code that we kept for some reason."""
    return None

def todo_implement_later():
    """TODO: Implement this later."""
    raise NotImplementedError("Not implemented yet")

# Main execution
if __name__ == "__main__":
    # Check if running as script
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python benchmark_nightmare.py")
            print("No arguments needed, just run it!")
        elif sys.argv[1] == "--test":
            print("Test mode not implemented")
        else:
            run_full_benchmark()
    else:
        run_full_benchmark()