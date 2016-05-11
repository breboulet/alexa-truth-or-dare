import pkg_resources
from tod import todmodel


def test_createdb():
    db = todmodel.TodModel().createdb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    assert cursor.fetchone() is None
    cursor.execute("SELECT * FROM questions")
    assert cursor.fetchone() is None


def test_addcategory_getallcategories():
    model = todmodel.TodModel()
    assert model.addcategory("category1") == 1
    assert model.addcategory("category2") == 2
    assert len(model.getallcategories()) == 2


def test_buildsqlitefromjson():
    # result = cli.buildsqlitefromjson(pkg_resources.resource_filename("resources", "tods_test_sample.json"))
    # for entry in result.cursor():
    #     print entry['category']
    assert True
