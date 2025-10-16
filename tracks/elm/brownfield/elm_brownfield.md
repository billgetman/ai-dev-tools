Brownfield: "The Data Structure Disaster"
Version 1.0 of the Deepgram Results Browser - built in a hurry with terrible state management

Prototype Results Browser built quickly. State management is a nightmare: one massive Model, no organization, redundant data everywhere, inefficient data structures.

```elm
-- The Nightmare Model
type alias Model =
    { -- Transcription results stored multiple ways (redundancy!)
      results : List TranscriptionResult
    , resultsFiltered : List TranscriptionResult
    , resultsSorted : List TranscriptionResult
    , resultsBackup : List TranscriptionResult
    , resultsFinal : List TranscriptionResult

    -- Search state chaos
    , searchQuery : String
    , lastSearchQuery : String
    , tempSearchQuery : String
    , searchInProgress : Bool
    , shouldUpdateSearch : Bool
    , searchNeedsUpdate : Bool

    -- Comparison state mixed in
    , comparisonMode : Bool
    , comparisonResults : List TranscriptionResult
    , comparisonSelection : List Int  -- Indices into results list
    , tempComparisonSelection : List Int

    -- WebSocket state tangled up
    , webSocketConnected : Bool
    , webSocketUrl : String
    , webSocketMessages : List String
    , pendingMessages : List String

    -- UI state everywhere
    , currentPage : Int
    , itemsPerPage : Int
    , sortBy : String
    , sortDirection : String
    , hoveredResult : Maybe Int
    , selectedResult : Maybe Int
    , lastSelectedResult : Maybe Int

    -- Flags and counters (why?!)
    , updateCounter : Int
    , renderFlag : Bool
    , needsRerender : Bool
    , tempFlag : Bool

    -- And 50 more poorly-named fields...
    }

-- Plus this terrible update function (300+ lines)
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        SearchQueryChanged query ->
            { model
                | searchQuery = query
                , lastSearchQuery = model.searchQuery
                , tempSearchQuery = query
                , searchInProgress = True
                , shouldUpdateSearch = True
                , resultsFiltered = filterResults query model.results
                , resultsSorted = sortResults model.sortBy model.resultsFiltered
                , updateCounter = model.updateCounter + 1
                , renderFlag = True
            }
            |> (\m -> (m, Cmd.none))

        -- 50+ more message handlers with similar copy-paste logic
```

**Phase 1: Decompose into modules**
- Identify what data is actually needed vs derived
- Separate concerns: Results, Search, Comparison, WebSocket, UI
- Create proper modules with opaque types
- Eliminate redundant state

**Phase 2: Use proper data structures**
- Replace `List` with `Dict` for keyed access (results by ID)
- Use `Set` for selections instead of `List Int`
- Build indices for fast filtering/searching
- Eliminate O(n²) operations

**Phase 3: Refactor update function**
- Extract update logic into module-specific functions
- Use helper functions to reduce duplication
- Make impossible states impossible (type-driven design)
- Add proper message routing

**Phase 4: Optimize performance**
- Implement virtualized scrolling (only render visible items)
- Lazy evaluation for expensive computations
- Debounce search input
- Target: <16ms per update (60 fps)

**Phase 5: Add WebGL visualization**
- Use Ports for WebGL rendering (separate from Elm)
- Clean interface between Elm state and visualization
- Confidence score heatmap over time
- Keep visualization state isolated

**Success criteria:**
- Model reduced to essential state (no redundant copies)
- Proper module boundaries with opaque types
- O(1) lookups using Dict instead of O(n) List scans
- Update function under 50 lines (logic extracted to modules)
- Handles 1000+ results smoothly (<16ms updates)
- Type system prevents invalid states (no runtime crashes)
- Time-travel debugging works without breaking