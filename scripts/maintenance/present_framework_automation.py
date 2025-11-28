"""
PRESENT Framework Automation System
Auto-detects, generates, and validates PRESENT stories for behavioral interviews

PRESENT Framework Components:
- P: Problem - What was the challenge?
- R: Role - What was your specific role?
- E: Execution - How did you execute the solution?
- S: Solution - What solution did you implement?
- E: Evaluation - What were the results?
- N: Next Steps - What would you do differently?
- T: Takeaways - What did you learn?
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class PRESENTStory:
    """Represents a complete PRESENT framework story"""
    problem: str
    role: str
    execution: str
    solution: str
    evaluation: str
    next_steps: str
    takeaways: str
    completeness_score: float = 0.0
    validation_errors: List[str] = None
    
    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []


class PRESENTFrameworkAutomation:
    """
    Automates PRESENT framework story creation and validation
    """
    
    def __init__(self):
        self.component_keywords = {
            'problem': [
                'challenge', 'problem', 'issue', 'difficulty', 'obstacle',
                'faced', 'encountered', 'struggling', 'conflict', 'crisis',
                'needed to', 'had to', 'requirement', 'situation'
            ],
            'role': [
                'my role', 'i was', 'responsible for', 'led', 'managed',
                'owned', 'coordinated', 'in charge of', 'tasked with',
                'as the', 'position', 'capacity'
            ],
            'execution': [
                'implemented', 'executed', 'carried out', 'performed',
                'conducted', 'organized', 'coordinated', 'facilitated',
                'initiated', 'launched', 'deployed', 'process', 'approach',
                'methodology', 'steps', 'actions'
            ],
            'solution': [
                'solution', 'resolved', 'fixed', 'addressed', 'solved',
                'created', 'developed', 'designed', 'built', 'established',
                'implemented', 'delivered', 'achieved', 'outcome'
            ],
            'evaluation': [
                'result', 'outcome', 'impact', 'improved', 'increased',
                'decreased', 'reduced', 'saved', 'generated', 'achieved',
                'metric', 'percentage', 'number', 'measurement', 'kpi',
                'success', 'successful'
            ],
            'next_steps': [
                'would', 'could have', 'should have', 'next time',
                'in the future', 'differently', 'improve', 'enhance',
                'if i had', 'looking back', 'retrospect', 'lesson'
            ],
            'takeaways': [
                'learned', 'lesson', 'takeaway', 'insight', 'realized',
                'understood', 'discovered', 'gained', 'key learning',
                'important to', 'showed me', 'taught me', 'experience'
            ]
        }
        
        self.question_prompts = {
            'problem': [
                "What was the specific challenge or problem you faced?",
                "Can you describe the situation in more detail?",
                "What made this situation challenging?",
                "What were the key obstacles?"
            ],
            'role': [
                "What was your specific role in this situation?",
                "What were your responsibilities?",
                "How were you involved?",
                "What did you personally own?"
            ],
            'execution': [
                "How did you approach solving this problem?",
                "What steps did you take?",
                "Walk me through your process.",
                "What methodology did you use?"
            ],
            'solution': [
                "What solution did you implement?",
                "What was the final outcome?",
                "How did you resolve the issue?",
                "What did you deliver?"
            ],
            'evaluation': [
                "What were the measurable results?",
                "How did you measure success?",
                "What was the impact?",
                "Can you quantify the results?"
            ],
            'next_steps': [
                "What would you do differently next time?",
                "What could have been improved?",
                "Looking back, what changes would you make?",
                "What lessons did this teach you about future approaches?"
            ],
            'takeaways': [
                "What did you learn from this experience?",
                "What was your key takeaway?",
                "How has this shaped your approach?",
                "What insights did you gain?"
            ]
        }
        
        self.min_word_counts = {
            'problem': 30,
            'role': 20,
            'execution': 50,
            'solution': 40,
            'evaluation': 30,
            'next_steps': 25,
            'takeaways': 30
        }
    
    def detect_present_components(self, text: str) -> Dict[str, float]:
        """
        Detect which PRESENT components are present in text
        Returns confidence scores for each component
        """
        text_lower = text.lower()
        component_scores = {}
        
        for component, keywords in self.component_keywords.items():
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            # Calculate confidence score (0-1)
            # Max score when 3+ keywords found
            confidence = min(matches / 3.0, 1.0)
            component_scores[component] = confidence
        
        return component_scores
    
    def extract_present_components(self, text: str) -> Dict[str, str]:
        """
        Extract PRESENT components from text using pattern matching
        """
        components = {
            'problem': '',
            'role': '',
            'execution': '',
            'solution': '',
            'evaluation': '',
            'next_steps': '',
            'takeaways': ''
        }
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Analyze each sentence
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Detect which component this sentence belongs to
            scores = self.detect_present_components(sentence)
            
            # Assign to component with highest score (if above threshold)
            max_component = max(scores.items(), key=lambda x: x[1])
            if max_component[1] >= 0.3:  # Threshold
                if components[max_component[0]]:
                    components[max_component[0]] += ' ' + sentence + '.'
                else:
                    components[max_component[0]] = sentence + '.'
        
        return components
    
    def validate_present_story(self, story: PRESENTStory) -> Tuple[float, List[str]]:
        """
        Validate completeness of PRESENT story
        Returns (completeness_score, validation_errors)
        """
        errors = []
        component_scores = []
        
        for component in ['problem', 'role', 'execution', 'solution', 
                         'evaluation', 'next_steps', 'takeaways']:
            content = getattr(story, component)
            min_words = self.min_word_counts[component]
            
            # Check if component exists
            if not content or not content.strip():
                errors.append(f"Missing {component.upper()} component")
                component_scores.append(0.0)
                continue
            
            # Check word count
            word_count = len(content.split())
            if word_count < min_words:
                errors.append(
                    f"{component.upper()} too short: {word_count} words "
                    f"(minimum {min_words})"
                )
                # Partial score based on word count
                component_scores.append(min(word_count / min_words, 1.0))
            else:
                component_scores.append(1.0)
            
            # Check for specificity (avoid generic language)
            generic_words = ['something', 'someone', 'things', 'stuff', 
                           'various', 'several', 'many']
            if any(word in content.lower() for word in generic_words):
                errors.append(
                    f"{component.upper()} contains generic language - be more specific"
                )
        
        # Calculate overall completeness score
        completeness_score = sum(component_scores) / len(component_scores)
        
        return completeness_score, errors
    
    def generate_missing_prompts(self, story: PRESENTStory) -> List[str]:
        """
        Generate prompts for missing or weak PRESENT components
        """
        prompts = []
        
        for component in ['problem', 'role', 'execution', 'solution', 
                         'evaluation', 'next_steps', 'takeaways']:
            content = getattr(story, component)
            min_words = self.min_word_counts[component]
            
            # If missing or too short
            if not content or len(content.split()) < min_words:
                # Add random prompt from component prompts
                import random
                prompt = random.choice(self.question_prompts[component])
                prompts.append(f"**{component.upper()}**: {prompt}")
        
        return prompts
    
    def create_present_template(self, topic: str = "your experience") -> str:
        """
        Generate a blank PRESENT template with prompts
        """
        template = f"""
# PRESENT Framework Story: {topic}

## P - Problem
**Prompt**: What was the specific challenge or problem you faced?

[Describe the situation, challenge, or problem - minimum 30 words]


## R - Role
**Prompt**: What was your specific role in this situation?

[Explain your responsibilities and involvement - minimum 20 words]


## E - Execution
**Prompt**: How did you approach solving this problem?

[Detail your process, methodology, and actions - minimum 50 words]


## S - Solution
**Prompt**: What solution did you implement?

[Describe the solution you delivered - minimum 40 words]


## E - Evaluation
**Prompt**: What were the measurable results?

[Quantify the impact and outcomes - minimum 30 words]


## N - Next Steps
**Prompt**: What would you do differently next time?

[Reflect on improvements for the future - minimum 25 words]


## T - Takeaways
**Prompt**: What did you learn from this experience?

[Share key insights and lessons learned - minimum 30 words]


---
*Complete each section with specific, measurable details. Use the STAR method within each component where applicable.*
"""
        return template
    
    def auto_improve_story(self, story: PRESENTStory) -> Dict[str, str]:
        """
        Generate suggestions to improve PRESENT story
        """
        suggestions = {}
        
        for component in ['problem', 'role', 'execution', 'solution', 
                         'evaluation', 'next_steps', 'takeaways']:
            content = getattr(story, component)
            component_suggestions = []
            
            if not content:
                continue
            
            # Check for metrics in evaluation
            if component == 'evaluation':
                if not re.search(r'\d+%|\d+x|increased|decreased|saved|\$\d+', content):
                    component_suggestions.append(
                        "Add specific metrics (percentages, dollar amounts, time saved)"
                    )
            
            # Check for action verbs
            action_verbs = ['led', 'created', 'implemented', 'designed', 
                          'developed', 'managed', 'coordinated']
            if component in ['role', 'execution', 'solution']:
                if not any(verb in content.lower() for verb in action_verbs):
                    component_suggestions.append(
                        "Use strong action verbs (led, created, implemented, etc.)"
                    )
            
            # Check for first-person perspective
            if not re.search(r'\bi\b|\bmy\b|\bme\b', content.lower()):
                component_suggestions.append(
                    "Use first-person perspective (I, my, me) to show ownership"
                )
            
            if component_suggestions:
                suggestions[component] = component_suggestions
        
        return suggestions
    
    def format_story_for_interview(self, story: PRESENTStory) -> str:
        """
        Format PRESENT story for verbal delivery in interview
        """
        formatted = f"""
 **Interview-Ready PRESENT Story**

 **PROBLEM**: {story.problem}

👤 **ROLE**: {story.role}

⚙️ **EXECUTION**: {story.execution}

 **SOLUTION**: {story.solution}

 **EVALUATION**: {story.evaluation}

 **NEXT STEPS**: {story.next_steps}

💡 **TAKEAWAYS**: {story.takeaways}

---
**Completeness Score**: {story.completeness_score:.1%}
**Ready for Interview**: {'Yes ' if story.completeness_score >= 0.9 else 'Needs Improvement '}
"""
        return formatted
    
    def save_story(self, story: PRESENTStory, filename: str) -> str:
        """
        Save PRESENT story to JSON file
        """
        output_dir = Path('present_stories')
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'story': asdict(story),
                'timestamp': datetime.now().isoformat(),
                'framework': 'PRESENT'
            }, f, indent=2)
        
        return str(filepath)
    
    def load_story(self, filename: str) -> PRESENTStory:
        """
        Load PRESENT story from JSON file
        """
        filepath = Path('present_stories') / f"{filename}.json"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return PRESENTStory(**data['story'])


def main():
    """Demo of PRESENT Framework Automation"""
    
    automation = PRESENTFrameworkAutomation()
    
    print("\n" + "="*70)
    print(" PRESENT FRAMEWORK AUTOMATION SYSTEM")
    print("="*70)
    
    # Example 1: Detect PRESENT components in text
    print("\n Example 1: Component Detection")
    print("-" * 70)
    
    sample_text = """
    I faced a challenge when our website performance degraded significantly.
    As the lead developer, I was responsible for identifying and fixing the issue.
    I analyzed the codebase, implemented caching, and optimized database queries.
    The solution reduced page load time by 60% and improved user satisfaction.
    I learned that proactive monitoring prevents performance issues.
    """
    
    components = automation.detect_present_components(sample_text)
    print("\nDetected Components:")
    for component, score in sorted(components.items(), key=lambda x: x[1], reverse=True):
        if score > 0:
            print(f"  • {component.upper()}: {score:.1%} confidence")
    
    # Example 2: Extract components
    print("\n Example 2: Component Extraction")
    print("-" * 70)
    
    extracted = automation.extract_present_components(sample_text)
    for component, content in extracted.items():
        if content:
            print(f"\n**{component.upper()}**: {content[:100]}...")
    
    # Example 3: Create and validate story
    print("\n Example 3: Story Validation")
    print("-" * 70)
    
    story = PRESENTStory(
        problem="Website performance degraded, causing user complaints and 30% bounce rate increase.",
        role="Lead developer responsible for site performance and optimization.",
        execution="Analyzed codebase with profiling tools, identified bottlenecks in database queries, implemented Redis caching layer, optimized image loading with lazy loading, and compressed static assets.",
        solution="Deployed comprehensive performance optimization reducing load times from 5s to 2s.",
        evaluation="Achieved 60% faster page loads, reduced bounce rate by 25%, increased conversions by 15%, and improved Core Web Vitals scores from 40 to 95.",
        next_steps="Would implement automated performance monitoring earlier to catch issues before they impact users.",
        takeaways="Learned that performance optimization requires both quick fixes and long-term architectural improvements. Regular monitoring and proactive optimization prevent major issues."
    )
    
    completeness, errors = automation.validate_present_story(story)
    story.completeness_score = completeness
    story.validation_errors = errors
    
    print(f"\n**Completeness Score**: {completeness:.1%}")
    
    if errors:
        print("\n**Validation Errors**:")
        for error in errors:
            print(f"    {error}")
    else:
        print("\n Story is complete and interview-ready!")
    
    # Example 4: Generate missing prompts
    print("\n❓ Example 4: Missing Component Prompts")
    print("-" * 70)
    
    incomplete_story = PRESENTStory(
        problem="Had a problem with the system",
        role="I worked on it",
        execution="",
        solution="",
        evaluation="",
        next_steps="",
        takeaways=""
    )
    
    prompts = automation.generate_missing_prompts(incomplete_story)
    print("\n**Questions to Complete Your Story**:")
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt}")
    
    # Example 5: Generate template
    print("\n Example 5: Blank Template Generation")
    print("-" * 70)
    
    template = automation.create_present_template("team conflict resolution")
    print("\n[Template generated - first 200 characters]")
    print(template[:200] + "...")
    
    # Example 6: Auto-improve suggestions
    print("\n💡 Example 6: Story Improvement Suggestions")
    print("-" * 70)
    
    suggestions = automation.auto_improve_story(story)
    if suggestions:
        print("\n**Improvement Suggestions**:")
        for component, tips in suggestions.items():
            print(f"\n{component.upper()}:")
            for tip in tips:
                print(f"  • {tip}")
    else:
        print("\n No improvements needed - story is well-structured!")
    
    # Example 7: Format for interview
    print("\n🎤 Example 7: Interview-Ready Format")
    print("-" * 70)
    
    formatted = automation.format_story_for_interview(story)
    print(formatted)
    
    # Save example story
    filepath = automation.save_story(story, "website_performance_optimization")
    print(f"\n Story saved to: {filepath}")
    
    print("\n" + "="*70)
    print(" PRESENT FRAMEWORK AUTOMATION DEMO COMPLETE")
    print("="*70)
    print("\nFeatures Demonstrated:")
    print("   Component detection with confidence scoring")
    print("   Automatic content extraction")
    print("   Story validation with completeness scoring")
    print("   Missing component prompt generation")
    print("   Template creation")
    print("   Auto-improvement suggestions")
    print("   Interview-ready formatting")
    print("   Story persistence (save/load)")
    print("\n System ready for integration with career coaching platform!")
    print()


if __name__ == "__main__":
    main()
