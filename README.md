# hidemyass-py
A Python library returns a list of free proxies from proxylist.hidemyass.com 

### Dependencies

```
click==6.6
enum34==1.1.6
lxml==3.6.0
requests==2.10.0
```

### Install

```
python setup.py install
```


### Usage

```
Usage: hidemyass [OPTIONS]

Options:
  -c, --country [China|Mexico|United States|Germany|Brazil|Russian Federation|Netherlands|France|Venezuela|Switzerland|United Kingdom|Japan|Thailand|Hong Kong|Korea, Republic of|Viet Nam|Taiwan|Sweden|Indonesia|Canada|Taiwan|Austria|Poland|Luxembourg|Belgium|Romania|Slovakia|Ukraine|Malaysia|Croatia|Israel|United Arab Emirates|Georgia|Hungary|Colombia|Iran|Europe|Netherlands Antilles|Saudi Arabia|Iceland|Angola|Bolivia|Australia|Norway|India|Bulgaria|Chile|Kenya|Italy|Lithuania|Czech Republic|Pakistan|Ecuador|Moldova, Republic of|Trinidad and Tobago|Argentina]
                                  one or multiple countries
  -p, --port TEXT                 one or multiple port numbers
  -o, --protocol [http|https|socks5]
  -a, --anonymity-level [none|low|medium|high|keepalive]
  --include-planet-lab / --exclude-planet-lab
  -s, --speed [slow|medium|fast]
  -t, --connection-time [slow|medium|fast]
  -n, --number INTEGER            number of proxies that will be returned
  -f, --output-format [json|compact]
                                  output format
  --help                          Show this message and exit.
```

#### Get 5 high speed and high+KA anonymity China proxies

```
> hidemyass -c China -o http -a keepalive -s fast -t fast -n 5
Proxy(ip='117.135.250.134', port='8083', country='China', speed='715', connection_time='212', protocol='HTTP', anonymity='High +KA')
Proxy(ip='124.88.67.21', port='80', country='China', speed='1320', connection_time='436', protocol='HTTP', anonymity='High +KA')
Proxy(ip='101.81.242.78', port='8118', country='China', speed='1220', connection_time='406', protocol='HTTP', anonymity='High +KA')
Proxy(ip='124.88.67.35', port='81', country='China', speed='1531', connection_time='505', protocol='HTTP', anonymity='High +KA')
Proxy(ip='124.88.67.54', port='843', country='China', speed='1623', connection_time='444', protocol='HTTP', anonymity='High +KA')
```

#### Get 5 proxies in compact format

```
> hidemyass -n 5 -f compact
HTTP://101.96.10.32:95
HTTP://101.96.10.30:93
HTTP://101.96.11.32:88
HTTP://101.96.10.33:91
HTTP://101.96.10.29:81
```

#### Get 5 proxies in json format

```
> hidemyass/cli.py -n 5 -f json
[{"ip": "203.66.159.46", "port": "3128", "country": "Taiwan", "speed": "6557", "connection_time": "324", "protocol": "HTTPS", "anonymity": "High +KA"}, {"ip": "112.239.75.99", "port": "8888", "country": "China", "speed": "6219", "connection_time": "404", "protocol": "HTTP", "anonymity": "High +KA"}, {"ip": "203.223.143.51", "port": "8080", "country": "Malaysia", "speed": "7527", "connection_time": "209", "protocol": "HTTPS", "anonymity": "High +KA"}, {"ip": "124.88.67.35", "port": "81", "country": "China", "speed": "4414", "connection_time": "450", "protocol": "HTTP", "anonymity": "High +KA"}, {"ip": "101.96.10.42", "port": "88", "country": "Viet Nam", "speed": "8947", "connection_time": "413", "protocol": "HTTP", "anonymity": "High +KA"}]
```
