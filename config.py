import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")

MAX_POLICY_TEXT_CHARS = 12000
URL_FETCH_TIMEOUT_SECONDS = 15
MIN_EXTRACTED_TEXT_CHARS = 200

DEFAULT_EMP_DESCRIPTION = """1. What the Program Is
The Explicit Mathematics Program (EMP) is a complete, turnkey primary mathematics program designed to provide teachers and schools with a structured, rigorous, and evidence-informed curriculum. It includes fully scripted Teacher Lesson Books, physical Student Workbooks, Assessment Books (both formative and summative), digital Daily Review & Quick Teach (DRQT) slides via the empschools.com portal, and automated diagnostic spreadsheets.
The program was architected and written by a small, specialized team of Australian educators and pure mathematics researchers, including Dr Wendy Taylor, Martin Ravindran, and co-founder/CEO Ollie Lovell, to ensure complete coherence and seamless sequencing across primary year levels.

2. Who It Is For
Target Year Levels: Currently available for Levels A through D (Foundation/Prep through Year 3/4), with one new level releasing each calendar year until Level G (Year 6) is available in 2029.
Tier 1 Whole-Class Curriculum: EMP is primarily designed and recommended as a universal Tier 1 primary mathematics curriculum for whole-class instruction.
Tier 2/3 Intervention: It is also used for targeted small-group or 1-on-1 intervention by increasing instruction dosage, utilizing prerequisite placement tests, and delivering specialized Scaffolded Fluency Practice.
Composite & Multi-Age Classes: Designed to support composite classrooms through flexible implementation models, including grade-level streaming, offset explicit lessons, or single level selection.

3. Methodology & Key Features
Grounded in the Science of Learning: Built explicitly on Cognitive Load Theory (Sweller), spaced retrieval practice, systematic skill sequencing, and the gradual release of responsibility model ("I do, we do, you do").
The Protected 60-Minute Daily Block: Lessons run 5 days per week across 3 integrated components:
- Daily Review & Quick Teach (DRQT) (10-25 mins): Fast-paced, cumulative slide reviews that systematically revisit previously learned concepts to consolidate long-term memory.
- Fact Fluency Practice (5 mins): Daily incremental rehearsal of basic addition, subtraction, multiplication, and division facts.
- Core Explicit Lesson (30-50 mins): Direct, step-by-step teacher modelling using a classroom visualiser camera, followed by guided practice and independent workbook tasks.
Visualiser-Based Delivery & Physical Workbooks: Teachers project and model student workbook pages under a document camera in real time, eliminating low-value copying from boards and ensuring low cognitive load.
Data-Driven Assessment Framework: Formative assessments occur every 5 blocks (~4 weeks) alongside summative reporting checks. Results are analyzed in custom Excel spreadsheets using an 85% mastery benchmark and a target fluency rate of 40 Digits Correct Per Minute (DCPM).
Ambitious National Curriculum Mapping: Mapped across all Australian state and territory curricula (v9.0, VIC 2.0, NSW, WA). The program intentionally pitches to ambitious outcomes to smooth out steep learning jumps between grade levels.

4. Outcomes & Claimed Evidence
Used across over 150 Australian schools, EMP reports significant measurable student progress on ACER Progressive Achievement Tests (PAT) in Mathematics:
- Cohort Growth: In first-year implementation data from 2025, Year 2 cohorts using EMP achieved 20 to 25 months of equivalent academic progress within a single 12-month period (compared to 12-17 months achieved by the same cohorts in prior years without EMP).
- Impact on At-Risk Students: The bottom 25% of students demonstrated accelerated growth, making the equivalent of 3 to 3.5+ years of progress on the national PAT scale compared to peer benchmarks."""

DISCLAIMER_TEXT = (
    "This fact sheet was prepared by the Explicit Mathematics Program (EMP) to summarise how "
    "EMP's curriculum relates to the policy referenced above. It is provided for internal "
    "information and promotional purposes and does not constitute advice from, or endorsement "
    "by, the issuing policy authority. School leaders should confirm current requirements "
    "directly with their education authority before relying on this document. Program and "
    "outcomes details are current as of the date of generation and may change — see "
    "empschools.com for the latest information."
)
