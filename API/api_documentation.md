# QnA API Documentation

## Questions

#### GET /questions/latest

Returns list of latest questions filtered by: amount, tag.

#### GET /questions/hottest

Returns list of hottest questions filtered by: amount, tag.

##### parameters

* __amount__: filters by amount, default = 10
* __tags__: filters by tags, default = [none]

JSON example:

	{
        "questions": [
            {
                "id": int,
                "topic": string,
                "content": string,
                "tags": [string, string, ...],
                "votesUp": int,
                "votesDown": int,
                "date": timestamp,
                "user": {
                	"userId": int,
                	"username": string,
                	"avatar": url
                },
                "comments": [
                	{
                		"userId": int,
                		"username": string,
                		"content": string,
                		"date": timestamp
                	},
                	{ ... }
                ],
                "answers": [
                	{
                		"id": int,
                		"content": string,
                		"userId": int,
                		"username": string,
                		"date": timestamp,
                        "votesUp": int,
                        "votesDown": int,
                		"comments": [
                			{
                				"userId": int,
                				"username": string,
                				"content": string,
                				"date": timestamp
                			},
                			{ ... }
                		]
                	},
                	{ ... }
                ]
            },
            { ... }
        ]
    }

#### POST /questions

Saves question to database.

	{
		"topic": string,
		"content": string,
		"userId": int,
		"tags": [string, string, ...]
	}

## Answers

#### POST /answers

Saves answer to database.

	{
		"questionId": int,
		"content": string,
		"userId": int
	}

## Comments

#### POST /comments

Saves comment to database.

	{
		"content": string,
		"username": string,
		"userId": int,
		"messageId": int
	}

