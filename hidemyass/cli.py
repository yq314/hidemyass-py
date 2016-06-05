#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import click
import json
import lxml.html
import requests
from enum import Enum
from collections import namedtuple


class Protocol(Enum):
    http = 0
    https = 1
    socks5 = 2


class AnonymityLevel(Enum):
    none = 0
    low = 1
    medium = 2
    high = 3
    keepalive = 4


class Speed(Enum):
    slow = 1
    medium = 2
    fast = 3


class ConnectionTime(Enum):
    slow = 1
    medium = 2
    fast = 3


class NoResults(Exception):
    pass


Proxy = namedtuple('Proxy', 'ip port country speed connection_time protocol anonymity')

HIDEMYASS_URL = 'http://proxylist.hidemyass.com'

COUNTRY = [
    'China', 'Mexico', 'United States', 'Germany', 'Brazil', 'Russian Federation', 'Netherlands', 'France',
    'Venezuela', 'Switzerland', 'United Kingdom', 'Japan', 'Thailand', 'Hong Kong', 'Korea, Republic of',
    'Viet Nam', 'Taiwan', 'Sweden', 'Indonesia', 'Canada', 'Taiwan', 'Austria', 'Poland', 'Luxembourg', 'Belgium',
    'Romania', 'Slovakia', 'Ukraine', 'Malaysia', 'Croatia', 'Israel', 'United Arab Emirates', 'Georgia',
    'Hungary', 'Colombia', 'Iran', 'Europe', 'Netherlands Antilles', 'Saudi Arabia', 'Iceland', 'Angola',
    'Bolivia', 'Australia', 'Norway', 'India', 'Bulgaria', 'Chile', 'Kenya', 'Italy', 'Lithuania', 'Czech Republic',
    'Pakistan', 'Ecuador', 'Moldova, Republic of', 'Trinidad and Tobago', 'Argentina'
]

@click.command()
@click.option(
    '--country', '-c',
    default=None,
    multiple=True,
    help="one or multiple countries",
    type=click.Choice(COUNTRY)
)
@click.option(
    '--port', '-p',
    default=None,
    multiple=True,
    help="one or multiple port numbers"
)
@click.option(
    '--protocol', '-o',
    default=Protocol.__members__.keys(),
    multiple=True,
    type=click.Choice(Protocol.__members__.keys())
)
@click.option(
    '--anonymity-level', '-a',
    default=AnonymityLevel.__members__.keys(),
    multiple=True,
    type=click.Choice(AnonymityLevel.__members__.keys())
)
@click.option(
    '--include-planet-lab/--exclude-planet-lab',
    default=False,
    is_flag=True
)
@click.option(
    '--speed', '-s',
    default=Speed.__members__.keys(),
    multiple=True,
    type=click.Choice(Speed.__members__.keys())
)
@click.option(
    '--connection-time', '-t',
    default=ConnectionTime.__members__.keys(),
    multiple=True,
    type=click.Choice(ConnectionTime.__members__.keys())
)
@click.option(
    '--number', '-n',
    default=100,
    type=int,
    help="number of proxies that will be returned"
)
@click.option(
    '--output-format', '-f',
    default=None,
    help="output format",
    type=click.Choice(['json', 'compact'])
)
def fetch(country, port, protocol, anonymity_level, include_planet_lab, speed, connection_time, number, output_format):
    payload = [
        ('s', 0),  # date tested
        ('o', 0),  # desc
        ('pp', 3),  # 100 per page
        ('sortBy', 'date')
    ]

    if not country:
        payload.append(('ac', 'on'))
        country = COUNTRY

    for c in country:
        payload.append(('c[]', c))

    if not port:
        payload.append(('allPorts', 1))
    payload.append(('p', port or ''))

    for o in protocol:
        payload.append(('pr[]', Protocol[o].value))

    for a in anonymity_level:
        payload.append(('a[]', AnonymityLevel[a].value))

    if include_planet_lab:
        payload.append(('pl', 'on'))

    for s in speed:
        payload.append(('sp[]', Speed[s].value))

    for t in connection_time:
        payload.append(('ct[]', ConnectionTime[t].value))

    with requests.Session() as session:
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        })

        session.get(HIDEMYASS_URL)

        page = total_pages = 1
        page_url = None
        output = []
        while number > 0:
            if page == 1:
                response = retrieve_first_page(session, payload)
                page_url, total_pages = get_pagination(response)
            else:
                response = retrieve_next_page(session, page_url, page)

            try:
                for proxy in get_proxy(response):
                    if output_format == 'json':
                        output.append(proxy.__dict__)
                    else:
                        click.echo(
                            '{}://{}:{}'.format(
                                proxy.protocol,
                                proxy.ip,
                                proxy.port
                            ) if output_format == 'compact' else proxy
                        )
                    number -= 1

                    if number == 0:
                        break
                page += 1
                if number == 0 or total_pages == 0 or page > total_pages:
                    break
            except NoResults:
                break

    if output_format == 'json':
        click.echo(json.dumps(output))


def get_pagination(response):
    pagination = lxml.html.fromstring(response['pagination'])
    return response['url'], len(pagination.xpath('//ul/li[position()>1 and position()<last()]'))


def get_proxy(response):
    table_html = lxml.html.fromstring(
        remove_hidden_items(response['table'])
    )

    for row in table_html.xpath('//tr'):
        if row.xpath('string(@id)') == 'noresult':
            raise NoResults

        protocol = row.xpath('string(./td[7])').strip().lower()
        yield Proxy(
            ip=row.xpath('string(./td[2])').strip(),
            port=row.xpath('string(./td[3])').strip(),
            country=row.xpath('string(./td[4])').strip(),
            speed=row.xpath('string(./td[5]/div/@value)').strip(),
            connection_time=row.xpath('string(./td[6]/div/@value)').strip(),
            protocol='socks5' if protocol == 'socks4/5' else protocol,
            anonymity=row.xpath('string(./td[8])').strip()
        )


def remove_hidden_items(table):
    hidden_classes = re.findall(r'\.([\w\-_]+)\s*\{display\s*:\s*none.*\}', table, flags=re.IGNORECASE)

    table = re.sub(
        r'<(\w+)\s+class="({}).*?/\1>'.format('|'.join(hidden_classes)),
        '',
        re.sub(
            r'<(\w+)\s+style="display\s*:\s*none.*?/\1>',
            '',
            re.sub(
                r'<style.*?/style>',
                '',
                table,
                flags=re.DOTALL
            ),
            flags=re.DOTALL | re.IGNORECASE
        ),
        flags=re.DOTALL | re.IGNORECASE
    )

    return table


def retrieve_first_page(session, payload):
    return session.post(
        HIDEMYASS_URL,
        data=payload,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': 1,
            'Referer': HIDEMYASS_URL,
            'X-Requested-With': 'XMLHttpRequest'
        }
    ).json()


def retrieve_next_page(session, page_url, page):
    return session.get(
        '{}/{}/{}'.format(HIDEMYASS_URL, page_url, page),
        headers={
            'DNT': 1,
            'Referer': '{}/{}/{}'.format(HIDEMYASS_URL, page_url, page - 1),
            'X-Requested-With': 'XMLHttpRequest'
        }
    ).json()


if __name__ == '__main__':
    fetch()
