from dynamodb_util import DynamodbUtil
import os

os.environ["LIBRARY_TABLE"] = "Library-table-dev"


def test_insert_item():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    response_check = dnb.get_item(response_serial_id)

    assert response_serial_id is not None
    assert response_check['Item']['authorName']['S'] == 'test_author_name', response_check
    assert response_check['Item']['bookName']['S'] == 'test_book_name', response_check


def test_get_item():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    response_check = dnb.get_item(response_serial_id)
    assert response_check is not None
    assert response_check['Item']['authorName']['S'] == 'test_author_name', response_check


def test_get_all_items():
    dnb = DynamodbUtil()
    response = dnb.get_all_items()
    assert 'Items' in response
    assert 'Count' in response


def test_update_item_book_name_author_name():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    updated_response = dnb.update_item(response_serial_id, "new_test_book_name", "new_test_author_name")
    response_check = dnb.get_item(response_serial_id)
    assert updated_response == "Information updated. New book name: " + "new_test_book_name" + "New author name"\
           + "new_test_author_name", updated_response
    assert response_check['Item']['authorName']['S'] == 'new_test_author_name', response_check
    assert response_check['Item']['bookName']['S'] == 'new_test_book_name', response_check


def test_update_item_book_name():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    updated_response = dnb.update_item(response_serial_id, book_name="new_test_book_name")
    response_check = dnb.get_item(response_serial_id)

    assert updated_response == "New book name " + "new_test_book_name", updated_response
    assert response_check['Item']['authorName']['S'] == 'test_author_name', response_check
    assert response_check['Item']['bookName']['S'] == 'new_test_book_name', response_check


def test_update_item_author_name():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    updated_response = dnb.update_item(response_serial_id, author_name="new_test_author_name")
    response_check = dnb.get_item(response_serial_id)
    assert updated_response == "New author name " + "new_test_author_name"
    assert response_check['Item']['authorName']['S'] == 'new_test_author_name', response_check
    assert response_check['Item']['bookName']['S'] == 'test_book_name', response_check


def test_delete_item():
    dnb = DynamodbUtil()
    response, response_serial_id = dnb.insert_item(book_name="test_book_name", author_name="test_author_name")
    delete_response = dnb.delete_item(response_serial_id)
    response_check = dnb.get_item(response_serial_id)
    assert delete_response == "Item deleted with serial id " + response_serial_id
    assert 'Item' not in response_check
