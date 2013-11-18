import json
import requests
from flask import Flask, render_template_string


class BaconNumber(object):

    app = Flask(__name__)
    NEO_4J = 'http://localhost:7474/'

    NEO_PATH = 'db/data/cypher'

    TEMPLATE = '''<!doctype html>
<meta charset=UTF-8>
<title>{{ kevin_last }} Number of {{ actor }} ({{ bacon_number }})</title>
<p><b>{{ kevin }}</b>'s {{ kevin_last }} Number is {{ bacon_number }}
<p>{% for actor, colleague, movie in actor_movies -%}
<em>{{ actor }}</em> and <em>{{ colleague }}</em>
appeared in <em>{{ movie }}</em><br>{%- endfor %}
'''

    TEMPLATE_404 = '''<!doctype html>
<meta charset=UTF-8>
<title>This is not the Bacon you're looking for</title>
<p>Sorry, don't know anything about <em>{{ actor }}</em>
and <em>{{ kevin }}
'''

    BACON_QUERY = u'''MATCH
p=shortestPath((kevin:Person)-[r:ACTED_IN*]-(actor))
WHERE kevin.name={kevin} AND actor.name={name}
RETURN length([m in nodes(p) WHERE m:Movie]) as BaconNumber,
       [m in nodes(p) WHERE m:Movie | m.title] as Movies,
       [a in nodes(p) WHERE a:Person | a.name][1..-1] as KnowsActors'''

    @staticmethod
    @app.route('/<actor>/<kevin>')
    def bacon_number(kevin, actor):
        kevin, actor = kevin.title(), actor.title()
        kevin_last = kevin.split(' ')[-1]

        params = dict(kevin=kevin, name=actor)
        query = dict(query=BaconNumber.BACON_QUERY, params=params)

        result = requests.post(BaconNumber.NEO_4J + BaconNumber.NEO_PATH,
                               json.dumps(query)).json()
        if not len(result['data']):
            return render_template_string(BaconNumber.TEMPLATE_404,
                                          kevin=kevin,
                                          actor=actor), 404

        data = {c: v for c, v in zip(result['columns'], result['data'][0])}

        actor_movies = zip(data['KnowsActors'] + [actor],
                           [kevin] + data['KnowsActors'],
                           data['Movies'])

        return render_template_string(BaconNumber.TEMPLATE, actor=actor,
                                      kevin=kevin, kevin_last=kevin_last,
                                      bacon_number=data['BaconNumber'],
                                      actor_movies=reversed(actor_movies))

    @staticmethod
    @app.route('/<actor>')
    def bacon(actor):
        return BaconNumber.bacon_number(u'Kevin Bacon', actor)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--debug', action='store_true',
                        help='turn on flask debug mode')
    parser.add_argument('-H', '--host', default='0.0.0.0',
                        help='listen on HOST')
    parser.add_argument('-p', '--port', type=int, default=7575,
                        help='listen on PORT')
    parser.add_argument('-n', '--neo4j', default=BaconNumber.NEO_4J,
                        help='location of Neo4j instance')

    args = parser.parse_args()

    BaconNumber.NEO_4J = args.neo4j
    BaconNumber.app.run(host=args.host, port=args.port, debug=args.debug)
