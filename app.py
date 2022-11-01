import os

import boto3

from flask import Flask, jsonify, request, json

app = Flask(__name__)

LIBRARY_TABLE = os.environ['LIBRARY_TABLE']
client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


@app.route("/hello")
def hello():
    return "Hello World!" + "Params: " + request.args['serialId']


@app.route("/item", methods=["POST"])
def create_user():
    serial_id = request.json.get('serialId')
    book_name = request.json.get('bookName')
    author_name = request.json.get('authorName')

    if not serial_id or not book_name or not author_name:
        return jsonify({'error': 'Please provide complete information'}), 400

    resp = client.put_item(
        TableName=LIBRARY_TABLE,
        Item={
            'serialId': {'S': serial_id},
            'bookName': {'S': book_name},
            'authorName': {'S': author_name}
        }
    )

    return jsonify({
        'serialId': serial_id,
        'bookName': book_name,
        'authorName': author_name
    })


@app.route("/item", methods=["GET"])
def get_user():


    serial_id = request.args['serialId']

    if serial_id is None:
        return jsonify({'error': 'SerialId does not exist'}), 404

    resp = client.get_item(
        TableName=LIBRARY_TABLE,
        Key={
            'serialId': {'S': serial_id}
        }
    )

    item = resp['Item']
    if not item:
        return jsonify({'error': 'SerialId does not exist'}), 404

    return jsonify({
        'serialId': item.get('serialId').get('S'),
        'bookName': item.get('bookName').get('S'),
        'authorName': item.get('authorName').get('S')

    })


@app.route("/itemlist", methods=["GET"])
def list_all_books():
    table = dynamodb.Table(LIBRARY_TABLE)
    result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response


@app.route("/updateitem", methods=['PUT'])
def update():

    serial_id = request.json.get('serialId')
    book_name = request.json.get('bookName')
    author_name = request.json.get('authorName')

    if not serial_id or not book_name or not author_name:
        return jsonify({'error': 'Please provide complete information'}), 400

    table = dynamodb.Table(LIBRARY_TABLE)

    if book_name:
        table.update_item(
            Key={
                'serialId': serial_id,
            },
            UpdateExpression="set bookName = :g",
            ExpressionAttributeValues={
                    ":g": book_name
            },
            ReturnValues="UPDATED_NEW"
        )

    if author_name:
        table.update_item(
            Key={
                'serialId': serial_id,
            },
            UpdateExpression="set authorName = :g",
            ExpressionAttributeValues={
                ":g": author_name
            },
            ReturnValues="UPDATED_NEW"
        )

    return jsonify({
        "MSG" : "New Updates=>",
        'serialId': serial_id,
        'bookName': book_name,
        'authorName': author_name
    })


# Todo: add a check mechanism for ID
@app.route("/deleteitem", methods=['DELETE'])
def delete():
    table = dynamodb.Table(LIBRARY_TABLE)

    to_delete_id = request.json.get('serialId')

    if not to_delete_id:
        return jsonify({'error': 'Please provide complete information'}), 400

    table.delete_item(
        Key={
            'serialId': to_delete_id
        }
    )

    response = {
        "statusCode": 200
    }

    return response
