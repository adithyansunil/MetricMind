import yaml
from pathlib import Path


# ============================================
# MetricMind - Semantic Engine
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent
SEMANTIC_DIR = BASE_DIR / "semantic_layer"


def load_yaml(filename: str):
    """Load a YAML configuration file."""
    file_path = SEMANTIC_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_metrics():
    """Load governed metric definitions."""
    return load_yaml("metrics.yml")["metrics"]


def load_dimensions():
    """Load governed dimension definitions."""
    return load_yaml("dimensions.yml")["dimensions"]


def get_metric(metric_name: str):
    """Return a metric definition by name."""
    metrics = load_metrics()

    metric = metrics.get(metric_name.lower())

    if metric is None:
        raise ValueError(f"Unknown metric: {metric_name}")

    return metric


def get_available_metrics():
    """Return all available metrics."""
    metrics = load_metrics()

    return {
        key: value["name"]
        for key, value in metrics.items()
    }


def get_available_dimensions():
    """Return all available dimensions."""
    dimensions = load_dimensions()

    return {
        key: value["name"]
        for key, value in dimensions.items()
    }


if __name__ == "__main__":
    print("MetricMind Semantic Engine")
    print("=" * 40)

    print("\nAvailable Metrics:")
    for key, name in get_available_metrics().items():
        print(f"  - {key}: {name}")

    print("\nAvailable Dimensions:")
    for key, name in get_available_dimensions().items():
        print(f"  - {key}: {name}")

    print("\nRevenue Definition:")
    print(get_metric("revenue"))