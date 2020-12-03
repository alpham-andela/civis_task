# HubSpot ETL

The purpose of this project is to demonestrate my skils with bonobo etl framework as part of intervewing with CIVIS Analytics team.

![HubSpot ETL Graph](graph.png "HubSpot ETL Graph")

## Getting started

### Direct installation

You will need to install the dependencies listed in `requirements.txt` using the following command line:

```bash
$ python -m pip install -r requirements.txt
```

That's it, you now have an environment that's ready to go...

#### Start the ETL

Just run the ETL module `hubspot_etl.py`

```bash
$ python ./hubspot_etl.py
```

#### Run the tests

We use `pytest` for testing the transformation functions, to run the tests:

```bash
$ python -m pytest tests.py
```

### Docker container installation

To build the docker image you need to run the following command:

```bash
$ docker build -t hubspot_etl:0.1 .
```

This will build a docker image that we can use in the followng steps.

#### Start the ETL inside docker container

Use `docker run` command for that:

```bash
$ docker run -it --rm --name hubspot_etl_container -v $(pwd)/results:/usr/src/app/results hubspot_etl:0.1
```

That command will run the ETL and leave the results in your current working direcotry in a new directory called `./results/`

To save the logs you can mount log file as a volume to the contianer as follows:

```bash
$ docker run -it --rm --name hubspot_etl_container -v $(pwd)/results:/usr/src/app/results -v $(pwd)/logs/:/usr/src/app/logs hubspot_etl:0.1
```

#### Run the tests inside docker container

You can run the tests inside a docker container as follows:
```bash
$ docker run -it --rm --name hubspot_etl_tests_container -v $(pwd)/logs/:/usr/src/app/logs hubspot_etl:0.1 python -m pytest tests.py
```

#### Development inside docker container

For that topic, I'll refer to [VSCode documentation](https://code.visualstudio.com/docs/remote/attach-container#:~:text=To%20attach%20to%20a%20Docker,you%20want%20to%20connect%20to.) but will add one hint to that.
To keep the docker container running all the time until you stop/kill it manually you can run `bash` command with `-i` and `-t` options to keep it running, and `-d` option to run in the background (daemonize the container):
```bash
$ docker run -it -d --name hubspot_etl_dev_env -v $(pwd)/:/usr/src/app hubspot_etl:0.1 bash
1d8b43f852e7780c7a6ac8b19851592a08f4fd82e4c1bcf54582158743f7685a
```

And when you list docker containers:
```bash
$ docker ps |grep hubspot_etl_dev_env
1d8b43f852e7        hubspot_etl:0.1             "bash"                   35 seconds ago      Up 34 seconds                                                                  hubspot_etl_dev_env
```

You can then use that container as a development environment, and when you finish don't forget to stop/kill it.
```bash
$ docker kill  hubspot_etl_dev_env
hubspot_etl_dev_env
```

And that's all folks ;)
