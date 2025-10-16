# Python Track: Deepgram QA & Observability

## Track Structure

Build a quality assurance platform for Deepgram's speech-to-text API:

1. **Greenfield: "The Deepgram Observatory"** - Monitoring and testing framework from scratch
2. **Brownfield: "The Benchmark Nightmare"** - Refactor a terrible benchmarking tool

Connection: Greenfield builds the infrastructure, brownfield refactors the analysis tool that plugs into it.

## Challenges

**Greenfield**
Phase 1 → Basic API wrapper logging to SQLite
Phase 2 → Add WER calculation and metrics
Phase 3 → Multi-model A/B testing
Phase 4 → Distributed monitoring with dashboards

**Brownfield**
Phase 1 → Understand and extract WER logic
Phase 2 → Vectorize and optimize (100x speedup target)
Phase 3 → Add async processing
Phase 4 → Real-time streaming mode

## Prerequisites

- Python 3.10+
- Deepgram API key
- Basic audio files for testing
- Ground truth transcripts

See [SETUP.md](./SETUP.md) for installation.

## Target Time

20-25 minutes total with AI assistance (hours without).

## Success Criteria

- API calls logged with latency and cost metrics
- WER calculated correctly (matches known benchmarks)
- Multi-model comparison working
- Benchmark tool processes 1000 files in seconds
- Real-time dashboard shows streaming metrics

## Presenter Notes

See [PRESENTER_GUIDE.md](./PRESENTER_GUIDE.md) for:
- 5-minute interval milestones
- Context layering strategy
- Recovery strategies for common pitfalls
