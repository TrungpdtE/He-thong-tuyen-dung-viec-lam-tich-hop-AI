from sqlalchemy.orm import Session

from app.db.models import Job, Resume


SKILL_GROUPS = [
    ["Python", "FastAPI", "PostgreSQL", "Docker", "REST API"],
    ["Python", "Machine Learning", "Embeddings", "Feature Engineering", "SQL"],
    ["Python", "NLP", "Search", "Ranking", "PostgreSQL"],
    ["Java", "Spring Boot", "MySQL", "Docker", "REST API"],
    ["React", "TypeScript", "CSS", "API Integration"],
    ["Python", "ETL", "Data Modeling", "PostgreSQL", "Analytics"],
    ["Docker", "Linux", "CI/CD", "Cloud", "Monitoring"],
    ["Python", "Redis", "PostgreSQL", "System Design", "API"],
]


COMPANIES = [
    "TechStart Labs", "NLPWorks", "CloudBridge", "DataNest", "FinAI Studio",
    "CareerMatch AI", "ByteCraft", "JobFlow", "TalentGraph", "VectorStack",
    "OpenHire", "CodeHarbor", "SkillBridge", "ResumeRanker", "InsightLoop",
    "QueryBox", "DevPath", "ApplyWise", "BackendForge", "NextHire",
    "SearchPilot", "RankSense", "InternLink", "PostgresPro", "DockerWorks",
    "FastTalent", "ModelOps", "DataRiver", "SemanticHub", "CareerOS",
    "HireSignal", "APIWorks", "StackMakers", "JobLens", "SkillMap",
    "TalentOps", "CloudMentor", "QueryMind", "CodeSpring", "RecruitIQ",
    "FeatureLab", "VectorHire", "BackendBase", "NLPBridge", "SearchNest",
    "RankFlow", "DataCraft", "JobScout", "TalentSpark", "CloudCareer",
    "InternPilot", "APINest", "ResumeFlow", "SkillPilot", "HireCraft",
    "DataMatch", "JobVector", "CodeSignal Labs", "BackendLoop", "AIFoundry",
]


def seed_database(db: Session) -> None:
    if db.query(Resume).count() == 0:
        db.add_all(
            [
                Resume(
                    raw_text="Python FastAPI PostgreSQL Docker REST API backend intern with NLP and recommendation projects.",
                    parsed_skills=["Python", "FastAPI", "PostgreSQL", "Docker", "REST API", "NLP"],
                ),
                Resume(
                    raw_text="Machine learning student with embeddings, feature engineering, ranking model, SQL and analytics experience.",
                    parsed_skills=["Python", "Machine Learning", "Embeddings", "Feature Engineering", "SQL"],
                ),
                Resume(
                    raw_text="Java Spring Boot backend developer with MySQL, Docker, REST API and basic system design.",
                    parsed_skills=["Java", "Spring Boot", "MySQL", "Docker", "REST API", "System Design"],
                ),
            ]
        )

    if db.query(Job).count() == 0:
        jobs: list[Job] = []
        for index, company in enumerate(COMPANIES, start=1):
            skills = SKILL_GROUPS[(index - 1) % len(SKILL_GROUPS)]
            title = _title_for_skills(skills)
            description = (
                f"{company} is hiring a {title}. The role works with {', '.join(skills)}. "
                "You will build production APIs, improve data-driven ranking, and collaborate with product teams."
            )
            jobs.append(
                Job(
                    title=title,
                    company=company,
                    description=description,
                    required_skills=skills,
                )
            )
        db.add_all(jobs)

    db.commit()
    print("Database seeded successfully", flush=True)


def _title_for_skills(skills: list[str]) -> str:
    if "FastAPI" in skills:
        return "Backend Engineer Intern"
    if "Machine Learning" in skills:
        return "AI Ranking Engineer Intern"
    if "NLP" in skills:
        return "Search and NLP Engineer Intern"
    if "Spring Boot" in skills:
        return "Java Backend Intern"
    if "React" in skills:
        return "Frontend Integration Intern"
    if "ETL" in skills:
        return "Data Engineer Intern"
    if "CI/CD" in skills:
        return "Platform Engineer Intern"
    return "Backend Platform Intern"
