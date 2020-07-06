import os
from pathlib import Path

from tfx.components import CsvExampleGen
from tfx.utils.dsl_utils import external_input
from tfx.dsl.component.experimental import container_component
from tfx.dsl.component.experimental import placeholders
from tfx.types import standard_artifacts
from tfx.orchestration import metadata
from tfx.orchestration import pipeline as pipeline_module
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner


def create_pipeline():
    data_path = Path(__file__) / "data.csv"
    download_data_component = container_component.create_container_component(
        name='DownloadData',
        outputs={
            'data_uri': standard_artifacts.ExternalArtifact
        },
        image='python:3.7',
        command=[
            "sh", "-exc",
            """
            data_uri="$0"
            python container_component/download_data.py  --uri "$data_uri"
            """,
            placeholders.OutputUriPlaceholder(data_path.as_posix())
        ]

    )
    example = CsvExampleGen(external_input(download_data_component.outputs['data']))

    xgb = container_component.create_container_component(
        name='XGBTrainer',
        inputs={
            'data':standard_artifacts.Examples
        },
        # outputs={
        #     'model': standard_artifacts.ExternalArtifact
        # },
        image="datmo/xgboost",
        command=[
            "sh", "-exc",
            """
            python container_component/xgb_train.py --example $0
            """,
            placeholders.InputUriPlaceholder('data')
        ],
    )

    component_instances = [
        download_data_component,
        example,
        xgb
    ]
    return component_instances


if __name__ == "__main__":
    pipeline_name = 'tfx-container-pipeline'

    tfx_root = Path(__file__)/ 'tfx_root'
    pipeline_root = tfx_root / 'pipelines' / pipeline_name
    # Sqlite ML-metadata db path.
    metadata_path = os.path.join(tfx_root.as_posix(), 'metadata', pipeline_name,
                                 'metadata.db')

    components = create_pipeline()
    pipeline = pipeline_module.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root.as_posix(),
        components=components,
        enable_cache=True,
        metadata_connection_config=metadata.sql_metadata_connection_config(
            metadata_path
        )

    )

    BeamDagRunner().run(pipeline)

