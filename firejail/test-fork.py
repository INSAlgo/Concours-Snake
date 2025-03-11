import multiprocessing
import os

def power(base, exponent):
    print(f"PID: {os.getpid()}", end=" ")  # print PID (Process ID) of the current process
    print(f"(PPID: {os.getppid()}", end=") ")  # print PPID (Parent Process ID) of the current process
    # print CPUID of the current process
    print(f"CPUID: {os.sched_getaffinity(0)}")
    return base ** exponent


def parallel_code():
    inputs = [(2, 3), (3, 3), (4, 2), (5, 3)]

    # check how many cores are available
    print(f"Number of cores: {multiprocessing.cpu_count()}")
    
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.starmap(power, inputs)
    
    print(results)  # Output: [8, 27, 16, 125]

if __name__ == "__main__":
    parallel_code()
