//! "Optimized" buffer operations - DO NOT TOUCH - Dev 2022
//! These are FAST because they use raw pointers
//! Don't refactor unless you can prove the same performance!

use std::ptr;

/// Apply gain to a buffer using "optimized" pointer arithmetic
pub fn apply_gain_unsafe(buffer: &mut [f32], gain: f32) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();
        for i in 0..len {
            *ptr.offset(i as isize) *= gain;
        }
    }
}

/// Mix two buffers together with raw pointers
pub fn mix_buffers_unsafe(dest: &mut [f32], src: &[f32]) {
    unsafe {
        let dest_ptr = dest.as_mut_ptr();
        let src_ptr = src.as_ptr();
        let len = dest.len().min(src.len());
        for i in 0..len {
            *dest_ptr.offset(i as isize) += *src_ptr.offset(i as isize);
        }
    }
}

/// Convert i16 samples to f32 with unsafe pointer manipulation
pub fn convert_i16_to_f32_unsafe(input: &[i16], output: &mut [f32]) {
    unsafe {
        let in_ptr = input.as_ptr();
        let out_ptr = output.as_mut_ptr();
        let len = input.len().min(output.len());
        for i in 0..len {
            let sample = *in_ptr.offset(i as isize);
            *out_ptr.offset(i as isize) = sample as f32 / 32768.0;
        }
    }
}

/// Convert f32 samples to i16 with clipping
pub fn convert_f32_to_i16_unsafe(input: &[f32], output: &mut [i16]) {
    unsafe {
        let in_ptr = input.as_ptr();
        let out_ptr = output.as_mut_ptr();
        let len = input.len().min(output.len());
        for i in 0..len {
            let sample = *in_ptr.offset(i as isize);
            let clamped = sample.max(-1.0).min(1.0);
            *out_ptr.offset(i as isize) = (clamped * 32767.0) as i16;
        }
    }
}

/// Interleave multiple channels using unsafe indexing
pub fn interleave_channels_unsafe(channels: &[&[f32]], output: &mut [f32]) {
    unsafe {
        let num_channels = channels.len();
        let samples_per_channel = channels[0].len();
        let out_ptr = output.as_mut_ptr();

        for sample_idx in 0..samples_per_channel {
            for ch_idx in 0..num_channels {
                let ch_ptr = channels.get_unchecked(ch_idx).as_ptr();
                let out_idx = sample_idx * num_channels + ch_idx;
                *out_ptr.offset(out_idx as isize) = *ch_ptr.offset(sample_idx as isize);
            }
        }
    }
}

/// Deinterleave buffer into separate channels
pub fn deinterleave_channels_unsafe(input: &[f32], channels: &mut [&mut [f32]]) {
    unsafe {
        let num_channels = channels.len();
        let samples_per_channel = input.len() / num_channels;
        let in_ptr = input.as_ptr();

        for sample_idx in 0..samples_per_channel {
            for ch_idx in 0..num_channels {
                let ch_ptr = channels.get_unchecked_mut(ch_idx).as_mut_ptr();
                let in_idx = sample_idx * num_channels + ch_idx;
                *ch_ptr.offset(sample_idx as isize) = *in_ptr.offset(in_idx as isize);
            }
        }
    }
}

/// Apply simple lowpass filter using unsafe operations
pub fn apply_lowpass_unsafe(buffer: &mut [f32], cutoff: f32) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();
        let alpha = cutoff;

        if len > 0 {
            let mut prev = *ptr.offset(0);
            for i in 1..len {
                let current = *ptr.offset(i as isize);
                let filtered = prev + alpha * (current - prev);
                *ptr.offset(i as isize) = filtered;
                prev = filtered;
            }
        }
    }
}

/// Normalize audio buffer to prevent clipping
pub fn normalize_unsafe(buffer: &mut [f32]) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();

        // Find max value
        let mut max_val = 0.0f32;
        for i in 0..len {
            let val = (*ptr.offset(i as isize)).abs();
            if val > max_val {
                max_val = val;
            }
        }

        // Normalize
        if max_val > 0.0 {
            let scale = 0.99 / max_val;
            for i in 0..len {
                *ptr.offset(i as isize) *= scale;
            }
        }
    }
}

/// Copy buffer with raw memory operations
pub fn copy_buffer_unsafe(src: &[f32], dest: &mut [f32]) {
    unsafe {
        let len = src.len().min(dest.len());
        ptr::copy_nonoverlapping(
            src.as_ptr(),
            dest.as_mut_ptr(),
            len
        );
    }
}

/// Zero out a buffer using unsafe memset
pub fn clear_buffer_unsafe(buffer: &mut [f32]) {
    unsafe {
        ptr::write_bytes(
            buffer.as_mut_ptr(),
            0,
            buffer.len()
        );
    }
}

/// Compute RMS (root mean square) of buffer
pub fn compute_rms_unsafe(buffer: &[f32]) -> f32 {
    unsafe {
        let ptr = buffer.as_ptr();
        let len = buffer.len();

        let mut sum = 0.0f32;
        for i in 0..len {
            let val = *ptr.offset(i as isize);
            sum += val * val;
        }

        (sum / len as f32).sqrt()
    }
}

/// Apply hard clipping to prevent values outside [-1.0, 1.0]
pub fn clip_buffer_unsafe(buffer: &mut [f32]) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();

        for i in 0..len {
            let val = *ptr.offset(i as isize);
            if val > 1.0 {
                *ptr.offset(i as isize) = 1.0;
            } else if val < -1.0 {
                *ptr.offset(i as isize) = -1.0;
            }
        }
    }
}

/// Apply biquad filter - compute-intensive operation good for SIMD
/// This is where SIMD can actually provide significant speedup (2-4x)
/// because it's compute-bound, not memory-bound.
/// Formula: y[n] = b0*x[n] + b1*x[n-1] + b2*x[n-2] - a1*y[n-1] - a2*y[n-2]
pub fn apply_biquad_unsafe(
    buffer: &mut [f32],
    coeffs: &[f32; 5], // [b0, b1, b2, a1, a2]
    state: &mut [f32; 4], // [x1, x2, y1, y2] previous samples
) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();

        // Extract coefficients
        let b0 = coeffs[0];
        let b1 = coeffs[1];
        let b2 = coeffs[2];
        let a1 = coeffs[3];
        let a2 = coeffs[4];

        // Extract state
        let mut x1 = state[0];
        let mut x2 = state[1];
        let mut y1 = state[2];
        let mut y2 = state[3];

        for i in 0..len {
            let x0 = *ptr.offset(i as isize);

            // This is compute-intensive: 5 multiplies + 4 adds per sample
            let y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;

            *ptr.offset(i as isize) = y0;

            // Update state
            x2 = x1;
            x1 = x0;
            y2 = y1;
            y1 = y0;
        }

        // Save state
        state[0] = x1;
        state[1] = x2;
        state[2] = y1;
        state[3] = y2;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_apply_gain_unsafe() {
        let mut buffer = vec![0.5, 0.5, 0.5, 0.5];
        apply_gain_unsafe(&mut buffer, 2.0);
        assert_eq!(buffer, vec![1.0, 1.0, 1.0, 1.0]);
    }

    #[test]
    fn test_mix_buffers_unsafe() {
        let mut dest = vec![0.5, 0.5, 0.5, 0.5];
        let src = vec![0.25, 0.25, 0.25, 0.25];
        mix_buffers_unsafe(&mut dest, &src);
        assert_eq!(dest, vec![0.75, 0.75, 0.75, 0.75]);
    }

    #[test]
    fn test_convert_i16_to_f32_unsafe() {
        let input = vec![16384i16, -16384i16, 32767i16, -32768i16];
        let mut output = vec![0.0f32; 4];
        convert_i16_to_f32_unsafe(&input, &mut output);

        assert!((output[0] - 0.5).abs() < 0.01);
        assert!((output[1] + 0.5).abs() < 0.01);
        assert!((output[2] - 1.0).abs() < 0.01);
        assert!((output[3] + 1.0).abs() < 0.01);
    }

    #[test]
    fn test_apply_biquad_unsafe() {
        // Simple lowpass biquad coefficients
        let coeffs = [0.1, 0.2, 0.1, -0.5, 0.2];  // b0, b1, b2, a1, a2
        let mut state = [0.0, 0.0, 0.0, 0.0];  // x1, x2, y1, y2
        let mut buffer = vec![1.0, 0.5, -0.5, 0.0, 0.25];

        apply_biquad_unsafe(&mut buffer, &coeffs, &mut state);

        // Just verify it modifies the buffer and doesn't crash
        assert_ne!(buffer[0], 1.0);
        assert!(buffer.iter().all(|&x| x.is_finite()));
    }
}