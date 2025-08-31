# bm_server

LLM Server Benchmarking Tools - Performance testing and visualization for language model servers.

## Overview

This repository contains tools for benchmarking LLM (Large Language Model) server performance by testing with progressively larger input sizes and visualizing the results.

## Features

- **Progressive input testing**: Automatically tests server with 1% to 100% of input file
- **Detailed metrics collection**: Captures prompt and prediction performance
- **Dual-axis visualization**: Shows both prompt and predicted tokens per second
- **Flexible configuration**: Customizable endpoints, token limits, and input sizes

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd bm_server

# Install dependencies (if needed)
pip install matplotlib requests
```

## Usage

### Running Benchmarks

```bash
# Basic usage - process a file with default settings
./benchmark.py path/to/input/file.cpp

# Save results to JSON
./benchmark.py input.cpp --output results.json

# Custom configuration
./benchmark.py input.cpp \
  --url http://localhost:8088/v1/chat/completions \
  --max-tokens 128 \
  --output results.json

# Test with specific line counts
./benchmark.py input.cpp --line-counts 100 500 1000 2000
```

### Visualizing Results

```bash
# Display plot from default out.json
python3 plot_benchmark.py

# Use custom input file
python3 plot_benchmark.py --input results.json

# Save plot to file
python3 plot_benchmark.py --save benchmark_plot.png
```

## Output Format

The benchmark tool generates JSON output with the following structure:
- `file`: Input filename
- `lines_used`: Number of lines processed
- `total_lines`: Total lines in file
- `max_tokens`: Maximum tokens requested
- `timings`: Performance metrics including:
  - `prompt_n`: Number of prompt tokens
  - `prompt_ms`: Time for prompt processing
  - `predicted_ms`: Time for prediction
  - `prompt_per_second`: Prompt tokens per second
  - `predicted_per_second`: Predicted tokens per second

## Visualization

The plot tool creates a dual Y-axis chart showing:
- **Blue line (left axis)**: Prompt tokens per second
- **Red line (right axis)**: Predicted tokens per second
- **X-axis**: Number of prompt tokens

This helps identify:
- Performance degradation with larger inputs
- Bottlenecks in prompt vs generation phases
- Optimal input sizes for your server configuration

## Requirements

- Python 3.x
- matplotlib (for plotting)
- requests (for API calls)
- Local or remote LLM server with compatible API

## License

[Add license information here]