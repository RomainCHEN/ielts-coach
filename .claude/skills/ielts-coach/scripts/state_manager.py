"""
IELTS Coach - State File Manager
Helper script for reading and updating JSON state files.
"""
import json
import os
from datetime import datetime, date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent  # Project root


def read_json(filename):
    """Read a JSON file, return empty dict if not exists."""
    path = BASE_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def write_json(filename, data):
    """Write data to a JSON file."""
    path = BASE_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def init_user_profile(exam_date, target_speaking, target_writing,
                      occupation, hobbies, city, hometown,
                      travel_experience, future_plans, difficult_topics):
    """Initialize the user profile."""
    profile = {
        "created_at": datetime.now().isoformat(),
        "exam_date": exam_date,
        "target_speaking": target_speaking,
        "target_writing": target_writing,
        "personal_info": {
            "occupation": occupation,
            "hobbies": hobbies,
            "city": city,
            "hometown": hometown,
            "travel_experience": travel_experience,
            "future_plans": future_plans,
            "difficult_topics": difficult_topics
        }
    }
    exam_dt = datetime.strptime(exam_date, "%Y-%m-%d")
    days_remaining = (exam_dt.date() - date.today()).days
    profile["days_remaining"] = days_remaining
    write_json("user_profile.json", profile)
    return profile


def get_user_profile():
    """Get the current user profile."""
    return read_json("user_profile.json")


def create_study_plan(speaking_sessions, writing_sessions, session_minutes):
    """Create initial study plan structure."""
    profile = get_user_profile()
    if not profile:
        raise ValueError("User profile not found. Run onboarding first.")

    plan = {
        "created_date": date.today().isoformat(),
        "exam_date": profile["exam_date"],
        "days_remaining": profile["days_remaining"],
        "target_speaking": profile["target_speaking"],
        "target_writing": profile["target_writing"],
        "total_speaking_sessions": speaking_sessions,
        "total_writing_sessions": writing_sessions,
        "session_minutes": session_minutes,
        "schedule": [],
        "topics_used": [],
        "completed_sessions": 0
    }
    write_json("study_plan.json", plan)
    return plan


def get_study_plan():
    """Get the current study plan."""
    return read_json("study_plan.json")


def update_study_plan(updates):
    """Update study plan with new data."""
    plan = get_study_plan()
    if plan:
        plan.update(updates)
        write_json("study_plan.json", plan)
    return plan


def get_progress():
    """Get progress data."""
    progress = read_json("progress.json")
    if not progress:
        progress = {
            "topics_completed": [],
            "sessions_completed": 0,
            "last_session_date": None,
            "answers_generated": 0,
            "daily_log": []
        }
        write_json("progress.json", progress)
    return progress


def mark_topic_completed(topic_key, answers_generated):
    """Mark a topic as completed and update progress."""
    progress = get_progress()
    if topic_key not in progress["topics_completed"]:
        progress["topics_completed"].append(topic_key)
    progress["answers_generated"] += answers_generated
    progress["last_session_date"] = date.today().isoformat()

    progress["daily_log"].append({
        "date": date.today().isoformat(),
        "topic": topic_key,
        "answers": answers_generated
    })

    write_json("progress.json", progress)

    # Also update study plan
    plan = get_study_plan()
    if plan:
        if topic_key not in plan["topics_used"]:
            plan["topics_used"].append(topic_key)
        write_json("study_plan.json", plan)

    return progress


def get_completion_stats():
    """Get completion statistics."""
    progress = get_progress()
    plan = get_study_plan()

    stats = {
        "topics_completed": len(progress.get("topics_completed", [])),
        "sessions_completed": progress.get("sessions_completed", 0),
        "answers_generated": progress.get("answers_generated", 0),
        "days_remaining": plan.get("days_remaining", "Unknown") if plan else "Unknown",
        "total_sessions_planned": (plan.get("total_speaking_sessions", 0) +
                                    plan.get("total_writing_sessions", 0)) if plan else 0
    }
    return stats


if __name__ == "__main__":
    print("IELTS Coach State Manager")
    print("=" * 40)

    profile = get_user_profile()
    if profile:
        print(f"User profile: Found")
        print(f"  Exam date: {profile.get('exam_date')}")
        print(f"  Target: Speaking {profile.get('target_speaking')}, Writing {profile.get('target_writing')}")
        print(f"  Days remaining: {profile.get('days_remaining')}")
    else:
        print("User profile: Not found (onboarding needed)")

    stats = get_completion_stats()
    print(f"\nProgress:")
    print(f"  Topics completed: {stats['topics_completed']}")
    print(f"  Answers generated: {stats['answers_generated']}")
    print(f"  Days remaining: {stats['days_remaining']}")
