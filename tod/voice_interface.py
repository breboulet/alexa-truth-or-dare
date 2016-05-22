import click
import pkg_resources
from tod import model


tod_model = model.Model()
tod_model.populate_from_json(pkg_resources.resource_filename("resources", "tods.json"))


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId'] +
          ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "SetTodCategory":
        return set_category(intent, session)
    elif intent_name == "GetTodCategories":
        return get_categories()
    elif intent_name == "GetRules":
        return get_rules()
    elif intent_name == "GetTruthOrDare":
        return get_truth_or_dare_question(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Truth or Dare game. " \
                    "If you want to hear the game rules, say: give me the rules." \
                    "If you want me to list the different categories, say: give me the categories."

    reprompt_text = "If you want to hear the game rules, say: give me the rules." \
                    "If you want me to list the different categories, say: give me the categories."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Truth or Dare game. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_category(intent, session):
    """ Sets the category in the session and prepares the speech to reply to the user. """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Category' in intent['slots']:
        category = intent['slots']['Category']['value']
        session_attributes = {"category": category}
        speech_output = "We'll now play with questions from the category " + category + ". " + \
                        "You can ask me a truth or a dare question by saying, " \
                        "give me a truth question, or give me a dare"
        reprompt_text = "You can ask me a truth or a dare question by saying, " \
                        "give me a truth question, or give me a dare"
    else:
        speech_output = "I'm not sure of which category you want to play. " \
                        "Please try again."
        reprompt_text = "I'm not sure of which category you want to play. " \
                        "Please tell me the category you want to play by saying, " \
                        "play category kids."
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_truth_or_dare_question(intent, session):
    card_title = intent['name']
    session_attributes = session['attributes']
    should_end_session = False

    if 'Type' in intent['slots']:
        category = None
        if 'Category' in intent['slots']:
            category = intent['slots']['Category']['value']
        elif 'category' in session['attributes']:
            category = session_attributes['category']

        if category:
            truth_or_dare = intent['slots']['Type']['value']
            questions = tod_model.get_questions_of_type_and_category(truth_or_dare,
                                                                     tod_model.get_category_id(category))
            if truth_or_dare in session_attributes:
                if 'cursor' in session_attributes[truth_or_dare]:
                    cursor = session_attributes[truth_or_dare]['cursor']
                else:
                    session_attributes[truth_or_dare]['cursor'] = 0
            else:
                pass
                # TODO
            cursor = 0 if session_attributes[truth_or_dare]['cursor'] is None \
                else session_attributes[truth_or_dare]['cursor']
            speech_output = questions[cursor]
            reprompt_text = None
            cursor += 1
            session_attributes['category'] = category
            session_attributes[truth_or_dare]['cursor'] = cursor
        else:
            speech_output = "I'm not sure which category you want to play. " \
                            "Please try again."
            reprompt_text = "I'm not sure which category you want to play. " \
                            "Please tell me the category you want to play by saying, " \
                            "play category kids."
    else:
        speech_output = "I'm not sure if you asked for a truth or a dare. " \
                        "Please try again."
        reprompt_text = "I'm not sure if you asked for a truth or a dare. " \
                        "You can ask me a truth or a dare question by saying, " \
                        "give me a truth question, or give me a dare"
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_rules():
    rules = "In the game of Truth or Dare each participant has the choice in whether they would like to complete " \
            "a challenge, or express a truth. Dares are challenges that must be completed by the participant that " \
            "they were given to. If a dare is not completed, there will be a penalty that will be decided by all " \
            "participants in the game. For example, if someone refuses to do a dare, the group may decide that " \
            "player cannot blink until next round.  If a participant chooses Truth, he or she must answer the given " \
            "question truthfully. The players may decide if there were will be limited or unlimited amount of " \
            "truths for each player. In the game of Truth or Dare, it is no fun if people pick truth every " \
            "single time."
    return build_response({}, build_speechlet_response("Rules", rules, None, False))


def get_categories():
    """ Gets the list of categories and asks the user to choose one. """

    categories = ""
    for category in tod_model.get_all_categories():
        categories += category[0] + '. '

    speech_output = categories + "Please tell me the category you want to play by saying, " \
                                 "play category kids."
    reprompt_text = "Please tell me the category you want to play by saying, " \
                    "play category kids." \
                    "If you want to hear the different categories again, say: give me the categories."
    return build_response({},
                          build_speechlet_response("List of Categories", speech_output, reprompt_text, False))


def prompt_category(categories):
    user_input = click.prompt("What category do you want to play?", hide_input=True)
    clean_user_input = user_input.strip().lower()
    if clean_user_input in categories.lower():
        play_category(user_input)
    else:
        apologize_and_exit()


def play_category(category_name):
    category_id = tod_model.get_category_id(category_name)
    if category_id is not None:
        click.echo("You're now playing in the category: " + category_name)
        prompt_truth_or_dare_in_category(category_id)
    else:
        apologize_and_exit()


def prompt_truth_or_dare_in_category(category_id, truth_cursor=0, dare_cursor=0):
    user_input = click.prompt("Now, Truth or Dare?", hide_input=True)
    clean_user_input = user_input.strip().lower()
    if clean_user_input in ["truth", "dare"]:
        say_question(category_id, user_input.strip().lower(), truth_cursor, dare_cursor)
    else:
        apologize_and_exit()


def prompt_truth_in_category(category_id, truth_cursor, dare_cursor):
    if click.confirm("Now, next Truth question?"):
        say_question(category_id, "truth", truth_cursor, dare_cursor)
    else:
        end_the_game()


def prompt_dare_in_category(category_id, truth_cursor, dare_cursor):
    if click.confirm("Now, next Dare question?"):
        say_question(category_id, "dare", truth_cursor, dare_cursor)
    else:
        end_the_game()


def say_question(category_id, truth_or_dare, truth_cursor, dare_cursor):
    questions = tod_model.get_questions_of_type_and_category(truth_or_dare, category_id)
    if truth_or_dare in "truth":
        if truth_cursor < len(questions):
            click.echo(questions[truth_cursor][1])
            truth_cursor += 1
        else:
            click.echo("Congratulations! You've heard all the Truth questions from this category!")
            if click.confirm("Do you want to play the remaining Dare questions?"):
                prompt_dare_in_category(category_id, truth_cursor, dare_cursor)
            else:
                end_the_game()
    else:
        if dare_cursor < len(questions):
            click.echo(questions[dare_cursor][1])
            dare_cursor += 1
        else:
            click.echo("Congratulations! You've heard all the Dare questions from this category!")
            if click.confirm("Do you want to play the remaining Truth questions?"):
                prompt_truth_in_category(category_id, truth_cursor, dare_cursor)
            else:
                end_the_game()
    prompt_truth_or_dare_in_category(category_id, truth_cursor, dare_cursor)


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

