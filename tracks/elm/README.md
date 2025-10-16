# Elm Track: Deepgram Results Explorer

## Track Structure

Build a web application for exploring Deepgram transcription results:

1. **Brownfield: "The Data Structure Disaster"** - Inherit messy prototype with terrible state management
2. **Greenfield: "The Results Browser"** - Refactor, then build out proper features

Connection: Brownfield is the messy v1.0 that someone built quickly. Clean it up, then add new features on the solid foundation.

Note: We do brownfield first (unusual) because you want a clean foundation before adding complex features in Elm.

## Challenges

**Brownfield**
Phase 1 → Decompose into modules (Results, Search, Comparison, WebSocket, UI)
Phase 2 → Use proper data structures (Dict, Set instead of List)
Phase 3 → Refactor update function (extract logic to modules)
Phase 4 → Optimize performance (<16ms updates for 60fps)
Phase 5 → Add WebGL visualization via Ports

**Greenfield**
Phase 1 → Display single transcription with metadata
Phase 2 → Search/filter across multiple results
Phase 3 → Side-by-side comparison of different models
Phase 4 → Live streaming via WebSocket

## Prerequisites

- Elm 0.19.1
- Node.js (for dev server)
- Sample Deepgram JSON responses

See [SETUP.md](./SETUP.md) for installation.

## Target Time

20-25 minutes total with AI assistance (hours without).

## Success Criteria

- Type system catches all refactoring errors (no runtime exceptions)
- Model has no redundant state (single source of truth)
- O(1) lookups using Dict instead of O(n) List scans
- Handles 1000+ results without lag (<16ms updates)
- Clean module boundaries with opaque types
- Search/filter/comparison features work smoothly
- WebSocket integration via Ports works correctly

## Key Message

No runtime exceptions + refactoring confidence. If it compiles, it works.

## Presenter Notes

See [PRESENTER_GUIDE.md](./PRESENTER_GUIDE.md) for:
- Phase-by-phase progression with timing
- How to demonstrate "impossible states made impossible"
- Common Elm patterns and pitfalls
