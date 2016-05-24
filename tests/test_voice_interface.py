from tod import voice_interface


def test_get_welcome_response():
    expected_response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': 'Welcome to the Truth or Dare game. If you want to hear the game rules, say: give me the '
                        'rules.If you want me to list the different categories, say: give me the categories.',
                'type': 'PlainText'
            },
            'shouldEndSession': False,
            'reprompt': {
                'outputSpeech': {
                    'text': 'If you want to hear the game rules, say: give me the rules.If you want me to '
                            'list the different categories, say: give me the categories.',
                    'type': 'PlainText'
                }
            },
            'card': {
                'content': 'SessionSpeechlet - Welcome to the Truth or Dare game. If you want to hear the game '
                           'rules, say: give me the rules.If you want me to list the different categories, say: '
                           'give me the categories.',
                'type': 'Simple',
                'title': 'SessionSpeechlet - Welcome'
            }
        },
        'sessionAttributes': {}
    }
    response = voice_interface.get_welcome_response()
    assert response == expected_response


def test_handle_session_end_request():
    expected_response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': 'Thank you for trying the Truth or Dare game. Have a nice day! ',
                'type': 'PlainText'
            },
            'shouldEndSession': True,
            'reprompt': {
                'outputSpeech': {
                    'text': None,
                    'type': 'PlainText'
                }
            },
            'card': {
                'content': 'SessionSpeechlet - Thank you for trying the Truth or Dare game. Have a nice day! ',
                'type': 'Simple',
                'title': 'SessionSpeechlet - Session Ended'
            }
        },
        'sessionAttributes': {}
    }
    response = voice_interface.handle_session_end_request()
    assert response == expected_response


def test_get_rules():
    response = voice_interface.get_rules()
    expected_response = {
        'version': '1.0',
        'response': {
             'outputSpeech': {
                 'text': 'In the game of Truth or Dare each participant has the choice in whether '
                         'they would like to complete a challenge, or express a truth. Dares are '
                         'challenges that must be completed by the participant that they were given '
                         'to. If a dare is not completed, there will be a penalty that will be decided '
                         'by all participants in the game. For example, if someone refuses to do a '
                         'dare, the group may decide that player cannot blink until next round.  If '
                         'a participant chooses Truth, he or she must answer the given question '
                         'truthfully. The players may decide if there were will be limited or '
                         'unlimited amount of truths for each player. In the game of Truth or Dare, '
                         'it is no fun if people pick truth every single time.',
                 'type': 'PlainText'},
             'shouldEndSession': False,
             'reprompt': {
                 'outputSpeech': {
                    'text': None,
                    'type': 'PlainText'
                }
             }, 'card': {
                 'content': 'SessionSpeechlet - In the game of Truth or Dare each participant has '
                            'the choice in whether they would like to complete a challenge, or '
                            'express a truth. Dares are challenges that must be completed by the '
                            'participant that they were given to. If a dare is not completed, '
                            'there will be a penalty that will be decided by all participants '
                            'in the game. For example, if someone refuses to do a dare, the group '
                            'may decide that player cannot blink until next round.  If a '
                            'participant chooses Truth, he or she must answer the given question '
                            'truthfully. The players may decide if there were will be limited or '
                            'unlimited amount of truths for each player. In the game of Truth or Dare, '
                            'it is no fun if people pick truth every single time.',
                 'type': 'Simple',
                 'title': 'SessionSpeechlet - Rules'
             }
         },
        'sessionAttributes': {}
        }
    assert response == expected_response


def test_get_categories():
    expected_response = {
        'response': {
            'card': {
                'content': 'SessionSpeechlet - new couples. dirty and sexy. married couples. kids. college students. '
                           'family game night. teens. adults. Please tell me the category you want to play by saying, '
                           'play category kids.',
                'title': 'SessionSpeechlet - List of Categories',
                'type': 'Simple'
            },
            'outputSpeech': {
                'text': 'new couples. dirty and sexy. married couples. kids. college students. family game night. '
                        'teens. adults. Please tell me the category you want to play by saying, play category kids.',
                'type': 'PlainText'
            },
            'reprompt': {
                'outputSpeech': {
                    'text': 'Please tell me the category you want to play by saying, play category kids.If you want '
                            'to hear the different categories again, say: give me the categories.',
                    'type': 'PlainText'}},
            'shouldEndSession': False},
        'sessionAttributes': {},
        'version': '1.0'}
    response = voice_interface.get_categories()
    assert response == expected_response


def test_set_category():
    expected_response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': "We'll now play with questions from the category family game night. You can ask me a truth "
                        "or a dare question by saying, give me a truth question, or give me a dare",
                'type': 'PlainText'
            },
            'shouldEndSession': False,
            'reprompt': {
                'outputSpeech': {
                    'text': 'You can ask me a truth or a dare question by saying, give me a truth question, or '
                            'give me a dare',
                    'type': 'PlainText'
                }
            },
            'card': {
                'content': "SessionSpeechlet - We'll now play with questions from the category family game night. "
                           "You can ask me a truth or a dare question by saying, give me a truth question, or "
                           "give me a dare",
                'type': 'Simple',
                'title': 'SessionSpeechlet - SetTodCategory'
            }
        },
        'sessionAttributes': {
            'category': 'family game night'
        }
    }
    intent = {
        "name": "SetTodCategory",
        "slots": {
            "Category": {
                "name": "Category",
                "value": "family game night"
            }
        }
    }
    session = {
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
    response = voice_interface.set_category(intent, session)
    assert expected_response == response


def test_get_truth_or_dare_question_with_empty_session_attributes():
    intent = {
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
    }
    session = {
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
    expected_response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': "Put peanut butter on your nose, and try to to lick it off",
                'type': 'PlainText'
            },
            'shouldEndSession': False,
            'reprompt': {
                'outputSpeech': {
                    'text': None,
                    'type': 'PlainText'
                }
            },
            'card': {
                'content': "SessionSpeechlet - Put peanut butter on your nose, and try to to lick it off",
                'type': 'Simple',
                'title': 'SessionSpeechlet - GetTruthOrDare'
            }
        },
        'sessionAttributes': {
            'category': 'family game night',
            'dare_index': 1
        }
    }
    response = voice_interface.get_truth_or_dare_question(intent, session)
    assert response == expected_response


def test_get_truth_or_dare_question_with_session_attributes():
    intent = {
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
    }
    session = {
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
    expected_response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': "Have you ever snuck anyone into to the house?",
                'type': 'PlainText'
            },
            'shouldEndSession': False,
            'reprompt': {
                'outputSpeech': {
                    'text': None,
                    'type': 'PlainText'
                }
            },
            'card': {
                'content': "SessionSpeechlet - Have you ever snuck anyone into to the house?",
                'type': 'Simple',
                'title': 'SessionSpeechlet - GetTruthOrDare'
            }
        },
        'sessionAttributes': {
            'category': 'family game night',
            'dare_index': 1,
            'truth_index': 3
        }
    }
    response = voice_interface.get_truth_or_dare_question(intent, session)
    assert response == expected_response




