from lxml import html
betfairURL = "https://www.betfair.com/exchange/cricket"
betfairPage = requests.get(betfairURL)
betfairTree = html.fromstring(betfairPage.text)
markets = betfairTree.xpath('(//ul[@class="list-coupons"])')
for market in markets:
    inplayFlag = market.xpath('.//li/span[@class="in-play-icon inplay"]')
    if len(inplayFlag) == 0: continue
    team1 = market.xpath('.//span[@class="home-team"]/text()')[0]
    team2 = market.xpath('.//span[@class="away-team"]/text()')[0]
    team1Back = float(market.xpath('.//li[@class="odds back selection-0 back-cell "]/button/span[@class="price"]/text()')[0].strip())
    team1Lay = float(market.xpath('.//li[@class="odds lay selection-0 lay-cell "]/button/span[@class="price"]/text()')[0].strip())
    team2Back = float(market.xpath('.//li[@class="odds back selection-1 back-cell "]/button/span[@class="price"]/text()')[0].strip())
    team2Lay = float(market.xpath('.//li[@class="odds lay selection-1 lay-cell "]/button/span[@class="price"]/text()')[0].strip())
    print team1 + " " + `team1Back` + "/" + `team1Lay` + " vs " + team2 + " " + `team2Back` + "/" + `team2Lay`
