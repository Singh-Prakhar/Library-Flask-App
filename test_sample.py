from dynamodb_util import DynamodbUtil
import os

os.environ["LIBRARY_TABLE"] = "Library-table-dev"


def test_insert_item():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    assert response_serial_id is not None


def test_get_item():
    dnb = DynamodbUtil()
    response = dnb.get_item("test_serial_id")
    assert response is not None


def test_get_all_items():
    dnb = DynamodbUtil()
    response = dnb.get_all_items()
    assert 'Items' in response
    assert 'Count' in response


def test_update_item_book_name_author_name():
    dnb = DynamodbUtil()
    response = dnb.update_item("test_serial_id", "test_book_name", "test_author_name")
    assert response == "Information updated. New book name: " + "test_book_name" + "New author name"\
           + "test_author_name", response


def test_update_item_book_name():
    dnb = DynamodbUtil()
    response = dnb.update_item("test_serial_id", book_name="test_book_name")
    assert response == "New book name " + "test_book_name", response


def test_update_item_author_name():
    dnb = DynamodbUtil()
    response = dnb.update_item("test_serial_id", author_name="test_author_name")
    assert response == "New author name " + "test_author_name"


def test_delete_item():
    dnb = DynamodbUtil()
    response = dnb.delete_item("test_serial_id")
    assert response == "Item deleted with serial id " + "test_serial_id"

