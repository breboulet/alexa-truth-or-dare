import pkg_resources
from tod import model


TOD_MODEL = model.Model()
TOD_MODEL.populate_from_json(pkg_resources.resource_filename("resources", "tods.json"))
WELCOME_SPEECH = "Welcome to the Truth or Dare game. " \
                 "If you want to hear the game rules, say: give me the rules. " \
                 "If you want me to list the different categories, say: give me the categories."
WELCOME_REPROMPT = "If you want to hear the game rules, say: give me the rules. " \
                   "If you want me to list the different categories, say: give me the categories."
END_SPEECH = "Thank you for trying the Truth or Dare game. Have a nice day!"
DEFAULT_SPEECH = "Just Ask"
RULES_SPEECH = "In the game of Truth or Dare each participant has the choice in whether they would like to complete " \
               "a challenge, or express a truth. Dares are challenges that must be completed by the participant that " \
               "they were given to. If a dare is not completed, there will be a penalty that will be decided by all " \
               "participants in the game. For example, if someone refuses to do a dare, the group may decide that " \
               "player cannot blink until next round.  If a participant chooses Truth, he or she must answer the " \
               "given question truthfully. The players may decide if there were will be limited or unlimited amount " \
               "of truths for each player. In the game of Truth or Dare, it is no fun if people pick truth every " \
               "single time."
HELP_SPEECH = "Here are some things you can say: give me the categories, give me the rules, give me a dare from the " \
              "category kids, play category kids. You can also say, stop, if you're done. So, how can I help?"


def lambda_handler(event, context=None):
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
    else:
        return default_handler(event['request'], event['session'])


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId'] +
          ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return launch_request_handler(launch_request, session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "AMAZON.HelpIntent":
        return help_intent_handler(intent, session)
    elif intent_name == "SetTodCategory":
        return set_category_intent_handler(intent, session)
    elif intent_name == "GetRules":
        return get_rules_intent_handler(intent, session)
    elif intent_name == "GetTodCategories":
        return get_categories_intent_handler(intent, session)
    elif intent_name == "GetTruthOrDare":
        return get_truth_or_dare_question_intent_handler(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return session_ended_request_handler(intent, session)
    else:
        return default_handler(intent, session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return session_ended_request_handler(session_ended_request, session)


# --------------- Functions that control the skill's behavior ------------------


def session_ended_request_handler(intent, session):
    return build_response(session.get('attributes', {}),
                          build_speechlet_response("Session Ended", END_SPEECH, None, True))


def default_handler(intent, session):
    return build_response(session.get('attributes', {}),
                          build_speechlet_response("Unknown Intent", DEFAULT_SPEECH, None, True))


def help_intent_handler(intent, session):
    return build_response(session.get('attributes', {}),
                          build_speechlet_response("Help", HELP_SPEECH, None, False))


def launch_request_handler(intent, session):
    return get_welcome_response(intent, session)


def get_welcome_response(intent, session):
    return build_response(session.get('attributes', {}),
                          build_speechlet_response("Welcome", WELCOME_SPEECH, WELCOME_REPROMPT, False))


def set_category_intent_handler(intent, session):
    """ Sets the category in the session and prepares the speech to reply to the user. """
    session_attributes = session.get('attributes', {})
    if session_attributes is None:  # fix crash on AWS lambda
        session_attributes = {}
    if 'Category' in intent['slots'] and 'value' in intent['slots']['Category']:
        category = intent['slots']['Category']['value']
        session_attributes['category'] = category
        speech_output = "We'll now play with questions from the category " + category + ". " + \
                        "You can ask me a truth or a dare question by saying, " \
                        "give me a truth question, or give me a dare."
        reprompt_text = "You can ask me a truth or a dare question by saying, " \
                        "give me a truth question, or give me a dare."
    else:
        speech_output = "I'm not sure of which category you want to play. " \
                        "Please try again."
        reprompt_text = "I'm not sure of which category you want to play. " \
                        "Please tell me the category you want to play by saying, " \
                        "play category kids, for example."
    return build_response(session_attributes,
                          build_speechlet_response("Set Category", speech_output, reprompt_text, False))


def get_truth_or_dare_question_intent_handler(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    if session_attributes is None:  # fix crash on AWS lambda
        session_attributes = {}
    slots = intent.get('slots', {})
    if 'Type' in slots:
        category = None
        if 'Category' in slots and 'value' in slots['Category']:
            category = slots['Category']['value']
        elif 'category' in session_attributes:
            category = session_attributes['category']

        if category:
            truth_or_dare = slots['Type']['value']
            questions = TOD_MODEL.get_questions_of_type_and_category(truth_or_dare,
                                                                     TOD_MODEL.get_category_id(category))
            index_key = truth_or_dare + '_index'
            if index_key in session_attributes:
                index = session_attributes[index_key]
            else:
                index = 0
            if index < len(questions):
                speech_output = questions[index][1]
                index += 1
                session_attributes['category'] = category
                session_attributes[index_key] = index
                speech_output += " Now tell me, do you want a Truth or a Dare?"
            else:
                speech_output = "Congratulations! You completed the category " + category + ". If you want to hear " \
                                                                                            "the list of categories " \
                                                                                            "again, say: give me " \
                                                                                            "the categories."
                session_attributes = {}
                should_end_session = True
            reprompt_text = None
        else:
            speech_output = "I'm not sure which category you want to play. " \
                            "Please try again."
            reprompt_text = "I'm not sure which category you want to play. " \
                            "Please tell me the category you want to play by saying, " \
                            "play category kids, for example."
            should_end_session = True
    else:
        speech_output = "I'm not sure if you asked for a truth or a dare. " \
                        "Please try again."
        reprompt_text = "I'm not sure if you asked for a truth or a dare. " \
                        "You can ask me a truth or a dare question by saying, " \
                        "give me a truth question, or give me a dare"
    return build_response(session_attributes,
                          build_speechlet_response("GetTruthOrDare", speech_output, reprompt_text, should_end_session))


def get_rules_intent_handler(intent, session):
    return build_response(session.get('attributes', {}),
                          build_speechlet_response("Rules", RULES_SPEECH, None, False))


def get_categories_intent_handler(intent, session):
    """ Gets the list of categories and asks the user to choose one. """

    categories = ""
    for category in TOD_MODEL.get_all_categories():
        categories += category[0] + '. '

    speech_output = "The available categories are: " + categories + "Please tell me the category you want to play by " \
                                                                    "saying, play category kids, for example."
    reprompt_text = "Please tell me the category you want to play by saying, " \
                    "play category kids, for example." \
                    "If you want to hear the different categories again, say: give me the categories."
    return build_response(session.get('attributes', {}),
                          build_speechlet_response("GetTodCategories", speech_output, reprompt_text, False))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
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


