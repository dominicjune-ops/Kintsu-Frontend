#!/usr/bin/env python3
"""
Notion Content Migration Script
Imports career coaching guides from Notion markdown exports to Supabase
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import markdown
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    print(" Missing required environment variables!")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Category mapping from directory names to category slugs
CATEGORY_MAPPING = {
    'career-planning': 'career-planning',
    'frameworks': 'frameworks',
    'interview': 'interview',
    'networking': 'networking',
    'resume': 'resume',
    'salary-negotiation': 'salary-negotiation'
}

def estimate_reading_time(content: str) -> int:
    """Estimate reading time in minutes based on word count."""
    words = len(content.split())
    # Average reading speed: 200-250 words per minute
    return max(1, round(words / 225))

def parse_markdown_sections(content: str) -> List[Dict]:
    """Parse markdown content into sections based on headers."""
    sections = []
    lines = content.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        if line.startswith('# '):
            # Main title - skip as it's the guide title
            continue
        elif line.startswith('## '):
            # New section
            if current_section:
                sections.append({
                    'title': current_section,
                    'content': '\n'.join(current_content).strip()
                })
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)

    # Add the last section
    if current_section and current_content:
        sections.append({
            'title': current_section,
            'content': '\n'.join(current_content).strip()
        })

    return sections

def extract_description(content: str, max_length: int = 300) -> str:
    """Extract a description from the content."""
    # Try to get the first paragraph after the title
    lines = content.split('\n')
    description_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            continue
        elif line.startswith('## '):
            break
        elif line and not line.startswith('---') and not line.startswith('*') and not line.startswith('-'):
            description_lines.append(line)
            if len(' '.join(description_lines)) > max_length:
                break

    description = ' '.join(description_lines).strip()
    if len(description) > max_length:
        description = description[:max_length].rstrip() + '...'

    return description or "Comprehensive guide for career success"

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def import_content_guide(category_slug: str, file_path: Path) -> bool:
    """Import a single content guide from markdown file."""
    try:
        # Read the markdown content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title from first line
        lines = content.split('\n')
        title = ""
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break

        if not title:
            print(f" No title found in {file_path}")
            return False

        # Get category ID
        category_result = supabase.table('content_categories').select('id').eq('slug', category_slug).execute()
        if not category_result.data:
            print(f" Category {category_slug} not found")
            return False

        category_id = category_result.data[0]['id']

        # Generate slug
        guide_slug = slugify(title)

        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['extra', 'codehilite', 'toc'])

        # Extract metadata
        description = extract_description(content)
        reading_time = estimate_reading_time(content)

        # Parse sections
        sections = parse_markdown_sections(content)

        # Prepare guide data
        guide_data = {
            'category_id': category_id,
            'slug': guide_slug,
            'title': title,
            'description': description,
            'content_markdown': content,
            'content_html': html_content,
            'reading_time_minutes': reading_time,
            'tags': [category_slug.replace('-', ' ').title()],
            'featured': False,
            'published': True,
            'published_at': datetime.now().isoformat()
        }

        # Insert guide
        guide_result = supabase.table('content_guides').insert(guide_data).execute()
        guide_id = guide_result.data[0]['id']

        # Insert sections
        for i, section in enumerate(sections):
            section_data = {
                'guide_id': guide_id,
                'title': section['title'],
                'content_markdown': section['content'],
                'content_html': markdown.markdown(section['content'], extensions=['extra', 'codehilite']),
                'sort_order': i
            }
            supabase.table('content_sections').insert(section_data).execute()

        print(f" Imported: {title} ({len(sections)} sections)")
        return True

    except Exception as e:
        print(f" Error importing {file_path}: {e}")
        return False

def main():
    """Main migration function."""
    print(" NOTION CONTENT MIGRATION")
    print("=" * 50)

    notion_exports_dir = Path("notion_exports")
    if not notion_exports_dir.exists():
        print(" notion_exports directory not found!")
        return

    total_imported = 0

    # Process each category directory
    for category_dir in notion_exports_dir.iterdir():
        if not category_dir.is_dir():
            continue

        category_slug = CATEGORY_MAPPING.get(category_dir.name)
        if not category_slug:
            print(f"  Skipping unknown category: {category_dir.name}")
            continue

        print(f"\n📁 Processing category: {category_slug}")

        # Process each markdown file in the category
        for md_file in category_dir.glob("*.md"):
            if import_content_guide(category_slug, md_file):
                total_imported += 1

    print(f"\n Migration complete! Imported {total_imported} content guides.")

    # Verify the import
    guides_result = supabase.table('content_guides').select('count').execute()
    sections_result = supabase.table('content_sections').select('count').execute()

    print(f" Database status:")
    print(f"   • Content guides: {guides_result.data[0]['count'] if guides_result.data else 0}")
    print(f"   • Content sections: {sections_result.data[0]['count'] if sections_result.data else 0}")

if __name__ == "__main__":
    main()