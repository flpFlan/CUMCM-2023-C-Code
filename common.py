# -- stdlib --
import json
from os import path
from dataclasses import dataclass
from typing import ClassVar, Self

# -- third party --
import pandas as pd
from pandas import Timestamp

# -- own --
# -- code --


@dataclass
class Item:
    Store: ClassVar[list[Self]] = []
    Map: ClassVar[dict[int, Self]] = {}
    item_code: int
    item_name: str
    class_code: int
    class_name: str

    @classmethod
    def by_code(cls, item_code: int):
        return cls.Map.get(item_code)

    @classmethod
    def by_name(cls, item_name: str):
        for i in cls.Map.values():
            if i.item_name == item_name:
                return i


@dataclass
class SaleFlow:
    Store: ClassVar[list[Self]] = []
    date: Timestamp
    time: Timestamp
    item_code: int
    volume: float
    sale_price: float
    type: str
    is_dicount: bool


@dataclass
class BatchFlow:
    Store: ClassVar[list[Self]] = []
    date: Timestamp
    item_code: int
    batch_price: float


@dataclass
class LossFlow:
    Store: ClassVar[list[Self]] = []
    item_code: int
    item_name: str
    loss_rate: float


def _read_to_store():
    if path.exists("附件1.json"):
        with open("附件1.json", "r") as f:
            for i in json.load(f):
                item = Item(i[0], i[1], i[2], i[3])
                Item.Store.append(item)
                Item.Map[item.item_code] = item
    else:
        with open("附件1.xlsx", "rb") as f:
            sheet = pd.read_excel(f, index_col=0, sheet_name=0)
            store = []
            for k, v in sheet.iterrows():
                item = Item(k, v[0], v[1], v[2])
                Item.Store.append(item)
                Item.Map[item.item_code] = item
                store.append([k, v[0], v[1], v[2]])
            with open("附件1.json", "w") as f:
                json.dump(store, f)

    if path.exists("附件2.json"):
        with open("附件2.json", "r") as f:
            for i in json.load(f):
                sale = SaleFlow(
                    Timestamp(i[0]), Timestamp(i[1]), i[2], i[3], i[4], i[5], i[6]
                )
                SaleFlow.Store.append(sale)
    else:
        with open("附件2.xlsx", "rb") as f:
            sheet = pd.read_excel(f, sheet_name=0)
            store = []
            for _, v in sheet.iterrows():
                SaleFlow.Store.append(
                    SaleFlow(
                        v[0],
                        Timestamp(v[1]),
                        v[2],
                        v[3],
                        v[4],
                        v[5],
                        False if v[6] == "否" else True,
                    )
                )
                store.append(
                    [
                        v[0].__str__(),
                        v[1].__str__(),
                        v[2],
                        v[3],
                        v[4],
                        v[5],
                        False if v[6] == "否" else True,
                    ]
                )
            with open("附件2.json", "w") as f:
                json.dump(store, f)

    if path.exists("附件3.json"):
        with open("附件3.json", "r") as f:
            for i in json.load(f):
                BatchFlow.Store.append(BatchFlow(Timestamp(i[0]), i[1], i[2]))
    else:
        with open("附件3.xlsx", "rb") as f:
            sheet = pd.read_excel(f, sheet_name=0)
            store = []
            for _, v in sheet.iterrows():
                BatchFlow.Store.append(BatchFlow(v[0], v[1], v[2]))
                store.append([v[0].__str__(), v[1], v[2]])
            with open("附件3.json", "w") as f:
                json.dump(store, f)

    if path.exists("附件4.json"):
        with open("附件4.json", "r") as f:
            for i in json.load(f):
                LossFlow.Store.append(LossFlow(i[0], i[1], i[2]))
    else:
        with open("附件4.xlsx", "rb") as f:
            sheet = pd.read_excel(f, sheet_name=0)
            store = []
            for _, v in sheet.iterrows():
                LossFlow.Store.append(LossFlow(v[0], v[1], v[2]))
                store.append([v[0], v[1], v[2]])
            with open("附件4.json", "w") as f:
                json.dump(store, f)


_read_to_store()
