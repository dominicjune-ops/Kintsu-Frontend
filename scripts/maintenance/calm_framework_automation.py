"""
CALM Framework Automation System
Auto-detects, generates, and validates CALM stories for communication and conflict resolution

CALM Framework Components:
- C: Context - What was the situation and background?
- A: Action - What specific actions did you take?
- L: Learning - What did you learn from the experience?
- M: Mindset - How did this shape your thinking and approach?
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class CALMStory:
    """Represents a complete CALM framework story"""
    context: str
    action: str
    learning: str
    mindset: str
    completeness_score: float = 0.0
    validation_errors: List[str] = None
    story_type: str = "communication"  # communication, conflict, teamwork
    
    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []


class CALMFrameworkAutomation:
    """
    Automates CALM framework story creation and validation
    Focused on communication, conflict resolution, and soft skills
    """
    
    def __init__(self):
        self.component_keywords = {
            'context': [
                'situation', 'background', 'context', 'circumstances',
                'scenario', 'setting', 'environment', 'when', 'where',
                'team', 'project', 'working with', 'stakeholder',
                'misunderstanding', 'disagreement', 'challenge'
            ],
            'action': [
                'i did', 'i took', 'i initiated', 'i communicated',
                'i listened', 'i explained', 'i facilitated', 'i mediated',
                'approached', 'spoke with', 'addressed', 'clarified',
                'scheduled', 'organized', 'coordinated', 'resolved',
                'action', 'steps', 'response'
            ],
            'learning': [
                'learned', 'lesson', 'discovered', 'realized',
                'understood', 'insight', 'showed me', 'taught me',
                'important', 'key takeaway', 'gained understanding',
                'now know', 'experience taught'
            ],
            'mindset': [
                'approach', 'perspective', 'mindset', 'philosophy',
                'belief', 'value', 'principle', 'how i think',
                'shaped my', 'influences', 'guides', 'helps me',
                'always', 'now', 'future', 'going forward'
            ]
        }
        
        self.question_prompts = {
            'context': [
                "What was the situation or background?",
                "Can you describe the circumstances?",
                "What led to this situation?",
                "Who was involved and what was happening?"
            ],
            'action': [
                "What specific actions did you take?",
                "How did you respond to the situation?",
                "Walk me through your communication approach.",
                "What steps did you take to address this?"
            ],
            'learning': [
                "What did you learn from this experience?",
                "What insights did you gain?",
                "What would you tell someone facing a similar situation?",
                "What was your key takeaway?"
            ],
            'mindset': [
                "How has this shaped your approach going forward?",
                "What principles guide your thinking now?",
                "How has this influenced your perspective?",
                "What mindset do you carry from this experience?"
            ]
        }
        
        self.min_word_counts = {
            'context': 40,
            'action': 60,
            'learning': 35,
            'mindset': 30
        }
        
        # Story type classifications
        self.story_types = {
            'communication': [
                'miscommunication', 'clarify', 'explain', 'presentation',
                'update', 'inform', 'communicate', 'message', 'stakeholder'
            ],
            'conflict': [
                'disagreement', 'conflict', 'tension', 'dispute',
                'argument', 'opposing', 'friction', 'clash', 'resolve'
            ],
            'teamwork': [
                'collaborate', 'team', 'cooperation', 'partnership',
                'work together', 'joint', 'collective', 'group', 'coordinate'
            ],
            'feedback': [
                'feedback', 'criticism', 'critique', 'improvement',
                'coaching', 'guidance', 'advice', 'suggestion'
            ],
            'leadership': [
                'lead', 'manage', 'mentor', 'guide', 'motivate',
                'inspire', 'direct', 'delegate', 'empower'
            ]
        }
    
    def detect_calm_components(self, text: str) -> Dict[str, float]:
        """
        Detect which CALM components are present in text
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
    
    def classify_story_type(self, text: str) -> str:
        """
        Classify the type of CALM story based on content
        """
        text_lower = text.lower()
        type_scores = {}
        
        for story_type, keywords in self.story_types.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            type_scores[story_type] = matches
        
        # Return type with highest score, default to communication
        if not type_scores or max(type_scores.values()) == 0:
            return 'communication'
        
        return max(type_scores.items(), key=lambda x: x[1])[0]
    
    def extract_calm_components(self, text: str) -> Dict[str, str]:
        """
        Extract CALM components from text using pattern matching
        """
        components = {
            'context': '',
            'action': '',
            'learning': '',
            'mindset': ''
        }
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Analyze each sentence
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Detect which component this sentence belongs to
            scores = self.detect_calm_components(sentence)
            
            # Assign to component with highest score (if above threshold)
            max_component = max(scores.items(), key=lambda x: x[1])
            if max_component[1] >= 0.3:  # Threshold
                if components[max_component[0]]:
                    components[max_component[0]] += ' ' + sentence + '.'
                else:
                    components[max_component[0]] = sentence + '.'
        
        return components
    
    def validate_calm_story(self, story: CALMStory) -> Tuple[float, List[str]]:
        """
        Validate completeness of CALM story
        Returns (completeness_score, validation_errors)
        """
        errors = []
        component_scores = []
        
        for component in ['context', 'action', 'learning', 'mindset']:
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
            generic_words = ['something', 'someone', 'things', 'stuff']
            if any(word in content.lower() for word in generic_words):
                errors.append(
                    f"{component.upper()} contains generic language - be more specific"
                )
            
            # Component-specific validation
            if component == 'action':
                # Check for first-person action verbs
                action_verbs = ['i communicated', 'i listened', 'i explained',
                              'i facilitated', 'i addressed']
                if not any(verb in content.lower() for verb in action_verbs):
                    errors.append(
                        "ACTION should include specific communication verbs "
                        "(communicated, listened, explained, etc.)"
                    )
            
            if component == 'mindset':
                # Check for forward-looking language
                future_words = ['now', 'going forward', 'always', 'helps me',
                              'guides me', 'approach', 'believe']
                if not any(word in content.lower() for word in future_words):
                    errors.append(
                        "MINDSET should include forward-looking perspective "
                        "(now, going forward, helps me, etc.)"
                    )
        
        # Calculate overall completeness score
        completeness_score = sum(component_scores) / len(component_scores)
        
        return completeness_score, errors
    
    def generate_missing_prompts(self, story: CALMStory) -> List[str]:
        """
        Generate prompts for missing or weak CALM components
        """
        prompts = []
        
        for component in ['context', 'action', 'learning', 'mindset']:
            content = getattr(story, component)
            min_words = self.min_word_counts[component]
            
            # If missing or too short
            if not content or len(content.split()) < min_words:
                # Add random prompt from component prompts
                import random
                prompt = random.choice(self.question_prompts[component])
                prompts.append(f"**{component.upper()}**: {prompt}")
        
        return prompts
    
    def create_calm_template(self, story_type: str = "communication") -> str:
        """
        Generate a blank CALM template with prompts
        """
        type_examples = {
            'communication': "explaining a complex technical concept to stakeholders",
            'conflict': "resolving a disagreement with a team member",
            'teamwork': "collaborating on a cross-functional project",
            'feedback': "receiving and acting on constructive criticism",
            'leadership': "guiding a team through a challenging situation"
        }
        
        example = type_examples.get(story_type, "your experience")
        
        template = f"""
# CALM Framework Story: {example}

**Story Type**: {story_type.title()}

## C - Context
**Prompt**: What was the situation or background?

[Describe the circumstances, who was involved, and what led to this situation - minimum 40 words]


## A - Action
**Prompt**: What specific actions did you take?

[Detail your communication approach and specific steps - minimum 60 words]


## L - Learning
**Prompt**: What did you learn from this experience?

[Share insights and key takeaways - minimum 35 words]


## M - Mindset
**Prompt**: How has this shaped your approach going forward?

[Explain how this influences your perspective and principles - minimum 30 words]


---
*The CALM framework is ideal for demonstrating soft skills like communication, conflict resolution, and emotional intelligence.*
"""
        return template
    
    def auto_improve_story(self, story: CALMStory) -> Dict[str, str]:
        """
        Generate suggestions to improve CALM story
        """
        suggestions = {}
        
        for component in ['context', 'action', 'learning', 'mindset']:
            content = getattr(story, component)
            component_suggestions = []
            
            if not content:
                continue
            
            # Check for communication-specific language
            if component == 'action':
                communication_verbs = ['listened', 'explained', 'clarified',
                                     'facilitated', 'mediated', 'communicated']
                if not any(verb in content.lower() for verb in communication_verbs):
                    component_suggestions.append(
                        "Add specific communication verbs (listened, explained, clarified)"
                    )
                
                # Check for dialogue or direct quotes
                if '"' not in content and "'" not in content:
                    component_suggestions.append(
                        "Consider adding specific dialogue or what you said"
                    )
            
            # Check for emotional intelligence indicators
            if component == 'context':
                emotion_words = ['felt', 'frustrated', 'concerned', 'anxious',
                               'motivated', 'confused', 'stressed']
                if not any(word in content.lower() for word in emotion_words):
                    component_suggestions.append(
                        "Include emotional context (how people felt in the situation)"
                    )
            
            # Check for reflection in learning
            if component == 'learning':
                reflection_words = ['realized', 'understood', 'discovered',
                                  'important', 'valuable']
                if not any(word in content.lower() for word in reflection_words):
                    component_suggestions.append(
                        "Add reflective language (realized, understood, discovered)"
                    )
            
            # Check for future application in mindset
            if component == 'mindset':
                future_words = ['now', 'always', 'going forward', 'helps me',
                              'guides', 'approach']
                if not any(word in content.lower() for word in future_words):
                    component_suggestions.append(
                        "Include how this shapes future behavior (now, always, going forward)"
                    )
            
            if component_suggestions:
                suggestions[component] = component_suggestions
        
        return suggestions
    
    def format_story_for_interview(self, story: CALMStory) -> str:
        """
        Format CALM story for verbal delivery in interview
        """
        formatted = f"""
 **Interview-Ready CALM Story**
**Type**: {story.story_type.title()}

🔵 **CONTEXT**: {story.context}

 **ACTION**: {story.action}

💡 **LEARNING**: {story.learning}

 **MINDSET**: {story.mindset}

---
**Completeness Score**: {story.completeness_score:.1%}
**Ready for Interview**: {'Yes ' if story.completeness_score >= 0.9 else 'Needs Improvement '}

**Best Used For**: Communication, conflict resolution, teamwork, or soft skills questions
"""
        return formatted
    
    def save_story(self, story: CALMStory, filename: str) -> str:
        """
        Save CALM story to JSON file
        """
        output_dir = Path('calm_stories')
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'story': asdict(story),
                'timestamp': datetime.now().isoformat(),
                'framework': 'CALM'
            }, f, indent=2)
        
        return str(filepath)
    
    def load_story(self, filename: str) -> CALMStory:
        """
        Load CALM story from JSON file
        """
        filepath = Path('calm_stories') / f"{filename}.json"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return CALMStory(**data['story'])
    
    def get_story_type_recommendations(self, story_type: str) -> Dict[str, List[str]]:
        """
        Get recommendations specific to story type
        """
        recommendations = {
            'communication': {
                'focus': [
                    "Clarity of message",
                    "Audience adaptation",
                    "Active listening",
                    "Follow-up and confirmation"
                ],
                'action_tips': [
                    "Describe how you tailored your message",
                    "Mention specific communication channels used",
                    "Show active listening behaviors"
                ]
            },
            'conflict': {
                'focus': [
                    "Understanding all perspectives",
                    "Finding common ground",
                    "Professional demeanor",
                    "Win-win solutions"
                ],
                'action_tips': [
                    "Show empathy for both sides",
                    "Describe your mediation approach",
                    "Emphasize collaborative resolution"
                ]
            },
            'teamwork': {
                'focus': [
                    "Collaboration skills",
                    "Shared goals",
                    "Individual contributions",
                    "Team dynamics"
                ],
                'action_tips': [
                    "Highlight coordination efforts",
                    "Show respect for team members",
                    "Describe your role in team success"
                ]
            },
            'feedback': {
                'focus': [
                    "Receptiveness to feedback",
                    "Growth mindset",
                    "Action on feedback",
                    "Continuous improvement"
                ],
                'action_tips': [
                    "Show openness to criticism",
                    "Describe specific improvements made",
                    "Demonstrate learning agility"
                ]
            },
            'leadership': {
                'focus': [
                    "Influence without authority",
                    "Team motivation",
                    "Decision-making",
                    "Accountability"
                ],
                'action_tips': [
                    "Show how you inspired others",
                    "Describe your leadership style",
                    "Emphasize team empowerment"
                ]
            }
        }
        
        return recommendations.get(story_type, recommendations['communication'])


def main():
    """Demo of CALM Framework Automation"""
    
    automation = CALMFrameworkAutomation()
    
    print("\n" + "="*70)
    print("🧘 CALM FRAMEWORK AUTOMATION SYSTEM")
    print("="*70)
    
    # Example 1: Detect CALM components in text
    print("\n Example 1: Component Detection")
    print("-" * 70)
    
    sample_text = """
    Our team had a disagreement about the project timeline. As the tech lead,
    I scheduled a meeting to discuss concerns. I listened to each person's
    perspective and facilitated a conversation to find middle ground. We agreed
    on a revised timeline that addressed everyone's concerns. I learned that
    early communication prevents conflicts. This experience shaped my approach
    to always seek input before setting deadlines.
    """
    
    components = automation.detect_calm_components(sample_text)
    print("\nDetected Components:")
    for component, score in sorted(components.items(), key=lambda x: x[1], reverse=True):
        if score > 0:
            print(f"  • {component.upper()}: {score:.1%} confidence")
    
    story_type = automation.classify_story_type(sample_text)
    print(f"\n**Story Type**: {story_type.title()}")
    
    # Example 2: Create and validate story
    print("\n Example 2: Story Validation")
    print("-" * 70)
    
    story = CALMStory(
        context="Our development team and product team had conflicting priorities for a major release. The product team wanted to add new features, while engineering wanted to focus on technical debt and stability. Tensions were rising, and the project was at risk of delays due to this disagreement.",
        action="I facilitated a joint planning session where both teams could voice their concerns. I listened actively to understand each perspective, then helped create a visual roadmap showing how we could balance both needs. I proposed a phased approach: address critical technical debt first (2 weeks), then implement high-priority features (4 weeks). I communicated this plan to stakeholders with clear timelines and rationales.",
        learning="I learned that most conflicts arise from lack of communication and understanding, not actual incompatibility of goals. By creating a space for open dialogue and showing both teams that I valued their perspectives, we found a solution that satisfied everyone. I also discovered that visual communication (the roadmap) helps align diverse stakeholders much better than verbal explanations alone.",
        mindset="This experience fundamentally shaped how I approach cross-functional conflicts. I now always start by seeking to understand all perspectives before proposing solutions. I believe that most disagreements are opportunities to find better solutions that incorporate multiple viewpoints. Going forward, I proactively schedule alignment meetings before conflicts arise, and I always use visual tools to communicate complex plans.",
        story_type="conflict"
    )
    
    completeness, errors = automation.validate_calm_story(story)
    story.completeness_score = completeness
    story.validation_errors = errors
    
    print(f"\n**Completeness Score**: {completeness:.1%}")
    
    if errors:
        print("\n**Validation Errors**:")
        for error in errors:
            print(f"    {error}")
    else:
        print("\n Story is complete and interview-ready!")
    
    # Example 3: Auto-improve suggestions
    print("\n💡 Example 3: Story Improvement Suggestions")
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
    
    # Example 4: Format for interview
    print("\n🎤 Example 4: Interview-Ready Format")
    print("-" * 70)
    
    formatted = automation.format_story_for_interview(story)
    print(formatted)
    
    # Example 5: Story type recommendations
    print("\n📚 Example 5: Story Type Recommendations")
    print("-" * 70)
    
    recommendations = automation.get_story_type_recommendations(story.story_type)
    print(f"\n**For {story.story_type.title()} Stories**:")
    print("\n**Focus Areas**:")
    for focus in recommendations['focus']:
        print(f"  • {focus}")
    print("\n**Action Tips**:")
    for tip in recommendations['action_tips']:
        print(f"  • {tip}")
    
    # Example 6: Generate template
    print("\n Example 6: Template Generation for Different Types")
    print("-" * 70)
    
    for story_type in ['communication', 'conflict', 'teamwork', 'feedback']:
        template = automation.create_calm_template(story_type)
        print(f"\n**{story_type.title()}** template (first line):")
        print(template.split('\n')[1])
    
    # Save example story
    filepath = automation.save_story(story, "cross_functional_conflict_resolution")
    print(f"\n Story saved to: {filepath}")
    
    print("\n" + "="*70)
    print(" CALM FRAMEWORK AUTOMATION DEMO COMPLETE")
    print("="*70)
    print("\nFeatures Demonstrated:")
    print("   Component detection with confidence scoring")
    print("   Story type classification (communication, conflict, etc.)")
    print("   Story validation with completeness scoring")
    print("   Auto-improvement suggestions")
    print("   Interview-ready formatting")
    print("   Story type-specific recommendations")
    print("   Template generation for different scenarios")
    print("   Story persistence (save/load)")
    print("\n CALM framework ready for soft skills coaching!")
    print()


if __name__ == "__main__":
    main()
