# TICKET: Refactor Results Browser State Management

**ID**: UI-2847
**Priority**: Critical
**File**: `src/MainBrownfield.elm`

## Context

Results Browser v1.0 was built during a hackathon. It "works" but the state management is unsustainable. New features are impossible to add without breaking existing functionality. Performance degrades after ~100 results.

## Current Issues

1. **Massive Model** - 60+ fields, most redundant
2. **O(n) everywhere** - Using List for everything, including lookups by ID
3. **Copy-paste update** - 580+ lines, same logic repeated for each message
4. **No module boundaries** - Everything in one 845-line file
5. **Performance** - Visible lag with >100 results

## Quick Analysis

```elm
-- Current model has 7 copies of results:
results : List TranscriptionResult
resultsFiltered : List TranscriptionResult
resultsSorted : List TranscriptionResult
resultsBackup : List TranscriptionResult
resultsFinal : List TranscriptionResult
resultsTemp : List TranscriptionResult
resultsCache : List TranscriptionResult

-- Why not just:
results : Dict String TranscriptionResult  -- By ID
filteredIds : Set String                   -- Currently visible
```

## Requirements

1. **Decompose into modules** - Separate Results, Search, Comparison, UI state

2. **Use proper data structures**:
   - `Dict` for results (O(1) lookup by ID)
   - `Set` for selections
   - Computed properties instead of cached copies

3. **Simplify update** - Extract logic, use helper functions

4. **Performance target** - Handle 1000+ results smoothly

## Suggested Module Structure

```
Results.elm      -- Core data model
Search.elm       -- Search state and logic
Comparison.elm   -- Comparison mode
Pagination.elm   -- Page state
WebSocket.elm    -- WebSocket handling (if needed)
Main.elm         -- Orchestration only
```

## Refactoring Approach

Start with the data model:
```elm
-- Instead of 60 fields, something like:
type alias Model =
    { results : Results.Model
    , search : Search.Model
    , comparison : Comparison.Model
    , ui : UiState
    }

-- Where Results.Model is:
type Model = Model
    { items : Dict String TranscriptionResult
    , order : List String  -- Maintain sort order
    }
```

## Key Functions to Extract

- `filterResults` → Search module
- `sortResults` → Results module
- Pagination logic → Pagination module
- Comparison selection → Comparison module

## Definition of Done

- [ ] Model reduced to <15 essential fields
- [ ] Update function <100 lines
- [ ] O(1) lookups for results by ID
- [ ] Module boundaries with opaque types
- [ ] No redundant state copies
- [ ] 1000+ results render in <16ms

## Hints

- Start by identifying what's derived state vs essential state
- `resultsFiltered` is just `results |> applyFilters`
- Use `Dict.get` instead of `List.drop n |> List.head`
- The Elm Architecture works better with small, focused updates
- Consider using `lazy` for rendering large lists

---

*The "v1.0" was supposed to be a prototype. Three years later, here we are.*