import click
import pkg_resources
from tod import model


@click.group()
@click.option('--json_data_filename', default=pkg_resources.resource_filename("resources", "tods_test_sample.json"),
              help="The filename of the JSON file where the Truth or Dare questions are stored.")
@click.pass_context
def init(ctx, json_data_filename):
    tod_model = model.Model()
    tod_model.populate_from_json(json_data_filename)
    ctx.obj = tod_model


@click.command(help="Describes the rules of the Truth or Dare game.")
def say_rules():
    click.echo("In the game of Truth or Dare each participant has the choice in whether they would like to complete "
               "a challenge, or express a truth. Dares are challenges that must be completed by the participant that "
               "they were given to. If a dare is not completed, there will be a penalty that will be decided by all "
               "participants in the game. For example, if someone refuses to do a dare, the group may decide that "
               "player cannot blink until next round.  If a participant chooses Truth, he or she must answer the given "
               "question truthfully. The players may decide if there were will be limited or unlimited amount of "
               "truths for each player. In the game of Truth or Dare, it is no fun if people pick truth every "
               "single time. For an exciting game of Truth or Dare, 5 truths per person is recommended.")


@init.command(help="Lists all the Truth Or Dare Categories available.")
@click.pass_obj
def say_list_of_categories(tod_model):
    categories = ""
    for category in tod_model.get_all_categories():
        categories += category[0] + ', '
    categories += "All the Truth or Dare Questions."
    click.echo(categories)
    prompt_category(tod_model, categories)


def prompt_category(tod_model, categories):
    user_input = click.prompt("What category do you want to play?", hide_input=True)
    if user_input in categories:
        play_category(tod_model, user_input)
    else:
        apologize_and_exit()


@init.command(help="Play questions from the selected category")
@click.option('--category_name')
@click.pass_obj
def play_category(tod_model, category_name):
    category_id = tod_model.get_category_id(category_name)
    if category_id is not None:
        click.echo("You're now playing in the category: " + category_name)
        prompt_truth_or_dare_in_category(tod_model, category_id)
    else:
        apologize_and_exit()


def prompt_truth_or_dare_in_category(tod_model, category_id, truth_cursor=0, dare_cursor=0):
    user_input = click.prompt("Now, Truth or Dare?", hide_input=True)
    clean_user_input = user_input.strip().lower()
    if "truth" in clean_user_input:
        say_question(0, tod_model.get_questions_of_type_and_category("Truth", category_id))
    elif "dare" in clean_user_input:
        say_question(0, tod_model.get_questions_of_type_and_category("Dare", category_id))
    else:
        apologize_and_exit()

# Implement end of category exit condition
def say_question(tod_model, category_id, truth_or_dare, truth_cursor, dare_cursor):
    questions = tod_model.get_questions_of_type_and_category(truth_or_dare, category_id)
    if truth_or_dare in "Truth":
        click.echo(questions[truth_cursor][1])
        truth_cursor += 1
    elif truth_or_dare in "Dare":
        click.echo(questions[dare_cursor][1])
        dare_cursor += 1
    else:
        apologize_and_exit()
    prompt_truth_or_dare_in_category(tod_model, category_id, truth_cursor, dare_cursor)


def apologize_and_exit():
    click.echo("Sorry, I'm not sure I understood your request.")
    exit(0)

