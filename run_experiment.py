#!/usr/bin/env python3
"""
Run the full discharge summary comprehension experiment from config file.
"""

import json
import sys
from persona_discharge_query import PersonaDischargeQueryEngine


def load_config(config_file: str = "experiment_config.json") -> dict:
    """Load experiment configuration."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)


def calculate_total_queries(config: dict) -> int:
    """Calculate total number of queries that will be made."""
    import itertools

    persona_keys = ['age', 'gender', 'education', 'ethnicity', 'doctor_visit', 'er_visit_frequency']
    persona_values = [config['persona_variations'][k] for k in persona_keys]
    num_personas = len(list(itertools.product(*persona_values)))

    if config.get('max_personas'):
        num_personas = min(num_personas, config['max_personas'])

    num_ds = len(config['discharge_summary_ids'])
    num_questions = len(config['question_ids'])

    return num_personas * num_ds * num_questions


def estimate_cost(total_queries: int, model: str) -> dict:
    """Estimate approximate cost based on model and query count."""
    # Rough estimates (actual cost depends on prompt length)
    avg_tokens_per_query = 600  # ~400 prompt + ~200 response

    costs_per_1k = {
        'gpt-4': 0.03,  # Input pricing (output is higher but we'll use average)
        'gpt-4-turbo': 0.01,
        'gpt-3.5-turbo': 0.001
    }

    cost_per_1k = costs_per_1k.get(model, 0.03)
    total_tokens = total_queries * avg_tokens_per_query
    estimated_cost = (total_tokens / 1000) * cost_per_1k

    return {
        'total_queries': total_queries,
        'estimated_tokens': total_tokens,
        'estimated_cost_usd': round(estimated_cost, 2),
        'model': model
    }


def main():
    """Run the experiment from config file."""

    # Load config
    config_file = sys.argv[1] if len(sys.argv) > 1 else "experiment_config.json"
    print(f"Loading configuration from: {config_file}")
    config = load_config(config_file)

    # Calculate and display cost estimate
    total_queries = calculate_total_queries(config)
    cost_info = estimate_cost(total_queries, config['model'])

    print("\n" + "="*80)
    print("COST ESTIMATE")
    print("="*80)
    print(f"Total queries: {cost_info['total_queries']:,}")
    print(f"Estimated tokens: {cost_info['estimated_tokens']:,}")
    print(f"Estimated cost: ${cost_info['estimated_cost_usd']:.2f} USD")
    print(f"Model: {cost_info['model']}")
    print("="*80)

    # Ask for confirmation if cost is high
    if cost_info['estimated_cost_usd'] > 10:
        response = input(f"\nEstimated cost is ${cost_info['estimated_cost_usd']:.2f}. Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Experiment cancelled.")
            return

    # Initialize engine
    try:
        engine = PersonaDischargeQueryEngine()
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nSet your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return

    # Run experiment
    print("\nStarting experiment...")
    results = engine.run_full_experiment(
        persona_variations=config['persona_variations'],
        discharge_summary_ids=config['discharge_summary_ids'],
        question_ids=config['question_ids'],
        model=config['model'],
        temperature=config['temperature'],
        max_personas=config.get('max_personas'),
        enable_reasoning=config.get('enable_reasoning', False)
    )

    # Save results
    output_file = config.get('output_file', 'results.json')
    engine.save_results(results, output_file)

    print(f"\nExperiment complete! Results saved to {output_file}")


if __name__ == "__main__":
    main()
