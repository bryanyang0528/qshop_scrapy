import csv
from qshop import settings

def write_to_csv(item):
    writer = csv.writer(open(settings.FEED_URI, 'a'), lineterminator='\n')
    writer.writerow([item[key] for key in item.keys()])

class WriteToCsv(object):
    def process_item(self, item, spider):
        write_to_csv(item)
        return item
