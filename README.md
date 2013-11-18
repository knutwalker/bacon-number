bacon-number
============

Calculates the [Bacon Number](http://en.wikipedia.org/wiki/Bacon_number#Bacon_numbers) based upon the Neo4j example data

### Usage ###

You'll need to have [Neo4j](http://www.neo4j.org/) running and populated with a data set about movies and actors.
Neo4j comes with such a data set as an example. The essential relationship is `(:Person)-[:ACTED_IN]->(:Movie)`

On *NIX, you can install Neo4j as follows

    wget -qO- http://dist.neo4j.org/neo4j-community-2.0.0-M06-unix.tar.gz | tar xzf -
    cd neo4j-community-2.0.0-M06/
    bin/neo4j start
    # open http://localhost:7474/browser/
    # stop with bin/neo4j stop

In this UI, type in `:play movies` and follow the instructions until the data in imported
(which will take a couple of secs).

Then, to start the python app, you'll have to install [flask](http://flask.pocoo.org/docs/installation/) and
[requests](http://www.python-requests.org/en/v2.0-0/user/install/#install).
Or you can just `pip install -r requirements.txt` in your favourite virtualenv.

Either way, start the app by

    python bacon_number.py

For more options, see `python bacon_number.py --help`

### API

The app has two endpoints:

- /\<actor>

  This will calculate the Bacon Number for the given author

- /\<actor>/\<some\_other\_actor>

  This will calculate the distance between the two given authors. (some\_other\_author is treated as Kevin Bacon)

The output format is shamelessly ripped off of [Google](https://www.google.com/#q=bacon+number+of+keanu+reeves)
