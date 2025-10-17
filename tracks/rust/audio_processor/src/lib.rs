//! Real-time audio processing with zero-copy operations.
//!
//! This crate provides low-level audio processing primitives designed for
//! real-time applications. All operations are allocation-free in the hot path
//! and leverage SIMD when available.
//!
//! # Architecture
//!
//! The crate is organized into three layers:
//! - **Primitives** (`unsafe_primitives`): Low-level buffer operations
//! - **Processing** (`AudioProcessor`): High-level effect chains
//! - **I/O** (`RingBuffer`): Lock-free audio streaming
//!
//! # Example
//!
//! ```rust
//! use audio_processor::AudioProcessor;
//!
//! let mut processor = AudioProcessor::new();
//! processor.set_gain(0.5);  // 50% volume
//!
//! // Process a buffer in-place
//! let mut samples = vec![1.0; 512];
//! processor.process_in_place(&mut samples);
//! assert_eq!(samples[0], 0.5);
//! ```
//!
//! # Performance
//!
//! All buffer operations are SIMD-accelerated on x86_64 (AVX2) and ARM (NEON).
//! Fallback scalar implementations ensure correctness on all platforms.
//!
//! # Safety
//!
//! The `unsafe_primitives` module contains performance-critical code that uses
//! unsafe blocks for optimization. These are being refactored to minimize unsafe
//! surface area while maintaining performance. See module documentation for details.

pub mod unsafe_primitives;

use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};

/// Audio processor for real-time stream processing.
///
/// Supports chaining multiple effects with zero intermediate allocations.
///
/// # Thread Safety
///
/// `AudioProcessor` is `Send` but not `Sync`. For concurrent processing,
/// use separate instances per thread or wrap in a `Mutex`.
pub struct AudioProcessor {
    gain: f32,
    buffer_size: usize,
}

impl AudioProcessor {
    /// Create a new audio processor with default buffer size (1024 samples).
    ///
    /// # Example
    /// ```
    /// let processor = AudioProcessor::new();
    /// ```
    pub fn new() -> Self {
        AudioProcessor {
            gain: 1.0,
            buffer_size: 1024,
        }
    }

    /// Create a processor with specified buffer size.
    ///
    /// # Arguments
    /// * `buffer_size` - Internal buffer size for processing
    ///
    /// # Panics
    /// Panics if buffer_size is 0.
    pub fn with_buffer_size(buffer_size: usize) -> Self {
        assert!(buffer_size > 0, "Buffer size must be > 0");
        AudioProcessor {
            gain: 1.0,
            buffer_size,
        }
    }

    /// Set the gain level.
    ///
    /// # Arguments
    /// * `gain` - Linear gain factor (1.0 = unity, 0.5 = -6dB, 2.0 = +6dB)
    pub fn set_gain(&mut self, gain: f32) {
        self.gain = gain;
    }

    /// Process audio samples from input to output buffer.
    ///
    /// # Arguments
    /// * `input` - Source samples
    /// * `output` - Destination buffer (must be at least as long as input)
    ///
    /// # Example
    /// ```
    /// let mut processor = AudioProcessor::new();
    /// processor.set_gain(0.5);
    ///
    /// let input = vec![1.0; 512];
    /// let mut output = vec![0.0; 512];
    /// processor.process(&input, &mut output);
    /// ```
    pub fn process(&mut self, input: &[f32], output: &mut [f32]) {
        // Basic implementation - to be expanded
        let len = input.len().min(output.len());
        for i in 0..len {
            output[i] = input[i] * self.gain;
        }
    }

    /// Process audio samples in-place.
    ///
    /// More efficient than `process()` as it avoids copies.
    ///
    /// # Arguments
    /// * `buffer` - Audio samples to process in-place
    pub fn process_in_place(&mut self, buffer: &mut [f32]) {
        unsafe_primitives::apply_gain_unsafe(buffer, self.gain);
    }
}

impl Default for AudioProcessor {
    fn default() -> Self {
        Self::new()
    }
}

/// Lock-free ring buffer for audio streaming.
///
/// Enables zero-copy audio transfer between threads without locks.
///
/// # Example
/// ```
/// let buffer = RingBuffer::new(4096);
/// // Producer thread writes samples
/// // Consumer thread reads samples
/// ```
pub struct RingBuffer {
    /// Internal buffer storage
    buffer: Arc<Vec<f32>>,
    /// Write position (producer)
    write_pos: Arc<AtomicUsize>,
    /// Read position (consumer)
    read_pos: Arc<AtomicUsize>,
}

impl RingBuffer {
    /// Create a new ring buffer with specified capacity.
    pub fn new(capacity: usize) -> Self {
        RingBuffer {
            buffer: Arc::new(vec![0.0; capacity]),
            write_pos: Arc::new(AtomicUsize::new(0)),
            read_pos: Arc::new(AtomicUsize::new(0)),
        }
    }

    /// Get the buffer capacity.
    pub fn capacity(&self) -> usize {
        self.buffer.len()
    }
}

/// High-level stream processor with effect chain support.
///
/// Combines multiple `AudioProcessor` instances into a processing pipeline.
pub struct StreamProcessor {
    processors: Vec<AudioProcessor>,
    buffer_size: usize,
}

impl StreamProcessor {
    /// Create a new stream processor.
    pub fn new(buffer_size: usize) -> Self {
        StreamProcessor {
            processors: Vec::new(),
            buffer_size,
        }
    }

    /// Add a gain stage to the processing chain.
    pub fn add_gain(&mut self, gain: f32) {
        let mut processor = AudioProcessor::with_buffer_size(self.buffer_size);
        processor.set_gain(gain);
        self.processors.push(processor);
    }

    /// Process audio through the entire effect chain.
    pub fn process(&mut self, buffer: &mut [f32]) -> Result<(), &'static str> {
        for processor in &mut self.processors {
            processor.process_in_place(buffer);
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_gain() {
        let mut processor = AudioProcessor::new();
        processor.set_gain(2.0);

        let input = vec![0.5; 1024];
        let mut output = vec![0.0; 1024];

        processor.process(&input, &mut output);

        assert!((output[0] - 1.0).abs() < 0.001);
    }
}