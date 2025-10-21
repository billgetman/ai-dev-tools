# AI Development Tools Demo Tracks

Demonstration tracks for presenting AI coding capabilities to experienced developers at Deepgram. Each track contains challenging exercises that require proper AI tool usage and context layering to solve efficiently.

## Overview

Three language tracks, each with greenfield and brownfield challenges:

| Track | Greenfield | Brownfield | Domain |
|-------|------------|------------|---------|
| **Python** | Deepgram Observatory (monitoring) | Benchmark Nightmare (1000-line mess) | API integration, WER calculation |
| **Rust** | Stream Orchestra (audio processor) | Unsafe Primitives (unsafe→safe) | Real-time processing, SIMD |
| **Elm** | Results Browser (clean UI) | Data Structure Disaster (60+ field Model) | State management, performance |

## Quick Start

Each track takes 20-25 minutes with AI assistance (hours without):

1. Choose a track based on language preference
2. Start with the challenge spec in `tracks/{language}/`
3. Use the TICKET.md for brownfield tasks
4. Test with provided data files

## Repository Structure

```
ai_tools_dev_track/
├── tracks/
│   ├── python/
│   │   ├── greenfield/         # Build monitoring system from scratch
│   │   ├── brownfield/         # Refactor broken benchmark tool
│   │   └── test_data/          # WER reference implementation
│   ├── rust/
│   │   ├── greenfield/         # Build audio processor
│   │   ├── brownfield/         # Refactor unsafe code
│   │   ├── audio_processor/    # Starter code
│   │   └── context/            # Design principles doc
│   └── elm/
│       ├── greenfield/         # Build results browser UI
│       ├── brownfield/         # Refactor 845-line file
│       ├── src/                # Starter Elm code
│       └── data/               # Test datasets
├── presentation_docs/          # Original specifications
└── example_prompts/            # Sample AI prompts

```

## Key Concepts Demonstrated

### Python Track
- **Problem**: Broken WER calculation, synchronous processing, pandas anti-patterns
- **Solution**: Levenshtein distance, async/await, vectorization
- **Performance**: 20x speedup (10 min → 30 sec for 100 files)

### Rust Track
- **Problem**: Unnecessary unsafe code, no SIMD, hardcoded types
- **Solution**: Safe abstractions, SIMD optimization, generics
- **Performance**: Safe matches unsafe, 20-50% SIMD gain (memory-bound reality)

### Elm Track
- **Problem**: 60+ field Model, List O(n) operations, redundant state
- **Solution**: Module decomposition, Dict for O(1) lookups, derived state
- **Performance**: 200ms → 16ms updates for 1000 items

## Success Metrics

- **Python**: Correct WER, async processing, 100+ files/second
- **Rust**: Zero unsafe blocks (or justified), benchmarks ≥100% original
- **Elm**: <15 Model fields, Dict-based lookups, 60fps updates

## For Presenters

1. Start with minimal context (just the spec)
2. Layer in information as needed
3. Let AI discover the problems
4. Focus on the refactoring process, not just the end result

## Prerequisites

- **Python**: 3.10+, Deepgram API key
- **Rust**: 1.75+, cargo
- **Elm**: 0.19.1, Node.js

See individual track SETUP.md files for details.

## Key Takeaway

AI tools excel at refactoring and optimization when given proper context. The challenges demonstrate how AI can help navigate complex codebases, identify anti-patterns, and implement best practices in any language.