import pkg_resources
from ask import alexa
from tod import model


tod_model = model.Model()
tod_model.populate_from_json(pkg_resources.resource_filename("resources", "tods.json"))
WELCOME_SPEECH = "Welcome to the Truth or Dare game. " \
                 "If you want to hear the game rules, say: give me the rules." \
                 "If you want me to list the different categories, say: give me the categories."
WELCOME_REPROMPT = "If you want to hear the game rules, say: give me the rules." \
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


def lambda_handler(request_obj, context=None):
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    return alexa.route_request(request_obj)


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(END_SPEECH, end_session=True, card_obj=alexa.create_card("Session Ended"))


@alexa.default_handler()
def default_handler(request):
    return alexa.create_response(DEFAULT_SPEECH)


@alexa.intent_handler("AMAZON.Help")
def help_intent_handler(request):
    return get_welcome_response(request)


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return get_welcome_response(request)


def get_welcome_response(request):
    return alexa.create_response(WELCOME_SPEECH,
                                 end_session=False,
                                 card_obj=alexa.create_card("Welcome"),
                                 reprompt_message=WELCOME_REPROMPT)


@alexa.intent_handler('SetTodCategory')
def set_category_intent_handler(request):
    """ Sets the category in the session and prepares the speech to reply to the user. """
    if 'Category' in request.slots:
        category = request.slots['Category']
        request.session['category'] = category
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
                        "play category kids."
    return alexa.create_response(speech_output,
                                 end_session=False,
                                 card_obj=alexa.create_card(request.intent_name),
                                 reprompt_message=reprompt_text)


@alexa.intent_handler('GetTruthOrDare')
def get_truth_or_dare_question_intent_handler(request):
    if 'Type' in request.slots:
        category = None
        if 'Category' in request.slots:
            category = request.slots['Category']
        elif 'category' in request.session:
            category = request.session['category']

        if category:
            truth_or_dare = request.slots['Type']
            questions = tod_model.get_questions_of_type_and_category(truth_or_dare,
                                                                     tod_model.get_category_id(category))
            index_key = truth_or_dare + '_index'
            if index_key in request.session:
                index = request.session[index_key]
            else:
                index = 0
            if index < len(questions):
                speech_output = questions[index][1]
                index += 1
                request.session['category'] = category
                request.session[index_key] = index
            else:
                speech_output = "Congratulations! You completed the category " + category + ". If you want to hear " \
                                                                                            "the list of categories " \
                                                                                            "again, say: give me " \
                                                                                            "the categories."
                request.session = {}
            reprompt_text = None
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
    return alexa.create_response(speech_output,
                                 end_session=False,
                                 card_obj=alexa.create_card(request.intent_name),
                                 reprompt_message=reprompt_text)


@alexa.intent_handler('GetRules')
def get_rules_intent_handler(request):
    return alexa.create_response(RULES_SPEECH,
                                 end_session=False,
                                 card_obj=alexa.create_card("Rules"))


@alexa.intent_handler('GetTodCategories')
def get_categories_intent_handler(request):
    """ Gets the list of categories and asks the user to choose one. """

    categories = ""
    for category in tod_model.get_all_categories():
        categories += category[0] + '. '

    speech_output = categories + "Please tell me the category you want to play by saying, " \
                                 "play category kids."
    reprompt_text = "Please tell me the category you want to play by saying, " \
                    "play category kids." \
                    "If you want to hear the different categories again, say: give me the categories."
    return alexa.create_response(speech_output,
                                 end_session=False,
                                 card_obj=alexa.create_card("Rules"),
                                 reprompt_message=reprompt_text)


