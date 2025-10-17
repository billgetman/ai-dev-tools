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

## Performance Notes

### The Problem with Lists

The brownfield code uses `List` for everything, causing major performance issues:

```elm
-- Current code (O(n) for every lookup):
getResultById : String -> List TranscriptionResult -> Maybe TranscriptionResult
getResultById id results =
    List.filter (\r -> r.id == id) results |> List.head

-- With Dict (O(log n)):
getResultById : String -> Dict String TranscriptionResult -> Maybe TranscriptionResult
getResultById id results =
    Dict.get id results
```

### Why 7 Copies of the Same Data?

The Model has:
- `results` - Original data
- `resultsFiltered` - After search (can be computed)
- `resultsSorted` - After sort (can be computed)
- `resultsBackup` - Copy of original (why?)
- `resultsFinal` - Another copy
- `resultsTemp` - Temporary copy
- `resultsCache` - Yet another copy

This should just be:
- `results : Dict String TranscriptionResult` - The data
- `searchQuery : String` - Current search
- `sortField : SortField` - Current sort

Everything else is derived: `results |> applySearch searchQuery |> applySort sortField`

### Performance Impact

With 10 results: ~1ms updates (invisible)
With 100 results: ~20ms updates (noticeable lag)
With 1000 results: ~200ms updates (painful)

Test with `data/large_dataset.json` to see the difference.

## Key Message

No runtime exceptions + refactoring confidence. If it compiles, it works.
