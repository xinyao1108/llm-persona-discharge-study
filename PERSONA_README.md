# Persona-Based Discharge Summary Comprehension Study

This script queries ChatGPT with different persona combinations to test comprehension of medical discharge summaries.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Run Small Test

```bash
python persona_discharge_query.py
```

This runs a small test with 2 personas, DS1, and questions Q1-Q3.

### 4. Run Full Experiment

```bash
python run_experiment.py
```

**WARNING:** The full experiment with default config will make **38,400 queries** (3×2×2×4×4×4 personas × 4 DS × 10 questions) and cost approximately **$700+** with GPT-4.

## Configuration

Edit [experiment_config.json](experiment_config.json) to customize:

### Persona Variations

```json
{
  "persona_variations": {
    "age": ["25", "45", "65"],
    "gender": ["male", "female"],
    "education": ["high", "low"],
    "ethnicity": ["White", "Black", "Hispanic", "Asian"],
    "doctor_visit": ["weekly", "monthly", "yearly", "never"],
    "er_visit_frequency": ["weekly", "monthly", "yearly", "never"]
  }
}
```

### Limit Scope (Recommended for Testing)

To reduce cost, limit the experiment:

```json
{
  "persona_variations": {
    "age": ["25", "65"],
    "gender": ["male", "female"],
    "education": ["high", "low"],
    "ethnicity": ["White"],
    "doctor_visit": ["monthly", "never"],
    "er_visit_frequency": ["yearly", "never"]
  },
  "discharge_summary_ids": ["DS1"],
  "question_ids": ["Q1", "Q2", "Q3"],
  "max_personas": 10
}
```

This would run only: 10 personas × 1 DS × 3 questions = **30 queries** (~$1-2)

### Use Cheaper Model

```json
{
  "model": "gpt-3.5-turbo"
}
```

This reduces cost by ~30x but may affect response quality.

## Built-in Components

### Discharge Summaries (4)

- **DS1**: Duodenal ulcer with medication prescription
- **DS2**: Post-procedure care with narcotics warnings
- **DS3**: Splint care and physical therapy instructions
- **DS4**: Drain care and activity restrictions

### Questions (10)

- **Q1**: Understanding level rating
- **Q2**: Medication name knowledge
- **Q3**: Diagnosis knowledge
- **Q4**: Side effects knowledge
- **Q5**: Other prescriptions
- **Q6**: Condition type identification
- **Q7**: Treatment type identification
- **Q8**: Activity/food restrictions
- **Q9**: Unclear or worrying aspects
- **Q10**: Difficulty rating

## Output Format

Results are saved as JSON:

```json
[
  {
    "success": true,
    "response": "B\n\nAs a 25 year old male with high education...",
    "model": "gpt-4",
    "tokens_used": 450,
    "persona": {
      "age": "25",
      "gender": "male",
      "education": "high",
      "ethnicity": "White",
      "doctor_visit": "monthly",
      "er_visit_frequency": "never"
    },
    "discharge_summary_id": "DS1",
    "question_id": "Q1",
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

## Running Specific Combinations

Create a custom script:

```python
from persona_discharge_query import PersonaDischargeQueryEngine

engine = PersonaDischargeQueryEngine()

test_cases = [
    {
        'persona': {
            'age': '65',
            'gender': 'female',
            'education': 'low',
            'ethnicity': 'Hispanic',
            'doctor_visit': 'never',
            'er_visit_frequency': 'monthly'
        },
        'ds_id': 'DS1',
        'question_id': 'Q1'
    }
]

results = engine.run_specific_combinations(test_cases)
engine.save_results(results, "my_results.json")
```

## Cost Management Tips

1. **Start small**: Test with `max_personas: 5` first
2. **Use gpt-3.5-turbo**: 30x cheaper than GPT-4
3. **Select specific DS/Questions**: Don't test all 40 combinations
4. **Check estimate**: Script shows cost before running
5. **Incremental approach**: Run one DS at a time

## Example: Cost-Effective Test

```json
{
  "persona_variations": {
    "age": ["25", "65"],
    "gender": ["male"],
    "education": ["high", "low"],
    "ethnicity": ["White"],
    "doctor_visit": ["monthly"],
    "er_visit_frequency": ["yearly"]
  },
  "discharge_summary_ids": ["DS1"],
  "question_ids": ["Q1", "Q10"],
  "model": "gpt-3.5-turbo",
  "max_personas": null
}
```

This runs: 4 personas × 1 DS × 2 questions = **8 queries** (~$0.05)

## Analyzing Results

Load and analyze the JSON output:

```python
import json
import pandas as pd

with open('results.json') as f:
    results = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(results)

# Group by education level
df.groupby(df['persona'].apply(lambda x: x['education']))['response'].value_counts()

# Check understanding by age group
df.groupby([df['persona'].apply(lambda x: x['age']), 'question_id'])['response'].first()
```

## Files

- [persona_discharge_query.py](persona_discharge_query.py) - Main engine
- [run_experiment.py](run_experiment.py) - Run from config file
- [experiment_config.json](experiment_config.json) - Configuration
- [requirements.txt](requirements.txt) - Dependencies
