import time
import os
import sys

def main():
    print(r"""
 █   █  █  ▄▀▀▄ ▀▀█▀▀  █  █   █ 
 █   █  █  █      █    █  █▀▄▀█ 
  ▀▄▀   █  ▀▄▄▀   █    █  █   █ 
    """)
    print(f"PID: {os.getpid()}")
    print("Simulating a memory leak (10 MB/s)...")
    print("Use Ctrl+C to stop.")

    leak_storage = []
    
    chunk_size = 10 * 1024 * 1024 

    try:
        while True:
            
            leak = bytearray(chunk_size)
            
            
            leak_storage.append(leak)
            
            current_usage = (len(leak_storage) * 10)
            print(f"[{time.strftime('%H:%M:%S')}] Leaked +10MB (Total: {current_usage} MB)")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nVictim stopped. Memory released.")

if __name__ == "__main__":
    main()