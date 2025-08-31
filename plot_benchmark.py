#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

def plot_benchmark_results(json_file):
    """Plot benchmark results with dual Y-axes."""
    
    # Read the JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract the data points
    prompt_n_values = []
    prompt_per_second_values = []
    predicted_per_second_values = []
    
    for result in data:
        if 'timings' in result and result['timings']:
            timings = result['timings']
            if 'prompt_n' in timings and 'prompt_per_second' in timings and 'predicted_per_second' in timings:
                prompt_n_values.append(timings['prompt_n'])
                prompt_per_second_values.append(timings['prompt_per_second'])
                predicted_per_second_values.append(timings['predicted_per_second'])
    
    if not prompt_n_values:
        print("No valid data points found in the JSON file")
        return
    
    # Create the plot with dual Y-axes
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot prompt_per_second on the left Y-axis
    color1 = 'tab:blue'
    ax1.set_xlabel('Prompt N (number of tokens)', fontsize=12)
    ax1.set_ylabel('Prompt per Second', color=color1, fontsize=12)
    line1 = ax1.plot(prompt_n_values, prompt_per_second_values, color=color1, 
                     marker='o', markersize=3, label='Prompt per Second', linewidth=1.5)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    
    # Create second Y-axis for predicted_per_second
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Predicted per Second', color=color2, fontsize=12)
    line2 = ax2.plot(prompt_n_values, predicted_per_second_values, color=color2,
                     marker='s', markersize=3, label='Predicted per Second', linewidth=1.5)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Add title
    plt.title('Benchmark Performance: Prompt vs Predicted Tokens per Second', fontsize=14, pad=20)
    
    # Add legend combining both lines
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')
    
    # Format the plot
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Show the plot
    plt.show()
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Data points: {len(prompt_n_values)}")
    print(f"Prompt N range: {min(prompt_n_values)} - {max(prompt_n_values)}")
    print(f"Prompt/s range: {min(prompt_per_second_values):.1f} - {max(prompt_per_second_values):.1f}")
    print(f"Predicted/s range: {min(predicted_per_second_values):.1f} - {max(predicted_per_second_values):.1f}")

def main():
    parser = argparse.ArgumentParser(description='Plot benchmark results from JSON file')
    parser.add_argument('--input', default='out.json', 
                        help='Input JSON file (default: out.json)')
    parser.add_argument('--save', help='Save plot to file instead of displaying')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Error: File {args.input} not found")
        return
    
    # Create the plot
    plot_benchmark_results(args.input)
    
    # Save if requested
    if args.save:
        plt.savefig(args.save, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {args.save}")

if __name__ == "__main__":
    main()