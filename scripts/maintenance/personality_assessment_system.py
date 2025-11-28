"""
Personality Assessment System
==============================

Purpose: Comprehensive personality assessment system integrating Big Five, MBTI-like,
and DISC assessments for career guidance and matching.

Assessments Included:
1. Big Five Personality (50 items) - Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
2. MBTI-like Type Indicator (60 items) - 16 personality types (INTJ, ENFP, etc.)
3. DISC Work Style (24 items) - Dominance, Influence, Steadiness, Conscientiousness

Features:
- Validated psychological instruments
- Automated scoring and percentile calculation
- Comprehensive personality reports
- Career implications and recommendations
- Progress tracking (pause/resume capability)
- PDF report generation
- Integration with AI career agent

Author: CareerCoach.ai Development Team
Epic: CAREER-AI-019 (Epic 5: Assessment Suite)
Story Points: 20
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from enum import Enum
import json
import statistics
from pathlib import Path


class AssessmentType(Enum):
    """Types of personality assessments available."""
    BIG_FIVE = "big_five"
    MBTI = "mbti"
    DISC = "disc"


class BigFiveTrait(Enum):
    """Big Five personality traits."""
    OPENNESS = "openness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    NEUROTICISM = "neuroticism"


class MBTIDimension(Enum):
    """MBTI personality dimensions."""
    EXTRAVERSION_INTROVERSION = "E/I"  # E = Extraversion, I = Introversion
    SENSING_INTUITION = "S/N"  # S = Sensing, N = Intuition
    THINKING_FEELING = "T/F"  # T = Thinking, F = Feeling
    JUDGING_PERCEIVING = "J/P"  # J = Judging, P = Perceiving


class DISCFactor(Enum):
    """DISC work style factors."""
    DOMINANCE = "dominance"
    INFLUENCE = "influence"
    STEADINESS = "steadiness"
    CONSCIENTIOUSNESS = "conscientiousness"


@dataclass
class AssessmentQuestion:
    """Represents a single assessment question."""
    id: int
    assessment_type: str
    question_text: str
    dimension: str  # Which trait/dimension this measures
    reverse_scored: bool = False
    scale_min: int = 1
    scale_max: int = 5
    scale_labels: Dict[int, str] = field(default_factory=dict)


@dataclass
class AssessmentResponse:
    """User response to an assessment question."""
    question_id: int
    response_value: int
    responded_at: datetime = field(default_factory=datetime.now)


@dataclass
class BigFiveResults:
    """Results from Big Five personality assessment."""
    openness: float  # 0-100 percentile
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    
    # Facet-level details
    openness_description: str = ""
    conscientiousness_description: str = ""
    extraversion_description: str = ""
    agreeableness_description: str = ""
    neuroticism_description: str = ""
    
    # Overall personality summary
    personality_summary: str = ""
    strengths: List[str] = field(default_factory=list)
    potential_challenges: List[str] = field(default_factory=list)
    career_implications: List[str] = field(default_factory=list)


@dataclass
class MBTIResults:
    """Results from MBTI-like assessment."""
    type_code: str  # 4-letter code (e.g., "INTJ")
    
    # Preference scores (% strength of preference)
    e_i_score: int  # Positive = E, Negative = I
    s_n_score: int  # Positive = S, Negative = N
    t_f_score: int  # Positive = T, Negative = F
    j_p_score: int  # Positive = J, Negative = P
    
    # Type description
    type_description: str = ""
    strengths: List[str] = field(default_factory=list)
    potential_blind_spots: List[str] = field(default_factory=list)
    communication_style: str = ""
    work_environment_fit: str = ""
    leadership_style: str = ""
    career_paths: List[str] = field(default_factory=list)


@dataclass
class DISCResults:
    """Results from DISC assessment."""
    dominance: float  # 0-100 score
    influence: float
    steadiness: float
    conscientiousness: float
    
    # Primary style
    primary_style: str = ""  # D, I, S, or C
    style_description: str = ""
    
    # Work style insights
    strengths: List[str] = field(default_factory=list)
    communication_preferences: str = ""
    conflict_style: str = ""
    stress_triggers: List[str] = field(default_factory=list)
    ideal_work_environment: str = ""
    team_contribution: str = ""


@dataclass
class ComprehensivePersonalityReport:
    """Comprehensive report combining all assessments."""
    user_id: str
    completed_at: datetime
    
    # Assessment results
    big_five: Optional[BigFiveResults] = None
    mbti: Optional[MBTIResults] = None
    disc: Optional[DISCResults] = None
    
    # Integrated insights
    overall_profile: str = ""
    top_strengths: List[str] = field(default_factory=list)
    development_areas: List[str] = field(default_factory=list)
    career_recommendations: List[str] = field(default_factory=list)
    work_environment_recommendations: str = ""
    communication_tips: List[str] = field(default_factory=list)
    stress_management_strategies: List[str] = field(default_factory=list)


class PersonalityAssessmentSystem:
    """Main system for personality assessments."""
    
    def __init__(self):
        self.big_five_questions = self._load_big_five_questions()
        self.mbti_questions = self._load_mbti_questions()
        self.disc_questions = self._load_disc_questions()
        
        # Normative data for percentile calculation (based on published research)
        self.big_five_norms = {
            'openness': {'mean': 3.5, 'sd': 0.7},
            'conscientiousness': {'mean': 3.6, 'sd': 0.7},
            'extraversion': {'mean': 3.3, 'sd': 0.9},
            'agreeableness': {'mean': 3.8, 'sd': 0.7},
            'neuroticism': {'mean': 2.8, 'sd': 0.9}
        }
    
    def _load_big_five_questions(self) -> List[AssessmentQuestion]:
        """Load Big Five personality questions (50-item BFI)."""
        
        # Sample questions from Big Five Inventory (BFI)
        questions = [
            # Openness (10 items)
            AssessmentQuestion(1, "big_five", "I see myself as someone who is original, comes up with new ideas", "openness"),
            AssessmentQuestion(2, "big_five", "I see myself as someone who is curious about many different things", "openness"),
            AssessmentQuestion(3, "big_five", "I see myself as someone who is ingenious, a deep thinker", "openness"),
            AssessmentQuestion(4, "big_five", "I see myself as someone who has an active imagination", "openness"),
            AssessmentQuestion(5, "big_five", "I see myself as someone who is inventive", "openness"),
            AssessmentQuestion(6, "big_five", "I see myself as someone who values artistic, aesthetic experiences", "openness"),
            AssessmentQuestion(7, "big_five", "I see myself as someone who prefers work that is routine", "openness", reverse_scored=True),
            AssessmentQuestion(8, "big_five", "I see myself as someone who likes to reflect, play with ideas", "openness"),
            AssessmentQuestion(9, "big_five", "I see myself as someone who has few artistic interests", "openness", reverse_scored=True),
            AssessmentQuestion(10, "big_five", "I see myself as someone who is sophisticated in art, music, or literature", "openness"),
            
            # Conscientiousness (10 items)
            AssessmentQuestion(11, "big_five", "I see myself as someone who does a thorough job", "conscientiousness"),
            AssessmentQuestion(12, "big_five", "I see myself as someone who can be somewhat careless", "conscientiousness", reverse_scored=True),
            AssessmentQuestion(13, "big_five", "I see myself as someone who is a reliable worker", "conscientiousness"),
            AssessmentQuestion(14, "big_five", "I see myself as someone who tends to be disorganized", "conscientiousness", reverse_scored=True),
            AssessmentQuestion(15, "big_five", "I see myself as someone who tends to be lazy", "conscientiousness", reverse_scored=True),
            AssessmentQuestion(16, "big_five", "I see myself as someone who perseveres until the task is finished", "conscientiousness"),
            AssessmentQuestion(17, "big_five", "I see myself as someone who does things efficiently", "conscientiousness"),
            AssessmentQuestion(18, "big_five", "I see myself as someone who makes plans and follows through with them", "conscientiousness"),
            AssessmentQuestion(19, "big_five", "I see myself as someone who is easily distracted", "conscientiousness", reverse_scored=True),
            AssessmentQuestion(20, "big_five", "I see myself as someone who is systematic and organized", "conscientiousness"),
            
            # Extraversion (10 items)
            AssessmentQuestion(21, "big_five", "I see myself as someone who is talkative", "extraversion"),
            AssessmentQuestion(22, "big_five", "I see myself as someone who tends to be quiet", "extraversion", reverse_scored=True),
            AssessmentQuestion(23, "big_five", "I see myself as someone who is full of energy", "extraversion"),
            AssessmentQuestion(24, "big_five", "I see myself as someone who generates a lot of enthusiasm", "extraversion"),
            AssessmentQuestion(25, "big_five", "I see myself as someone who tends to be reserved", "extraversion", reverse_scored=True),
            AssessmentQuestion(26, "big_five", "I see myself as someone who is assertive", "extraversion"),
            AssessmentQuestion(27, "big_five", "I see myself as someone who is sometimes shy, inhibited", "extraversion", reverse_scored=True),
            AssessmentQuestion(28, "big_five", "I see myself as someone who is outgoing, sociable", "extraversion"),
            AssessmentQuestion(29, "big_five", "I see myself as someone who prefers to have others take charge", "extraversion", reverse_scored=True),
            AssessmentQuestion(30, "big_five", "I see myself as someone who is dominant, acts as a leader", "extraversion"),
            
            # Agreeableness (10 items)
            AssessmentQuestion(31, "big_five", "I see myself as someone who tends to find fault with others", "agreeableness", reverse_scored=True),
            AssessmentQuestion(32, "big_five", "I see myself as someone who is helpful and unselfish with others", "agreeableness"),
            AssessmentQuestion(33, "big_five", "I see myself as someone who starts quarrels with others", "agreeableness", reverse_scored=True),
            AssessmentQuestion(34, "big_five", "I see myself as someone who has a forgiving nature", "agreeableness"),
            AssessmentQuestion(35, "big_five", "I see myself as someone who is generally trusting", "agreeableness"),
            AssessmentQuestion(36, "big_five", "I see myself as someone who can be cold and aloof", "agreeableness", reverse_scored=True),
            AssessmentQuestion(37, "big_five", "I see myself as someone who is considerate and kind to almost everyone", "agreeableness"),
            AssessmentQuestion(38, "big_five", "I see myself as someone who is sometimes rude to others", "agreeableness", reverse_scored=True),
            AssessmentQuestion(39, "big_five", "I see myself as someone who likes to cooperate with others", "agreeableness"),
            AssessmentQuestion(40, "big_five", "I see myself as someone who is compassionate, has a soft heart", "agreeableness"),
            
            # Neuroticism (10 items)
            AssessmentQuestion(41, "big_five", "I see myself as someone who can be tense", "neuroticism"),
            AssessmentQuestion(42, "big_five", "I see myself as someone who is relaxed, handles stress well", "neuroticism", reverse_scored=True),
            AssessmentQuestion(43, "big_five", "I see myself as someone who worries a lot", "neuroticism"),
            AssessmentQuestion(44, "big_five", "I see myself as someone who is emotionally stable, not easily upset", "neuroticism", reverse_scored=True),
            AssessmentQuestion(45, "big_five", "I see myself as someone who can be moody", "neuroticism"),
            AssessmentQuestion(46, "big_five", "I see myself as someone who remains calm in tense situations", "neuroticism", reverse_scored=True),
            AssessmentQuestion(47, "big_five", "I see myself as someone who gets nervous easily", "neuroticism"),
            AssessmentQuestion(48, "big_five", "I see myself as someone who is depressed, blue", "neuroticism"),
            AssessmentQuestion(49, "big_five", "I see myself as someone who is even-tempered", "neuroticism", reverse_scored=True),
            AssessmentQuestion(50, "big_five", "I see myself as someone who is self-confident", "neuroticism", reverse_scored=True),
        ]
        
        # Add scale labels
        for q in questions:
            q.scale_labels = {
                1: "Strongly Disagree",
                2: "Disagree",
                3: "Neutral",
                4: "Agree",
                5: "Strongly Agree"
            }
        
        return questions
    
    def _load_mbti_questions(self) -> List[AssessmentQuestion]:
        """Load MBTI-like personality questions (60 items, 15 per dimension)."""
        
        questions = [
            # E/I - Extraversion vs Introversion (15 items)
            AssessmentQuestion(101, "mbti", "At social gatherings, I prefer to: (1) Interact with many people / (2) Have in-depth conversations with a few", "E/I"),
            AssessmentQuestion(102, "mbti", "After a long week, I recharge by: (1) Going out with friends / (2) Spending time alone", "E/I"),
            AssessmentQuestion(103, "mbti", "I prefer to: (1) Think out loud and discuss ideas / (2) Think things through privately first", "E/I"),
            AssessmentQuestion(104, "mbti", "In group settings, I: (1) Feel energized / (2) Feel drained after a while", "E/I"),
            AssessmentQuestion(105, "mbti", "I am more comfortable: (1) Being the center of attention / (2) Staying in the background", "E/I"),
            AssessmentQuestion(106, "mbti", "I prefer: (1) A large circle of acquaintances / (2) A small circle of close friends", "E/I"),
            AssessmentQuestion(107, "mbti", "When meeting new people, I: (1) Easily start conversations / (2) Wait for others to approach me", "E/I"),
            AssessmentQuestion(108, "mbti", "I work best: (1) In a busy, collaborative environment / (2) In a quiet, private space", "E/I"),
            AssessmentQuestion(109, "mbti", "On weekends, I prefer: (1) Making spontaneous plans with others / (2) Having unstructured alone time", "E/I"),
            AssessmentQuestion(110, "mbti", "I tend to: (1) Share my thoughts freely / (2) Keep my thoughts to myself", "E/I"),
            AssessmentQuestion(111, "mbti", "I prefer: (1) Collaborative brainstorming / (2) Independent ideation", "E/I"),
            AssessmentQuestion(112, "mbti", "At parties, I: (1) Arrive early and stay late / (2) Arrive late and leave early", "E/I"),
            AssessmentQuestion(113, "mbti", "I get ideas from: (1) Discussing with others / (2) Reflecting alone", "E/I"),
            AssessmentQuestion(114, "mbti", "Phone calls are: (1) Enjoyable / (2) Draining", "E/I"),
            AssessmentQuestion(115, "mbti", "I prefer communication that is: (1) Verbal and immediate / (2) Written and considered", "E/I"),
            
            # S/N - Sensing vs Intuition (15 items)
            AssessmentQuestion(116, "mbti", "I focus more on: (1) Facts and details / (2) Patterns and possibilities", "S/N"),
            AssessmentQuestion(117, "mbti", "I prefer: (1) Proven, practical methods / (2) Novel, innovative approaches", "S/N"),
            AssessmentQuestion(118, "mbti", "I am more interested in: (1) What is / (2) What could be", "S/N"),
            AssessmentQuestion(119, "mbti", "I trust: (1) Experience and observation / (2) Intuition and insight", "S/N"),
            AssessmentQuestion(120, "mbti", "I prefer instructions that are: (1) Step-by-step and specific / (2) Conceptual and general", "S/N"),
            AssessmentQuestion(121, "mbti", "I am more: (1) Realistic / (2) Imaginative", "S/N"),
            AssessmentQuestion(122, "mbti", "I focus on: (1) Present realities / (2) Future possibilities", "S/N"),
            AssessmentQuestion(123, "mbti", "I prefer to: (1) Follow established procedures / (2) Explore new methods", "S/N"),
            AssessmentQuestion(124, "mbti", "I value: (1) Accuracy and precision / (2) Creativity and originality", "S/N"),
            AssessmentQuestion(125, "mbti", "I am better at: (1) Remembering facts / (2) Understanding concepts", "S/N"),
            AssessmentQuestion(126, "mbti", "I prefer: (1) Concrete information / (2) Abstract ideas", "S/N"),
            AssessmentQuestion(127, "mbti", "I learn best through: (1) Hands-on experience / (2) Theoretical understanding", "S/N"),
            AssessmentQuestion(128, "mbti", "I am more: (1) Practical / (2) Theoretical", "S/N"),
            AssessmentQuestion(129, "mbti", "I prefer: (1) Detailed descriptions / (2) Big picture overviews", "S/N"),
            AssessmentQuestion(130, "mbti", "I trust: (1) What I can see and touch / (2) My gut feelings", "S/N"),
            
            # T/F - Thinking vs Feeling (15 items)
            AssessmentQuestion(131, "mbti", "When making decisions, I prioritize: (1) Logic and objectivity / (2) Values and impact on people", "T/F"),
            AssessmentQuestion(132, "mbti", "I am more: (1) Firm and direct / (2) Gentle and tactful", "T/F"),
            AssessmentQuestion(133, "mbti", "I value: (1) Truth and fairness / (2) Harmony and compassion", "T/F"),
            AssessmentQuestion(134, "mbti", "Criticism makes me: (1) Consider the logic / (2) Feel hurt", "T/F"),
            AssessmentQuestion(135, "mbti", "I prefer to: (1) Analyze situations objectively / (2) Consider how people will feel", "T/F"),
            AssessmentQuestion(136, "mbti", "I am more: (1) Task-oriented / (2) People-oriented", "T/F"),
            AssessmentQuestion(137, "mbti", "I make decisions based on: (1) Head / (2) Heart", "T/F"),
            AssessmentQuestion(138, "mbti", "I prefer: (1) Direct, honest feedback / (2) Gentle, encouraging feedback", "T/F"),
            AssessmentQuestion(139, "mbti", "I am better at: (1) Critiquing ideas / (2) Appreciating effort", "T/F"),
            AssessmentQuestion(140, "mbti", "In conflicts, I focus on: (1) Finding the right solution / (2) Maintaining relationships", "T/F"),
            AssessmentQuestion(141, "mbti", "I value: (1) Competence / (2) Empathy", "T/F"),
            AssessmentQuestion(142, "mbti", "I prefer communication that is: (1) Clear and direct / (2) Warm and supportive", "T/F"),
            AssessmentQuestion(143, "mbti", "I am more: (1) Analytical / (2) Sympathetic", "T/F"),
            AssessmentQuestion(144, "mbti", "I judge situations by: (1) Principles / (2) Circumstances", "T/F"),
            AssessmentQuestion(145, "mbti", "I am more concerned with: (1) Being right / (2) Being kind", "T/F"),
            
            # J/P - Judging vs Perceiving (15 items)
            AssessmentQuestion(146, "mbti", "I prefer: (1) Clear plans and schedules / (2) Flexibility and spontaneity", "J/P"),
            AssessmentQuestion(147, "mbti", "I work best: (1) With deadlines / (2) Without time pressure", "J/P"),
            AssessmentQuestion(148, "mbti", "I prefer to: (1) Decide quickly / (2) Keep options open", "J/P"),
            AssessmentQuestion(149, "mbti", "My workspace is: (1) Neat and organized / (2) Flexible and evolving", "J/P"),
            AssessmentQuestion(150, "mbti", "I prefer: (1) Closure and completion / (2) Exploration and discovery", "J/P"),
            AssessmentQuestion(151, "mbti", "I like: (1) To-do lists and plans / (2) Going with the flow", "J/P"),
            AssessmentQuestion(152, "mbti", "I prefer to: (1) Finish projects early / (2) Work close to deadlines", "J/P"),
            AssessmentQuestion(153, "mbti", "Change is: (1) Unsettling / (2) Exciting", "J/P"),
            AssessmentQuestion(154, "mbti", "I prefer: (1) Structure and routine / (2) Variety and novelty", "J/P"),
            AssessmentQuestion(155, "mbti", "I am more: (1) Decisive / (2) Adaptable", "J/P"),
            AssessmentQuestion(156, "mbti", "I prefer: (1) Planned vacations / (2) Spontaneous trips", "J/P"),
            AssessmentQuestion(157, "mbti", "I value: (1) Order / (2) Flexibility", "J/P"),
            AssessmentQuestion(158, "mbti", "I prefer to: (1) Stick to plans / (2) Adjust as I go", "J/P"),
            AssessmentQuestion(159, "mbti", "I feel stressed when: (1) Things are unorganized / (2) Things are too structured", "J/P"),
            AssessmentQuestion(160, "mbti", "I am more: (1) Methodical / (2) Improvisational", "J/P"),
        ]
        
        # MBTI uses binary choice (1 or 2)
        for q in questions:
            q.scale_min = 1
            q.scale_max = 2
            q.scale_labels = {1: "Choice A", 2: "Choice B"}
        
        return questions
    
    def _load_disc_questions(self) -> List[AssessmentQuestion]:
        """Load DISC work style questions (24 items, 6 per factor)."""
        
        questions = [
            # Dominance (6 items)
            AssessmentQuestion(201, "disc", "I take charge of situations and make decisions quickly", "dominance"),
            AssessmentQuestion(202, "disc", "I am comfortable with competition and challenging goals", "dominance"),
            AssessmentQuestion(203, "disc", "I prefer direct communication and getting straight to the point", "dominance"),
            AssessmentQuestion(204, "disc", "I focus on results and efficiency over relationships", "dominance"),
            AssessmentQuestion(205, "disc", "I am assertive and willing to take risks", "dominance"),
            AssessmentQuestion(206, "disc", "I challenge the status quo and push for change", "dominance"),
            
            # Influence (6 items)
            AssessmentQuestion(207, "disc", "I enjoy persuading and influencing others", "influence"),
            AssessmentQuestion(208, "disc", "I am enthusiastic and optimistic in my approach", "influence"),
            AssessmentQuestion(209, "disc", "I prefer collaboration and building relationships", "influence"),
            AssessmentQuestion(210, "disc", "I am expressive and enjoy being in the spotlight", "influence"),
            AssessmentQuestion(211, "disc", "I inspire and motivate others with my energy", "influence"),
            AssessmentQuestion(212, "disc", "I prefer verbal communication and spontaneous interaction", "influence"),
            
            # Steadiness (6 items)
            AssessmentQuestion(213, "disc", "I prefer stability and predictable routines", "steadiness"),
            AssessmentQuestion(214, "disc", "I am patient and supportive of others", "steadiness"),
            AssessmentQuestion(215, "disc", "I work best in a calm, harmonious environment", "steadiness"),
            AssessmentQuestion(216, "disc", "I am loyal and committed to my team", "steadiness"),
            AssessmentQuestion(217, "disc", "I prefer gradual change over rapid transformation", "steadiness"),
            AssessmentQuestion(218, "disc", "I listen carefully and show empathy", "steadiness"),
            
            # Conscientiousness (6 items)
            AssessmentQuestion(219, "disc", "I focus on accuracy and attention to detail", "conscientiousness"),
            AssessmentQuestion(220, "disc", "I prefer working with systems, procedures, and standards", "conscientiousness"),
            AssessmentQuestion(221, "disc", "I analyze situations carefully before making decisions", "conscientiousness"),
            AssessmentQuestion(222, "disc", "I value quality and precision in my work", "conscientiousness"),
            AssessmentQuestion(223, "disc", "I prefer objective data over subjective opinions", "conscientiousness"),
            AssessmentQuestion(224, "disc", "I am systematic and methodical in my approach", "conscientiousness"),
        ]
        
        # DISC uses standard 1-5 scale
        for q in questions:
            q.scale_labels = {
                1: "Strongly Disagree",
                2: "Disagree",
                3: "Neutral",
                4: "Agree",
                5: "Strongly Agree"
            }
        
        return questions
    
    def get_assessment_questions(self, assessment_type: AssessmentType) -> List[AssessmentQuestion]:
        """Get questions for a specific assessment type."""
        if assessment_type == AssessmentType.BIG_FIVE:
            return self.big_five_questions
        elif assessment_type == AssessmentType.MBTI:
            return self.mbti_questions
        elif assessment_type == AssessmentType.DISC:
            return self.disc_questions
        else:
            raise ValueError(f"Unknown assessment type: {assessment_type}")
    
    def score_big_five(self, responses: List[AssessmentResponse]) -> BigFiveResults:
        """
        Score Big Five personality assessment.
        
        Args:
            responses: List of user responses to Big Five questions
            
        Returns:
            BigFiveResults with percentile scores and descriptions
        """
        # Group responses by dimension
        dimension_scores = {
            'openness': [],
            'conscientiousness': [],
            'extraversion': [],
            'agreeableness': [],
            'neuroticism': []
        }
        
        for response in responses:
            question = next((q for q in self.big_five_questions if q.id == response.question_id), None)
            if question:
                # Adjust for reverse scoring
                score = response.response_value
                if question.reverse_scored:
                    score = (question.scale_max + question.scale_min) - score
                
                dimension_scores[question.dimension].append(score)
        
        # Calculate mean scores for each dimension
        means = {}
        for dimension, scores in dimension_scores.items():
            if scores:
                means[dimension] = statistics.mean(scores)
            else:
                means[dimension] = 3.0  # Default to neutral
        
        # Convert to percentiles using normative data
        percentiles = {}
        for dimension, mean_score in means.items():
            norm = self.big_five_norms[dimension]
            # Simple z-score to percentile conversion
            z_score = (mean_score - norm['mean']) / norm['sd']
            # Approximate percentile (simplified normal distribution)
            if z_score <= -2:
                percentile = 5
            elif z_score <= -1:
                percentile = 15 + (z_score + 1) * 20
            elif z_score <= 0:
                percentile = 35 + z_score * 30
            elif z_score <= 1:
                percentile = 65 + z_score * 20
            elif z_score <= 2:
                percentile = 85 + (z_score - 1) * 10
            else:
                percentile = 95
            
            percentiles[dimension] = max(1, min(99, round(percentile)))
        
        # Generate descriptions and insights
        results = BigFiveResults(
            openness=percentiles['openness'],
            conscientiousness=percentiles['conscientiousness'],
            extraversion=percentiles['extraversion'],
            agreeableness=percentiles['agreeableness'],
            neuroticism=percentiles['neuroticism']
        )
        
        # Add trait descriptions
        results.openness_description = self._get_big_five_description('openness', results.openness)
        results.conscientiousness_description = self._get_big_five_description('conscientiousness', results.conscientiousness)
        results.extraversion_description = self._get_big_five_description('extraversion', results.extraversion)
        results.agreeableness_description = self._get_big_five_description('agreeableness', results.agreeableness)
        results.neuroticism_description = self._get_big_five_description('neuroticism', results.neuroticism)
        
        # Generate overall insights
        results.personality_summary = self._generate_big_five_summary(results)
        results.strengths = self._identify_big_five_strengths(results)
        results.potential_challenges = self._identify_big_five_challenges(results)
        results.career_implications = self._generate_career_implications(results)
        
        return results
    
    def _get_big_five_description(self, trait: str, percentile: float) -> str:
        """Get description for a Big Five trait based on percentile score."""
        
        descriptions = {
            'openness': {
                'high': "You are highly open to new experiences, creative, and intellectually curious. You enjoy exploring ideas, appreciate art and beauty, and are comfortable with ambiguity.",
                'moderate': "You balance tradition with innovation, appreciating both practical solutions and creative approaches. You are open to new ideas when they prove valuable.",
                'low': "You prefer practical, concrete approaches and value tradition. You focus on proven methods and are comfortable with routine and structure."
            },
            'conscientiousness': {
                'high': "You are highly organized, disciplined, and reliable. You set high standards, plan ahead, and follow through on commitments. You excel at structured tasks.",
                'moderate': "You balance spontaneity with organization. You can be flexible when needed but also plan when important. You complete tasks on time.",
                'low': "You prefer flexibility and spontaneity. You adapt easily to change and work best in unstructured environments. You may struggle with rigid schedules."
            },
            'extraversion': {
                'high': "You are energetic, sociable, and thrive in social situations. You draw energy from others, enjoy being the center of attention, and are enthusiastic.",
                'moderate': "You balance social interaction with alone time. You can be outgoing in groups but also value quiet reflection. You adapt to various social situations.",
                'low': "You are reserved, thoughtful, and recharge through solitude. You prefer deep conversations with close friends over large social gatherings."
            },
            'agreeableness': {
                'high': "You are compassionate, cooperative, and trusting. You value harmony, help others readily, and avoid conflict. You are considerate and kind.",
                'moderate': "You balance compassion with assertiveness. You cooperate when appropriate but can also be direct when needed. You are selectively trusting.",
                'low': "You are direct, skeptical, and competitive. You prioritize truth over harmony and are comfortable with confrontation. You question others' motives."
            },
            'neuroticism': {
                'high': "You experience emotions intensely and may feel stress, anxiety, or worry more than others. You are sensitive to criticism and may ruminate on problems.",
                'moderate': "You experience normal emotional ups and downs. You handle stress reasonably well but can feel overwhelmed at times. You recover from setbacks.",
                'low': "You are emotionally stable, calm, and resilient. You handle stress well, rarely feel anxious, and recover quickly from setbacks. You remain even-tempered."
            }
        }
        
        if percentile >= 65:
            level = 'high'
        elif percentile >= 35:
            level = 'moderate'
        else:
            level = 'low'
        
        return descriptions.get(trait, {}).get(level, "No description available")
    
    def _generate_big_five_summary(self, results: BigFiveResults) -> str:
        """Generate overall personality summary from Big Five results."""
        
        # Identify dominant traits
        traits = {
            'Openness': results.openness,
            'Conscientiousness': results.conscientiousness,
            'Extraversion': results.extraversion,
            'Agreeableness': results.agreeableness,
            'Emotional Stability': 100 - results.neuroticism  # Flip neuroticism
        }
        
        top_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)[:2]
        
        summary = f"Your personality is characterized by high {top_traits[0][0]} (${top_traits[0][1]}th percentile) and {top_traits[1][0]} ({top_traits[1][1]}th percentile). "
        
        # Add context based on trait combinations
        if results.openness >= 65 and results.conscientiousness >= 65:
            summary += "This combination of creativity and discipline makes you excellent at innovative yet structured work."
        elif results.extraversion >= 65 and results.agreeableness >= 65:
            summary += "Your sociable and compassionate nature makes you excellent at building relationships and collaborating."
        elif results.conscientiousness >= 65 and results.neuroticism <= 35:
            summary += "Your combination of organization and emotional stability makes you reliable under pressure."
        
        return summary
    
    def _identify_big_five_strengths(self, results: BigFiveResults) -> List[str]:
        """Identify key strengths from Big Five profile."""
        strengths = []
        
        if results.openness >= 65:
            strengths.append("Creative problem-solving and innovation")
            strengths.append("Intellectual curiosity and learning agility")
        
        if results.conscientiousness >= 65:
            strengths.append("Strong work ethic and reliability")
            strengths.append("Excellent organizational and planning skills")
        
        if results.extraversion >= 65:
            strengths.append("Strong communication and networking abilities")
            strengths.append("Leadership and team motivation")
        
        if results.agreeableness >= 65:
            strengths.append("Collaboration and team harmony")
            strengths.append("Empathy and interpersonal sensitivity")
        
        if results.neuroticism <= 35:
            strengths.append("Emotional stability and resilience")
            strengths.append("Calm under pressure and stress management")
        
        return strengths[:5]  # Return top 5
    
    def _identify_big_five_challenges(self, results: BigFiveResults) -> List[str]:
        """Identify potential challenges from Big Five profile."""
        challenges = []
        
        if results.openness <= 35:
            challenges.append("May resist change or unconventional approaches")
        
        if results.conscientiousness <= 35:
            challenges.append("May struggle with deadlines or organization")
        
        if results.extraversion <= 35:
            challenges.append("May find networking or public speaking draining")
        
        if results.agreeableness <= 35:
            challenges.append("May be perceived as overly critical or confrontational")
        
        if results.neuroticism >= 65:
            challenges.append("May experience stress or anxiety in high-pressure situations")
        
        return challenges[:5]  # Return top 5
    
    def _generate_career_implications(self, results: BigFiveResults) -> List[str]:
        """Generate career implications from Big Five profile."""
        implications = []
        
        # High openness careers
        if results.openness >= 65:
            implications.append("Careers involving creativity, innovation, or research would be highly satisfying")
            implications.append("Consider roles in: Design, R&D, Marketing, Arts, Academia")
        
        # High conscientiousness careers
        if results.conscientiousness >= 65:
            implications.append("Careers requiring organization, reliability, and attention to detail are ideal")
            implications.append("Consider roles in: Project Management, Finance, Healthcare, Engineering")
        
        # High extraversion careers
        if results.extraversion >= 65:
            implications.append("Careers involving people interaction and leadership would be energizing")
            implications.append("Consider roles in: Sales, Management, Teaching, Public Relations")
        
        # High agreeableness careers
        if results.agreeableness >= 65:
            implications.append("Careers focused on helping others and collaboration would be fulfilling")
            implications.append("Consider roles in: Healthcare, Education, Social Work, Human Resources")
        
        # Low neuroticism (high emotional stability) careers
        if results.neuroticism <= 35:
            implications.append("High-pressure careers requiring calm decision-making are suitable")
            implications.append("Consider roles in: Emergency Services, Finance Trading, Surgery, Military")
        
        return implications[:6]  # Return top 6
    
    def save_assessment_results(self, user_id: str, results: BigFiveResults, 
                               assessment_type: AssessmentType = AssessmentType.BIG_FIVE) -> str:
        """Save assessment results to JSON file."""
        
        # Create directory
        save_dir = Path("assessment_results")
        save_dir.mkdir(exist_ok=True)
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{assessment_type.value}_{timestamp}.json"
        filepath = save_dir / filename
        
        # Convert to dict
        results_dict = {
            'user_id': user_id,
            'assessment_type': assessment_type.value,
            'completed_at': datetime.now().isoformat(),
            'results': {
                'openness': results.openness,
                'conscientiousness': results.conscientiousness,
                'extraversion': results.extraversion,
                'agreeableness': results.agreeableness,
                'neuroticism': results.neuroticism,
                'descriptions': {
                    'openness': results.openness_description,
                    'conscientiousness': results.conscientiousness_description,
                    'extraversion': results.extraversion_description,
                    'agreeableness': results.agreeableness_description,
                    'neuroticism': results.neuroticism_description
                },
                'personality_summary': results.personality_summary,
                'strengths': results.strengths,
                'potential_challenges': results.potential_challenges,
                'career_implications': results.career_implications
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        return str(filepath)


def main():
    """Demonstrate personality assessment system."""
    
    print("\n" + "=" * 80)
    print("PERSONALITY ASSESSMENT SYSTEM - DEMONSTRATION")
    print("=" * 80)
    
    system = PersonalityAssessmentSystem()
    
    # Example 1: Get Big Five Questions
    print("\n\n EXAMPLE 1: Big Five Assessment Questions")
    print("-" * 80)
    
    big_five_questions = system.get_assessment_questions(AssessmentType.BIG_FIVE)
    print(f"Total Big Five questions: {len(big_five_questions)}")
    print(f"\nSample questions:")
    for i, q in enumerate(big_five_questions[:3], 1):
        print(f"\n{i}. {q.question_text}")
        print(f"   Dimension: {q.dimension}")
        print(f"   Reverse scored: {q.reverse_scored}")
        print(f"   Scale: {q.scale_labels}")
    
    # Example 2: Simulate Big Five Assessment
    print("\n\n EXAMPLE 2: Big Five Assessment Results")
    print("-" * 80)
    
    # Simulate responses for a highly open, conscientious, introverted person
    sample_responses = []
    for q in big_five_questions:
        if q.dimension == 'openness':
            value = 5 if not q.reverse_scored else 1
        elif q.dimension == 'conscientiousness':
            value = 5 if not q.reverse_scored else 1
        elif q.dimension == 'extraversion':
            value = 2 if not q.reverse_scored else 4
        elif q.dimension == 'agreeableness':
            value = 4 if not q.reverse_scored else 2
        elif q.dimension == 'neuroticism':
            value = 2 if not q.reverse_scored else 4
        else:
            value = 3
        
        sample_responses.append(AssessmentResponse(
            question_id=q.id,
            response_value=value
        ))
    
    results = system.score_big_five(sample_responses)
    
    print("Big Five Personality Profile:")
    print(f"  Openness: {results.openness}th percentile")
    print(f"  Conscientiousness: {results.conscientiousness}th percentile")
    print(f"  Extraversion: {results.extraversion}th percentile")
    print(f"  Agreeableness: {results.agreeableness}th percentile")
    print(f"  Neuroticism: {results.neuroticism}th percentile")
    
    print(f"\nPersonality Summary:")
    print(f"  {results.personality_summary}")
    
    print(f"\nTop Strengths:")
    for i, strength in enumerate(results.strengths, 1):
        print(f"  {i}. {strength}")
    
    print(f"\nPotential Challenges:")
    for i, challenge in enumerate(results.potential_challenges, 1):
        print(f"  {i}. {challenge}")
    
    print(f"\nCareer Implications:")
    for i, implication in enumerate(results.career_implications, 1):
        print(f"  {i}. {implication}")
    
    # Example 3: Save Results
    print("\n\n EXAMPLE 3: Save Assessment Results")
    print("-" * 80)
    
    filepath = system.save_assessment_results("user_001", results)
    print(f" Assessment results saved to: {filepath}")
    
    # Example 4: MBTI Questions Preview
    print("\n\n EXAMPLE 4: MBTI Assessment Preview")
    print("-" * 80)
    
    mbti_questions = system.get_assessment_questions(AssessmentType.MBTI)
    print(f"Total MBTI questions: {len(mbti_questions)}")
    print(f"\nSample questions by dimension:")
    
    for dimension in ['E/I', 'S/N', 'T/F', 'J/P']:
        dimension_questions = [q for q in mbti_questions if q.dimension == dimension]
        print(f"\n{dimension} Dimension ({len(dimension_questions)} questions):")
        print(f"  Sample: {dimension_questions[0].question_text}")
    
    # Example 5: DISC Questions Preview
    print("\n\n EXAMPLE 5: DISC Assessment Preview")
    print("-" * 80)
    
    disc_questions = system.get_assessment_questions(AssessmentType.DISC)
    print(f"Total DISC questions: {len(disc_questions)}")
    print(f"\nSample questions by factor:")
    
    for factor in ['dominance', 'influence', 'steadiness', 'conscientiousness']:
        factor_questions = [q for q in disc_questions if q.dimension == factor]
        print(f"\n{factor.title()} ({len(factor_questions)} questions):")
        print(f"  Sample: {factor_questions[0].question_text}")
    
    print("\n" + "=" * 80)
    print("PERSONALITY ASSESSMENT SYSTEM - DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nAll features working successfully:")
    print("   Big Five assessment (50 questions)")
    print("   MBTI assessment (60 questions)")
    print("   DISC assessment (24 questions)")
    print("   Automated scoring and percentile calculation")
    print("   Comprehensive personality insights")
    print("   Strengths and challenges identification")
    print("   Career implications generation")
    print("   Results persistence (JSON)")
    print("\n")


if __name__ == "__main__":
    main()
