# Elm Track Presenter Guide

Target time: 20-25 minutes

**Note**: Start with brownfield (refactoring), then greenfield (features). Need clean foundation before adding complexity.

## Part 1: Brownfield (10-13 min)

### Phase 1: Understand the Mess (0-3 min)

Prompt AI:
```
Analyze src/MainBrownfield.elm. What's wrong with the Model? What data is actually needed
vs redundant? This is a Deepgram transcription results browser.
```

Context: `src/MainBrownfield.elm`, `brownfield/elm_brownfield.md`, `data/sample_results.json`

Expected: Identification of redundant fields (results, resultsFiltered, resultsSorted, resultsBackup), derived data, module boundaries, Dict vs List recommendations.

### Phase 2: Decompose into Modules (3-6 min)

Prompt AI:
```
Refactor into separate modules: Results (transcription data), Search (filter state),
Comparison (side-by-side), UI (pagination, selection). Use opaque types - expose type but
not constructor. Each module exports only what's needed.
```

Context: Current code, opaque type pattern
```elm
-- In Results.elm
type Results = Results (Dict String TranscriptionResult)
-- Export: Results, empty, insert, get
-- Don't export: constructor
```

Expected: `src/Results.elm`, `src/Search.elm`, `src/Comparison.elm`, `src/UI.elm`, updated `src/Main.elm`.

Test compilation:
```bash
elm make src/Main.elm --output=public/elm.js
```

### Phase 3: Optimize Data Structures (6-9 min)

Prompt AI:
```
Change Results module from List to Dict keyed by result ID for O(log n) lookups instead
of O(n). Use Set for selected IDs instead of List Int. Update all functions.
```

Context: Current `Results.elm`, requirement to handle 1000+ results efficiently.

Expected:
```elm
-- Before: O(n)
type Results = Results (List TranscriptionResult)
get id (Results list) = List.filter (\r -> r.id == id) list |> List.head

-- After: O(log n)
type Results = Results (Dict String TranscriptionResult)
get id (Results dict) = Dict.get id dict
```

### Phase 4: Clean Update Function (9-12 min)

Prompt AI:
```
Extract update logic into modules (Results.update, Search.update, etc.). Use custom
types for states instead of Bool flags. Make impossible states impossible.
```

Context: Current update function, impossible states pattern
```elm
-- Bad: Can be loading AND have error
{ loading : Bool, error : Maybe String }

-- Good: Can only be in one state
type LoadingState = Loading | Loaded Results | Failed String
```

Expected:
```elm
-- Before: 300 lines
update msg model =
    case msg of
        SearchQueryChanged query ->
            { model | searchQuery = query, lastSearchQuery = model.searchQuery, ... }

-- After: Delegated
update msg model =
    case msg of
        SearchMsg searchMsg ->
            let (newSearch, results) = Search.update searchMsg model.search model.results
            in ( { model | search = newSearch }, Cmd.none )
```

### Phase 5: Performance Optimization (Optional, 12-13 min)

Prompt AI:
```
Use Html.Lazy to prevent unnecessary re-renders. Implement virtualized scrolling for
visible items only. Target <16ms updates for 60fps.
```

Expected:
```elm
import Html.Lazy

view model =
    div []
        [ Html.Lazy.lazy viewSearch model.search
        , Html.Lazy.lazy2 viewResults model.results model.ui
        ]
```

## Part 2: Greenfield (10-12 min)

### Phase 1: Display Single Result (0-3 min)

Prompt AI:
```
Create view for single transcription result: transcript text, model name, duration, cost,
WER, timestamp. Highlight words with confidence <0.7 in yellow.
```

Context: Refactored `Results.elm`, `data/sample_results.json`

Expected: JSON decoder for TranscriptionResult, view function, confidence highlighting.

### Phase 2: Search and Filter (3-6 min)

Prompt AI:
```
Add search functionality filtering by transcript text. Add filters for: model type
(nova-2, nova-3, whisper), date range, WER threshold. Results update as user types.
```

Context: `Search.elm` module, `Results.elm`

Expected:
```elm
type alias Search =
    { query : String
    , modelFilter : Maybe ModelType
    , dateRange : Maybe (Time.Posix, Time.Posix)
    , maxWer : Maybe Float
    }

search : Search -> Results -> List TranscriptionResult
search config results =
    Results.toList results
        |> List.filter (matchesQuery config.query)
        |> List.filter (matchesModel config.modelFilter)
        |> List.filter (matchesWer config.maxWer)
```

### Phase 3: Side-by-Side Comparison (6-9 min)

Prompt AI:
```
Implement comparison mode. Select 2-4 results (different models, same audio) and view
side-by-side. Show diff highlighting where transcripts differ. Display metrics table.
```

Context: `Comparison.elm`, simple word-by-word diff algorithm

Expected:
```elm
type alias Comparison =
    { selected : Set String
    , mode : ComparisonMode
    }

type ComparisonMode
    = NotComparing
    | Comparing (List TranscriptionResult)

viewComparison comparison =
    case comparison.mode of
        NotComparing -> text ""
        Comparing results -> div [] [ viewDiff results, viewMetricsTable results ]
```

### Phase 4: WebSocket Streaming (9-12 min)

Prompt AI:
```
Add WebSocket for streaming real-time transcription results. Use Ports to communicate
with JavaScript. Results appear as they arrive. Show 'Live' indicator when streaming.
```

Context: Port pattern, `public/index.html` JavaScript wrapper
```elm
port connectWebSocket : String -> Cmd msg
port receiveWebSocketMessage : (String -> msg) -> Sub msg
```

Expected:
```elm
port connectWebSocket : String -> Cmd msg
port receiveWebSocketMessage : (String -> msg) -> Sub msg

type Msg = ConnectStream String | StreamMessage String | ...

update msg model =
    case msg of
        ConnectStream url -> ( { model | streaming = True }, connectWebSocket url )
        StreamMessage json ->
            case Decode.decodeString transcriptDecoder json of
                Ok result -> ( { model | results = Results.insert result model.results }, Cmd.none )

subscriptions model =
    if model.streaming then receiveWebSocketMessage StreamMessage else Sub.none
```

## Context Layering

Incremental context:
1. Start: Terrible code, challenge spec
2. Add: Refactored modules, performance requirements
3. Provide: Sample JSON, UI requirements
4. Show: Port pattern for JS interop

## Common Issues

**Type errors**: Remove type annotation temporarily, compiler will infer. Show error to AI.
**Circular dependencies**: Extract shared types to separate module, use opaque types.
**JSON decoder fails**: Test in `elm repl`, add `Debug.log`, fix decoder to match JSON.
**Performance slow**: Use browser profiler, add `Html.Lazy` to expensive views.
**Ports not working**: Check JS console, verify port names match exactly.

## Success Criteria

Brownfield:
- [ ] Model decomposed into modules
- [ ] No redundant state
- [ ] Proper data structures (Dict, Set)
- [ ] Clean update function (<50 lines)
- [ ] Handles 1000+ results smoothly
- [ ] Type system prevents invalid states

Greenfield:
- [ ] Clean UI for results
- [ ] Working search and filter
- [ ] Side-by-side comparison
- [ ] WebSocket streaming (or attempted)
- [ ] JSON decoders working

Overall:
- [ ] Refactoring without runtime errors
- [ ] Type system catching bugs
- [ ] Completed in ~20-25 minutes
- [ ] No exceptions thrown

Done in ~20-25 minutes.
