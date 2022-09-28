# Pasta Bot 🍝

> A inteligência artificial mais esparguete que existe

<p align="center">
    <img src="marta.png">
</p>

A Fediverse bot that automatically uploads all image posts on [ptchan](https://ptchan.org/) along with their text content.

## Useful links 

- [jschan documentation](http://fatchan.gitgud.site/jschan-docs/#introduction) 

## Roadmap

- Periodically update with new threads
- Handle large size files
- Handle editing
- Handle removing
- Handle formatting

## Set up

### Create an application

Start by creating a new application:

`POST https://pleroma.example/api/v1/apps`

#### Payload

```json
{
    "client_name": <CLIENT_NAME>,
    "redirect_uris": <REDIRECT_URIS>,
    "scopes": "read write follow push"
}
```

### Authorize

Authorize the application and obtain the code:

`GET https://pleroma.example/oauth/authorize`

#### Query

- `client_id`: `CLIENT_ID`
- `scope`: `read write follow push`
- `redirect_uri`: `<REDIRECT_URI>`
- `response_type`: `code`

### Credentials

Obtain the access token:

`POST https://pleroma.example/oauth/token`

#### Payload

```json
{
    "grant_type": "authorization_code",
    "client_id": <CLIENT_ID>,
    "client_secret": <CLIENT_SECRET>,
    "redirect_uri": <REDIRECT_URI>,
    "code": <CODE>,
    "scope": "read write follow push"
}
```

###  Fill `.env`

Create a copy of `.env.example` named `.env` and fill the variables with the respective values.
