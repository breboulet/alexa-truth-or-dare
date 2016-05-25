from tod import voice_interface


def test_session_ended_request_handler():
    request = {
        "request": {
            "type": "SessionEndedRequest"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.END_SPEECH


def test_launch_request_route_to_welcome():
    request = {
        "request": {
            "type": "LaunchRequest"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)

    assert response['response']['outputSpeech']['text'] == voice_interface.WELCOME_SPEECH


def test_default_handler():
    request = {
        "request": {
            "type": "UnknownRequest"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.DEFAULT_SPEECH


def test_help_intent_handler():
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "AMAZON.Help",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.WELCOME_SPEECH


def test_launch_request_handler():
    request = {
        "request": {
            "type": "IntentRequest",
            "requestId": "1234",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
                "name": "AMAZON.Help",
            },
            "locale": "en-US"
        },
        "version": "1.0"
    }
    response = voice_interface.lambda_handler(request)
    assert response['response']['outputSpeech']['text'] == voice_interface.WELCOME_SPEECH


def test_get_rules_intent_handler():
    request = {
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


def test_get_truth_or_dare_question_with_empty_session_attributes():
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
    assert response['response']['outputSpeech']['text'] == "Put peanut butter on your nose, and try to to lick it off"


def test_get_truth_or_dare_question_with_session_attributes():
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
    assert response['response']['outputSpeech']['text'] == "Have you ever snuck anyone into to the house?"
    assert response['sessionAttributes'] == {'category': 'family game night', 'dare_index': 1, 'truth_index': 3}





