"""
MATCH Framework Automation System
==================================

Purpose: Automate the creation, validation, and optimization of MATCH framework stories
for demonstrating company culture fit and values alignment during interviews.

MATCH Components:
- Mission: How your values align with the company's mission and purpose
- Alignment: Your career goals matching the company's direction
- Teamwork: Your collaborative style fitting the team culture
- Challenge: Growth opportunities and challenges you seek
- Heuristic: Decision-making frameworks and problem-solving approaches

Features:
- Component detection with confidence scoring
- Company culture fit analysis
- Values alignment validation
- Team dynamics compatibility assessment
- Growth opportunity identification
- Template generation for different company types
- Interview-ready formatting
- Story persistence and retrieval

Author: CareerCoach.ai Development Team
Epic: CAREER-AI-018 (Epic 4: Content Intelligence Automation)
Story Points: 15
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import json
import re
from datetime import datetime
from pathlib import Path


@dataclass
class MATCHStory:
    """Represents a MATCH framework story for company culture fit."""
    
    mission: str = ""
    alignment: str = ""
    teamwork: str = ""
    challenge: str = ""
    heuristic: str = ""
    
    # Metadata
    company_name: str = ""
    company_type: str = ""  # startup, enterprise, nonprofit, tech, etc.
    position: str = ""
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Analysis results
    culture_fit_score: float = 0.0
    values_alignment: List[str] = field(default_factory=list)
    team_compatibility: str = ""
    growth_potential: str = ""


class MATCHFrameworkAutomation:
    """Main automation system for MATCH framework stories."""
    
    def __init__(self):
        # Keywords for each component
        self.component_keywords = {
            'mission': [
                'mission', 'purpose', 'vision', 'values', 'believe in',
                'passionate about', 'committed to', 'dedicated to',
                'inspired by', 'resonate with', 'align with mission',
                'share values', 'company purpose', 'organizational values',
                'core beliefs', 'guiding principles', 'what drives me',
                'why I joined', 'attracted to mission', 'meaningful work'
            ],
            'alignment': [
                'career goals', 'growth path', 'long-term vision', 'aspirations',
                'professional development', 'career trajectory', 'where I see myself',
                'next step', 'career progression', 'skill development',
                'learning objectives', 'future role', 'advancement opportunities',
                'career alignment', 'goals match', 'direction aligns',
                'perfect fit for growth', 'trajectory matches', 'develop skills'
            ],
            'teamwork': [
                'collaboration style', 'team dynamics', 'working with others',
                'communication approach', 'team player', 'collaborative',
                'cross-functional', 'partnership', 'team environment',
                'work culture', 'team values', 'collaborative mindset',
                'team contribution', 'group work', 'collective success',
                'support teammates', 'team chemistry', 'cultural fit'
            ],
            'challenge': [
                'challenges', 'growth opportunities', 'learning experiences',
                'stretch assignments', 'push boundaries', 'difficult problems',
                'complex projects', 'innovation', 'cutting-edge',
                'new territory', 'ambitious goals', 'high impact',
                'meaningful challenges', 'problem-solving', 'innovation opportunities',
                'technical challenges', 'scale problems', 'difficult work'
            ],
            'heuristic': [
                'decision-making', 'problem-solving approach', 'framework',
                'methodology', 'process', 'how I think', 'approach problems',
                'analytical framework', 'mental model', 'principles',
                'decision framework', 'evaluation criteria', 'prioritization',
                'trade-offs', 'systematic approach', 'thinking process',
                'judgment calls', 'weighing options', 'decision criteria'
            ]
        }
        
        # Company type characteristics
        self.company_types = {
            'startup': {
                'values': ['innovation', 'speed', 'ownership', 'impact', 'flexibility'],
                'challenges': ['scaling', 'rapid growth', 'ambiguity', 'wearing multiple hats'],
                'culture': 'fast-paced, collaborative, entrepreneurial'
            },
            'enterprise': {
                'values': ['stability', 'process', 'collaboration', 'excellence', 'scale'],
                'challenges': ['complexity', 'large-scale impact', 'cross-functional coordination'],
                'culture': 'structured, professional, team-oriented'
            },
            'tech': {
                'values': ['innovation', 'technical excellence', 'continuous learning', 'impact'],
                'challenges': ['technical complexity', 'cutting-edge problems', 'scale'],
                'culture': 'engineering-driven, collaborative, growth-oriented'
            },
            'nonprofit': {
                'values': ['mission', 'impact', 'service', 'community', 'purpose'],
                'challenges': ['resource constraints', 'maximizing impact', 'sustainability'],
                'culture': 'purpose-driven, collaborative, community-focused'
            },
            'consulting': {
                'values': ['client impact', 'excellence', 'learning', 'problem-solving'],
                'challenges': ['diverse problems', 'rapid context switching', 'client expectations'],
                'culture': 'analytical, professional, growth-focused'
            }
        }
    
    def detect_match_components(self, text: str) -> Dict[str, float]:
        """
        Detect MATCH components in text with confidence scores.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary mapping component names to confidence scores (0-100%)
        """
        text_lower = text.lower()
        results = {}
        
        for component, keywords in self.component_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            confidence = min(100, (matches / len(keywords)) * 100 * 3)  # Boost score
            results[component] = round(confidence, 1)
        
        return results
    
    def classify_company_type(self, company_description: str) -> str:
        """
        Classify company type based on description.
        
        Args:
            company_description: Description of the company
            
        Returns:
            Company type (startup, enterprise, tech, nonprofit, consulting)
        """
        desc_lower = company_description.lower()
        
        # Keywords for each company type
        type_keywords = {
            'startup': ['startup', 'early-stage', 'seed', 'series a', 'series b', 'founder', 'fast-growing'],
            'enterprise': ['enterprise', 'fortune 500', 'large company', 'established', 'corporate'],
            'tech': ['tech company', 'software', 'saas', 'platform', 'engineering', 'technology'],
            'nonprofit': ['nonprofit', 'non-profit', 'ngo', 'foundation', 'charity', 'mission-driven'],
            'consulting': ['consulting', 'advisory', 'professional services', 'consulting firm']
        }
        
        # Count keyword matches
        matches = {}
        for comp_type, keywords in type_keywords.items():
            matches[comp_type] = sum(1 for keyword in keywords if keyword in desc_lower)
        
        # Return type with most matches, default to 'tech'
        return max(matches.items(), key=lambda x: x[1])[0] if any(matches.values()) else 'tech'
    
    def analyze_culture_fit(self, story: MATCHStory) -> Tuple[float, List[str]]:
        """
        Analyze culture fit based on MATCH components.
        
        Args:
            story: The MATCH story to analyze
            
        Returns:
            Tuple of (culture_fit_score, values_alignment_list)
        """
        score = 0.0
        aligned_values = []
        
        # Get company type characteristics
        company_char = self.company_types.get(story.company_type, self.company_types['tech'])
        
        # Score each component (20 points each)
        if len(story.mission.split()) >= 40:
            score += 20
            # Check for value alignment
            for value in company_char['values']:
                if value.lower() in story.mission.lower():
                    aligned_values.append(value)
        
        if len(story.alignment.split()) >= 35:
            score += 20
        
        if len(story.teamwork.split()) >= 35:
            score += 20
            # Check for culture keywords
            if company_char['culture'].split(', ')[0] in story.teamwork.lower():
                aligned_values.append('culture_fit')
        
        if len(story.challenge.split()) >= 30:
            score += 20
            # Check for relevant challenges
            for challenge in company_char['challenges']:
                if challenge.lower() in story.challenge.lower():
                    aligned_values.append(f'challenge: {challenge}')
        
        if len(story.heuristic.split()) >= 30:
            score += 20
        
        return round(score, 1), list(set(aligned_values))
    
    def validate_match_story(self, story: MATCHStory) -> Tuple[float, List[str]]:
        """
        Validate MATCH story completeness and quality.
        
        Args:
            story: The story to validate
            
        Returns:
            Tuple of (completeness_score, error_list)
        """
        errors = []
        score = 0.0
        
        # Minimum word counts
        requirements = {
            'mission': 40,
            'alignment': 35,
            'teamwork': 35,
            'challenge': 30,
            'heuristic': 30
        }
        
        for component, min_words in requirements.items():
            component_text = getattr(story, component)
            word_count = len(component_text.split())
            
            if word_count >= min_words:
                score += 20
            else:
                errors.append(
                    f"{component.upper()} too short: {word_count} words (min {min_words})"
                )
        
        # Check metadata
        if not story.company_name:
            errors.append("Company name is required")
        if not story.position:
            errors.append("Position is required")
        
        return round(score, 1), errors
    
    def generate_company_specific_prompts(self, company_type: str, component: str) -> List[str]:
        """
        Generate company-type-specific prompts for each component.
        
        Args:
            company_type: Type of company
            component: MATCH component name
            
        Returns:
            List of tailored prompts
        """
        company_char = self.company_types.get(company_type, self.company_types['tech'])
        
        prompts = {
            'mission': [
                f"What aspects of the company's mission resonate with your personal values?",
                f"How do the company's core values ({', '.join(company_char['values'][:3])}) align with yours?",
                f"What meaningful impact do you hope to achieve at this company?",
                f"Why is this company's purpose particularly compelling to you?"
            ],
            'alignment': [
                f"How does this role fit into your 3-5 year career vision?",
                f"What skills will you develop that align with your career goals?",
                f"How does this opportunity advance your professional trajectory?",
                f"What growth path do you see for yourself at this company?"
            ],
            'teamwork': [
                f"How does your collaboration style fit this {company_char['culture']} culture?",
                f"Describe your ideal team environment and how this matches it.",
                f"What do you contribute to a {company_char['culture']} team?",
                f"How do you adapt your communication style to different team dynamics?"
            ],
            'challenge': [
                f"Which of these challenges excite you: {', '.join(company_char['challenges'][:2])}?",
                f"What complex problems are you hoping to solve in this role?",
                f"How do you approach {company_char['challenges'][0]}?",
                f"What type of growth challenges are you seeking?"
            ],
            'heuristic': [
                f"How do you make decisions when facing trade-offs in {company_char['culture']} environments?",
                f"What framework do you use to prioritize competing objectives?",
                f"How do you balance speed vs. quality in your decision-making?",
                f"What principles guide your problem-solving approach?"
            ]
        }
        
        return prompts.get(component, [])
    
    def create_match_template(self, company_name: str, company_type: str, position: str) -> MATCHStory:
        """
        Create a blank MATCH story template with company-specific prompts.
        
        Args:
            company_name: Name of the company
            company_type: Type of company
            position: Position applying for
            
        Returns:
            Template MATCHStory with guidance
        """
        company_char = self.company_types.get(company_type, self.company_types['tech'])
        
        template = MATCHStory(
            company_name=company_name,
            company_type=company_type,
            position=position
        )
        
        # Add component guidance
        template.mission = f"[Explain how your values align with {company_name}'s mission. Focus on: {', '.join(company_char['values'][:3])}. Minimum 40 words.]"
        template.alignment = f"[Describe how this {position} role fits your career goals and growth trajectory. Minimum 35 words.]"
        template.teamwork = f"[Explain how your collaboration style fits this {company_char['culture']} culture. Minimum 35 words.]"
        template.challenge = f"[Describe the challenges you're excited about: {', '.join(company_char['challenges'][:2])}. Minimum 30 words.]"
        template.heuristic = f"[Explain your decision-making framework and problem-solving approach. Minimum 30 words.]"
        
        return template
    
    def auto_improve_story(self, story: MATCHStory) -> Dict[str, List[str]]:
        """
        Generate improvement suggestions for each component.
        
        Args:
            story: The story to improve
            
        Returns:
            Dictionary mapping component names to suggestion lists
        """
        suggestions = {}
        company_char = self.company_types.get(story.company_type, self.company_types['tech'])
        
        # Mission suggestions
        mission_suggestions = []
        if story.mission:
            if not any(value in story.mission.lower() for value in company_char['values']):
                mission_suggestions.append(f"Reference company values: {', '.join(company_char['values'][:3])}")
            if 'passionate' not in story.mission.lower() and 'believe' not in story.mission.lower():
                mission_suggestions.append("Show emotional connection to the mission")
            if story.company_name and story.company_name.lower() not in story.mission.lower():
                mission_suggestions.append(f"Explicitly mention {story.company_name}")
        if mission_suggestions:
            suggestions['mission'] = mission_suggestions
        
        # Alignment suggestions
        alignment_suggestions = []
        if story.alignment:
            if 'year' not in story.alignment.lower():
                alignment_suggestions.append("Include specific timeframe (3-5 years)")
            if not re.search(r'\b(skill|learn|develop|grow)\w*\b', story.alignment.lower()):
                alignment_suggestions.append("Mention specific skills you'll develop")
            if 'goal' not in story.alignment.lower():
                alignment_suggestions.append("State explicit career goals")
        if alignment_suggestions:
            suggestions['alignment'] = alignment_suggestions
        
        # Teamwork suggestions
        teamwork_suggestions = []
        if story.teamwork:
            culture_keywords = company_char['culture'].lower().split(', ')
            if not any(keyword in story.teamwork.lower() for keyword in culture_keywords):
                teamwork_suggestions.append(f"Address {company_char['culture']} culture fit")
            if not re.search(r'\b(collaborat|communicat|partner|support)\w*\b', story.teamwork.lower()):
                teamwork_suggestions.append("Use specific collaboration verbs")
            if 'example' not in story.teamwork.lower():
                teamwork_suggestions.append("Include a brief example of your teamwork style")
        if teamwork_suggestions:
            suggestions['teamwork'] = teamwork_suggestions
        
        # Challenge suggestions
        challenge_suggestions = []
        if story.challenge:
            if not any(chal in story.challenge.lower() for chal in company_char['challenges']):
                challenge_suggestions.append(f"Reference relevant challenges: {', '.join(company_char['challenges'][:2])}")
            if not re.search(r'\b(excite|eager|passionate|interested)\w*\b', story.challenge.lower()):
                challenge_suggestions.append("Show enthusiasm for the challenges")
            if not re.search(r'\b(learn|grow|develop|improve)\w*\b', story.challenge.lower()):
                challenge_suggestions.append("Connect challenges to growth opportunities")
        if challenge_suggestions:
            suggestions['challenge'] = challenge_suggestions
        
        # Heuristic suggestions
        heuristic_suggestions = []
        if story.heuristic:
            if not re.search(r'\b(framework|approach|process|method|principle)\w*\b', story.heuristic.lower()):
                heuristic_suggestions.append("Describe your specific framework or approach")
            if not re.search(r'\b(decide|evaluate|prioritize|analyze|weigh)\w*\b', story.heuristic.lower()):
                heuristic_suggestions.append("Use decision-making action verbs")
            if 'example' not in story.heuristic.lower():
                heuristic_suggestions.append("Provide a brief example of your decision-making process")
        if heuristic_suggestions:
            suggestions['heuristic'] = heuristic_suggestions
        
        return suggestions
    
    def format_story_for_interview(self, story: MATCHStory) -> str:
        """
        Format MATCH story for interview use with visual indicators.
        
        Args:
            story: The story to format
            
        Returns:
            Formatted story string
        """
        score, errors = self.validate_match_story(story)
        culture_score, values = self.analyze_culture_fit(story)
        
        output = []
        output.append("=" * 80)
        output.append(f"MATCH FRAMEWORK STORY: {story.position} at {story.company_name}")
        output.append("=" * 80)
        output.append(f"\nCompany Type: {story.company_type.upper()}")
        output.append(f"Completeness: {score}%")
        output.append(f"Culture Fit: {culture_score}%")
        output.append(f"Values Aligned: {len(values)}")
        
        if score >= 80 and culture_score >= 60:
            output.append("Status:  Ready for Interview")
        else:
            output.append("Status:  Needs Refinement")
        
        output.append("\n" + "-" * 80)
        
        # Mission
        output.append("\n MISSION: Values & Purpose Alignment")
        output.append("-" * 40)
        output.append(story.mission if story.mission else "[Not provided]")
        
        # Alignment
        output.append("\n ALIGNMENT: Career Goals Match")
        output.append("-" * 40)
        output.append(story.alignment if story.alignment else "[Not provided]")
        
        # Teamwork
        output.append("\n🤝 TEAMWORK: Culture & Collaboration Fit")
        output.append("-" * 40)
        output.append(story.teamwork if story.teamwork else "[Not provided]")
        
        # Challenge
        output.append("\n CHALLENGE: Growth Opportunities")
        output.append("-" * 40)
        output.append(story.challenge if story.challenge else "[Not provided]")
        
        # Heuristic
        output.append("\n HEURISTIC: Decision-Making Framework")
        output.append("-" * 40)
        output.append(story.heuristic if story.heuristic else "[Not provided]")
        
        # Analysis
        output.append("\n" + "=" * 80)
        output.append("CULTURE FIT ANALYSIS")
        output.append("=" * 80)
        if values:
            output.append(f" Aligned Values: {', '.join(values)}")
        else:
            output.append(" No clear value alignment detected")
        
        if errors:
            output.append("\n Areas for Improvement:")
            for error in errors:
                output.append(f"  - {error}")
        
        output.append("\n" + "=" * 80)
        
        return "\n".join(output)
    
    def save_story(self, story: MATCHStory, filename: Optional[str] = None) -> str:
        """
        Save MATCH story to JSON file.
        
        Args:
            story: The story to save
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        # Create directory if it doesn't exist
        save_dir = Path("match_stories")
        save_dir.mkdir(exist_ok=True)
        
        # Generate filename
        if filename is None:
            safe_name = re.sub(r'[^\w\s-]', '', story.company_name.lower())
            safe_name = re.sub(r'[-\s]+', '_', safe_name)
            filename = f"{safe_name}_{story.position.lower().replace(' ', '_')}.json"
        
        filepath = save_dir / filename
        
        # Convert to dict
        story_dict = {
            'mission': story.mission,
            'alignment': story.alignment,
            'teamwork': story.teamwork,
            'challenge': story.challenge,
            'heuristic': story.heuristic,
            'company_name': story.company_name,
            'company_type': story.company_type,
            'position': story.position,
            'created_date': story.created_date,
            'culture_fit_score': story.culture_fit_score,
            'values_alignment': story.values_alignment,
            'team_compatibility': story.team_compatibility,
            'growth_potential': story.growth_potential,
            'framework': 'MATCH'
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(story_dict, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_story(self, filepath: str) -> MATCHStory:
        """
        Load MATCH story from JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            MATCHStory object
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return MATCHStory(
            mission=data.get('mission', ''),
            alignment=data.get('alignment', ''),
            teamwork=data.get('teamwork', ''),
            challenge=data.get('challenge', ''),
            heuristic=data.get('heuristic', ''),
            company_name=data.get('company_name', ''),
            company_type=data.get('company_type', ''),
            position=data.get('position', ''),
            created_date=data.get('created_date', ''),
            culture_fit_score=data.get('culture_fit_score', 0.0),
            values_alignment=data.get('values_alignment', []),
            team_compatibility=data.get('team_compatibility', ''),
            growth_potential=data.get('growth_potential', '')
        )


def main():
    """Demonstrate MATCH Framework automation capabilities."""
    
    print("\n" + "=" * 80)
    print("MATCH FRAMEWORK AUTOMATION SYSTEM - DEMONSTRATION")
    print("=" * 80)
    
    automation = MATCHFrameworkAutomation()
    
    # Example 1: Component Detection
    print("\n\n EXAMPLE 1: Component Detection")
    print("-" * 80)
    
    example_text = """
    I'm passionate about Stripe's mission to increase the GDP of the internet and make 
    online payments accessible to everyone. Their values around transparency and user-first 
    design align perfectly with my own principles. In my 5-year career vision, I see myself 
    becoming a senior product manager leading payment infrastructure initiatives, and this 
    role is the perfect next step for developing my technical product skills. I thrive in 
    collaborative, engineering-driven environments where I can partner closely with technical 
    teams. I'm excited about the challenges of scaling payment systems and solving complex 
    technical problems that impact millions of users. When making product decisions, I use 
    a framework that balances user impact, technical feasibility, and business objectives,
    always prioritizing the most critical trade-offs first.
    """
    
    detection_results = automation.detect_match_components(example_text)
    print("Detected components:")
    for component, confidence in detection_results.items():
        print(f"  {component.upper()}: {confidence}% confidence")
    
    # Example 2: Company Type Classification
    print("\n\n🏢 EXAMPLE 2: Company Type Classification")
    print("-" * 80)
    
    company_desc = "Fast-growing Series B startup building payment infrastructure for online businesses"
    company_type = automation.classify_company_type(company_desc)
    print(f"Company description: {company_desc}")
    print(f"Classified as: {company_type.upper()}")
    print(f"Culture characteristics: {automation.company_types[company_type]['culture']}")
    print(f"Key values: {', '.join(automation.company_types[company_type]['values'])}")
    
    # Example 3: Complete Story Validation
    print("\n\n EXAMPLE 3: Story Validation")
    print("-" * 80)
    
    complete_story = MATCHStory(
        company_name="Stripe",
        company_type="startup",
        position="Senior Product Manager",
        mission="I'm deeply passionate about Stripe's mission to increase the GDP of the internet by making online payments accessible to everyone. Their core values around transparency, user-first design, and building robust infrastructure resonate strongly with my own principles. I believe technology should empower businesses of all sizes, and Stripe's commitment to serving startups and enterprises alike aligns perfectly with my values.",
        alignment="This Senior PM role aligns perfectly with my 5-year career vision of leading payment infrastructure products at scale. I want to develop deep technical product skills in distributed systems and financial technology, and Stripe offers the ideal environment for this growth. My goal is to become a product leader who can drive complex technical initiatives while maintaining a customer-centric approach.",
        teamwork="I thrive in Stripe's collaborative, engineering-driven culture. My communication style emphasizes transparency and data-driven decision-making, which fits perfectly with how Stripe teams operate. I actively partner with engineering teams, seek diverse perspectives, and believe the best products come from cross-functional collaboration where everyone's expertise is valued.",
        challenge="I'm excited about the challenges of scaling payment systems to handle millions of transactions while maintaining 99.99% uptime. The complexity of building global payment infrastructure, handling edge cases across different countries and payment methods, and innovating on developer experience are exactly the types of ambitious problems I want to solve. I love working on systems where technical excellence directly impacts user success.",
        heuristic="My decision-making framework prioritizes user impact first, then evaluates technical feasibility and business value. When facing trade-offs, I use a scoring system that weighs customer pain points, implementation complexity, and strategic alignment. I believe in making reversible decisions quickly while taking more time on one-way doors, and I always validate assumptions with data before committing to major directions."
    )
    
    score, errors = automation.validate_match_story(complete_story)
    print(f"Validation Results:")
    print(f"  Completeness Score: {score}%")
    if errors:
        print(f"  Errors found: {len(errors)}")
        for error in errors:
            print(f"    - {error}")
    else:
        print("   Story is complete and interview-ready!")
    
    # Example 4: Culture Fit Analysis
    print("\n\n EXAMPLE 4: Culture Fit Analysis")
    print("-" * 80)
    
    culture_score, values = automation.analyze_culture_fit(complete_story)
    complete_story.culture_fit_score = culture_score
    complete_story.values_alignment = values
    
    print(f"Culture Fit Score: {culture_score}%")
    print(f"Aligned Values: {', '.join(values) if values else 'None detected'}")
    
    # Example 5: Auto-Improvement Suggestions
    print("\n\n💡 EXAMPLE 5: Auto-Improvement Suggestions")
    print("-" * 80)
    
    incomplete_story = MATCHStory(
        company_name="Google",
        company_type="enterprise",
        position="Software Engineer",
        mission="I like Google's mission to organize information.",
        alignment="This role fits my career goals.",
        teamwork="I work well with teams.",
        challenge="I want to solve hard problems.",
        heuristic="I make good decisions."
    )
    
    suggestions = automation.auto_improve_story(incomplete_story)
    print(f"Improvement suggestions for incomplete story:")
    for component, component_suggestions in suggestions.items():
        print(f"\n  {component.upper()}:")
        for suggestion in component_suggestions:
            print(f"    - {suggestion}")
    
    # Example 6: Company-Specific Prompts
    print("\n\n❓ EXAMPLE 6: Company-Specific Prompts")
    print("-" * 80)
    
    print("Mission prompts for STARTUP:")
    for i, prompt in enumerate(automation.generate_company_specific_prompts('startup', 'mission'), 1):
        print(f"  {i}. {prompt}")
    
    # Example 7: Template Generation
    print("\n\n EXAMPLE 7: Template Generation")
    print("-" * 80)
    
    template = automation.create_match_template("Amazon", "enterprise", "Product Manager")
    print(f"Template created for {template.position} at {template.company_name}")
    print(f"MISSION guidance: {template.mission[:100]}...")
    
    # Example 8: Interview Formatting
    print("\n\n🎤 EXAMPLE 8: Interview-Ready Formatting")
    print("-" * 80)
    
    formatted = automation.format_story_for_interview(complete_story)
    print(formatted)
    
    # Example 9: Story Persistence
    print("\n\n EXAMPLE 9: Story Persistence")
    print("-" * 80)
    
    saved_path = automation.save_story(complete_story)
    print(f" Story saved to: {saved_path}")
    
    # Load it back
    loaded_story = automation.load_story(saved_path)
    print(f" Story loaded successfully")
    print(f"   Company: {loaded_story.company_name}")
    print(f"   Position: {loaded_story.position}")
    print(f"   Culture Fit: {loaded_story.culture_fit_score}%")
    
    print("\n" + "=" * 80)
    print("MATCH FRAMEWORK AUTOMATION - DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nAll features working successfully:")
    print("   Component detection with confidence scoring")
    print("   Company type classification")
    print("   Story validation with completeness scoring")
    print("   Culture fit analysis")
    print("   Auto-improvement suggestions")
    print("   Company-specific prompts")
    print("   Template generation")
    print("   Interview-ready formatting")
    print("   Story persistence (save/load)")
    print("\n")


if __name__ == "__main__":
    main()
