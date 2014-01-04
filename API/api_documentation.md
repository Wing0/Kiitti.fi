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
                "votes_up": int,
                "votes_down": int,
                "date": timestamp,
                "user": {
                	"user_id": int,
                	"username": string,
                	"avatar": url
                },
                "comments": [
                	{
                		"user_id": int,
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
                		"user_id": int,
                		"username": string,
                		"date": timestamp,
                		"comments": [
                			{
                				"user_id": int,
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
		"user_id": int,
		"tags": [string, string, ...]
	}
	
## Answers
	
#### POST /answers

Saves answer to database.

	{
		"question_id": int,
		"content": string,
		"user_id": int
	}
	
## Comments

#### POST /comments

Saves comment to database.

	{
		"content": string,
		"username": string,
		"user_id": int,
		"message_id": int
	}
	
