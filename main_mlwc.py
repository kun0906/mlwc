"""


"""

from parser import ICRL, NeurIPS, ICML
from show import plot_wordranking, plot_wordcloud

def conf_parser(conf=''):
    conf_name = conf['name']
    url = conf['url']
    paper_type = conf['paper_type']

    if conf_name == 'ICRL':
        cf = ICRL(url=url, params=conf)
    elif conf_name == 'ICML':
        cf = ICML(url=url, params=conf)
    elif conf_name == 'NeurIPS':
        cf = NeurIPS(url=url, params=conf)
    else:
        msg = f'{conf_name}|{url}|{paper_type}'
        raise NotImplementedError(msg)
    data = cf.parsing_url()

    return data


def main():
    # year = 2022
    conferences = [
        # {'name': 'ICRL', 'url': 'https://openreview.net/group?id=ICLR.cc/2023/Conference',
        #  'year': 2023, 'paper_type': 'notable-top-5-'}, # if not work, please wait a few seconds and rerun it.
        # {'name': 'ICRL', 'url': 'https://openreview.net/group?id=ICLR.cc/2022/Conference',
        # 'year': 2022, 'paper_type': 'oral-submissions'},
        # {'name': 'NeurIPS', 'url': 'https://openreview.net/group?id=NeurIPS.cc/2022/Conference',
        #  'year': 2022, 'paper_type': 'accepted_papers'},

        {'name': 'ICML', 'url': 'https://icml.cc/virtual/2022/events/spotlight',
         'year': 2022, 'paper_type': 'grid-displaycards'},

    ]
    out_dir = 'out'
    for conf in conferences:
        conf['out_dir'] = out_dir
        conf_data_csv = conf_parser(conf)
        # conf_data_csv = 'ICRL_2023.csv' # for debugging

        for column in ['title', 'keywords']:
            print(conf_data_csv, f', column: {column}')
            plot_wordranking(conf_data_csv, column=column)  # show top words in column
            plot_wordcloud(conf_data_csv, column=column)  # show words cloud in column


if __name__ == '__main__':
    main()
