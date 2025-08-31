#!/usr/bin/env python3

import json
import sys
import requests
import argparse
from pathlib import Path


def send_request(content, url, max_tokens):
    """Send request to the API with the given content."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer no-key"
    }
    
    payload = {
        "model": "local_model",
        "max_tokens": max_tokens,
        "cache_prompt": False,
        "messages": [{
            "role": "user",
            "content": f"Explain what this library is doing and show some usage examples:\n{content}"
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def process_file_versions(filename, url, max_tokens, line_counts=None):
    """Process multiple versions of the file with different line counts."""
    file_path = Path(filename)
    
    if not file_path.exists():
        print(f"Error: File {filename} does not exist")
        return
    
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    total_lines = len(all_lines)
    
    # Default line counts if not specified
    if line_counts is None:
        # Generate versions: 1%, 2%, 3%, ..., 100% of file (100 versions)
        percentages = [i / 100.0 for i in range(1, 101)]
        line_counts = [max(1, int(total_lines * p)) for p in percentages]
        # Remove duplicates and sort
        line_counts = sorted(set(line_counts))
    
    results = []
    
    for n_lines in line_counts:
        if n_lines > total_lines:
            n_lines = total_lines
        
        content = ''.join(all_lines[:n_lines])
        
        print(f"\nProcessing {filename} with first {n_lines}/{total_lines} lines...")
        print(f"Max tokens: {max_tokens}")
        
        try:
            response = send_request(content, url, max_tokens)
            
            # Extract timings if available
            timings = response.get('timings', {})
            
            result = {
                'file': filename,
                'lines_used': n_lines,
                'total_lines': total_lines,
                'max_tokens': max_tokens,
                'timings': timings
            }
            
            results.append(result)
            
            # Print timings
            if timings:
                print(f"Timings: {json.dumps(timings, indent=2)}")
            
        except Exception as e:
            print(f"Error processing {n_lines} lines: {e}")
            results.append({
                'file': filename,
                'lines_used': n_lines,
                'total_lines': total_lines,
                'max_tokens': max_tokens,
                'error': str(e)
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Explain code library using AI API')
    parser.add_argument('filename', help='Input file to process')
    parser.add_argument('--url', default='http://localhost:8088/v1/chat/completions',
                        help='API endpoint URL (default: http://localhost:8088/v1/chat/completions)')
    parser.add_argument('--max-tokens', type=int, default=64,
                        help='Maximum tokens for response (default: 64)')
    parser.add_argument('--line-counts', type=int, nargs='*',
                        help='Specific line counts to test (e.g., 10 20 50 100). If not specified, uses percentages.')
    parser.add_argument('--output', help='Output JSON file for results')
    
    args = parser.parse_args()
    
    results = process_file_versions(
        args.filename,
        args.url,
        args.max_tokens,
        args.line_counts
    )
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    for result in results:
        lines_info = f"{result['lines_used']}/{result['total_lines']}"
        if 'error' in result:
            print(f"Lines {lines_info}: ERROR - {result['error']}")
        else:
            timings = result.get('timings', {})
            if timings:
                # Use the correct keys from the JSON
                prompt_ms = timings.get('prompt_ms', 0) / 1000  # Convert ms to seconds
                predicted_ms = timings.get('predicted_ms', 0) / 1000  # Convert ms to seconds
                total = prompt_ms + predicted_ms  # Calculate total
                print(f"Lines {lines_info}: Total={total:.2f}s, Prompt={prompt_ms:.2f}s, Predicted={predicted_ms:.2f}s")
            else:
                print(f"Lines {lines_info}: Completed (no timing data)")


if __name__ == "__main__":
    main()