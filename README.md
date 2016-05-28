[![Build Status](https://travis-ci.org/breboulet/alexa-truth-or-dare.svg?branch=master)](https://travis-ci.org/breboulet/alexa-truth-or-dare)
[![Coverage Status](https://coveralls.io/repos/github/breboulet/alexa-truth-or-dare/badge.svg?branch=master)](https://coveralls.io/github/breboulet/alexa-truth-or-dare?branch=master)

# Truth or Dare Unrated Alexa Skill

## Synopsis

An alexa skill to play the famous Truth or Dare Party Game with categories that ranges from Kids to Adults.
Party of 5? No! Party of 6 with Alexa! With Truth or Dare Unrated, let Alexa surprise you and share your secrets and adventures with your friends! This apps will bring fun to your most quiet evenings

## Motivation

This project started to participate in a live contest: Hey Alexa! The Amazon Alexa Skill Contest on [Hackster.io](https://www.hackster.io)
I did it mainly to learn new things and share what I learned with the community.

## How to use

1. Enable the skill in the Amazon Skills Section at alexa.amazon.com.
2. Say "Alexa, ask Truth or Dare Unrated" to your Amazon device that supports Alexa (Echo, FireOS, FireTV, etc.)
3. Alexa will prompt you with instructions on how to use Truth or Dare Unrated

Reading advice: [Getting started guide for the Alexa Skills Kit](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide)

## API: Examples of utterances to play with the skill:
```
  Alexa, ask Truth or Dare Unrated to give me the categories
  Alexa, ask Truth or Dare Unrated a dare from the category kids
  Alexa, ask Truth or Dare Unrated to give me the rules
```
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

