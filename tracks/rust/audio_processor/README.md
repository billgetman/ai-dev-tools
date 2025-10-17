# audio_processor

Real-time audio processing primitives with zero-copy operations and SIMD acceleration.

## Usage

```rust
use audio_processor::{RingBuffer, StreamProcessor};

let mut processor = StreamProcessor::new(512);
processor.add_gain(0.5);
processor.add_lowpass(4000.0, 44100);

// Process interleaved stereo audio
processor.process(&mut samples)?;
```

## Performance

M1 Pro benchmarks (512 sample buffer):

| Operation | Time | Throughput |
|-----------|------|------------|
| apply_gain | 0.12 µs | 4.2M samples/sec |
| mix_buffers | 0.18 µs | 2.8M samples/sec |
| interleave_4ch | 0.45 µs | 1.1M samples/sec |
| convert_i16_f32 | 0.31 µs | 1.6M samples/sec |

## Running

```bash
# Run tests
cargo test

# Run benchmarks
cargo bench --bench buffer_ops

# Check for undefined behavior
cargo +nightly miri test
```

## Notes

The `unsafe_primitives` module contains legacy code being refactored for safety. See [brownfield/TICKET.md](../brownfield/TICKET.md) for details.