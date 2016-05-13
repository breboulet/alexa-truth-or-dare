import pkg_resources
from tod import model


def test_createdb():
    db = model.Model().createdb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    assert cursor.fetchone() is None
    cursor.execute("SELECT * FROM questions")
    assert cursor.fetchone() is None


def test_addcategory():
    _model = model.Model()
    assert _model.addcategory("category1") == 1
    assert _model.addcategory("category2") == 2
    assert _model.addcategory("category2") == 2


def test_getallcategories():
    _model = model.Model()
    assert len(_model.getallcategories()) == 0
    _model.addcategory("category1")
    assert len(_model.getallcategories()) == 1


def test_addquestion():
    _model = model.Model()
    assert _model.addquestion("Question 1", "Truth", "Category 1") == (1, 1)
    assert _model.addquestion("Question 2", "Truth", "Category 1") == (2, 1)
    assert _model.addquestion("Question 3", "Truth", "Category 2") == (3, 2)
    assert _model.addquestion("Question 3", "Truth", "Category 2") == (3, 2)
    assert _model.addquestion("Question 3", "Truth", "Category 3") == (3, 2)


def test_getcategoryid():
    _model = model.Model()
    assert not _model.getcategoryid("category1")
    _model.addcategory("category1")
    assert _model.getcategoryid("category1") == 1


def test_getquestionid():
    _model = model.Model()
    assert not _model.getquestionid("Question 1")
    _model.addquestion("Question 1", "Truth", "Category 1")
    assert _model.getquestionid("Question 1") == 1


def test_getquestionsoftypeandcategory():
    _model = model.Model()
    _model.addquestion("Question 1", "Truth", "Category 1")
    _model.addquestion("Question 2", "Truth", "Category 1")
    _model.addquestion("Question 3", "Truth", "Category 2")
    _model.addquestion("Question 3", "Truth", "Category 2")
    _model.addquestion("Question 3", "Truth", "Category 3")
    _model.addquestion("Question 4", "Truth", "Category 2")
    _model.addquestion("Question 5", "Dare", "Category 2")
    assert len(_model.getquestionsoftypeandcategory("Truth", 2)) == 2
    assert len(_model.getquestionsoftypeandcategory("Dare", 2)) == 1
    assert len(_model.getquestionsoftypeandcategory("Dare", 1)) == 0


def test_getquestionwithid():
    _model = model.Model()
    _model.addquestion("Question 1", "Truth", "Category 1")
    assert _model.getquestionwithid(0) is None
    assert _model.getquestionwithid(1)[2] == 1


def test_populatefromjson():
    _model = model.Model()
    _model.populatefromjson(pkg_resources.resource_filename("resources", "tods_test_sample.json"))
    assert len(_model.getallcategories()) == 2
    assert len(_model.getallquestions()) == 8
    assert len(_model.getquestionsoftypeandcategory('Truth', 2)) == 2
