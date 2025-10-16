Greenfield: "The Deepgram Observatory"
Real-time monitoring and testing framework for Deepgram API

**Phase 1: Request wrapper**
- Wrap Deepgram SDK to log all API calls
- Track: latency, response codes, model, duration, cost
- Store in SQLite

**Phase 2: Metrics & accuracy**
- Calculate WER on test audio with known ground truth
- Track accuracy trends
- Prometheus-compatible metrics endpoint
- Cost analysis per request/project

**Phase 3: Multi-model comparison**
- Run same audio through different models (Nova-2, Nova-3, Flux)
- A/B testing framework
- Benchmark against ground truth with Levenshtein distance
- Alert when WER spikes above threshold

**Phase 4: Distributed monitoring**
- Monitor multiple Deepgram deployments (cloud + self-hosted)
- Synthetic audio testing for edge cases
- Dashboards: accuracy heatmaps, cost analysis, latency percentiles
- Auto-scaling recommendations from `engine_active_requests` metrics