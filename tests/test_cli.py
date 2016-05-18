from click.testing import CliRunner
from tod import cli


def test_init():
    result = CliRunner().invoke(cli.init)
    assert result.exit_code == 0
    assert not result.exception


def test_say_list_of_categories():
    result = CliRunner().invoke(cli.init, ['say_list_of_categories'], input="Invalid Category")
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == "Truth or Dare for New Couples, Truth or Dare Questions for Married Couples, " \
                                    "All the Truth or Dare Questions.\n" \
                                    "What category do you want to play?: \n" \
                                    "Sorry, I'm not sure I understood your request."


def test_play_category():
    result = CliRunner().invoke(cli.init, ['play_category', "Truth or Dare for New Couples"])
    assert result.exit_code == 0
    assert not result.exception


def test_say_rules():
    result = CliRunner().invoke(cli.say_rules)
    assert result.exit_code == 0
    assert not result.exception



