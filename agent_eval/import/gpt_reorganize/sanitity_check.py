import json
from pathlib import Path


SCHEMA = {
    "title": "",
    "data": [
        {
            "name": "overview",
            "value": [
                {"name": "name", "value": "", "description": "Name of the model.", "type": "short text"},
                {"name": "description", "value": "", "description": "Model purpose, capabilities, novelty and caveats", "type": "long text"},
                {"name": "creator", "value": "", "description": "Person or organization developed the model.", "type": "short text"},
                {"name": "date", "value": "", "description": "Model development completion date.", "type": "date"},
                {"name": "version", "value": "", "description": "Version of the model.", "type": "short text"},
                {"name": "type", "value": "", "description": "Model architecture or algorithm type."},
                {"name": "task", "value": "", "description": "Model task."},
                {"name": "license", "value": "", "description": "Licence and intellectual property (IP) information.", "type": "short text"},
                {"name": "home", "value": "", "description": "URL hosting the model.", "type": "short text"},
                {"name": "contact", "value": "", "description": "Author contact information.", "type": "short text"},
                {"name": "citation", "value": "", "description": "How should the model be cited? Typically includes title, author, year, and publisher. May be a formatted citation or bibtex entries like @article.", "type": "short text"},
                {"name": "more", "value": "", "description": "Additional model information not found above.", "type": "long text"},
            ],
        },
        {
            "name": "use",
            "value": [
                {"name": "use_cases", "value": "", "description": "Intended uses of the model.", "type": "long text"},
                {"name": "oversight", "value": "", "description": "Defines the level of human control over the system.", "type": "list:self-learning/autonomous,human-in-the-loop,human-on-the-loop,human-in-command,unknown"},
                {"name": "user_groups", "value": "", "description": "Intended users.", "type": "long text"},
                {"name": "out_of_scope_use", "value": "", "description": "Unintended and improper use of model.", "type": "long text"},
                {"name": "software", "value": "", "description": "Software requirements and dependencies?", "type": "long text"},
                {"name": "instructions", "value": "", "description": "Use instructions.", "type": "long text"},
                {"name": "inputs_outputs", "value": "", "description": "Description of the model's inputs and outputs", "type": "long text"},
                {"name": "factors", "value": "", "description": "Foreseeable salient factors for which model performance may vary.", "type": "long text"},
                {"name": "hardware", "value": "", "description": "Hardware requirements for training and inference.", "type": "long text"},
                {"name": "more", "value": "", "description": "Additional information about intended uses not found above.", "type": "long text"},
            ],
        },
        {
            "name": "training",
            "value": [
                {"name": "datasets", "value": "", "description": "Dataset(s) used during training.", "type": "long text"},
                {"name": "motivation", "value": "", "description": "Why were training datasets chosen?", "type": "long text"},
                {"name": "preprocessing", "value": "", "description": "Data pre-processing for training (tokenizer, data augmentation etc.).", "type": "long text"},
                {"name": "standards", "value": "", "description": "Technical or ethical frameworks used that define best practices for safety, quality, transparency, or risk management.", "type": "list:none,ISO,IEEE,unknown"},
                {"name": "update", "value": "", "description": "Is tge training set up-to-date, of high quality, complete and representative of the environment the system will be deployed in?", "type": "list:no,yes,unknown"},
                {"name": "more", "value": "", "description": "Additional training set information not found above.", "type": "long text"},
            ],
        },
        {
            "name": "evaluation",
            "value": [
                {"name": "datasets", "value": "", "description": "Dataset(s) used during evaluation.", "type": "long text"},
                {"name": "motivation", "value": "", "description": "Why were evaluation datasets chosen?", "type": "long text"},
                {"name": "preprocessing", "value": "", "description": "Data pre-processing for evaluation (tokenizer, data augmentation etc.).", "type": "long text"},
                {"name": "standards", "value": "", "description": "Technical or ethical frameworks used that define best practices for safety, quality, transparency, or risk management.", "type": "list:none,ISO,IEEE,unknown"},
                {"name": "update", "value": "", "description": "Is the evalution set up-to-date, of high quality, complete and representative of the environment the system will be deployed in?", "type": "list:no,yes,unknown"},
                {"name": "more", "value": "", "description": "Additional evaluation set information not found above.", "type": "long text"},
            ],
        },
        {
            "name": "performance",
            "value": [
                {"name": "analysis", "value": "", "description": "Analysis and explanation of performance results.", "type": "long text"},
                {"name": "metrics", "value": "", "description": "Benchmark results for any performance metrics.", "type": "long text"},
                {"name": "thresholds", "value": "", "description": "If decision thresholds are used, what are they, and why were those parameters chosen?", "type": "long text"},
                {"name": "methodology", "value": "", "description": "Explanation of how metrics are calculated and averaged, with uncertainty measures and evaluation method.", "type": "long text"},
                {"name": "environmental_impact", "value": "", "description": "Report of energy consumption, CO2 emissions or any other environmental impact.", "type": "long text"},
                {"name": "bias", "value": "", "description": "Performance and bias across different groups (e.g. ethnicity, gender)", "type": "long text"},
            ],
        },
        {
            "name": "safety",
            "value": [
                {"name": "ethics", "value": "", "description": "Ethical considerations regarding datasets and usage of model. Recommended mitigation measures.", "type": "long text"},
                {"name": "fairness", "value": "", "description": "Definition of fairness applied in setting up the AI system.", "type": "long text"},
                {"name": "risks", "value": "", "description": "Possible threats to the AI system (design faults, technical faults, environmental threats) and the possible consequences.", "type": "long text"},
                {"name": "security", "value": "", "description": "Is the AI system certified for cybersecurity or is it compliant with specific security standards?", "type": "long text"},
                {"name": "caveats", "value": "", "description": "Additional concerns that were not covered in the previous sections.", "type": "long text"},
            ],
        },
    ],
}


def check_schema(actual, expected, path="root"):
    errors = []

    # Check that both are dictionaries
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected object, got {type(actual).__name__}"]

        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())

        # Missing keys
        for key in sorted(expected_keys - actual_keys):
            errors.append(f"{path}: missing key '{key}'")

        # Unexpected keys
        for key in sorted(actual_keys - expected_keys):
            errors.append(f"{path}: unexpected key '{key}'")

        # Check existing keys
        for key in expected_keys & actual_keys:
            errors.extend(
                check_schema(actual[key], expected[key], f"{path}.{key}")
            )

    # Check lists
    elif isinstance(expected, list):
        if not isinstance(actual, list):
            return [f"{path}: expected list, got {type(actual).__name__}"]

        if len(actual) != len(expected):
            errors.append(
                f"{path}: expected {len(expected)} items, got {len(actual)}"
            )

        # Match list objects by "name" rather than position
        if (
            all(isinstance(x, dict) and "name" in x for x in expected)
            and all(isinstance(x, dict) and "name" in x for x in actual)
        ):
            expected_by_name = {x["name"]: x for x in expected}
            actual_by_name = {x["name"]: x for x in actual}

            for name in expected_by_name:
                if name not in actual_by_name:
                    errors.append(f"{path}: missing item '{name}'")
                else:
                    errors.extend(
                        check_schema(
                            actual_by_name[name],
                            expected_by_name[name],
                            f"{path}[name={name}]",
                        )
                    )

            for name in actual_by_name:
                if name not in expected_by_name:
                    errors.append(f"{path}: unexpected item '{name}'")

        else:
            for i, expected_item in enumerate(expected):
                if i < len(actual):
                    errors.extend(
                        check_schema(
                            actual[i],
                            expected_item,
                            f"{path}[{i}]",
                        )
                    )

    # # Check primitive values
    # else:
    #     if actual != expected:
    #         errors.append(
    #             f"{path}: expected {expected!r}, got {actual!r}"
    #         )

    return errors


def main():
    root = Path(".")

    json_files = sorted(root.glob("*.json"))

    if not json_files:
        print("No JSON files found.")
        return

    valid = 0
    invalid = 0

    print(f"Checking {len(json_files)} JSON files...\n")

    for json_file in json_files:
        try:
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            invalid += 1
            print(f"❌ {json_file.name}")
            print(f"   Invalid JSON: {e}\n")
            continue
        except OSError as e:
            invalid += 1
            print(f"❌ {json_file.name}")
            print(f"   Could not read file: {e}\n")
            continue

        errors = check_schema(data, SCHEMA)

        if errors:
            invalid += 1
            print(f"❌ {json_file.name}")

            for error in errors:
                print(f"   - {error}")

            print()
        else:
            valid += 1
            print(f"✓ {json_file.name}")

    print("\n" + "=" * 50)
    print(f"Total:   {len(json_files)}")
    print(f"Valid:   {valid}")
    print(f"Invalid: {invalid}")
    print("=" * 50)


if __name__ == "__main__":
    main()