#!/usr/bin/env python3
"""
Memory Monitor for Test Runs
Monitors memory usage during pytest execution
"""

import time
import os
import sys
import platform
from datetime import datetime
import subprocess

def get_memory_usage():
    """Get current memory usage percentage using system commands"""
    try:
        if platform.system() == "Windows":
            # Windows - use wmic
            result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize', '/Value'],
                                  capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            free_mem = total_mem = 0
            for line in lines:
                if line.startswith('FreePhysicalMemory='):
                    free_mem = int(line.split('=')[1])
                elif line.startswith('TotalVisibleMemorySize='):
                    total_mem = int(line.split('=')[1])

            if total_mem > 0:
                usage_percent = ((total_mem - free_mem) / total_mem) * 100
                available_gb = free_mem / (1024 * 1024)
                total_gb = total_mem / (1024 * 1024)
                return usage_percent, available_gb, total_gb

        else:
            # Linux/Unix - use free command
            result = subprocess.run(['free', '-m'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                mem_line = lines[1].split()
                total_mem = int(mem_line[0])
                available_mem = int(mem_line[6])  # available includes buffers/cache
                used_mem = total_mem - available_mem
                usage_percent = (used_mem / total_mem) * 100
                available_gb = available_mem / 1024
                total_gb = total_mem / 1024
                return usage_percent, available_gb, total_gb

    except Exception as e:
        print(f"Error getting memory usage: {e}")

    # Fallback
    return 0, 0, 0

def monitor_memory(duration_seconds=300, check_interval=10):
    """Monitor memory usage for a specified duration"""
    print(" Memory Monitor Started")
    print("=" * 50)

    start_time = time.time()
    max_memory_used = 0
    alerts_triggered = 0

    while time.time() - start_time < duration_seconds:
        try:
            usage_percent, available_gb, total_gb = get_memory_usage()
            max_memory_used = max(max_memory_used, usage_percent)

            timestamp = datetime.now().strftime("%H:%M:%S")
            status = "" if usage_percent < 80 else "" if usage_percent < 90 else "🚨"

            print(f"[{timestamp}] {status} Memory: {usage_percent:.1f}% ({available_gb:.1f}GB free / {total_gb:.1f}GB total)")

            if usage_percent > 95:
                print(f"🚨 CRITICAL: Memory usage above 95%! Current: {usage_percent:.1f}%")
                alerts_triggered += 1
                if alerts_triggered >= 3:
                    print("🚨 MULTIPLE CRITICAL ALERTS: Terminating to prevent system instability")
                    return False
            elif usage_percent > 90:
                print(f" WARNING: Memory usage above 90%! Current: {usage_percent:.1f}%")
                alerts_triggered += 1

            time.sleep(check_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error monitoring memory: {e}")
            time.sleep(check_interval)

    print("=" * 50)
    print(" Memory Monitor Completed")
    print(f"Peak memory usage: {max_memory_used:.1f}%")
    print(f"Alerts triggered: {alerts_triggered}")

    return max_memory_used < 95  # Return success if memory never exceeded 95%

if __name__ == "__main__":
    # Run for 5 minutes by default, or specified duration
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    success = monitor_memory(duration)
    sys.exit(0 if success else 1)