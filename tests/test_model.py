import pkg_resources
from tod import model


def test_create_db():
    db = model.Model().create_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    assert cursor.fetchone() is None
    cursor.execute("SELECT * FROM questions")
    assert cursor.fetchone() is None


def test_add_category():
    _model = model.Model()
    assert _model.add_category("category1") == 1
    assert _model.add_category("category2") == 2
    assert _model.add_category("category2") == 2


def test_get_all_categories():
    _model = model.Model()
    assert len(_model.get_all_categories()) == 0
    _model.add_category("category1")
    assert len(_model.get_all_categories()) == 1


def test_add_question():
    _model = model.Model()
    assert _model.add_question("Question 1", "Truth", "Category 1") == (1, 1)
    assert _model.add_question("Question 2", "Truth", "Category 1") == (2, 1)
    assert _model.add_question("Question 3", "Truth", "Category 2") == (3, 2)
    assert _model.add_question("Question 3", "Truth", "Category 2") == (3, 2)
    assert _model.add_question("Question 3", "Truth", "Category 3") == (3, 2)


def test_get_category_id():
    _model = model.Model()
    assert not _model.get_category_id("category1")
    _model.add_category("category1")
    assert _model.get_category_id("category1") == 1


def test_get_question_id():
    _model = model.Model()
    assert not _model.get_question_id("Question 1")
    _model.add_question("Question 1", "Truth", "Category 1")
    assert _model.get_question_id("Question 1") == 1


def test_get_questions_of_type_and_category():
    _model = model.Model()
    _model.add_question("Question 1", "Truth", "Category 1")
    _model.add_question("Question 2", "Truth", "Category 1")
    _model.add_question("Question 3", "Truth", "Category 2")
    _model.add_question("Question 3", "Truth", "Category 2")
    _model.add_question("Question 3", "Truth", "Category 3")
    _model.add_question("Question 4", "Truth", "Category 2")
    _model.add_question("Question 5", "Dare", "Category 2")
    assert len(_model.get_questions_of_type_and_category("Truth", 2)) == 2
    assert len(_model.get_questions_of_type_and_category("Dare", 2)) == 1
    assert len(_model.get_questions_of_type_and_category("Dare", 1)) == 0


def test_get_question_with_id():
    _model = model.Model()
    _model.add_question("Question 1", "Truth", "Category 1")
    assert _model.get_question_with_id(0) is None
    assert _model.get_question_with_id(1)[3] == 1


def test_populate_from_json():
    _model = model.Model()
    _model.populate_from_json(pkg_resources.resource_filename("resources", "tods_test_sample.json"))
    assert len(_model.get_all_categories()) == 2
    assert len(_model.get_all_questions()) == 8
    assert len(_model.get_questions_of_type_and_category('Truth', 2)) == 2

def test_get_questions_of_type():
    _model = model.Model()
    _model.add_question("Question 1", "Truth", "Category 1")
    _model.add_question("Question 2", "Truth", "Category 2")
    _model.add_question("Question 3", "Dare", "Category 3")
    assert len(_model.get_questions_of_type("Truth")) == 2
    assert len(_model.get_questions_of_type("Dare")) == 1
