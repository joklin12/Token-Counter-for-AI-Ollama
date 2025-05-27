"""
Ollama API Tokens Counter Per Second
Developed by: Joko Supriyanto, SST, M.Kom
Institution: Universitas Siber Muhammadiyah
Year: 2025

Fungsi:
- Berinteraksi dengan model bahasa lokal melalui Ollama API
- Mengirim prompt dan menerima response secara streaming
- Menghitung token dan statistik performa

Endpoint yang digunakan: http://localhost:11434/api/chat
"""

import requests
import time
import json

def main():
    prompt = "buatkan 2 naskah pidato untuk hari kemerdekaan RI 17 agustus"
    data = {
        "model": "llama3.2:1b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    url = "http://localhost:11434/api/chat"

    print(f"Prompt: {prompt}")
    print("Generating response...\n")

    start_time = time.time()
    token_count = 0
    full_response = ""

    try:
        with requests.post(url, json=data, stream=True) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                # Skip empty lines and keep-alive comments
                if not line:
                    continue
                
                try:
                    decoded = json.loads(line.decode('utf-8'))
                    
                    if 'message' in decoded and 'content' in decoded['message']:
                        content = decoded['message']['content']
                        if content:  # Only count non-empty content
                            token_count += 1
                            full_response += content
                            print(content, end='', flush=True)
                    elif 'response' in decoded:  # Fallback for alternative response format
                        content = decoded['response']
                        if content:
                            token_count += 1
                            full_response += content
                            print(content, end='', flush=True)
                            
                except json.JSONDecodeError as je:
                    print(f"\nWarning: Failed to decode JSON chunk: {line}")
                    continue
                except Exception as e:
                    print(f"\nWarning: Unexpected error processing chunk: {e}")
                    continue

    except requests.exceptions.RequestException as e:
        print(f"\nError during request: {e}")
        return

    end_time = time.time()
    elapsed = end_time - start_time

    print("\n\nSummary:")
    print(f"Total tokens generated: {token_count}")
    print(f"Full response length: {len(full_response)} characters")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    if elapsed > 0:
        print(f"Tokens per second: {token_count / elapsed:.2f}")
    else:
        print("Elapsed time too small to calculate speed.")

if __name__ == "__main__":
    main()