# Rest In Tor (RIT)

A restful http services to create and manage socks5 proxies using the TOR network

## Installation

### Requirements
You must have [tor](https://github.com/torproject/tor) installed on the host machine.

### Installing dependencies
```shell
$ pipenv install --dev
```

## Running the project

```shell
$ pipenv shell
$ flask -app src run
```

## Running tests

```shell
$ pipenv run python -m tests
```

### Running a single test file

```shell
$ pipenv run python -m tests.proxy.test_routes  
```
