[![Build Status](https://travis-ci.org/breboulet/alexa-truth-or-dare.svg?branch=master)](https://travis-ci.org/breboulet/alexa-truth-or-dare)
[![Coverage Status](https://coveralls.io/repos/github/breboulet/alexa-truth-or-dare/badge.svg?branch=master)](https://coveralls.io/github/breboulet/alexa-truth-or-dare?branch=master)

# Truth or Dare Unrated Alexa Skill

## Synopsis

An AWS Lambda function implementing an alexa skill to play the famous Truth or Dare Party Game with multiple categories.

## Motivation

This project started to participate in a live contest: Hey Alexa! The Amazon Alexa Skill Contest on [Hackster.io](https://www.hackster.io)
I did it mainly to learn new things and share what I learned with the community.

## Setup

To run this example skill you need to do two things. The first is to deploy the example code in lambda, and the second is to configure the Alexa skill to use Lambda.

### AWS Lambda Setup
1. Go to the AWS Console and click on the Lambda link. Note: ensure you are in us-east or you won't be able to use Alexa with Lambda.
2. Click on the Create a Lambda Function or Get Started Now button.
3. Skip the blueprint
4. Name the Lambda Function "truthOrDareUnrated".
5. Select the runtime as Pyhton
6. Edit the lambda.json file with your own AWS Lambda settings (see [lambda-uploader](https://github.com/rackerlabs/lambda-uploader) for more info)
7. In the root directory of the project execute: "lambda-uploader"
8. Set the Handler to "tod/voice_interface.lambda_handler".
9. Create a "Lambda Basic Execution" role and click create.
10. Leave the Advanced settings as the defaults.
11. Click "Next" and review the settings then click "Create Function"
12. Click the "Event Sources" tab and select "Add event source"
13. Set the Event Source type as Alexa Skills kit and Enable it now. Click Submit.
14. Copy the ARN from the top right to be used later in the Alexa Skill Setup.

### Alexa Skill Setup
1. Go to the [Alexa Console](https://developer.amazon.com/edw/home.html) and click Add a New Skill.
2. Set "TruthOrDareUnrated" for the skill name and "truth or dare unrated" as the invocation name, this is what is used to activate your skill. For example you would say: "Alexa, Ask truth or dare unrated to give me the categories."
3. Select the Lambda ARN for the skill Endpoint and paste the ARN copied from above. Click Next.
4. Copy the custom slot types from the customSlotTypes folder. Each file in the folder represents a new custom slot type. The name of the file is the name of the custom slot type, and the values in the file are the values for the custom slot.
5. Copy the Intent Schema from the included intent_schema.json.
6. Copy the Sample Utterances from the included utterances.txt. Click Next.
8. You are now able to start testing your sample skill! You should be able to go to the [Echo webpage](http://echo.amazon.com/#skills) and see your skill enabled.
9. In order to test it, try to say some of the Sample Utterances from the Examples section below.
10. Your skill is now saved and once you are finished testing you can continue to publish your skill.

## Examples
### Dialog model:
    User: "Alexa, open truth or dare unrated"
    Alexa: "Welcome to the Truth or Dare game. If you want to hear the game rules, say: give me the rules. If you want me to list the different categories, say: give me the categories."
    User: "Give me the categories"
    Alexa: "The available categories are: category1. category2. category3. Please tell me the category you want to play by saying, play category category2, for example."
    User: "Play category category2"
    Alexa: "We'll now play with questions from the category category2. You can ask me a truth or a dare question by saying, give me a truth question, or give me a dare."
    User: "Give me a dare"
    Alexa: "[Dare]"
    User: "Give me a truth question"
    Alexa: "[Truth question]"
    ...

### One-shot model:
    User: "Alexa, ask truth or dare unrated to give me a dare from the category kids."
    Alexa: "[Dare from category kids]"
    
## Tests

Simply run tox in the project folder:
```
tox -c tox.ini
```

## Contribution

Pull requests are more than welcome! 
Once merged, project is automatically build, packaged, and uploaded to the AWS Lambda. 
Which will end up updating the Alexa Skill people play with in one click!

## License

MIT

