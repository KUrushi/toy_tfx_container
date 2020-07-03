from typing import Any, Dict, List, Text
import tensorflow as tf
from tfx_bsl.tfxio import tf_example_record
from tfx.utils import io_utils
from tfx import types


def load_tfrecord(input_dict: Dict[Text, List[types.Artifact]]):
    pass


def convert_dict(dataset: tf.data.Dataset):
    """
    convert tfrecord to dict
    :return: dict
    """
    pass
