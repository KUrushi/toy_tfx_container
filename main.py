import os
from pathlib import Path

from tfx.orchestration import metadata
from tfx.orchestration import pipeline as pipeline_module
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

from pipeline import create_pipeline

if __name__ == "__main__":
    pipeline_name = 'tfx-container-pipeline'

    tfx_root = Path(__file__).parent / 'tfx_root'
    pipeline_root = tfx_root / 'pipelines' / pipeline_name
    # Sqlite ML-metadata db path.
    metadata_path = tfx_root /'metadata' / pipeline_name / 'metadata.db'

    components = create_pipeline()
    pipeline = pipeline_module.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root.as_posix(),
        components=components,
        metadata_connection_config=metadata.sqlite_metadata_connection_config(
            metadata_path.as_posix()
        )

    )

    BeamDagRunner().run(pipeline)
