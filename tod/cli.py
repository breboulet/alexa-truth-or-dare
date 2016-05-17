import click
import pkg_resources
from tod import model


class AppState(object):
    def __init__(self):
        self.todModel.populate_from_json(pkg_resources.resource_filename("resources", "tods_test_sample.json"))
    todModel = model.Model()
    currentCategoryId = None
    currentType = None


@click.group()
@click.pass_context
def main(ctx):
    """An Alexa skill to play Truth or Dare"""
    ctx.obj = AppState()
    click.echo("Welcome to the Truth Or Dare Game.")


@main.command(help="Describes the rules of the Truth or Dare game.")
def say_rules():
    click.echo("In the game of Truth or Dare each participant has the choice in whether they would like to complete "
               "a challenge, or express a truth. Dares are challenges that must be completed by the participant that "
               "they were given to. If a dare is not completed, there will be a penalty that will be decided by all "
               "participants in the game. For example, if someone refuses to do a dare, the group may decide that "
               "player cannot blink until next round.  If a participant chooses Truth, he or she must answer the given "
               "question truthfully. The players may decide if there were will be limited or unlimited amount of "
               "truths for each player. In the game of Truth or Dare, it is no fun if people pick truth every "
               "single time. For an exciting game of Truth or Dare, 5 truths per person is recommended.")


@main.command(help="Lists all the Truth Or Dare Categories available.")
@click.pass_obj
def say_list_of_categories(app_state):
    output_speech = ""
    for category in app_state.todModel.get_all_categories():
        output_speech += category[0] + ', '
    output_speech += "What category do you want to play with?"
    click.echo(output_speech)


@main.command(help="Go and ask questions from the selected category")
@click.option('--category_name')
@click.pass_obj
def set_current_category(app_state, category_name):
    app_state.currentCategoryId = app_state.todModel.get_category_id(category_name)
    if app_state.currentCategoryId is not None:
        click.echo("You're now in the category: " + category_name)
    else:
        apologize_and_exit()


def set_current_type(truth_or_dare):
    comparable_truth_or_dare = truth_or_dare.strip().lower()
    global currentType
    if comparable_truth_or_dare == "truth" or comparable_truth_or_dare == "dare":
        currentType = comparable_truth_or_dare
    else:
        apologize_and_exit()


def apologize_and_exit():
    click.echo("Sorry, I'm not sure I understood your request.")
    exit()

