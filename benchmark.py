#!/usr/bin/env python3

import json
import sys
import requests
import argparse
from pathlib import Path

# Constants
REQUEST_TIMEOUT_SECONDS = 1800  # 30 minutes timeout for large files


def send_request(content, url, max_tokens):
    """Send request to the API with the given content.
    
    Raises:
        requests.RequestException: For network errors
        ValueError: For invalid responses
    """
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
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise requests.RequestException(f"Request timed out after {REQUEST_TIMEOUT_SECONDS} seconds")
    except requests.exceptions.ConnectionError:
        raise requests.RequestException("Failed to connect to server. Is the server running?")
    except requests.exceptions.HTTPError as e:
        raise requests.RequestException(f"HTTP error: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {e}")


def process_file_versions(filename, url, max_tokens, num_splits=100):
    """Process multiple versions of the file with different line counts.
    
    Args:
        filename: Input file to process
        url: API endpoint URL
        max_tokens: Maximum tokens for response
        num_splits: Number of test points (1 = entire file, 100 = test at 1%, 2%, ..., 100%)
    
    Returns:
        List of results or None if file doesn't exist
    """
    file_path = Path(filename)
    
    if not file_path.exists():
        print(f"\nError: File '{filename}' does not exist")
        return None
    
    try:
        with open(file_path, 'r') as f:
            all_lines = f.readlines()
    except PermissionError:
        print(f"\nError: Permission denied reading file '{filename}'")
        return None
    except Exception as e:
        print(f"\nError reading file '{filename}': {e}")
        return None
    
    total_lines = len(all_lines)
    
    # Generate line counts based on number of splits
    if total_lines == 0:
        print(f"\nError: File '{filename}' is empty")
        return None
    
    if num_splits < 1:
        print(f"\nError: Invalid splits value {num_splits}. Must be >= 1")
        return None
    
    if num_splits == 1:
        # Test entire file only
        line_counts = [total_lines]
    else:
        # Generate evenly distributed test points
        percentages = [i / num_splits for i in range(1, num_splits + 1)]
        line_counts = [max(1, int(total_lines * p)) for p in percentages]
        # Remove duplicates and sort
        line_counts = sorted(set(line_counts))
    
    results = []
    
    for n_lines in line_counts:
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
            
        except requests.RequestException as e:
            print(f"Network error processing {n_lines} lines: {e}")
            results.append({
                'file': filename,
                'lines_used': n_lines,
                'total_lines': total_lines,
                'max_tokens': max_tokens,
                'error': f"Network error: {str(e)}"
            })
        except KeyboardInterrupt:
            print("\n\nBenchmark interrupted by user")
            return results
        except Exception as e:
            print(f"Unexpected error processing {n_lines} lines: {e}")
            results.append({
                'file': filename,
                'lines_used': n_lines,
                'total_lines': total_lines,
                'max_tokens': max_tokens,
                'error': f"Unexpected error: {str(e)}"
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Explain code library using AI API')
    parser.add_argument('filename', help='Input file to process')
    parser.add_argument('--url', default='http://localhost:8088/v1/chat/completions',
                        help='API endpoint URL (default: http://localhost:8088/v1/chat/completions)')
    parser.add_argument('--max-tokens', type=int, default=64,
                        help='Maximum tokens for response (default: 64)')
    parser.add_argument('--splits', type=int, default=100,
                        help='Number of test points (1=entire file, 100=test at 1%%, 2%%, ..., 100%%). Default: 100')
    parser.add_argument('--output', help='Output JSON file for results')
    
    args = parser.parse_args()
    
    results = process_file_versions(
        args.filename,
        args.url,
        args.max_tokens,
        args.splits
    )
    
    # Check if processing failed
    if results is None:
        print("\nBenchmark failed. Please check the file path and try again.")
        sys.exit(1)
    
    if not results:
        print("\nNo results generated.")
        sys.exit(1)
    
    # Save results if output file specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"\nWarning: Failed to save results to {args.output}: {e}")
    
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