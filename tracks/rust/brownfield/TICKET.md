# TICKET: Refactor Audio Primitives

**ID**: AUDIO-4387
**Priority**: High
**File**: `audio_processor/src/unsafe_primitives.rs`

## Context

Legacy buffer operations from 2022. Every function is marked unsafe but most don't need to be. Client security audit flagged this. Also missing SIMD and generic type support that we now need.

## Current Issues

1. **Pointless unsafe** - `apply_gain_unsafe` just iterates and multiplies. The compiler already optimizes this.
2. **Manual offset arithmetic** - Using `.offset(i as isize)` instead of safe indexing
3. **No SIMD** - Processing audio samples one at a time
4. **Hardcoded f32** - Need i16 support for new codec
5. **Miri failures** - Run `cargo +nightly miri test` to see alignment issues

## Quick Analysis

```rust
// Current (13 lines with unsafe):
pub fn apply_gain_unsafe(buffer: &mut [f32], gain: f32) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();
        for i in 0..len {
            *ptr.offset(i as isize) *= gain;
        }
    }
}

// Equivalent safe version (2 lines):
pub fn apply_gain(buffer: &mut [f32], gain: f32) {
    buffer.iter_mut().for_each(|x| *x *= gain);
}
```

Check the assembly with `cargo asm` - the safe version is identical or better.

## Requirements

1. **Remove unnecessary unsafe** - Most of these functions don't need it. Keep `ptr::copy_nonoverlapping` and `ptr::write_bytes` where appropriate.

2. **Add SIMD** - Use `std::simd` or `wide` crate. Process chunks with `chunks_exact_mut`.

3. **Generic types** - At minimum support `i16` and `f32`. Consider a `Sample` trait.

4. **Maintain performance** - Existing benchmarks in `benches/buffer_ops.rs` must not regress.

## Functions to Refactor

- `apply_gain_unsafe` - trivial safe rewrite
- `mix_buffers_unsafe` - zip iterators
- `convert_i16_to_f32_unsafe` - safe iteration
- `convert_f32_to_i16_unsafe` - safe with clamp
- `interleave_channels_unsafe` - chunks and iterators
- `deinterleave_channels_unsafe` - chunks_exact
- `apply_lowpass_unsafe` - fold or scan
- `normalize_unsafe` - find max, then scale
- `compute_rms_unsafe` - iterator sum
- `clip_buffer_unsafe` - clamp method
- `copy_buffer_unsafe` - keep ptr::copy_nonoverlapping but document safety
- `clear_buffer_unsafe` - keep ptr::write_bytes or use fill(0.0)

## Definition of Done

- [ ] Unnecessary unsafe removed
- [ ] Remaining unsafe has `// SAFETY:` comments
- [ ] Passes `cargo miri test`
- [ ] Benchmarks ≥100% of original performance
- [ ] SIMD path for applicable functions
- [ ] Generic over `i16` and `f32` at minimum

## Hints

- Start with the trivial ones: `apply_gain`, `clip_buffer`, `compute_rms`
- For SIMD: `f32x8::splat(gain) * f32x8::from_slice(chunk)`
- The interleave/deinterleave functions are where SIMD really shines
- `copy_buffer_unsafe` and `clear_buffer_unsafe` already use the right primitives

---

*The "DO NOT TOUCH" comment is from someone who left in 2022. Touch away.*