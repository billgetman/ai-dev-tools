# Rust Track: Real-Time Audio Stream Processor

## Track Structure

Build a high-performance, real-time audio processing system:

1. **Greenfield: "The Stream Orchestra"** - Real-time audio processing pipeline from scratch
2. **Brownfield: "The Unsafe Primitives"** - Refactor unsafe low-level buffer operations

Connection: Brownfield primitives (buffer operations, sample conversions) are the building blocks that power the greenfield architecture.

## Challenges

**Greenfield**
Phase 1 → Single-threaded processor with basic effects
Phase 2 → Multi-channel processing with effect chains
Phase 3 → Lock-free ring buffers, <10ms latency
Phase 4 → Zero-copy inter-process communication

**Brownfield**
Phase 1 → Make unsafe code safe without performance loss
Phase 2 → Add SIMD (4x-8x speedup target)
Phase 3 → Make generic over sample types (i16, f32, etc.)
Phase 4 → Thread safety (Send+Sync)
Phase 5 → Const evaluation

## Prerequisites

- Rust 1.75+
- Cargo and rustup
- Basic audio samples
- Performance measurement tools

See [SETUP.md](./SETUP.md) for installation.

## Target Time

20-25 minutes total with AI assistance (days without).

## Success Criteria

- <10ms latency proven
- Zero allocations in hot path
- Lock-free queues working correctly
- Safe code benchmarks at ≥100% of unsafe code performance
- SIMD operations show 4x-8x speedup
- All types are Send + Sync
- Miri reports no undefined behavior

## Key Message

Safe Rust code can be as fast as unsafe code. AI tools help navigate Rust's complexity while maintaining correctness and performance.
