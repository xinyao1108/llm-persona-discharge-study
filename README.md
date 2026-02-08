# Persona-Based Discharge Summary Comprehension Study

Query ChatGPT with different persona combinations to test comprehension of medical discharge summaries.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# 3. Run a small test (8 queries, ~$0.50)
python run_experiment.py test_config.json

# 4. Run full experiment (38,400 queries, ~$700)
python run_experiment.py experiment_config.json
```

## What's Included

### 4 Discharge Summaries (DS1-DS4)
- DS1: Duodenal ulcer with medication
- DS2: Post-procedure care with narcotics
- DS3: Splint care and physical therapy
- DS4: Drain care instructions

### 10 Questions (Q1-Q10)
- Q1: Understanding level
- Q2-Q5: Knowledge checks (medications, diagnosis, side effects, prescriptions)
- Q6-Q7: Comprehension (condition, treatment)
- Q8-Q9: Application (restrictions, concerns)
- Q10: Difficulty rating

### Persona Attributes
- Age, Gender, Education, Ethnicity, Doctor visit frequency, ER visit frequency

## Files

- [persona_discharge_query.py](persona_discharge_query.py) - Main engine
- [run_experiment.py](run_experiment.py) - Run experiments with cost estimation
- [test_config.json](test_config.json) - Small test (8 queries)
- [experiment_config.json](experiment_config.json) - Full experiment (38,400 queries)
- [PERSONA_README.md](PERSONA_README.md) - Detailed documentation

## Cost Management

⚠️ The full experiment is expensive! To reduce cost:

1. **Use test config first**: `python run_experiment.py test_config.json`
2. **Use cheaper model**: Set `"model": "gpt-3.5-turbo"` in config
3. **Limit scope**: Select specific DS/Questions in config
4. **Set max_personas**: Limit persona combinations

See [PERSONA_README.md](PERSONA_README.md) for full documentation.
