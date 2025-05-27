"""
Ollama API Tokens Counter Per Second
Developed by: Joko Supriyanto, SST, M.Kom
Institution: Universitas Siber Muhammadiyah
Year: 2025

Fungsi:
- Berinteraksi dengan model bahasa lokal melalui Ollama API
- Mengirim prompt dan menerima response secara streaming
- Menghitung token dan statistik performa

Endpoint yang digunakan: http://localhost:11434/api/generate
"""

import requests
import time
import json

def main():
    prompt = "buatkan 2 naskah pidato untuk hari kemerdekaan RI 17 agustus"
    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": True
    }

    url = "http://localhost:11434/api/generate"

    print(f"Prompt: {prompt}")
    print("Generating response...\n")

    start_time = time.time()
    token_count = 0

    try:
        with requests.post(url, json=data, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded = json.loads(line)
                    if 'response' in decoded:
                        token_count += 1
                        print(decoded['response'], end='', flush=True)

    except requests.exceptions.RequestException as e:
        print(f"\nError during request: {e}")
        return

    end_time = time.time()
    elapsed = end_time - start_time

    print("\n\nSummary:")
    print(f"Total tokens generated: {token_count}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    if elapsed > 0:
        print(f"Tokens per second: {token_count / elapsed:.2f}")
    else:
        print("Elapsed time too small to calculate speed.")

if __name__ == "__main__":
    main()
