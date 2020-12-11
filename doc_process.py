import pandas as pd

from settings import FIELD_COMMODITY, FIELD_LINK, FIELD_MONEY, \
    FIELD_NUM, FIELD_PRICE, FIELD_UNIT, FIELD_NUMBER, SAMPLE_INVOICE
from func import get_amount_tax, get_df


class DocProcess:
    def __init__(self, path: str):
        self.path = path
        self.df = get_df(path)

    def summary(self) -> str:
        df = pd.DataFrame(
            self.df.groupby([FIELD_COMMODITY, FIELD_UNIT, FIELD_PRICE],
                            as_index=False
                            )[FIELD_NUM].sum())
        df[FIELD_MONEY] = df[FIELD_NUM] * df[FIELD_PRICE]
        df.insert(0, FIELD_NUMBER, range(1, len(df) + 1), )
        self.path = self.path[:-5] + self.path[-5:].replace('.', '(汇总).')
        df.to_excel(self.path, encoding='utf-8', index=False)
        return self.path

    def add_links(self, links_data: dict):
        link = []
        names = self.df[FIELD_COMMODITY] + self.df[FIELD_PRICE].astype(str)
        for name in names:
            if name in links_data.keys():
                link.append(links_data[name])
            else:
                link.append(None)
        self.df[FIELD_LINK] = link
        self.path = self.path[:-5] + self.path[-5:].replace('.', '(链接).')
        self.df.to_excel(self.path, encoding='utf-8', index=False)
        return self.path

    def generator_invoice(self, commodity_data: dict):
        k = 1
        mode_df = pd.read_excel(SAMPLE_INVOICE)
        err = []
        best = None
        for row in self.df.itertuples():
            num = getattr(row, FIELD_NUM)
            name = getattr(row, FIELD_COMMODITY)
            unit = getattr(row, FIELD_UNIT)
            price = getattr(row, FIELD_PRICE)

            if num <= 0:
                err.append(k)
                continue
            length = 0
            for word in commodity_data.keys():
                if word == name:
                    best = word
                    length = 1
                    break
                elif word in name and len(word) > length:
                    length = len(word)
                    best = word
            if length != 0:
                line = [
                    k, best, unit, None, num,
                    num * price, commodity_data[best][0], None, None,
                    get_amount_tax(num, price, commodity_data[best][0]),
                    None, None, price, 1, commodity_data[best][1],
                    commodity_data[best][2], None, commodity_data[best][3], None, None, 0
                ]
                mode_df.loc[k] = line
            else:
                print(k)
                err.append(k)
            k += 1
        mode_df.to_excel(
            self.path[:-5] + self.path[-5:].replace('.', '(发票).'),
            encoding='utf-8', index=False
        )

        err_df = pd.DataFrame(self.df.loc[err])
        self.path = self.path[:-5] + self.path[-5:].replace('.', '(无).')
        err_df.to_excel(self.path, encoding='utf-8', index=False)
        return self.path
