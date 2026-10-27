
from pathlib import Path
import math

import mlflow


def configure_tracking(tracking_uri=None):
    """Configure le stockage MLflow si une URI est fournie."""
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)


def get_or_create_experiment(name="ChestScan_AI"):
    """Sélectionne l'expérience existante ou la crée."""
    experiment = mlflow.get_experiment_by_name(name)

    if experiment is not None:
        return experiment.experiment_id

    return mlflow.create_experiment(name)


def log_historical_run(
    run_name,
    params=None,
    metrics=None,
    tags=None,
    artifacts=None,
    experiment_name="ChestScan_AI",
):
    """
    Enregistre des informations historiques vérifiées.
    Ne charge aucun modèle et ne lance aucun entraînement.
    """
    get_or_create_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.set_tag("record_type", "historical")

        for key, value in (tags or {}).items():
            if value is not None:
                mlflow.set_tag(str(key), str(value))

        clean_params = {
            str(key): str(value)
            for key, value in (params or {}).items()
            if value is not None
        }

        if clean_params:
            mlflow.log_params(clean_params)

        clean_metrics = {}

        for key, value in (metrics or {}).items():
            if isinstance(value, bool) or not isinstance(
                value, (int, float)
            ):
                raise ValueError(
                    f"La métrique {key} doit être numérique."
                )

            value = float(value)

            if not math.isfinite(value):
                raise ValueError(
                    f"La métrique {key} doit être finie."
                )

            clean_metrics[str(key)] = value

        if clean_metrics:
            mlflow.log_metrics(clean_metrics)

        for artifact in (artifacts or []):
            path = Path(artifact).resolve()

            if not path.exists():
                raise FileNotFoundError(
                    f"Artefact introuvable : {path}"
                )

            if path.is_file():
                mlflow.log_artifact(str(path))
            elif path.is_dir():
                mlflow.log_artifacts(str(path))

        return run.info.run_id
