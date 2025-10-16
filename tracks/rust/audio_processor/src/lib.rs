//! Audio Stream Processor
//!
//! Real-time audio processing with zero allocations in the hot path.

pub mod unsafe_primitives;

/// Audio processor for real-time stream processing
pub struct AudioProcessor {
    gain: f32,
    buffer_size: usize,
}

impl AudioProcessor {
    /// Create a new audio processor
    pub fn new() -> Self {
        AudioProcessor {
            gain: 1.0,
            buffer_size: 1024,
        }
    }

    /// Set the gain level
    pub fn set_gain(&mut self, gain: f32) {
        self.gain = gain;
    }

    /// Process audio samples
    pub fn process(&mut self, input: &[f32], output: &mut [f32]) {
        // Basic implementation - to be expanded
        let len = input.len().min(output.len());
        for i in 0..len {
            output[i] = input[i] * self.gain;
        }
    }
}

impl Default for AudioProcessor {
    fn default() -> Self {
        Self::new()
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