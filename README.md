# Welwick's Oracle
This is a bot for Mastodon that toots our your fortune, which you can see on [@welwick@uncontrollablegas.com](https://uncontrollablegas.com/@welwick). You can also use this as an example of how to write a basic bot written in Python that generates content for Mastodon.

## Getting Started
You can use this bot in two ways: (1) directly in Python or (2) using the Docker container.  But before you start, follow these steps to prepare Mastodon.

First, create an account on some Mastodon server. It doesn't matter which server you use.

Second, use the user interface to create an "Application". You need to set an application name and that is it. You can ignore all of the other fields. By default your bot can read and write its own timeline and modify followers. You don't need to grant anymore permissions beyond that to use this bot.

![List of applications](https://github.com/paullockaby/welwick/blob/main/docs/images/developer-link.png?raw=true)

![New application form](https://github.com/paullockaby/welwick/blob/main/docs/images/application-form.png?raw=true)

Once the application is created you can click on it from the Developer page and you'll see a "Client key", a "Client secret", and "Your access token". The only value that you need is your access token. Do not share this access token. It is a secret that lets you (or anyone who you may share it with) toot on your behalf.

### Using Python

This tool uses Poetry run so you may need to install Poetry and then set up Poetry, like this:

```
$ peotry install
```

After you've installed Poetry and used Poetry to install the dependencies, you can run the tool in a variety of ways.

```
# pass arguments
$ poetry run welwick --token=$API_TOKEN --api-url=https://yourmastodoninstance.com/

# pass arguments through stdin
$ echo $API_TOKEN | poetry run welwick --token-stdin --api-url=https://yourmastodoninstance.com/

# pass arguments through environment variables
$ API_TOKEN=yoursecrettoken API_URL=https://yourmastodoninstance.com/ poetry run welwick
```

### Using Docker

You can build the container like this:

```
$ make build
```

Or you can just use this container, like this:

```
# pass arguments
$ docker run --rm ghcr.io/paullockaby/welwick:latest --token=$API_TOKEN --api-url=https://yourmastodoninstance.com/

# pass arguments through environment variables
$ docker run --rm -e API_TOKEN=yoursecrettoken -e API_URL=https://yourmastodoninstance.com/ ghcr.io/paullockaby/welwick:latest
```

The tool will print out what fortune it generated and then post it to the account for which the token is valid.

## Development

In order to do development on this repository you must have [poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/) installed. For example, if you have Homebrew installed you can run this command:

```commandline
brew install poetry pre-commit
```

After installing these, clone this project and run this commands:

```commandline
make install
```

Running that will install the pre-commit hook and set up your poetry environment. Now you can begin development. Some common development commands:

```commandline
make test  # run all tests, perform static typing checks, and generate a coverage report
make pre-commit  # run pre-commit hooks (i.e. black, isort, and flake8) before committing
```
