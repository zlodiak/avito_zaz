from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def del_quotes(text):
    return text.replace('\n', '')


def trim_spaces(text):
    return text.strip(' ')


class ZazItem(Item):
    title = Field(
        input_processor=MapCompose(trim_spaces),
        output_processor=TakeFirst()
    )
    address = Field(
        input_processor=MapCompose(del_quotes, trim_spaces),
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(trim_spaces),
        output_processor=TakeFirst()
    )