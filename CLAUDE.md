# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains AI development tool demonstration tracks designed for presenting AI coding capabilities to experienced developers at Deepgram. The project aims to showcase how AI tools like Claude Code can assist with software development through practical, challenging exercises that require proper context layering.

## Repository Structure

The repository is organized into three programming language tracks, each containing specifications for greenfield and brownfield challenges:

```
ai_tools_dev_track/
├── presentation_docs/
│   └── tracks_spec.md          # Main specification document
└── tracks/
    ├── python/
    │   ├── greenfield/          # "The Chaos Experiment" - chaos engineering tool
    │   └── brownfield/          # "The Data Science Frankenstein" - notebook refactoring
    ├── rust/
    │   ├── greenfield/          # "The Zero-Copy Orchestra" - audio mixer
    │   └── brownfield/          # "The Unsafe Wasteland" - unsafe code refactoring
    └── elm/
        ├── greenfield/          # "The Impossible UI" - DAW-style editor
        └── brownfield/          # "The State Management Disaster" - Model decomposition
```

## Track Specifications

### Python Track
- **Greenfield**: Build a chaos engineering tool for testing audio services with escalating complexity from simple endpoint hammering to distributed failure coordination
- **Brownfield**: Refactor a 1000-line Jupyter notebook converted to .py with performance optimization and async streaming requirements

### Rust Track
- **Greenfield**: Create a zero-copy audio mixer with real-time performance requirements and lock-free threading
- **Brownfield**: Refactor unsafe performance-critical code to be safe while maintaining performance, adding SIMD and generic type support

### Elm Track
- **Greenfield**: Develop a DAW-style multitrack editor UI with draggable regions, real-time effects preview, and collaborative editing
- **Brownfield**: Decompose a monolithic Model structure into modules while implementing WebSocket handling and WebGL visualization

## Development Guidelines

### Implementation Requirements
- Each track must be solvable within 20-25 minutes using AI coding tools
- Projects should be challenging enough that they cannot be easily solved without proper AI context layering
- Greenfield and brownfield projects within each track should share the same codebase
- All projects should be loosely tied to audio/speech processing (Deepgram's domain)
- Each challenge should progressively escalate in complexity

### When Implementing Tracks

For Python implementations:
- Use virtual environments for dependency management
- Include requirements.txt for dependencies
- Consider using pytest for testing
- Document audio processing libraries used (e.g., numpy, scipy, librosa)

For Rust implementations:
- Use Cargo.toml for dependency management
- Include benchmarks for performance-critical code
- Document unsafe code requirements and invariants
- Consider using criterion for benchmarking

For Elm implementations:
- Use elm.json for package management
- Include elm-test for testing
- Document any JavaScript interop requirements
- Consider performance implications of large Models

## Challenge Progression

Each track follows a similar progression pattern:
1. **Start**: Simple, achievable baseline implementation
2. **Escalate**: Add complexity and real-world requirements
3. **Peak**: Introduce performance or architectural challenges
4. **Finale**: Add unexpected requirements that test adaptability

The challenges are designed to demonstrate AI tool capabilities in:
- Understanding existing code architecture
- Refactoring and optimization
- Implementing complex features with minimal context
- Handling performance-critical requirements
- Managing technical debt and legacy code