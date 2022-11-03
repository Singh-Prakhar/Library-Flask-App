import os
import uuid
import boto3
from dynamodb_util import DynamodbUtil
from flask import Flask, jsonify, request, json

app = Flask(__name__)


client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
ddb_util = DynamodbUtil()


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/item", methods=["POST"])
def create_item():
    book_name = request.json.get('bookName')
    author_name = request.json.get('authorName')

    if not book_name or not author_name:
        return jsonify({'error': 'Please provide complete information'}), 400

    resp, serial_id = ddb_util.insert_item(book_name,author_name)

    return jsonify({
        'serialId': serial_id,
        'bookName': book_name,
        'authorName': author_name
    })


@app.route("/item", methods=["GET"])
def get_item():
    serial_id = None

    serial_id = request.args['serialId']

    if serial_id is None:
        return jsonify({'error': 'SerialId missing'}), 404

    response = ddb_util.get_item(serial_id)
    item = response['Item']

    if not item:
        return jsonify({'error': 'SerialId does not exist'}), 404

    return jsonify({
        'serialId': item.get('serialId').get('S'),
        'bookName': item.get('bookName').get('S'),
        'authorName': item.get('authorName').get('S')

    })


@app.route("/itemlist", methods=["GET"])
def list_all_books():
    result = ddb_util.get_all_items()
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }
    return response


@app.route("/updateitem", methods=['PUT'])
def update():
    serial_id = None
    book_name = None
    author_name = None
    if 'serialId' in request.args:
        serial_id = request.args['serialId']
    if 'bookName' in request.args:
        book_name = request.args['bookName']
    if 'authorName' in request.args:
        author_name = request.args['authorName']

    if serial_id is None:
        return jsonify({'error': 'Please provide serial ID'}), 400

    response = ddb_util.update_item(serial_id, book_name, author_name)

    return jsonify({
        "MSG": response
    })


@app.route("/deleteitem", methods=['DELETE'])
def delete():

    to_delete_id = request.args['serialId']

    if not to_delete_id:
        return jsonify({'error': 'Please provide correct ID'}), 400

    ddb_util.delete_item(to_delete_id)

    return jsonify({
        'status code': "200"
    })

