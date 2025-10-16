module MainBrownfield exposing (main)

{-| Deepgram Results Browser v1.0 - "Built in a hurry"
DO NOT TOUCH THIS CODE - IT WORKS! (sort of)
- Dev, 2023
-}

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as Decode exposing (Decoder)
import Time


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }



-- THE NIGHTMARE MODEL (50+ redundant fields!)


type alias Model =
    { -- Transcription results stored multiple ways (redundancy!)
      results : List TranscriptionResult
    , resultsFiltered : List TranscriptionResult
    , resultsSorted : List TranscriptionResult
    , resultsBackup : List TranscriptionResult
    , resultsFinal : List TranscriptionResult
    , resultsTemp : List TranscriptionResult
    , resultsCache : List TranscriptionResult

    -- Search state chaos
    , searchQuery : String
    , lastSearchQuery : String
    , tempSearchQuery : String
    , previousSearchQuery : String
    , searchInProgress : Bool
    , shouldUpdateSearch : Bool
    , searchNeedsUpdate : Bool
    , searchDirty : Bool

    -- Comparison state mixed in
    , comparisonMode : Bool
    , comparisonActive : Bool
    , comparisonResults : List TranscriptionResult
    , comparisonSelection : List Int -- Indices into results list
    , tempComparisonSelection : List Int
    , lastComparisonSelection : List Int
    , comparisonCache : List TranscriptionResult

    -- WebSocket state tangled up
    , webSocketConnected : Bool
    , webSocketActive : Bool
    , webSocketUrl : String
    , webSocketMessages : List String
    , pendingMessages : List String
    , processedMessages : List String
    , messageQueue : List String

    -- UI state everywhere
    , currentPage : Int
    , lastPage : Int
    , tempPage : Int
    , itemsPerPage : Int
    , sortBy : String
    , lastSortBy : String
    , sortDirection : String
    , lastSortDirection : String
    , hoveredResult : Maybe Int
    , selectedResult : Maybe Int
    , lastSelectedResult : Maybe Int
    , tempSelectedResult : Maybe Int

    -- Flags and counters (why?!)
    , updateCounter : Int
    , renderCounter : Int
    , renderFlag : Bool
    , needsRerender : Bool
    , forceRerender : Bool
    , tempFlag : Bool
    , debugFlag : Bool
    , loadingFlag : Bool

    -- Filter state duplicated
    , filterModel : Maybe String
    , lastFilterModel : Maybe String
    , filterMinWer : Maybe Float
    , filterMaxWer : Maybe Float
    , filterMinDuration : Maybe Float
    , filterMaxDuration : Maybe Float
    , filterActive : Bool
    , lastFilterActive : Bool

    -- Even more unnecessary state
    , errorMessage : Maybe String
    , lastErrorMessage : Maybe String
    , warningMessage : Maybe String
    , statusMessage : String
    , tempStatusMessage : String
    , isLoading : Bool
    , wasLoading : Bool
    , loadingStartTime : Maybe Int
    , timestamp : Int
    , lastTimestamp : Int
    }


type alias TranscriptionResult =
    { id : String
    , model : String
    , duration : Float
    , cost : Float
    , wer : Float
    , timestamp : Int
    , transcript : Transcript
    }


type alias Transcript =
    { text : String
    , words : List Word
    }


type alias Word =
    { word : String
    , start : Float
    , end : Float
    , confidence : Float
    }



-- THE TERRIBLE UPDATE FUNCTION (300+ lines of copy-paste logic)


type Msg
    = NoOp
    | SearchQueryChanged String
    | SearchSubmitted
    | ClearSearch
    | SelectResult Int
    | ToggleComparison Int
    | SortByField String
    | ChangePage Int
    | FilterByModel String
    | FilterByWer Float Float
    | ToggleWebSocket
    | LoadResults
    | ResultsLoaded (Result Http.Error (List TranscriptionResult))
    | Tick Time.Posix


init : () -> ( Model, Cmd Msg )
init _ =
    ( { results = []
      , resultsFiltered = []
      , resultsSorted = []
      , resultsBackup = []
      , resultsFinal = []
      , resultsTemp = []
      , resultsCache = []
      , searchQuery = ""
      , lastSearchQuery = ""
      , tempSearchQuery = ""
      , previousSearchQuery = ""
      , searchInProgress = False
      , shouldUpdateSearch = False
      , searchNeedsUpdate = False
      , searchDirty = False
      , comparisonMode = False
      , comparisonActive = False
      , comparisonResults = []
      , comparisonSelection = []
      , tempComparisonSelection = []
      , lastComparisonSelection = []
      , comparisonCache = []
      , webSocketConnected = False
      , webSocketActive = False
      , webSocketUrl = ""
      , webSocketMessages = []
      , pendingMessages = []
      , processedMessages = []
      , messageQueue = []
      , currentPage = 0
      , lastPage = 0
      , tempPage = 0
      , itemsPerPage = 10
      , sortBy = "timestamp"
      , lastSortBy = ""
      , sortDirection = "desc"
      , lastSortDirection = ""
      , hoveredResult = Nothing
      , selectedResult = Nothing
      , lastSelectedResult = Nothing
      , tempSelectedResult = Nothing
      , updateCounter = 0
      , renderCounter = 0
      , renderFlag = False
      , needsRerender = False
      , forceRerender = False
      , tempFlag = False
      , debugFlag = False
      , loadingFlag = False
      , filterModel = Nothing
      , lastFilterModel = Nothing
      , filterMinWer = Nothing
      , filterMaxWer = Nothing
      , filterMinDuration = Nothing
      , filterMaxDuration = Nothing
      , filterActive = False
      , lastFilterActive = False
      , errorMessage = Nothing
      , lastErrorMessage = Nothing
      , warningMessage = Nothing
      , statusMessage = "Ready"
      , tempStatusMessage = ""
      , isLoading = False
      , wasLoading = False
      , loadingStartTime = Nothing
      , timestamp = 0
      , lastTimestamp = 0
      }
    , Cmd.none
    )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NoOp ->
            ( model, Cmd.none )

        SearchQueryChanged query ->
            -- Copy-paste nightmare begins!
            let
                newModel =
                    { model
                        | searchQuery = query
                        , lastSearchQuery = model.searchQuery
                        , tempSearchQuery = query
                        , previousSearchQuery = model.lastSearchQuery
                        , searchInProgress = True
                        , shouldUpdateSearch = True
                        , searchNeedsUpdate = True
                        , searchDirty = True
                        , updateCounter = model.updateCounter + 1
                        , renderFlag = True
                        , needsRerender = True
                        , forceRerender = True
                        , statusMessage = "Searching..."
                        , tempStatusMessage = model.statusMessage
                    }

                filtered =
                    filterResults query model.results

                sorted =
                    sortResults model.sortBy model.sortDirection filtered
            in
            ( { newModel
                | resultsFiltered = filtered
                , resultsSorted = sorted
                , resultsFinal = sorted
                , resultsTemp = filtered
                , renderCounter = model.renderCounter + 1
                , currentPage = 0
                , lastPage = model.currentPage
                , tempPage = 0
              }
            , Cmd.none
            )

        SearchSubmitted ->
            let
                newModel =
                    { model
                        | searchInProgress = False
                        , shouldUpdateSearch = False
                        , searchNeedsUpdate = False
                        , lastSearchQuery = model.searchQuery
                        , previousSearchQuery = model.lastSearchQuery
                        , updateCounter = model.updateCounter + 1
                        , statusMessage = "Search complete"
                        , tempStatusMessage = model.statusMessage
                        , renderFlag = False
                        , needsRerender = False
                    }

                filtered =
                    filterResults model.searchQuery model.results

                sorted =
                    sortResults model.sortBy model.sortDirection filtered
            in
            ( { newModel
                | resultsFiltered = filtered
                , resultsSorted = sorted
                , resultsFinal = sorted
                , resultsBackup = model.results
                , resultsCache = filtered
              }
            , Cmd.none
            )

        ClearSearch ->
            { model
                | searchQuery = ""
                , lastSearchQuery = model.searchQuery
                , tempSearchQuery = ""
                , previousSearchQuery = model.lastSearchQuery
                , searchInProgress = False
                , shouldUpdateSearch = False
                , searchNeedsUpdate = False
                , searchDirty = False
                , resultsFiltered = model.results
                , resultsSorted = model.results
                , resultsFinal = model.results
                , resultsTemp = model.results
                , resultsCache = model.results
                , currentPage = 0
                , lastPage = model.currentPage
                , updateCounter = model.updateCounter + 1
                , renderCounter = model.renderCounter + 1
                , statusMessage = "Search cleared"
                , tempStatusMessage = model.statusMessage
            }
                |> (\m -> ( m, Cmd.none ))

        SelectResult index ->
            let
                newModel =
                    { model
                        | selectedResult = Just index
                        , lastSelectedResult = model.selectedResult
                        , tempSelectedResult = Just index
                        , updateCounter = model.updateCounter + 1
                        , renderFlag = True
                    }
            in
            ( newModel, Cmd.none )

        ToggleComparison index ->
            let
                newSelection =
                    if List.member index model.comparisonSelection then
                        List.filter (\i -> i /= index) model.comparisonSelection

                    else
                        index :: model.comparisonSelection

                compResults =
                    List.filterMap
                        (\i -> getResultAt i model.resultsSorted)
                        newSelection

                isActive =
                    List.length newSelection > 0

                newModel =
                    { model
                        | comparisonSelection = newSelection
                        , lastComparisonSelection = model.comparisonSelection
                        , tempComparisonSelection = newSelection
                        , comparisonResults = compResults
                        , comparisonCache = model.comparisonResults
                        , comparisonMode = isActive
                        , comparisonActive = isActive
                        , updateCounter = model.updateCounter + 1
                        , renderCounter = model.renderCounter + 1
                        , renderFlag = True
                        , needsRerender = True
                    }
            in
            ( newModel, Cmd.none )

        SortByField field ->
            let
                newDirection =
                    if model.sortBy == field then
                        if model.sortDirection == "asc" then
                            "desc"

                        else
                            "asc"

                    else
                        "asc"

                sorted =
                    sortResults field newDirection model.resultsFiltered

                newModel =
                    { model
                        | sortBy = field
                        , lastSortBy = model.sortBy
                        , sortDirection = newDirection
                        , lastSortDirection = model.sortDirection
                        , resultsSorted = sorted
                        , resultsFinal = sorted
                        , resultsTemp = sorted
                        , resultsCache = model.resultsSorted
                        , updateCounter = model.updateCounter + 1
                        , renderCounter = model.renderCounter + 1
                        , currentPage = 0
                        , lastPage = model.currentPage
                    }
            in
            ( newModel, Cmd.none )

        ChangePage page ->
            { model
                | currentPage = page
                , lastPage = model.currentPage
                , tempPage = page
                , updateCounter = model.updateCounter + 1
                , renderFlag = True
            }
                |> (\m -> ( m, Cmd.none ))

        FilterByModel modelName ->
            let
                newFilter =
                    if model.filterModel == Just modelName then
                        Nothing

                    else
                        Just modelName

                filtered =
                    if newFilter == Nothing then
                        model.results

                    else
                        List.filter (\r -> r.model == modelName) model.results

                sorted =
                    sortResults model.sortBy model.sortDirection filtered

                newModel =
                    { model
                        | filterModel = newFilter
                        , lastFilterModel = model.filterModel
                        , filterActive = newFilter /= Nothing
                        , lastFilterActive = model.filterActive
                        , resultsFiltered = filtered
                        , resultsSorted = sorted
                        , resultsFinal = sorted
                        , resultsTemp = filtered
                        , resultsCache = model.resultsFiltered
                        , currentPage = 0
                        , lastPage = model.currentPage
                        , updateCounter = model.updateCounter + 1
                        , renderCounter = model.renderCounter + 1
                    }
            in
            ( newModel, Cmd.none )

        FilterByWer minWer maxWer ->
            let
                filtered =
                    List.filter
                        (\r -> r.wer >= minWer && r.wer <= maxWer)
                        model.results

                sorted =
                    sortResults model.sortBy model.sortDirection filtered

                newModel =
                    { model
                        | filterMinWer = Just minWer
                        , filterMaxWer = Just maxWer
                        , filterActive = True
                        , lastFilterActive = model.filterActive
                        , resultsFiltered = filtered
                        , resultsSorted = sorted
                        , resultsFinal = sorted
                        , resultsTemp = filtered
                        , currentPage = 0
                        , lastPage = model.currentPage
                        , updateCounter = model.updateCounter + 1
                    }
            in
            ( newModel, Cmd.none )

        ToggleWebSocket ->
            let
                newConnected =
                    not model.webSocketConnected

                newModel =
                    { model
                        | webSocketConnected = newConnected
                        , webSocketActive = newConnected
                        , updateCounter = model.updateCounter + 1
                        , statusMessage =
                            if newConnected then
                                "WebSocket connected"

                            else
                                "WebSocket disconnected"
                        , tempStatusMessage = model.statusMessage
                    }
            in
            ( newModel, Cmd.none )

        LoadResults ->
            ( { model
                | isLoading = True
                , wasLoading = model.isLoading
                , loadingFlag = True
                , statusMessage = "Loading results..."
                , tempStatusMessage = model.statusMessage
              }
            , Cmd.none
            )

        ResultsLoaded (Ok results) ->
            let
                sorted =
                    sortResults model.sortBy model.sortDirection results

                newModel =
                    { model
                        | results = results
                        , resultsBackup = model.results
                        , resultsFiltered = results
                        , resultsSorted = sorted
                        , resultsFinal = sorted
                        , resultsTemp = results
                        , resultsCache = model.results
                        , isLoading = False
                        , wasLoading = model.isLoading
                        , loadingFlag = False
                        , statusMessage = "Results loaded"
                        , tempStatusMessage = model.statusMessage
                        , updateCounter = model.updateCounter + 1
                        , renderCounter = model.renderCounter + 1
                    }
            in
            ( newModel, Cmd.none )

        ResultsLoaded (Err error) ->
            ( { model
                | isLoading = False
                , wasLoading = model.isLoading
                , loadingFlag = False
                , errorMessage = Just "Failed to load results"
                , lastErrorMessage = model.errorMessage
                , statusMessage = "Error loading results"
                , tempStatusMessage = model.statusMessage
                , updateCounter = model.updateCounter + 1
              }
            , Cmd.none
            )

        Tick time ->
            let
                posixTime =
                    Time.posixToMillis time
            in
            ( { model
                | timestamp = posixTime
                , lastTimestamp = model.timestamp
                , updateCounter = model.updateCounter + 1
              }
            , Cmd.none
            )



-- HELPER FUNCTIONS (also terrible)


filterResults : String -> List TranscriptionResult -> List TranscriptionResult
filterResults query results =
    if String.isEmpty query then
        results

    else
        let
            lowerQuery =
                String.toLower query
        in
        List.filter
            (\result ->
                String.contains lowerQuery (String.toLower result.transcript.text)
            )
            results


sortResults : String -> String -> List TranscriptionResult -> List TranscriptionResult
sortResults field direction results =
    let
        sorted =
            case field of
                "timestamp" ->
                    List.sortBy .timestamp results

                "wer" ->
                    List.sortBy .wer results

                "duration" ->
                    List.sortBy .duration results

                "cost" ->
                    List.sortBy .cost results

                _ ->
                    results
    in
    if direction == "desc" then
        List.reverse sorted

    else
        sorted


getResultAt : Int -> List TranscriptionResult -> Maybe TranscriptionResult
getResultAt index results =
    List.drop index results |> List.head



-- VIEW (also a mess)


view : Model -> Html Msg
view model =
    div [ style "padding" "20px", style "font-family" "sans-serif" ]
        [ h1 [] [ text "Deepgram Results Browser v1.0" ]
        , div [ style "margin" "20px 0" ]
            [ text ("Status: " ++ model.statusMessage)
            , text (" | Results: " ++ String.fromInt (List.length model.resultsFinal))
            , text (" | Page: " ++ String.fromInt (model.currentPage + 1))
            , text (" | Updates: " ++ String.fromInt model.updateCounter)
            ]
        , viewSearchBox model
        , viewFilters model
        , viewResults model
        , viewComparison model
        , viewDebugInfo model
        ]


viewSearchBox : Model -> Html Msg
viewSearchBox model =
    div [ style "margin" "20px 0" ]
        [ input
            [ type_ "text"
            , placeholder "Search transcripts..."
            , value model.searchQuery
            , onInput SearchQueryChanged
            , style "width" "300px"
            , style "padding" "8px"
            ]
            []
        , button
            [ onClick SearchSubmitted
            , style "margin-left" "10px"
            , style "padding" "8px 16px"
            ]
            [ text "Search" ]
        , button
            [ onClick ClearSearch
            , style "margin-left" "10px"
            , style "padding" "8px 16px"
            ]
            [ text "Clear" ]
        ]


viewFilters : Model -> Html Msg
viewFilters model =
    div [ style "margin" "20px 0" ]
        [ button
            [ onClick (FilterByModel "nova-2")
            , style "margin-right" "10px"
            , style "padding" "8px 16px"
            ]
            [ text "Nova-2" ]
        , button
            [ onClick (FilterByModel "nova-3")
            , style "margin-right" "10px"
            , style "padding" "8px 16px"
            ]
            [ text "Nova-3" ]
        , button
            [ onClick (FilterByModel "whisper")
            , style "margin-right" "10px"
            , style "padding" "8px 16px"
            ]
            [ text "Whisper" ]
        ]


viewResults : Model -> Html Msg
viewResults model =
    let
        startIndex =
            model.currentPage * model.itemsPerPage

        endIndex =
            startIndex + model.itemsPerPage

        pageResults =
            List.drop startIndex model.resultsFinal
                |> List.take model.itemsPerPage
    in
    div []
        [ div [ style "margin" "20px 0" ]
            [ button [ onClick (SortByField "timestamp") ]
                [ text "Sort by Time" ]
            , button [ onClick (SortByField "wer"), style "margin-left" "10px" ]
                [ text "Sort by WER" ]
            , button [ onClick (SortByField "duration"), style "margin-left" "10px" ]
                [ text "Sort by Duration" ]
            ]
        , div [] (List.indexedMap viewResult pageResults)
        , viewPagination model
        ]


viewResult : Int -> TranscriptionResult -> Html Msg
viewResult index result =
    div
        [ style "border" "1px solid #ccc"
        , style "margin" "10px 0"
        , style "padding" "15px"
        , style "background" "#f9f9f9"
        ]
        [ div [ style "font-weight" "bold" ]
            [ text ("ID: " ++ result.id ++ " | Model: " ++ result.model) ]
        , div [ style "margin" "5px 0" ]
            [ text result.transcript.text ]
        , div [ style "font-size" "12px", style "color" "#666" ]
            [ text ("WER: " ++ String.fromFloat result.wer)
            , text (" | Duration: " ++ String.fromFloat result.duration ++ "s")
            , text (" | Cost: $" ++ String.fromFloat result.cost)
            ]
        , button
            [ onClick (SelectResult index)
            , style "margin-top" "10px"
            , style "padding" "4px 8px"
            ]
            [ text "Select" ]
        , button
            [ onClick (ToggleComparison index)
            , style "margin-left" "10px"
            , style "padding" "4px 8px"
            ]
            [ text "Compare" ]
        ]


viewPagination : Model -> Html Msg
viewPagination model =
    let
        totalPages =
            ceiling (toFloat (List.length model.resultsFinal) / toFloat model.itemsPerPage)
    in
    div [ style "margin" "20px 0" ]
        [ button
            [ onClick (ChangePage (model.currentPage - 1))
            , disabled (model.currentPage == 0)
            , style "padding" "8px 16px"
            ]
            [ text "Previous" ]
        , span [ style "margin" "0 20px" ]
            [ text ("Page " ++ String.fromInt (model.currentPage + 1) ++ " of " ++ String.fromInt totalPages) ]
        , button
            [ onClick (ChangePage (model.currentPage + 1))
            , disabled (model.currentPage >= totalPages - 1)
            , style "padding" "8px 16px"
            ]
            [ text "Next" ]
        ]


viewComparison : Model -> Html Msg
viewComparison model =
    if model.comparisonActive then
        div
            [ style "margin" "30px 0"
            , style "padding" "20px"
            , style "border" "2px solid #007bff"
            , style "background" "#e7f3ff"
            ]
            [ h2 [] [ text "Comparison Mode" ]
            , div [] [ text ("Comparing " ++ String.fromInt (List.length model.comparisonResults) ++ " results") ]
            , div [] (List.map viewComparisonResult model.comparisonResults)
            ]

    else
        div [] []


viewComparisonResult : TranscriptionResult -> Html Msg
viewComparisonResult result =
    div
        [ style "margin" "10px 0"
        , style "padding" "10px"
        , style "background" "white"
        ]
        [ div [ style "font-weight" "bold" ] [ text result.model ]
        , div [] [ text result.transcript.text ]
        , div [ style "font-size" "12px" ]
            [ text ("WER: " ++ String.fromFloat result.wer ++ " | Cost: $" ++ String.fromFloat result.cost) ]
        ]


viewDebugInfo : Model -> Html Msg
viewDebugInfo model =
    if model.debugFlag then
        div
            [ style "margin-top" "40px"
            , style "padding" "20px"
            , style "background" "#f0f0f0"
            , style "font-family" "monospace"
            , style "font-size" "12px"
            ]
            [ h3 [] [ text "Debug Info" ]
            , div [] [ text ("Update Counter: " ++ String.fromInt model.updateCounter) ]
            , div [] [ text ("Render Counter: " ++ String.fromInt model.renderCounter) ]
            , div [] [ text ("Results: " ++ String.fromInt (List.length model.results)) ]
            , div [] [ text ("Filtered: " ++ String.fromInt (List.length model.resultsFiltered)) ]
            , div [] [ text ("Sorted: " ++ String.fromInt (List.length model.resultsSorted)) ]
            , div [] [ text ("Final: " ++ String.fromInt (List.length model.resultsFinal)) ]
            ]

    else
        div [] []


subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every 1000 Tick
