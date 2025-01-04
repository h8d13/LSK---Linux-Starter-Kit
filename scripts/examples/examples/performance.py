import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

def cpu_heavy_task(n):
    """CPU-intensive task"""
    total = 0
    for i in range(n):
        for j in range(i):
            total += i * j ** 2
    return total

def io_heavy_task(iteration):
    """I/O-intensive task using file operations"""
    filename = f'temp_file_{iteration}.txt'
    
    # Write
    with open(filename, 'w') as f:
        f.write('x' * 10000)
    
    # Read and process
    with open(filename, 'r') as f:
        content = f.read()
    
    # Cleanup
    os.remove(filename)
    return len(content)

def compare_approaches():
    print("CPU-Heavy Task Comparison:")
    numbers = [20000] * 8  # Significant CPU work
    
    # Single thread - CPU
    start = time.time()
    [cpu_heavy_task(n) for n in numbers]
    print(f"Single thread: {time.time() - start:.2f} seconds")
    
    # Multiprocessing - CPU
    start = time.time()
    with ProcessPoolExecutor() as executor:
        list(executor.map(cpu_heavy_task, numbers))
    print(f"Multiprocessing: {time.time() - start:.2f} seconds")

    print("\nI/O-Heavy Task Comparison:")
    iterations = range(100)  # Significant I/O work
    
    # Single thread - I/O
    start = time.time()
    [io_heavy_task(i) for i in iterations]
    print(f"Single thread: {time.time() - start:.2f} seconds")
    
    # Threading - I/O
    start = time.time()
    with ThreadPoolExecutor() as executor:
        list(executor.map(io_heavy_task, iterations))
    print(f"Threading: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    compare_approaches()