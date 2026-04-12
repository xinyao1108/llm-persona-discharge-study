# Persona-Based Discharge Summary Comprehension Study

Query LLMs (OpenAI + Anthropic) with different persona combinations to test comprehension of medical discharge summaries.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API keys
export OPENAI_API_KEY='your-openai-key'
export ANTHROPIC_API_KEY='your-anthropic-key'

# 3. Configure settings in experiment_config.json
# Current experiment: 3 models, temperature=1.0, enable_reasoning=true
#   - GPT-4.1 (10 iterations)
#   - GPT-5.2 (9 iterations)
#   - Claude Sonnet 4.5 (9 iterations)

# 4. Run a small test
python run_experiment.py test_config.json

# 5. Run full experiment
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

## Configuration Options

### Core Settings
- **models**: List of model configurations, each with:
  - `model`: Model ID (e.g., "gpt-4.1", "claude-opus-4-6")
  - `provider`: "openai" or "anthropic"
  - `iterations`: Number of times to repeat the full experiment
- **temperature**: Sampling temperature (default: 1.0)
- **enable_reasoning**: Controls prompt behavior
  - `true`: Ask model to "Explain with your reasoning, then provide the letter"
  - `false`: Ask model to "Answer with only letter"
- **max_personas**: Limit number of persona combinations (optional)
- **output_dir**: Directory for results (files named `{model}_iter{n}.json`)

## Running the Experiment

Results are saved per model per iteration to the `output_dir`:

```
results/
├── gpt-4.1_iter1.json
├── gpt-4.1_iter2.json
├── gpt-4.1_iter3.json
├── gpt-4.1_iter4.json
├── gpt-4.1_iter5.json
├── gpt-5.2_iter1.json
├── gpt-5.2_iter2.json
├── gpt-5.2_iter3.json
├── gpt-5.2_iter4.json
├── claude-sonnet-4-5-20241022_iter1.json
├── claude-sonnet-4-5-20241022_iter2.json
├── claude-sonnet-4-5-20241022_iter3.json
└── claude-sonnet-4-5-20241022_iter4.json
```

You only need the API key(s) for the providers you want to run. The engine skips models whose provider key is missing.

## Current Experiment Summary

- **192 persona combinations** (3 age × 2 gender × 2 education × 4 ethnicity × 2 doctor_visit × 2 er_visit)
- **7,680 queries per iteration** (192 personas × 4 DS × 10 Q)
- **215,040 total queries** across all models and iterations

| Model | Provider | Iterations | Queries |
|-------|----------|-----------|---------|
| gpt-4.1 | OpenAI | 10 | 76,800 |
| gpt-5.2 | OpenAI | 9 | 69,120 |
| claude-sonnet-4-5 | Anthropic | 9 | 69,120 |
| **Total** | | **28** | **215,040** |

## Files

- [persona_discharge_query.py](persona_discharge_query.py) - Main engine (supports OpenAI + Anthropic)
- [run_experiment.py](run_experiment.py) - Run experiments with multi-model/iteration support
- [test_config.json](test_config.json) - Small test config
- [experiment_config.json](experiment_config.json) - Full experiment config
- [PERSONA_README.md](PERSONA_README.md) - Detailed documentation

## Cost Management

⚠️ The full experiment (~215,040 queries) can be expensive! To reduce cost:

1. **Use test config first**: `python run_experiment.py test_config.json`
2. **Reduce iterations**: Lower iteration count per model
3. **Disable reasoning**: Set `"enable_reasoning": false` for shorter responses
4. **Limit scope**: Select specific DS/Questions in config
5. **Set max_personas**: Limit persona combinations

See [PERSONA_README.md](PERSONA_README.md) for full documentation.
