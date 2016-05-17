from click.testing import CliRunner
from tod import cli


def test_cli():
    result = CliRunner().invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception


def test_say_list_of_categories():
    result = CliRunner().invoke(cli.main, ['say_list_of_categories'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == "Truth or Dare for New Couples\n" \
                                    "Truth or Dare Questions for Married Couples\n" \
                                    "What category do you want to play with?"


def test_cli_set_category():
    result = CliRunner().invoke(cli.set_current_category, ['--category_name', "Truth or Dare for New Couples"])
    assert result.exit_code == 0
    assert not result.exception


def test_cli_say_rules():
    result = CliRunner().invoke(cli.say_rules)
    assert result.exit_code == 0
    assert not result.exception



