import os
import boto3
import uuid


class DynamodbUtil:
    def __init__(self):
        self.LIBRARY_TABLE = os.environ['LIBRARY_TABLE']
        self.client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')

    def insert_item(self, book_name, author_name):
        serial_id = str(uuid.uuid4())
        resp = self.client.put_item(
            TableName=self.LIBRARY_TABLE,
            Item={
                'serialId': {'S': serial_id},
                'bookName': {'S': book_name},
                'authorName': {'S': author_name}
            }
        )
        return resp,serial_id

    def get_item(self, serial_id):
        resp = self.client.get_item(
            TableName=self.LIBRARY_TABLE,
            Key={
                'serialId': {'S': serial_id}
            }
        )
        return resp

    def get_all_items(self):
        table = self.dynamodb.Table(self.LIBRARY_TABLE)
        result = table.scan()
        return result

    def update_item(self, serial_id, book_name=None, author_name=None):
        table = self.dynamodb.Table(self.LIBRARY_TABLE)
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

        return "Information updated"

    def delete_item(self, serial_id):
        table = self.dynamodb.Table(self.LIBRARY_TABLE)
        response = table.delete_item(
            Key={
                'serialId': serial_id
            }
        )