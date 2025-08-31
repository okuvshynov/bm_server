# CLAUDE.md - Development Notes

## Project Overview
Benchmarking tools for testing LLM server performance with varying input sizes.

## Recent Changes (2025-08-31)
- Added `benchmark.py`: Main benchmarking script for testing LLM server with progressively larger inputs
- Added `plot_benchmark.py`: Visualization tool for benchmark results with dual Y-axis plotting
- Fixed JSON key mismatch issue in summary computation (prompt_ms/predicted_ms instead of non-existent duration keys)
- Replaced specific line counts option with `--splits` parameter for more intuitive control (1 = entire file, 100 = 100 test points)

## Technical Details

### benchmark.py
- Tests server with file inputs divided into configurable number of test points
- `--splits` parameter controls granularity (1 = entire file, 100 = test at 1%, 2%, ..., 100%)
- Sends requests to configurable API endpoint (default: http://localhost:8088/v1/chat/completions)
- Collects timing metrics and saves to JSON

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