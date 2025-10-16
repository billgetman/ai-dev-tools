Greenfield: "The Results Browser"
UI for exploring and comparing Deepgram transcription results

**Phase 1: Display single result**
- Show transcription text with metadata
- Display: duration, model used (nova-2, nova-3), cost, WER
- Confidence score highlighting (low confidence = yellow/red)
- Basic Elm Architecture (Model, Msg, update, view)
- Parse JSON from Deepgram API response

**Phase 2: Search and filter**
- Load multiple transcription results from JSON
- Search by text content, filter by model/date/WER
- Sort by confidence, duration, cost
- Timeline view showing results over time
- Pagination for large result sets

**Phase 3: Compare transcriptions side-by-side**
- Select 2-4 transcriptions of the same audio (different models/settings)
- Side-by-side diff view highlighting differences
- Metrics comparison table (WER, latency, cost per model)
- Word-level alignment showing where transcripts diverge
- Visual confidence comparison (charts/graphs)

**Phase 4: Live streaming**
- WebSocket integration (via Ports to JavaScript)
- Real-time results appear as Deepgram processes audio
- Streaming progress indicator
- Handle incremental updates (partial results)
- Auto-refresh results list when new data arrives