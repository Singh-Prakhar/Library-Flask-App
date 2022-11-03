import os

import pytest
from flask import Flask
from app import app
import boto3
from dynamodb_util import DynamodbUtil
import os
from unittest import mock

LIBRARY_TABLE = os.environ['LIBRARY_TABLE']


@mock.patch.dict(os.environ, {"LIBRARY_TABLE": "Library-table-dev"})
def test_get_all_items():
    dnb = DynamodbUtil()
    response = dnb.get_all_items()
    assert response == True, response
