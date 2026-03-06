"""
Data Schema for AI Teams Candidate Assessment System

Defines the structure for candidate interview data and outcomes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class InterviewOutcome(Enum):
    """Final hiring outcomes"""
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    NO_OFFER = "no_offer"
    WITHDREW = "withdrew"


@dataclass
class MLFundamentalsInterview:
    """Round 1: Machine Learning Fundamentals Interview"""
    # Core ML Knowledge (1-5 scale)
    ml_theory_score: float  # Understanding of ML algorithms, concepts
    statistics_score: float  # Statistical foundations
    deep_learning_score: float  # Neural networks, architectures
    model_evaluation_score: float  # Metrics, validation, bias-variance
    practical_application_score: float  # Real-world ML problem solving

    # Soft skills
    communication_score: float  # Ability to explain concepts
    problem_approach_score: float  # Structured thinking

    # Overall
    overall_score: float  # Interviewer's overall assessment (1-5)
    interviewer_confidence: float  # How confident is interviewer (1-5)

    # Metadata
    interviewer_id: str
    interview_date: datetime
    duration_minutes: int
    notes: Optional[str] = None


@dataclass
class CodingInterview:
    """Round 2: Long-form Python Coding Interview (Real-world problems)"""
    # Core rubric criteria (1-5 scale each)
    workable_solution_score: float  # Solution works with minimal bugs
    time_efficiency_score: float  # Completed within time limit
    code_cleanliness_score: float  # Readability, structure, style
    algorithmic_efficiency_score: float  # Optimal complexity, performance

    # Additional technical signals
    debugging_ability_score: float  # How well they debug/fix issues
    edge_case_handling_score: float  # Consideration of edge cases
    testing_approach_score: float  # Testing methodology

    # Problem-solving process
    problem_understanding_score: float  # Clarifying questions, understanding
    solution_design_score: float  # Initial approach/planning

    # Soft skills
    communication_score: float  # Explaining thought process
    collaboration_score: float  # Working with interviewer

    # Overall
    overall_score: float  # Interviewer's overall assessment (1-5)
    interviewer_confidence: float  # How confident is interviewer (1-5)

    # Metadata
    interviewer_id: str
    interview_date: datetime
    duration_minutes: int
    problems_attempted: int
    problems_solved: int
    notes: Optional[str] = None


@dataclass
class CandidateProfile:
    """Basic candidate information"""
    candidate_id: str
    years_of_experience: float
    years_ml_experience: float
    has_phd: bool
    has_masters: bool
    previous_ai_role: bool
    top_tier_company: bool  # FAANG/similar
    research_publications: int

    # Application data
    application_date: datetime
    recruiter_screen_score: Optional[float] = None


@dataclass
class OnsiteInterview:
    """Onsite interview results (for training data)"""
    system_design_score: float
    ml_system_design_score: float
    behavioral_score: float
    coding_onsite_score: float

    overall_onsite_score: float
    bar_raiser_score: Optional[float] = None

    interview_date: datetime


@dataclass
class CandidateRecord:
    """Complete candidate record for modeling"""
    # Identifiers
    candidate_id: str

    # Profile
    profile: CandidateProfile

    # Pre-onsite interviews
    ml_fundamentals: MLFundamentalsInterview
    coding_interview: CodingInterview

    # Onsite (only for historical training data)
    onsite: Optional[OnsiteInterview] = None

    # Outcome (only for historical training data)
    final_outcome: Optional[InterviewOutcome] = None
    offer_extended: Optional[bool] = None  # Target variable

    # Metadata
    cohort: str = "unknown"  # For tracking different hiring periods


@dataclass
class PredictionResult:
    """Model prediction output"""
    candidate_id: str
    offer_probability: float  # 0-1 probability of receiving offer
    percentile_rank: float  # 0-100 percentile among all candidates
    confidence_interval_lower: float  # Lower bound of 95% CI
    confidence_interval_upper: float  # Upper bound of 95% CI

    # Feature contributions
    top_positive_features: List[tuple]  # [(feature_name, contribution), ...]
    top_negative_features: List[tuple]

    # Recommendation
    recommendation: str  # "Strong Proceed", "Proceed", "Borderline", "Do Not Proceed"
    prediction_date: datetime = field(default_factory=datetime.now)
