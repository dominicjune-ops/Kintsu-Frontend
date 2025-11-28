#!/usr/bin/env python3
"""
CareerCoach.ai Log Viewer
View and analyze application logs with filtering and search capabilities
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import re

class LogViewer:
    """Log viewer and analysis tool"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_files = {
            'app': self.log_dir / 'application.log',
            'error': self.log_dir / 'errors.log',
            'api': self.log_dir / 'api.log',
            'database': self.log_dir / 'database.log',
            'performance': self.log_dir / 'performance.log',
            'security': self.log_dir / 'security.log'
        }
    
    def parse_log_line(self, line: str) -> Optional[Dict]:
        """Parse a JSON log line"""
        try:
            return json.loads(line.strip())
        except (json.JSONDecodeError, ValueError):
            return None
    
    def read_logs(self, log_type: str, limit: int = None) -> List[Dict]:
        """Read logs from specified log file"""
        if log_type not in self.log_files:
            print(f" Unknown log type: {log_type}")
            print(f"Available types: {', '.join(self.log_files.keys())}")
            return []
        
        log_file = self.log_files[log_type]
        if not log_file.exists():
            print(f" Log file not found: {log_file}")
            return []
        
        logs = []
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        log_entry = self.parse_log_line(line)
                        if log_entry:
                            logs.append(log_entry)
        except Exception as e:
            print(f" Error reading log file: {e}")
            return []
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        if limit:
            logs = logs[:limit]
        
        return logs
    
    def filter_logs(self, logs: List[Dict], level: str = None, 
                   search: str = None, since: str = None) -> List[Dict]:
        """Filter logs by various criteria"""
        filtered = logs
        
        # Filter by level
        if level:
            filtered = [log for log in filtered if log.get('level', '').lower() == level.lower()]
        
        # Filter by search term
        if search:
            search_lower = search.lower()
            filtered = [
                log for log in filtered 
                if search_lower in log.get('message', '').lower()
            ]
        
        # Filter by time
        if since:
            try:
                if since.endswith('h'):
                    hours = int(since[:-1])
                    cutoff = datetime.utcnow() - timedelta(hours=hours)
                elif since.endswith('d'):
                    days = int(since[:-1])
                    cutoff = datetime.utcnow() - timedelta(days=days)
                elif since.endswith('m'):
                    minutes = int(since[:-1])
                    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
                else:
                    cutoff = datetime.fromisoformat(since)
                
                cutoff_str = cutoff.isoformat()
                filtered = [
                    log for log in filtered 
                    if log.get('timestamp', '') >= cutoff_str
                ]
            except ValueError:
                print(f" Invalid time format: {since}")
        
        return filtered
    
    def display_logs(self, logs: List[Dict], format_type: str = 'table'):
        """Display logs in various formats"""
        if not logs:
            print("No logs found matching criteria")
            return
        
        if format_type == 'json':
            for log in logs:
                print(json.dumps(log, indent=2, default=str))
                print("-" * 50)
        
        elif format_type == 'table':
            print(f"Found {len(logs)} log entries")
            print("=" * 120)
            print(f"{'Time':<20} {'Level':<8} {'Logger':<20} {'Message':<60}")
            print("-" * 120)
            
            for log in logs:
                timestamp = log.get('timestamp', 'N/A')[:19].replace('T', ' ')
                level = log.get('level', 'N/A')
                logger = log.get('logger', 'N/A').replace('careercoach.', '')
                message = log.get('message', 'N/A')[:60]
                
                # Color code by level
                if level == 'ERROR':
                    level_color = f"\033[91m{level}\033[0m"  # Red
                elif level == 'WARNING':
                    level_color = f"\033[93m{level}\033[0m"  # Yellow
                else:
                    level_color = level
                
                print(f"{timestamp:<20} {level_color:<8} {logger:<20} {message:<60}")
        
        elif format_type == 'summary':
            self.display_summary(logs)
    
    def display_summary(self, logs: List[Dict]):
        """Display log summary statistics"""
        if not logs:
            return
        
        # Count by level
        level_counts = {}
        logger_counts = {}
        recent_errors = []
        
        for log in logs:
            level = log.get('level', 'UNKNOWN')
            logger = log.get('logger', 'unknown')
            
            level_counts[level] = level_counts.get(level, 0) + 1
            logger_counts[logger] = logger_counts.get(logger, 0) + 1
            
            if level in ['ERROR', 'CRITICAL'] and len(recent_errors) < 5:
                recent_errors.append(log)
        
        print("Log Summary")
        print("=" * 50)
        print(f"Total entries: {len(logs)}")
        print("\nBy Level:")
        for level, count in sorted(level_counts.items()):
            print(f"  {level}: {count}")
        
        print("\nBy Logger:")
        for logger, count in sorted(logger_counts.items()):
            logger_name = logger.replace('careercoach.', '')
            print(f"  {logger_name}: {count}")
        
        if recent_errors:
            print(f"\nRecent Errors ({len(recent_errors)}):")
            for error in recent_errors:
                timestamp = error.get('timestamp', 'N/A')[:19].replace('T', ' ')
                message = error.get('message', 'N/A')[:80]
                print(f"  {timestamp} - {message}")
    
    def tail_logs(self, log_type: str, lines: int = 10):
        """Show last N lines from log file (like tail -f)"""
        logs = self.read_logs(log_type, limit=lines)
        print(f"Last {len(logs)} entries from {log_type} log:")
        print("=" * 80)
        self.display_logs(logs)
    
    def search_errors(self, search_term: str = None, since: str = "24h"):
        """Search for errors in all log files"""
        print(f"Searching for errors in last {since}")
        if search_term:
            print(f"Containing: '{search_term}'")
        print("=" * 80)
        
        all_errors = []
        for log_type in self.log_files.keys():
            logs = self.read_logs(log_type)
            errors = self.filter_logs(logs, level='ERROR', search=search_term, since=since)
            all_errors.extend(errors)
        
        # Sort by timestamp
        all_errors.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        self.display_logs(all_errors)

def main():
    """Command line interface for log viewer"""
    parser = argparse.ArgumentParser(description='CareerCoach.ai Log Viewer')
    parser.add_argument('command', choices=['view', 'tail', 'errors', 'summary'], 
                       help='Command to execute')
    parser.add_argument('--type', '-t', choices=['app', 'error', 'api', 'database', 'performance', 'security'],
                       default='app', help='Log type to view')
    parser.add_argument('--level', '-l', help='Filter by log level (INFO, ERROR, WARNING, etc.)')
    parser.add_argument('--search', '-s', help='Search for specific text in messages')
    parser.add_argument('--since', help='Show logs since time (e.g., 1h, 30m, 2d)')
    parser.add_argument('--limit', '-n', type=int, default=50, help='Limit number of entries')
    parser.add_argument('--format', '-f', choices=['table', 'json', 'summary'], 
                       default='table', help='Output format')
    
    args = parser.parse_args()
    
    viewer = LogViewer()
    
    if args.command == 'view':
        logs = viewer.read_logs(args.type, limit=args.limit)
        filtered = viewer.filter_logs(logs, level=args.level, search=args.search, since=args.since)
        viewer.display_logs(filtered, format_type=args.format)
    
    elif args.command == 'tail':
        viewer.tail_logs(args.type, lines=args.limit)
    
    elif args.command == 'errors':
        viewer.search_errors(search_term=args.search, since=args.since or "24h")
    
    elif args.command == 'summary':
        logs = viewer.read_logs(args.type)
        filtered = viewer.filter_logs(logs, since=args.since)
        viewer.display_summary(filtered)

if __name__ == "__main__":
    if len(__import__('sys').argv) == 1:
        # Interactive mode if no arguments
        viewer = LogViewer()
        print("CareerCoach.ai Log Viewer - Interactive Mode")
        print("=" * 50)
        print("Available commands:")
        print("  python log_viewer.py view --type api --level ERROR")
        print("  python log_viewer.py tail --type error")
        print("  python log_viewer.py errors --search 'database'")
        print("  python log_viewer.py summary --type api --since 1h")
        print()
        
        # Show quick summary of all logs
        print("Quick Summary:")
        for log_type in ['error', 'api', 'app']:
            logs = viewer.read_logs(log_type, limit=100)
            if logs:
                print(f"  {log_type}: {len(logs)} entries")
                errors = [log for log in logs if log.get('level') == 'ERROR']
                if errors:
                    print(f"    └─ {len(errors)} errors")
    else:
        main()