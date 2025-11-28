#!/usr/bin/env bash
# Memory Optimization Script for ADONIYAH-Agent-2
# Run this script to free up memory on the self-hosted agent

echo " Memory Optimization Script for ADONIYAH-Agent-2"
echo "=================================================="

# Function to get memory info
get_memory_info() {
    echo "=== Current Memory Status ==="
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value
        echo "Free Memory (MB): $(wmic OS get FreePhysicalMemory /Value | grep -o '[0-9]*')"
        echo "Total Memory (MB): $(wmic OS get TotalVisibleMemorySize /Value | grep -o '[0-9]*')"
    else
        # Linux/Unix
        free -h
        echo "Memory usage details:"
        ps aux --sort=-%mem | head -10
    fi
}

# Show initial memory status
get_memory_info

echo ""
echo "🧹 Starting Memory Cleanup..."
echo "================================"

# Clear system caches (Linux only)
if [[ "$OSTYPE" != "msys" ]] && [[ "$OSTYPE" != "win32" ]]; then
    echo "Clearing system caches..."
    sudo sync
    sudo echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || echo "Could not clear caches (requires sudo)"
fi

# Clear Python cache files
echo "Clearing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Clear temporary files
echo "Clearing temporary files..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    rd /s /q "%TEMP%" 2>nul || true
    rd /s /q "%TMP%" 2>nul || true
else
    # Linux/Unix
    rm -rf /tmp/* 2>/dev/null || true
    rm -rf ~/.cache/* 2>/dev/null || true
fi

# Kill memory-intensive processes (be careful!)
echo "Checking for memory-intensive processes..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows - check for high memory processes
    echo "High memory processes:"
    tasklist /FI "MEMUSAGE gt 100000" 2>nul || echo "Could not check processes"
else
    # Linux - show top memory consumers
    echo "Top memory consumers:"
    ps aux --sort=-%mem | head -5
fi

# Clear Docker resources if Docker is available
if command -v docker &> /dev/null; then
    echo "Cleaning Docker resources..."
    docker system prune -f 2>/dev/null || echo "Could not prune Docker system"
    docker volume prune -f 2>/dev/null || echo "Could not prune Docker volumes"
fi

# Clear npm/yarn cache if available
if command -v npm &> /dev/null; then
    echo "Clearing npm cache..."
    npm cache clean --force 2>/dev/null || true
fi

if command -v yarn &> /dev/null; then
    echo "Clearing yarn cache..."
    yarn cache clean 2>/dev/null || true
fi

echo ""
echo " Memory cleanup completed!"
echo "=============================="

# Show final memory status
get_memory_info

echo ""
echo "💡 Recommendations:"
echo "- Monitor memory usage during pipeline runs"
echo "- Consider increasing RAM on the agent if issues persist"
echo "- Run this script before critical pipeline operations"
echo "- Check for memory leaks in applications"