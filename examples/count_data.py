import transparency_service
import os

mc = transparency_service.model_card_generator.ModelCard()

base = os.path.expanduser('~/.transparency_service/data/std')
dic = transparency_service.utils.count_data([
    f'{base}/Horne2017/Horne2017.csv',
    fr'{base}/fake-or-real-news/fake_or_real_news.csv',
])

dic = transparency_service.utils.count_data([
    fr'{base}/gpt-2-output-dataset', # a folder that contains files _read_data_structure.get_supported_types()
])


dic = transparency_service.utils.count_data([
    fr'{base}/FakeNewsCorpus/news_cleaned_2018_02_13.csv',
], model_card=mc, split='type')

base = os.path.expanduser('~/rine/data1/train/')
transparency_service.utils.count_data([
        f'{base}airplane', f'{base}bicycle', f'{base}bird', f'{base}boat', f'{base}bottle', f'{base}bus',
        f'{base}car', f'{base}cat', f'{base}chair', f'{base}cow', f'{base}diningtable', f'{base}dog',
        f'{base}horse', f'{base}motorbike', f'{base}person', f'{base}pottedplant', f'{base}sheep', f'{base}sofa',
        f'{base}tvmonitor',
        ], model_card=mc)

#mc.save(filename='count_data')