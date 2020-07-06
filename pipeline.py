import os
from pathlib import Path

from tfx.components import CsvExampleGen
from tfx.utils.dsl_utils import external_input
from tfx.dsl.component.experimental import container_component
from tfx.dsl.component.experimental import placeholders
from tfx.types import standard_artifacts

data_path = Path(__file__).parent / "data" / "data.csv"
# TODO コンテナの中に該当するスクリプトがないのでエラーになる
download_data_component = container_component.create_container_component(
    name='DownloadData',
    outputs={
        'data_uri': standard_artifacts.ExternalArtifact
    },
    image='google/cloud-sdk:278.0.0',
    command=[
        "sh", "-exc",
        """
        data_uri="$0"
        python container_component/download_data.py  --uri "$data_uri" 
        """,
        placeholders.OutputUriPlaceholder("data_uri")
    ]

)

xgb_component = container_component.create_container_component(
    name='XGBTrainer',
    inputs={
        'data': standard_artifacts.Examples
    },
    # outputs={
    #     'model': standard_artifacts.ExternalArtifact
    # },
    image="datmo/xgboost",
    command=[
        "sh", "-exc",
        """
        data="$0"
        python container_component/xgb_train.py --example $data
        """,
        placeholders.InputUriPlaceholder('data')
    ],
)


def create_pipeline():
    download_data = download_data_component()
    example = CsvExampleGen(external_input(download_data.outputs['data_uri']))
    xgb = xgb_component(
        data=example.outputs['examples']
    )

    component_instances = [
        download_data,
        # example,
        # xgb
    ]
    return component_instances
