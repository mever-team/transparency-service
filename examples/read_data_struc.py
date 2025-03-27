import transparency_service
import pandas as pd
import os

base = os.path.expanduser('~/.transparency_service/data/std')
transparency_service.utils.get_data(fr"{base}/tweepfake/validation.csv", delimiter =';')
transparency_service.utils.get_data(fr"{base}/liar/test.tsv", names =['id', 'label'	, 'statement', 'subject', 'speaker', 'job', 'state', 'party', 'barely_true_c', 'false_c', 'half_true_c', 'mostly_true_c', 'pants_on_fire_c', 'venue'])
# transparency_service.utils.get_data(r"C:\Users\jgnikoul\Desktop\mct\helloooo.json")
# transparency_service.utils.get_data(r"E:\data\gpt-2-output-dataset\large-762M.test.jsonl")
# transparency_service.utils.get_data(r"E:\data\test.xml")
# transparency_service.utils.get_data(r"E:\data\test.yml")
# transparency_service.utils.get_data(r"E:\data\test.parquet")
# transparency_service.utils.get_data(r"E:\data\test.feather")
# transparency_service.utils.get_data(r"E:\data\test.pickle")
# transparency_service.utils.get_data(r"E:\data\test.html")
transparency_service.utils.get_data(fr"{base}/gpt-2-output-dataset")
# paths_dic,_ = transparency_service.utils.get_data(r"E:\data\Horne2017\Horne2017_FakeNewsData\Public Data\Buzzfeed Political News Dataset")
# for k in paths_dic.keys():
#     print(f"{k}: {len(paths_dic[k])}")