# Rust Track Setup

## Requirements

- Rust 1.75+
- ~2GB disk for toolchain and dependencies

## Install Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
rustc --version  # Should show 1.75+
```

Install nightly (for Miri):
```bash
rustup toolchain install nightly
rustup component add miri --toolchain nightly
```

## Install Tools

```bash
# Linter and formatter
rustup component add clippy rustfmt

# Performance tools
cargo install flamegraph cargo-show-asm

# Optional: Memory profiling (Linux)
sudo apt-get install valgrind
```

## Initialize Project

```bash
cd tracks/rust
cargo new --lib audio_processor
cd audio_processor
```

## Configure Cargo.toml

```toml
[package]
name = "audio_processor"
version = "0.1.0"
edition = "2021"

[dependencies]
crossbeam = "0.8"
rayon = "1.8"
thiserror = "1.0"
shared_memory = "0.12"
memmap2 = "0.9"

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
approx = "0.5"

[[bench]]
name = "buffer_ops"
harness = false

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

Install dependencies:
```bash
cargo build --release
```

## Test Audio Data

Generate with sox:
```bash
# macOS
brew install sox

# Linux
sudo apt-get install sox

# Generate test files
sox -n -r 48000 -c 2 test_sine_440hz.wav synth 5 sine 440
```

Or generate in Rust:
```rust
// examples/generate_test_audio.rs
fn main() {
    let sample_rate = 48000;
    let duration = 5;
    let frequency = 440.0;

    let samples: Vec<f32> = (0..(sample_rate * duration))
        .map(|i| {
            let t = i as f32 / sample_rate as f32;
            (2.0 * std::f32::consts::PI * frequency * t).sin()
        })
        .collect();

    println!("Generated {} samples", samples.len());
}
```

## Create Brownfield Starting Code

Before demo, create `src/unsafe_primitives.rs`:

```rust
/// "Optimized" buffer operations - DO NOT TOUCH - Dev 2022
pub fn apply_gain_unsafe(buffer: &mut [f32], gain: f32) {
    unsafe {
        let ptr = buffer.as_mut_ptr();
        for i in 0..buffer.len() {
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
```

See brownfield spec for full implementation.

## Verify

```bash
cargo build --release
cargo test
cargo bench --no-run
cargo +nightly miri --version
```

Ready for demo.
