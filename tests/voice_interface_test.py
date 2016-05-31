from tod import voice_interface
import mock


def test_session_ended_request_handler():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "requestId": "EdwRequestId.1234",
            "timestamp": "2016-05-27T05:55:21Z",
            "type": "SessionEndedRequest"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)

    assert response['response']['outputSpeech']['text'] == voice_interface.END_SPEECH


def test_session_ended_intent():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "AMAZON.CancelIntent",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)

    assert response['response']['outputSpeech']['text'] == voice_interface.END_SPEECH


def test_unknown_intent():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "UnknownIntent",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)

    assert response['response']['outputSpeech']['text'] == voice_interface.DEFAULT_SPEECH


def test_launch_request_route_to_welcome():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": True
        },
        "request": {
            "requestId": "EdwRequestId.1234",
            "timestamp": "2016-05-27T05:55:21Z",
            "type": "LaunchRequest"

        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)

    assert response['response']['outputSpeech']['text'] == voice_interface.WELCOME_SPEECH


def test_default_handler():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "requestId": "EdwRequestId.1234",
            "timestamp": "2016-05-27T05:55:21Z",
            "type": "UnknownRequest"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.DEFAULT_SPEECH


def test_help_intent_handler():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "AMAZON.HelpIntent",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.HELP_SPEECH


def test_launch_request_handler():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "LaunchRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.WELCOME_SPEECH


def test_get_rules_intent_handler():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetRules",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.RULES_SPEECH


def test_set_category_intent_handler():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "SetTodCategory",
                "slots": {
                    "Category": {
                        "name": "Category",
                        "value": "family game night"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "We'll now play with questions from the category family " \
                                                           "game night. You can ask me a truth or a dare question " \
                                                           "by saying, give me a truth question, or give me a dare."


def test_set_category_intent_handler_empty_slots():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "SetTodCategory",
                "slots": {}
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "I'm not sure of which category you want to play. " \
                                                           "Please try again."


def test_set_category_intent_handler_slot_without_value():
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "SetTodCategory",
                "slots": {
                    "Category": {
                        "name": "Category"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "I'm not sure of which category you want to play. " \
                                                           "Please try again."


@mock.patch('tod.model.Model.get_questions_of_type_and_category')
def test_get_truth_or_dare_question_with_empty_session_attributes(get_questions_of_type_and_category):
    get_questions_of_type_and_category.return_value = [
        (1, "dare question 1", "dare", 6),
        (2, "dare question 2", "dare", 6),
        (3, "dare question 3", "dare", 6),
    ]
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTruthOrDare",
                "slots": {
                    "Category": {
                        "name": "Category",
                        "value": "family game night"
                    },
                    "Type": {
                        "name": "Type",
                        "value": "dare"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.account.1234"
            }
        }
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "dare question 1"


@mock.patch('tod.model.Model.get_questions_of_type_and_category')
def test_get_truth_or_dare_question_with_category_in_session_not_slot(get_questions_of_type_and_category):
    get_questions_of_type_and_category.return_value = [
        (1, "dare question 1", "dare", 6),
        (2, "dare question 2", "dare", 6),
        (3, "dare question 3", "dare", 6),
    ]
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTruthOrDare",
                "slots": {
                    "Type": {
                        "name": "Type",
                        "value": "dare"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "attributes": {"category": "family game night"},
            "user": {
                "userId": "amzn1.account.1234"
            }
        }
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "dare question 1"


@mock.patch('tod.model.Model.get_questions_of_type_and_category')
def test_get_truth_or_dare_question_without_category(get_questions_of_type_and_category):
    get_questions_of_type_and_category.return_value = [
        (1, "dare question 1", "dare", 6),
        (2, "dare question 2", "dare", 6),
        (3, "dare question 3", "dare", 6),
    ]
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTruthOrDare",
                "slots": {
                    "Type": {
                        "name": "Type",
                        "value": "dare"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.account.1234"
            }
        }
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "I'm not sure which category you want to play. " \
                                                           "Please try again."


@mock.patch('tod.model.Model.get_questions_of_type_and_category')
def test_get_truth_or_dare_question_with_session_attributes(get_questions_of_type_and_category):
    get_questions_of_type_and_category.return_value = [
        (1, "truth question 1", "truth", 6),
        (2, "truth question 2", "truth", 6),
        (3, "truth question 3", "truth", 6),
    ]
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTruthOrDare",
                "slots": {
                    "Category": {
                        "name": "Category",
                        "value": "family game night"
                    },
                    "Type": {
                        "name": "Type",
                        "value": "truth"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "attributes": {
                'category': 'family game night',
                'dare_index': 1,
                'truth_index': 2
            },
            "user": {
                "userId": "amzn1.account.1234"
            }
        }
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "truth question 3"
    assert response['sessionAttributes'] == {'category': 'family game night', 'dare_index': 1, 'truth_index': 3}


@mock.patch('tod.model.Model.get_questions_of_type_and_category')
def test_get_truth_or_dare_question_category_completed(get_questions_of_type_and_category):
    get_questions_of_type_and_category.return_value = [
        (1, "truth question 1", "truth", 6),
        (2, "truth question 2", "truth", 6),
        (3, "truth question 3", "truth", 6),
    ]
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTruthOrDare",
                "slots": {
                    "Category": {
                        "name": "Category",
                        "value": "family game night"
                    },
                    "Type": {
                        "name": "Type",
                        "value": "truth"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "attributes": {
                'category': 'family game night',
                'truth_index': 3
            },
            "user": {
                "userId": "amzn1.account.1234"
            }
        }
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "Congratulations! You completed the category family " \
                                                           "game night. " \
                                                           "If you want to hear the list of categories again, " \
                                                           "say: give me the categories."
    assert response['sessionAttributes'] == {}


@mock.patch('tod.model.Model.get_questions_of_type_and_category')
def test_get_truth_or_dare_question_without_type(get_questions_of_type_and_category):
    get_questions_of_type_and_category.return_value = [
        (1, "dare question 1", "dare", 6),
        (2, "dare question 2", "dare", 6),
        (3, "dare question 3", "dare", 6),
    ]
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTruthOrDare",
                "slots": {
                    "Category": {
                        "name": "Category",
                        "value": "family game night"
                    }
                }
            },
            "locale": "en-US"
        },
        "version": "1.0",
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.account.1234"
            }
        }
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == "I'm not sure if you asked for a truth or a dare. " \
                                                           "Please try again."


@mock.patch('tod.model.Model.get_all_categories')
def test_get_categories_intent_handler(get_all_categories):
    category1 = "category1"
    category2 = "category2"
    category3 = "category3"
    get_all_categories.return_value = [(category1,), (category2,), (category3,)]
    request = {
        "session": {
            "sessionId": "SessionId.1234",
            "application": {
                "applicationId": "amzn1.echo-sdk-ams.app.1234"
            },
            "user": {
                "userId": "amzn1.ask.account.1234"
            },
            "new": False
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "GetTodCategories",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == (
        category1 + ". " + category2 + ". " + category3 + ". Please tell me the category you want to play by saying, "
                                                          "play category kids, for example.")





