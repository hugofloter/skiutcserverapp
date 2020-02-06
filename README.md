# Rest API of SKI'UTC application

<p align="center">
  <img width="400" height="150" src="https://raw.githubusercontent.com/ski-utc/skiutnativeapp/master/assets/images/logo.png">
</p>

This repository contains the rest API of the SKI'UTC application (https://github.com/ski-utc/skiutnativeapp)

API using Python 3.6.8 and bottle.py

<p align="center">
  <img width="460" height="200" src="https://bottlepy.org/docs/dev/_static/logo_nav.png">
</p>

Table of Contents
=================
  * [Architecture](#architecture)
  * [Documentation](#documentation)
    * [User](#user)
    * [News](#news)
    * [Potin](#potin)
    * [Group](#group)
    * [Animation](#animation)
    * [Bot](#bot)
  * [Models](#models)
    * [User](#user)
    * [News](#news)
    * [Potin](#potin)
    * [Group](#group)
    * [UserGroup](#usergroup)
    * [AnimationUser](#animationuser)
    * [AnimationKey](#animationkey)
    * [BotUser](#botuser)
  * [Authors](#authors)
  * [Licence](#licence)
  
Architecture
======

This Restful API follow a MV model (Model-View). `app.py` file is located at the root of the project and includes all of webapis contents (1 file per module).
Each module has its own folder that holds the model and the view.
```
.
│   README.md
│   app.py    
│
└── webapis
│   │   user.py
│   │   news.py
│   │   potin.py
│   │   group.py
│   │   animation.py
│   │   bot.py
│   
└── user
│   │   model.py
│   │   view.py
.   .
.   .
```

Documentation
======

## **User**

Module that handle all user's operation (authentication, modification, upload, ...)

- authentication
- retrieval
- profile picture upload
- modification

### *Route : /v1/authenticate*

- / : route for authentication
    
### POST
#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| login  | String | Yes | login of the user you want to connect |
| password  | String | Yes | password of the user you want to connect |
| token  | String | No | token to check whether user is already authenticated |

#### Returns
```{json}
{
 "user": <user_object>,
 "token": token,
}
```

### *Routes : /v1/users*

- / : route for users info

### GET @authenticate

Get list of user object. Selection might be shrunk if query parameter is passed

#### Parameters

| Parameter | Type | Mandatory  | Description |
|---|---|---|---|
| query  | String | No | query to get a thinner search on user list |

#### Returns
```{json}
{
 1: <user_object>,
 2: <user_object>,
 ...
}
```

### PUT @authenticate

You can change change user's information here : 
- password
- profile picture
- location

#### Parameters

| Parameter | Type | Mandatory  | Description |
|---|---|---|---|
| password  | String | No | old password |
| new_password | String | No | new password |
| location  | Object | No | new (latitude,longitude) couple coordinate |
| img_url  | String | No | url of the new profile picture of the user |

#### Returns
```{json}
{
    <user_object>
}
```

- /images : route for uploading image profile

### POST @authenticate
#### Parameters

| Parameter | Type | Mandatory  | Description |
|---|---|---|---|
| image  | Multipart File | Yes | image file to be the new profile picture of the user |

#### Returns
```{json}
{
    "img_url": img_url
}
```

## **News**

Module that manipulates news on the database

- retrieval
- creation
- deletion
- modification
- photos upload

### *Route : /v1/news*

- / : route for news handling
    
### GET @authenticate

List all news as json object

#### Returns
```{json}
{
 0: <news_object>,
 1: <news_object>,
 ...
}
```
    
### POST @admin

Create a news, admin status is needed

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| title  | String | Yes | title of the news |
| text  | String | Yes | content of the news |

#### Returns
```{json}
{
 <news_object>
}
```

- /<id> : route for handling a specific news

### GET @authenticate

Get a specific news

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the news |

#### Returns
```{json}
{
 <news_object>
}
```

### DELETE @admin

Delete a specific news, admin status id needed

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the news |

#### Returns
```{json}
{
 0: <news_object>,
 1: <news_object>,
 ...
}
```

- /images : route for uploading news image

### POST @admin

Add an image linked to a specific news, admin status id needed

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| image  | Multipart File | Yes | image file to be the linked to the news |

#### Returns
```{json}
{
    "img_url": img_url
}
```

## **Potin**

Module that manipulates gossips on the database

- retrieval
- creation
- deletion
- modification

### *Route : /v1/potins*

- / : route for potins handling
    
### GET @authenticate

List all valid potins as json object

#### Returns
```{json}
{
 0: <potin_object>,
 1: <potin_object>,
 ...
}
```

### POST @authenticate

Create a potin

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| title  | String | Yes | title of the potin |
| text  | String | Yes | content of the potin |
| isAnonymous  | boolean | Yes | if gossip is anonymous or not |


#### Returns
```{json}
{
 <potin_object>
}
```

- /<id> : route for handling a specific valid potin

### GET @authenticate

Get a specific valid potin

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the potin |

#### Returns
```{json}
{
 <potin_object>
}
```

- /admin : route for administrating potins

### GET @admin

Get all potins in await of validation, admin status is needed

#### Returns
```{json}
{
 0: <potin_object>,
 1: <potin_object>,
 ...
}
```

- /admin/<id> : route for validate or delete potins as admin

### DELETE @admin

Delete a specific potin in await of validation, admin status is needed

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the potin |

#### Returns
```{json}
{
 0: <potin_object>,
 1: <potin_object>,
 ...
}
```

### PUT @admin

Validate a specific potin that has not been yet accepted, admin status is needed

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the potin |

#### Returns
```{json}
{
 <potin_object>
}
```

## **Group**

Module that manipulates groups on the database

- retrieval
- creation
- deletion
- modification
- send notification to group
- allow location

### *Route : /v1/groups*

- / : route for groups information
    
### GET @authenticate

Lists all groups to which the user belongs

#### Returns
```{json}
{
 0: <group_object>,
 1: <group_object>,
 ...
}
```

### POST @authenticate

Create a group, and send notification to added users if they are

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| name  | String | Yes | name of the group |
| list_login  | Array | No | list of login to add to the group |

#### Returns
```{json}
{
 <group_object>
}
```

- /<id> : route for manipulating a specific group

### GET @authenticate

Get a specific group and its list of users. 
User must belong to the group

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the group |

#### Returns

```{json}
{
 <group_object>,
 "users": {
         0: <user_object>,
         1: <user_object>,
         ...    
 },
 "share_position": bool
}
//share_position : whether user allows sharing his postition
```

### DELETE @authenticate

Delete a specific group.
User must be owner of this group

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the group |

#### Returns
```{json}
{
 0: <group_object>,
 1: <group_object>,
 ...
}
```

### PUT @authenticate

Operation on a specific group 
- accept/reject invitation
- send notification
- location permission
- adding user to group
- remove someone from group (User must be owner)

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| id  | Integer | Yes | id of the potin |
| invitation  | String | No | handle invitation of user (accept, reject) |
| beer_call  | Boolean | No | send a specific notification to all user that belongs to the group |
| title  | String | No (Yes if beer_call) | title of the notification to be sent |
| message  | String | No (Yes if beer_call) | message of the notification to be sent |
| location_permission  | Boolean | No | change permission to locate user within the group |
| list_login  | Array | No | list of login to invite to group |
| to_remove  | String | No | login to remove from the group |

#### Returns
```{json}
{
 <group_object>,
 "users": {
         0: <user_object>,
         1: <user_object>,
         ...    
 },
 "share_position": bool
}
//share_position : whether user allows sharing his postition
```

## **Animation**

Module that manipulates groups on the database

- retrieval
- creation
- deletion
- modification
- send notification to group
- allow location

### *Route : /v1/animation*

- / : route for animation information
    
### GET @authenticate

Get current user level

#### Returns
```{json}
{
 0: user_level
}
```

- /<key> : route for managing level of animation for a user

### GET @authenticate

Unlock a new level for the user

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| key  | String | Yes | key of the animation to unlock new level |

#### Returns
```{json}
{
 user_level
}
```

- /admin : route for leaderboard of animation

### GET @admin

Get leaderboard by desc level

#### Returns
```{json}
{
 0: <useranimation_object>,
 1: <useranimation_object>,
 ...    
}
```

## **Bot**

Module that handles facebook bot

### *Route : /v1/webhook*

- / : route for bot handling messages
    
### GET

Verification of the token

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| hub.verify_token  | String | Yes | token verification |
| hub.challenge  | String | Yes | challenge |

#### Returns
```{json}
{
 challenge
}
```

### POST

Handling message of user to bot.
Payload has "entry" parameters and is an array of entry received by bot. Each entry has the following : 

- 'messaging' = webhook event
- 'sender' = fb object of the sender
- 'recipient' = recipient object of the page
- 'timestamp' = date received

messaging can be of type : 
- message (in which we can handle the message)
- postback (eg. button callback or so on...)

#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| payload  | Object | Yes | object received by fb api |

#### Returns
```{json}
'EVENT_RECEIVED'
```

### *Route : /v1/link_account*

- / : route for linking his fb account to fb bot

### POST
#### Parameters

| Parameter | Type| Mandatory  | Description |
|---|---|---|---|
| login  | String | Yes | login of the user you want to connect |
| password  | String | Yes | password of the user you want to connect |
| token  | String | Yes | token to check whether user is already linked |

#### Returns
```{json}
{
 <user_object>
}
```

Models
======

## **User**
```{json}
{
    'login': self.login,
    'lastname': self.lastname,
    'firstname': self.firstname,
    'email': self.email,
    'isAdmin': self.is_admin,
    'avatar': self.avatar
}
```

## **News**
```{json}
{
    'id': self.id,
    'title': self.title,
    'img_url': self.img_url,
    'img_width': self.img_width,
    'img_height': self.img_height,
    'date': self.date,
    'text': self.text,
    'type': self.type,
}
```

## **Potin**
```{json}
{
    'id': self.id,
    'title': self.title,
    'text': self.text,
    'approved': self.approved,
    'sender': self.sender,
    'isAnonymous': self.isAnonymous
}
```

## **Group**
```{json}
{
    'id': self.id,
    'name': self.name,
    'owner': self.owner,
    'beer_call': self.beer_call
}
```

## **UserGroup**
```{json}
{
    'login_user': self.login_user,
    'id_group': self.id_group,
    'status': self.status,
    'share_position': self.share_position,
    'expiration_date': self.expiration_date
}
```

## **AnimationUser**
```{json}
{
    'login_user': self.login_user,
    'level': self.level
}
```


## **AnimationKey**
```{json}
{
    'key': self.key,
    'level': self.level,
    'next_indice': self.next_indice
}
```


## **BotUser**
```{json}
{
    'fb_id': self.fb_id,
    'login': self.login,
    'token': self.token,
    'last_action': self.last_action
}
```

Authors
=======
* **[PAIGNEAU Hugo](https://github.com/hugofloter)** - *Initial work*
* **[RICHARD Quentin](https://github.com/qprichard)** - *Initial work*
* **[LEBRE Clément](https://github.com/clebre)** - *Initial work*

Licence
=======

Cette application est soumise à la licence [Beerware](http://fr.wikipedia.org/wiki/Beerware).
