Brownfield: "The Unsafe Primitives"
Low-level audio buffer primitives that power the Stream Orchestra, full of `unsafe` blocks

These are the building blocks used by the greenfield processor: buffer operations, sample format conversions, and effect kernels. Someone wrote them "fast" using raw pointers. Refactor to be safe without losing performance.

```rust
// audio_primitives/src/buffer.rs
/// "Optimized" buffer operations - DO NOT TOUCH - Dev 2022
pub fn apply_gain_unsafe(buffer: &mut [f32], gain: f32) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        let len = buffer.len();
        for i in 0..len {
            *ptr.offset(i as isize) *= gain;
        }
    }
}

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

pub fn convert_i16_to_f32_unsafe(input: &[i16], output: &mut [f32]) {
    unsafe {
        let in_ptr = input.as_ptr();
        let out_ptr = output.as_mut_ptr();
        for i in 0..input.len() {
            let sample = *in_ptr.offset(i as isize);
            *out_ptr.offset(i as isize) = sample as f32 / 32768.0;
        }
    }
}

// More unsafe operations for ring buffers, atomics, etc...
```

**Phase 1: Make safe without losing performance**
- Remove unnecessary `unsafe` blocks
- Use iterators and safe abstractions
- Prove performance identical with benchmarks (criterion)
- Document why any remaining `unsafe` is necessary

**Phase 2: Add SIMD**
- Use `std::simd` or `packed_simd2` for vectorization
- Safe SIMD abstractions (no raw intrinsics)
- Target: 20-50% speedup for memory-bound operations (gain, mix)
- Target: 2-4x speedup for compute-intensive operations (filters, interleaving)
- Note: Safe iterators often compile to same assembly as unsafe
- Graceful fallback for non-SIMD targets

**Phase 3: Make generic over sample types**
- Support `i16`, `i32`, `f32`, `f64`
- Use traits: `Sample`, `FromSample`, `IntoSample`
- Zero-cost abstractions (monomorphization)
- Const generics for buffer sizes where applicable

**Phase 4: Thread safety (Send + Sync)**
- Multi-threaded processing requires thread safety
- Prove buffer types are `Send + Sync`
- Add proper synchronization primitives
- Use `Arc` correctly without data races

**Phase 5: Const evaluation**
- Const generics for compile-time buffer size validation
- Const functions for compile-time conversions
- Type-level guarantees about buffer alignment
- Zero runtime overhead for safety checks

**Success criteria:**
- Zero `unsafe` blocks (or justified with safety comments)
- Benchmarks show ≥100% performance of original
- SIMD provides measurable speedup where applicable (20-50% typical)
- Generic over sample types (at least i16, f32)
- All types are `Send + Sync`
- Passes Miri (undefined behavior detector)