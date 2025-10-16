# Rust Track Presenter Guide

Target time: 20-25 minutes

## Part 1: Greenfield (10-12 min)

### Phase 1: Basic Processor (0-3 min)

Prompt AI:
```
Create audio stream processor in Rust. Read f32 samples from buffer, apply gain effect,
write to output. Use Vec<f32> and iterators. Create module structure and test.
```

Context: `greenfield/rust_greenfield.md`, Cargo.toml

Expected: `src/processor.rs` with AudioProcessor struct, `process()` method, basic test.

Test:
```rust
#[test]
fn test_gain() {
    let input = vec![0.5; 1024];
    let mut output = vec![0.0; 1024];
    let mut processor = AudioProcessor::new();
    processor.set_gain(2.0);
    processor.process(&input, &mut output);
    assert!((output[0] - 1.0).abs() < 0.001);
}
```

### Phase 2: Multi-Channel + Effects (3-6 min)

Prompt AI:
```
Extend processor for multi-channel audio (stereo, 5.1). Add effect chain system.
Implement normalize and denoise effects. Handle channel interleaving (LRLRLR...).
```

Context: Current processor.rs, channel layout explanation

Expected: `ChannelLayout` enum, `Effect` trait, multiple effect implementations, effect chaining.

Benchmark:
```rust
fn bench_effect_chain(c: &mut Criterion) {
    let input = vec![0.5; 48000];
    group.bench_function("gain", |b| {
        b.iter(|| processor.process(&input, &mut output));
    });
}
```

Run: `cargo bench`

### Phase 3: Lock-Free Ring Buffer (6-9 min)

Prompt AI:
```
Refactor to use lock-free ring buffer. Use crossbeam's SPSC queue. I/O thread writes samples,
processing thread reads. Target: <10ms latency, zero allocations in steady state.
```

Context: Current code, Cargo.toml (crossbeam), real-time constraints

Expected: Fixed-size ring buffers, `crossbeam::queue::ArrayQueue`, separate threads, latency measurement.

Verify zero allocations:
```bash
cargo run --release --features dhat-heap
# Or use Instruments (macOS) / valgrind (Linux)
```

### Phase 4: Zero-Copy IPC (9-12 min)

Prompt AI:
```
Implement IPC using shared memory. One process produces audio, another consumes.
Use shared_memory crate. Maintain lock-free properties with atomic operations.
```

Context: Current lock-free code, Cargo.toml (shared_memory)

Expected: Shared memory setup, producer/consumer processes, atomic synchronization.

Test:
```bash
# Terminal 1
cargo run --example producer

# Terminal 2
cargo run --example consumer
```

## Part 2: Brownfield (10-13 min)

### Phase 1: Make Safe (0-3 min)

Prompt AI:
```
Refactor src/unsafe_primitives.rs. Remove unnecessary unsafe blocks. Use iterators.
Add benchmarks to ensure performance identical.
```

Context: `unsafe_primitives.rs`, brownfield spec

Expected:
```rust
// Before: unsafe with raw pointers
// After: safe with iterators
pub fn apply_gain_safe(buffer: &mut [f32], gain: f32) {
    for sample in buffer.iter_mut() {
        *sample *= gain;
    }
}
```

Benchmark:
```bash
cargo bench --bench buffer_ops
# Should show identical performance
```

### Phase 2: Add SIMD (3-6 min)

Prompt AI:
```
Add SIMD vectorization using std::simd. Implement SIMD versions of gain, mix, convert.
Provide scalar fallback. Target: 4x-8x speedup.
```

Context: Current safe implementations

Expected:
```rust
use std::simd::*;

pub fn apply_gain_simd(buffer: &mut [f32], gain: f32) {
    let gain_vec = f32x4::splat(gain);
    for chunk in buffer.chunks_exact_mut(4) {
        let samples = f32x4::from_slice(chunk);
        (samples * gain_vec).copy_to_slice(chunk);
    }
    // Handle remainder with scalar
}
```

### Phase 3: Make Generic (6-9 min)

Prompt AI:
```
Make buffer operations generic over sample types. Create Sample trait.
Implement for i16, i32, f32, f64. Use const generics for buffer sizes.
Zero-cost abstractions.
```

Context: Current implementations

Expected:
```rust
pub trait Sample: Copy + Send + Sync {
    fn to_f32(self) -> f32;
    fn from_f32(val: f32) -> Self;
}

pub fn apply_gain<T: Sample>(buffer: &mut [T], gain: f32) {
    for sample in buffer.iter_mut() {
        *sample = T::from_f32(sample.to_f32() * gain);
    }
}
```

### Phase 4: Send + Sync + Const (9-13 min)

Prompt AI:
```
Ensure all types are Send + Sync. Add const generic parameters for buffer sizes.
Use const functions where possible. Run Miri to verify no undefined behavior.
```

Context: Current generic code

Expected:
```rust
pub struct AudioBuffer<T: Sample, const SIZE: usize> {
    data: [T; SIZE],
}

unsafe impl<T: Sample, const SIZE: usize> Send for AudioBuffer<T, SIZE> {}
unsafe impl<T: Sample, const SIZE: usize> Sync for AudioBuffer<T, SIZE> {}
```

Verify:
```bash
cargo +nightly miri test
```

Final benchmark:
```bash
cargo bench --bench buffer_ops
# Show: unsafe vs safe (same), safe+SIMD (4x faster), generic (zero-cost)
```

## Context Layering

Incremental context:
1. Start: Challenge spec, Cargo.toml
2. Add: Previous code as created
3. Provide: Concurrency docs (crossbeam, atomics), SIMD docs
4. Show: Performance requirements

## Common Issues

**Borrow checker errors**: Ask AI to explain, restructure ownership if needed
**Performance regression**: Check `--release`, look at assembly with `cargo asm`
**SIMD not working**: Use `RUSTFLAGS="-C target-cpu=native"`, verify chunk sizes
**Send/Sync errors**: Identify non-Send field, wrap in Arc/Mutex if needed

## Success Criteria

Greenfield:
- [ ] Real-time processor working
- [ ] Multi-channel + effects
- [ ] Lock-free, <10ms latency
- [ ] Zero allocations proven

Brownfield:
- [ ] All unsafe removed or justified
- [ ] Benchmarks ≥100% of original
- [ ] SIMD 4x+ speedup
- [ ] Generic over sample types
- [ ] Send + Sync bounds
- [ ] Miri passes

Done in ~20-25 minutes.
