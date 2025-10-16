Greenfield: "The Stream Orchestra"
Real-time audio stream processor with zero allocations in hot path

**Phase 1: Single-threaded processor**
- Read audio samples from input stream
- Apply gain/volume control
- Write to output stream
- Use `Vec<f32>` for sample buffers
- Basic error handling

**Phase 2: Multi-channel processing**
- Support stereo and multi-channel audio (2, 4, 6, 8 channels)
- Effects: normalize, denoise, VAD
- Effect chaining/pipeline architecture
- Process chunks efficiently (no per-sample allocation)

**Phase 3: Lock-free ring buffers**
- Replace `Vec` with fixed-size ring buffers (no allocations in hot path)
- Lock-free SPSC queues
- Separate I/O thread from processing thread
- Measure latency (target: <10ms)
- Benchmark to prove zero allocations

**Phase 4: Zero-copy IPC**
- Inter-process communication using shared memory
- Producer/consumer processes (microservice architecture)
- Use memory-mapped files or OS primitives
- Maintain lock-free properties across process boundaries
- Handle process crashes gracefully