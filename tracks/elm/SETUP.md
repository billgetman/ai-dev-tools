# Elm Track Setup

## Requirements

- Elm 0.19.1
- Node.js 14+
- ~500MB disk

## Install Elm

```bash
# macOS
brew install elm

# Or via npm
npm install -g elm

# Verify
elm --version  # Should show 0.19.1
```

## Install Tools

```bash
npm install -g elm-live elm-format elm-test
```

## Initialize Project

```bash
cd tracks/elm
elm init  # Creates elm.json
```

Configure `elm.json`:
```json
{
    "type": "application",
    "source-directories": ["src"],
    "elm-version": "0.19.1",
    "dependencies": {
        "direct": {
            "elm/browser": "1.0.2",
            "elm/core": "1.0.5",
            "elm/html": "1.0.0",
            "elm/json": "1.1.3",
            "elm/http": "2.0.0",
            "elm/time": "1.0.0"
        }
    }
}
```

Install dependencies:
```bash
elm install elm/browser
elm install elm/json
elm install elm/http
elm install elm/time
```

## Sample Data

Create `data/sample_results.json`:
```json
[
  {
    "id": "result_001",
    "model": "nova-2",
    "duration": 5.4,
    "cost": 0.0108,
    "wer": 0.03,
    "transcript": {
      "text": "Yeah. Life moves pretty fast.",
      "words": [
        {"word": "Yeah", "start": 0.0, "end": 0.3, "confidence": 0.99}
      ]
    }
  }
]
```

Add 20-30 entries for testing search/filter.

## HTML Wrapper

Create `public/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Deepgram Results Explorer</title>
</head>
<body>
    <div id="app"></div>
    <script src="/elm.js"></script>
    <script>
        var app = Elm.Main.init({
            node: document.getElementById('app')
        });

        // WebSocket port (for finale)
        // app.ports.connectWebSocket.subscribe(function(url) {
        //     var ws = new WebSocket(url);
        //     ws.onmessage = function(e) {
        //         app.ports.receiveWebSocketMessage.send(e.data);
        //     };
        // });
    </script>
</body>
</html>
```

## Starter Code

Create `src/Main.elm`:
```elm
module Main exposing (main)

import Browser
import Html exposing (Html, div, h1, text)

main =
    Browser.element
        { init = \_ -> ({ message = "Deepgram Results Explorer" }, Cmd.none)
        , view = \model -> div [] [ h1 [] [ text model.message ] ]
        , update = \msg model -> (model, Cmd.none)
        , subscriptions = \_ -> Sub.none
        }
```

## Create Brownfield Starting Code

Before demo, create `src/MainBrownfield.elm` with the terrible Model from brownfield spec:

```elm
type alias Model =
    { results : List TranscriptionResult
    , resultsFiltered : List TranscriptionResult
    , resultsSorted : List TranscriptionResult
    , resultsBackup : List TranscriptionResult
    , searchQuery : String
    , lastSearchQuery : String
    -- ... 50 more redundant fields
    }
```

See brownfield spec for full implementation.

## Run Dev Server

```bash
cd tracks/elm
elm-live src/Main.elm --open -- --output=public/elm.js
```

Auto-compiles and reloads on file changes.

Manual compilation:
```bash
elm make src/Main.elm --output=public/elm.js
python3 -m http.server 8000 --directory public
```

## Verify

```bash
elm --version
elm make src/Main.elm --output=/dev/null
```

Ready for demo.
