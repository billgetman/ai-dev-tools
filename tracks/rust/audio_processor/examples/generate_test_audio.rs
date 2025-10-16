//! Generate test audio data for testing the audio processor

use std::f32::consts::PI;

fn main() {
    println!("Generating test audio samples...\n");

    // Generate a 440Hz sine wave (A4 note)
    let sample_rate = 48000;
    let duration = 5; // seconds
    let frequency = 440.0; // Hz

    let samples: Vec<f32> = (0..(sample_rate * duration))
        .map(|i| {
            let t = i as f32 / sample_rate as f32;
            (2.0 * PI * frequency * t).sin()
        })
        .collect();

    println!("Generated {} samples ({} seconds @ {}Hz)",
             samples.len(), duration, sample_rate);
    println!("First 10 samples: {:?}", &samples[..10]);

    // Generate stereo test data (left channel sine, right channel cosine)
    let stereo_left: Vec<f32> = (0..(sample_rate * duration))
        .map(|i| {
            let t = i as f32 / sample_rate as f32;
            (2.0 * PI * frequency * t).sin() * 0.5 // 50% amplitude
        })
        .collect();

    let stereo_right: Vec<f32> = (0..(sample_rate * duration))
        .map(|i| {
            let t = i as f32 / sample_rate as f32;
            (2.0 * PI * frequency * t).cos() * 0.5 // 50% amplitude, phase shifted
        })
        .collect();

    println!("\nGenerated stereo samples:");
    println!("  Left channel: {} samples", stereo_left.len());
    println!("  Right channel: {} samples", stereo_right.len());

    // Generate white noise
    let noise: Vec<f32> = (0..(sample_rate * 1))
        .map(|i| {
            // Simple pseudo-random using sine of large numbers
            ((i as f32 * 12.9898).sin() * 43758.5453).fract() * 2.0 - 1.0
        })
        .collect();

    println!("\nGenerated {} samples of white noise", noise.len());

    // Generate a sweep from 100Hz to 1000Hz
    let sweep_duration = 3; // seconds
    let start_freq = 100.0;
    let end_freq = 1000.0;

    let sweep: Vec<f32> = (0..(sample_rate * sweep_duration))
        .map(|i| {
            let t = i as f32 / sample_rate as f32;
            let progress = t / sweep_duration as f32;
            let current_freq = start_freq + (end_freq - start_freq) * progress;
            (2.0 * PI * current_freq * t).sin() * 0.7
        })
        .collect();

    println!("\nGenerated frequency sweep:");
    println!("  Duration: {} seconds", sweep_duration);
    println!("  Frequency range: {}Hz to {}Hz", start_freq, end_freq);
    println!("  Samples: {}", sweep.len());

    // Test the audio processor with generated data
    use audio_processor::AudioProcessor;

    let mut processor = AudioProcessor::new();
    processor.set_gain(0.5);

    let input = &samples[0..1024];
    let mut output = vec![0.0f32; 1024];

    processor.process(input, &mut output);

    println!("\nProcessed 1024 samples through AudioProcessor");
    println!("  Input RMS: {:.4}", compute_rms(input));
    println!("  Output RMS: {:.4}", compute_rms(&output));
    println!("  Gain applied: 0.5");

    // Test with the unsafe primitives
    use audio_processor::unsafe_primitives::*;

    let mut test_buffer = vec![0.5f32; 1024];

    println!("\nTesting unsafe primitives:");

    apply_gain_unsafe(&mut test_buffer, 2.0);
    println!("  Applied gain of 2.0");

    let rms = compute_rms_unsafe(&test_buffer);
    println!("  Buffer RMS after gain: {:.4}", rms);

    normalize_unsafe(&mut test_buffer);
    println!("  Normalized buffer");

    let rms_normalized = compute_rms_unsafe(&test_buffer);
    println!("  Buffer RMS after normalization: {:.4}", rms_normalized);
}

fn compute_rms(buffer: &[f32]) -> f32 {
    let sum: f32 = buffer.iter().map(|x| x * x).sum();
    (sum / buffer.len() as f32).sqrt()
}