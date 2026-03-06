"""
Generate sample training data for the candidate assessment system.

This simulates historical hiring data for model training.
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List
from data_schema import (
    CandidateRecord, CandidateProfile, MLFundamentalsInterview,
    CodingInterview, OnsiteInterview, InterviewOutcome
)


def generate_candidate_profile(candidate_id: str) -> CandidateProfile:
    """Generate a realistic candidate profile"""
    return CandidateProfile(
        candidate_id=candidate_id,
        years_of_experience=np.random.gamma(5, 1.5),  # Mean ~7.5 years
        years_ml_experience=np.random.gamma(3, 1.2),  # Mean ~3.6 years
        has_phd=random.random() < 0.25,
        has_masters=random.random() < 0.45,
        previous_ai_role=random.random() < 0.6,
        top_tier_company=random.random() < 0.3,
        research_publications=np.random.poisson(2) if random.random() < 0.4 else 0,
        application_date=datetime.now() - timedelta(days=random.randint(30, 365)),
        recruiter_screen_score=np.clip(np.random.normal(3.5, 0.8), 1, 5)
    )


def generate_ml_interview(quality_level: float, interviewer_num: int) -> MLFundamentalsInterview:
    """
    Generate ML fundamentals interview scores
    quality_level: 0-1, represents candidate's underlying ability
    """
    base_score = 1 + quality_level * 4  # Scale to 1-5
    noise = np.random.normal(0, 0.4)

    return MLFundamentalsInterview(
        ml_theory_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        statistics_score=np.clip(base_score + np.random.normal(0, 0.4), 1, 5),
        deep_learning_score=np.clip(base_score + np.random.normal(0, 0.6), 1, 5),
        model_evaluation_score=np.clip(base_score + np.random.normal(0, 0.4), 1, 5),
        practical_application_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        communication_score=np.clip(base_score + np.random.normal(0, 0.6), 1, 5),
        problem_approach_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        overall_score=np.clip(base_score + noise, 1, 5),
        interviewer_confidence=np.clip(base_score + np.random.normal(0, 0.7), 1, 5),
        interviewer_id=f"interviewer_ml_{interviewer_num}",
        interview_date=datetime.now() - timedelta(days=random.randint(20, 350)),
        duration_minutes=random.choice([45, 60]),
        notes="Simulated interview data"
    )


def generate_coding_interview(quality_level: float, interviewer_num: int) -> CodingInterview:
    """
    Generate coding interview scores based on the rubric
    quality_level: 0-1, represents candidate's underlying ability
    """
    base_score = 1 + quality_level * 4

    # Core rubric - slight variations
    workable = np.clip(base_score + np.random.normal(0, 0.5), 1, 5)
    time_eff = np.clip(base_score + np.random.normal(0, 0.6), 1, 5)
    clean = np.clip(base_score + np.random.normal(0, 0.4), 1, 5)
    algo_eff = np.clip(base_score + np.random.normal(0, 0.5), 1, 5)

    return CodingInterview(
        workable_solution_score=workable,
        time_efficiency_score=time_eff,
        code_cleanliness_score=clean,
        algorithmic_efficiency_score=algo_eff,
        debugging_ability_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        edge_case_handling_score=np.clip(base_score + np.random.normal(0, 0.6), 1, 5),
        testing_approach_score=np.clip(base_score + np.random.normal(0, 0.6), 1, 5),
        problem_understanding_score=np.clip(base_score + np.random.normal(0, 0.4), 1, 5),
        solution_design_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        communication_score=np.clip(base_score + np.random.normal(0, 0.6), 1, 5),
        collaboration_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        overall_score=np.clip(np.mean([workable, time_eff, clean, algo_eff]) + np.random.normal(0, 0.3), 1, 5),
        interviewer_confidence=np.clip(base_score + np.random.normal(0, 0.7), 1, 5),
        interviewer_id=f"interviewer_coding_{interviewer_num}",
        interview_date=datetime.now() - timedelta(days=random.randint(15, 345)),
        duration_minutes=random.choice([90, 120]),
        problems_attempted=random.randint(2, 4),
        problems_solved=max(1, int(quality_level * 3 + random.randint(0, 1))),
        notes="Simulated coding interview"
    )


def generate_onsite_interview(quality_level: float) -> OnsiteInterview:
    """Generate onsite interview results"""
    base_score = 1 + quality_level * 4
    noise = np.random.normal(0, 0.5)

    return OnsiteInterview(
        system_design_score=np.clip(base_score + np.random.normal(0, 0.6), 1, 5),
        ml_system_design_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        behavioral_score=np.clip(base_score + np.random.normal(0, 0.7), 1, 5),
        coding_onsite_score=np.clip(base_score + np.random.normal(0, 0.5), 1, 5),
        overall_onsite_score=np.clip(base_score + noise, 1, 5),
        bar_raiser_score=np.clip(base_score + np.random.normal(0, 0.8), 1, 5) if random.random() < 0.8 else None,
        interview_date=datetime.now() - timedelta(days=random.randint(5, 340))
    )


def determine_outcome(quality_level: float, onsite_score: float) -> tuple:
    """
    Determine if candidate gets offer based on quality and onsite performance
    Returns: (offer_extended: bool, final_outcome: InterviewOutcome)
    """
    # Probability of offer based on quality and onsite
    offer_prob = 0.1 + 0.8 * quality_level + 0.1 * (onsite_score / 5)
    offer_prob = np.clip(offer_prob, 0, 0.95)  # Cap at 95%

    offer_extended = random.random() < offer_prob

    if not offer_extended:
        return False, InterviewOutcome.NO_OFFER

    # If offer extended, did they accept?
    accept_prob = 0.7 + 0.2 * quality_level  # Better candidates more likely to accept
    if random.random() < accept_prob:
        return True, InterviewOutcome.OFFER_ACCEPTED
    else:
        return True, InterviewOutcome.OFFER_DECLINED


def generate_candidate_record(candidate_num: int) -> CandidateRecord:
    """Generate a complete candidate record"""
    candidate_id = f"CAND_{candidate_num:05d}"

    # Generate underlying quality (bell curve, slightly right-skewed)
    quality_level = np.clip(np.random.beta(5, 3), 0, 1)

    profile = generate_candidate_profile(candidate_id)
    ml_interview = generate_ml_interview(quality_level, random.randint(1, 20))
    coding_interview = generate_coding_interview(quality_level, random.randint(1, 15))
    onsite = generate_onsite_interview(quality_level)

    offer_extended, final_outcome = determine_outcome(quality_level, onsite.overall_onsite_score)

    return CandidateRecord(
        candidate_id=candidate_id,
        profile=profile,
        ml_fundamentals=ml_interview,
        coding_interview=coding_interview,
        onsite=onsite,
        final_outcome=final_outcome,
        offer_extended=offer_extended,
        cohort=random.choice(["2024_Q1", "2024_Q2", "2024_Q3", "2024_Q4", "2025_Q1"])
    )


def generate_training_dataset(n_candidates: int = 500) -> List[CandidateRecord]:
    """Generate training dataset with n historical candidates"""
    print(f"Generating {n_candidates} candidate records...")
    random.seed(42)
    np.random.seed(42)

    records = []
    for i in range(n_candidates):
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{n_candidates} records")
        records.append(generate_candidate_record(i))

    print("Dataset generation complete!")
    return records


def records_to_dataframe(records: List[CandidateRecord]) -> pd.DataFrame:
    """Convert CandidateRecord objects to pandas DataFrame for modeling"""
    data = []

    for record in records:
        row = {
            # Identifiers
            'candidate_id': record.candidate_id,

            # Profile features
            'years_experience': record.profile.years_of_experience,
            'years_ml_experience': record.profile.years_ml_experience,
            'has_phd': int(record.profile.has_phd),
            'has_masters': int(record.profile.has_masters),
            'previous_ai_role': int(record.profile.previous_ai_role),
            'top_tier_company': int(record.profile.top_tier_company),
            'research_publications': record.profile.research_publications,
            'recruiter_screen_score': record.profile.recruiter_screen_score,

            # ML Fundamentals scores
            'ml_theory_score': record.ml_fundamentals.ml_theory_score,
            'statistics_score': record.ml_fundamentals.statistics_score,
            'deep_learning_score': record.ml_fundamentals.deep_learning_score,
            'model_evaluation_score': record.ml_fundamentals.model_evaluation_score,
            'practical_application_score': record.ml_fundamentals.practical_application_score,
            'ml_communication_score': record.ml_fundamentals.communication_score,
            'ml_problem_approach_score': record.ml_fundamentals.problem_approach_score,
            'ml_overall_score': record.ml_fundamentals.overall_score,
            'ml_interviewer_confidence': record.ml_fundamentals.interviewer_confidence,

            # Coding interview scores
            'workable_solution_score': record.coding_interview.workable_solution_score,
            'time_efficiency_score': record.coding_interview.time_efficiency_score,
            'code_cleanliness_score': record.coding_interview.code_cleanliness_score,
            'algorithmic_efficiency_score': record.coding_interview.algorithmic_efficiency_score,
            'debugging_ability_score': record.coding_interview.debugging_ability_score,
            'edge_case_handling_score': record.coding_interview.edge_case_handling_score,
            'testing_approach_score': record.coding_interview.testing_approach_score,
            'coding_problem_understanding_score': record.coding_interview.problem_understanding_score,
            'coding_solution_design_score': record.coding_interview.solution_design_score,
            'coding_communication_score': record.coding_interview.communication_score,
            'coding_collaboration_score': record.coding_interview.collaboration_score,
            'coding_overall_score': record.coding_interview.overall_score,
            'coding_interviewer_confidence': record.coding_interview.interviewer_confidence,
            'problems_attempted': record.coding_interview.problems_attempted,
            'problems_solved': record.coding_interview.problems_solved,

            # Target variable
            'offer_extended': int(record.offer_extended) if record.offer_extended is not None else None,

            # Metadata
            'cohort': record.cohort
        }

        data.append(row)

    return pd.DataFrame(data)


if __name__ == "__main__":
    # Generate sample dataset
    records = generate_training_dataset(n_candidates=500)

    # Convert to DataFrame
    df = records_to_dataframe(records)

    # Save to CSV
    df.to_csv('ai_teams_training_data.csv', index=False)
    print(f"\nSaved {len(df)} records to ai_teams_training_data.csv")
    print(f"Offer rate: {df['offer_extended'].mean():.1%}")
    print(f"\nFirst few rows:")
    print(df.head())
