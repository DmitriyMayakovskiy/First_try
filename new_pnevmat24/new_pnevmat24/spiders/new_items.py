import scrapy
class ProductSpider(scrapy.Spider):
    name="pnevmat_new"
    start_urls = ['https://pnevmat24.ru/novinki/']
    def parse(self, response):
        for link in response.css('div.product-card__image a::attr(href)'):
            yield response.follow(link, callback=self.parse_product)
        for i in range(1,74):
            next_page = f'https://pnevmat24.ru/novinki/?page={i}'
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        full_har = ''
        name = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        price = response.css('div.product-info__price::text').get().strip() if response.css('div.product-info__price::text').get() else f"Скидка! {response.css('div.product-info__new-price::text').get().strip()}"
        atr = [i.get() for i in response.css('#tab-description').css('table').css('td::text')]
        atr = [i.strip() for i in atr if i != ':' and i != 'Сертификат:' and i != 'Сертификат' and i != 'Взрыв-схема:' and i != 'Взрыв-схема']


        while atr:
            print(atr[0])
            if ':' in atr[0]:
                atr[0] = atr[0][:-1:]

            full_har += f'{atr[0]}: {atr[1]}\n'
            atr.pop(0)
            atr.pop(0)

        dict = {
            'name' : name,
            'price' : price,
            'full_har' : full_har
        }
        print(dict['name'], dict['price'], sep='\n')
        print(full_har)
        yield dict
