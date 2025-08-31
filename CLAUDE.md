# CLAUDE.md - Development Notes

## Project Overview
Benchmarking tools for testing LLM server performance with varying input sizes.

## Recent Changes (2025-08-31)
- Added `benchmark.py`: Main benchmarking script for testing LLM server with progressively larger inputs
- Added `plot_benchmark.py`: Visualization tool for benchmark results with dual Y-axis plotting
- Fixed JSON key mismatch issue in summary computation (prompt_ms/predicted_ms instead of non-existent duration keys)

## Technical Details

### benchmark.py
- Tests server with file inputs from 1% to 100% of total lines
- Sends requests to configurable API endpoint (default: http://localhost:8088/v1/chat/completions)
- Collects timing metrics and saves to JSON
- Supports custom line counts or automatic percentage-based testing

### plot_benchmark.py
- Reads benchmark results from JSON
- Creates dual Y-axis plot:
  - Left axis: prompt tokens per second
  - Right axis: predicted tokens per second
  - X-axis: number of prompt tokens
- Helps identify performance bottlenecks and scaling characteristics

## Testing Commands
```bash
# Run lint and typecheck if available
# Note: No specific lint/typecheck commands configured yet
# Ask user for these commands if needed
```

## Known Issues
- No lint or typecheck configuration set up yet
- Consider adding these for code quality checks