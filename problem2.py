# -- stdlib --
from collections import defaultdict

# -- third party --
from pandas import Timestamp
from pyecharts.charts import Bar, Line
from pyecharts.options import (
    InitOpts,
    ToolBoxFeatureDataZoomOpts,
    ToolboxOpts,
    ToolBoxFeatureOpts,
    DataZoomOpts,
    ToolBoxFeatureSaveAsImageOpts,
    AxisOpts,
)
from sklearn.linear_model import LinearRegression
import numpy as np

# -- own --
from common import SaleFlow, Item, BatchFlow

# -- code --


def class_saleflow_correspond_to_increasement_of(class_code: int, class_name: str):
    dates = set()
    sale_graph: dict[Timestamp, float] = defaultdict(lambda: 0.0)
    inc_graph: dict[Timestamp, list[float]] = defaultdict(list)

    batch_store = [
        i
        for i in BatchFlow.Store
        if Item.by_code(i.item_code).class_code == class_code
        and i.date.month == 6
        and i.date.year == 2023
    ]
    sale_store = [
        i
        for i in SaleFlow.Store
        if Item.by_code(i.item_code).class_code == class_code
        and i.date.month == 6
        and i.date.year == 2023
    ]
    for batch in batch_store:
        expire = flag = False
        for sale in sale_store:
            if sale.is_dicount:
                continue
            if expire:
                break
            if not sale.date == batch.date:
                expire = flag
                continue
            flag = True
            inc = ((sale.sale_price - batch.batch_price) / batch.batch_price) * 100
            inc_graph[sale.date].append(inc)
            sale_graph[sale.date] += sale.volume
            dates.add(sale.date)

    dates = sorted(dates)  # type: ignore

    bar = Bar(InitOpts(width="100vw", height="100vh"))
    bar.set_global_opts(
        toolbox_opts=ToolboxOpts(
            feature=ToolBoxFeatureOpts(
                data_zoom=ToolBoxFeatureDataZoomOpts(),
                save_as_image=ToolBoxFeatureSaveAsImageOpts(background_color="#fff"),
            )
        ),
        datazoom_opts=[DataZoomOpts(), DataZoomOpts(type_="inside")],
    )
    bar.add_xaxis(list(map(lambda t: f"{t.year}-{t.month}-{t.day}", dates)))
    volume_acc = []
    for k in sale_graph:
        volume_acc.append(sale_graph[k] + ((volume_acc or 0) and volume_acc[-1]))
    bar.add_yaxis(f"(类){class_name}销量", volume_acc)
    bar.extend_axis(yaxis=AxisOpts(name="涨幅"))

    inc_acc = []
    for k in inc_graph:
        inc = sum(inc_graph[k]) / len(inc_graph[k])
        inc_acc.append(inc + ((inc_acc or 0) and inc_acc[-1]))
    # line = (
    #     Line()
    #     .add_xaxis(list(map(lambda t: f"{t.year}-{t.month}-{t.day}", dates)))
    #     .add_yaxis(
    #         f"(类){class_name}涨幅",
    #         inc_acc,
    #         yaxis_index=1,
    #     )
    # )
    # bar.overlap(line).render(f"(类){class_name}(23年6月)涨幅销量关系.html")

    x = np.array(list(map(lambda x: x.day, dates)))
    y = np.array(volume_acc)
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y.reshape(-1, 1))
    print(f"(类){class_name}6月系数:", model.coef_[0])
    print(f"(类){class_name}6月截距:", model.intercept_)
    print()


def main():
    item = Item.by_name("牛首生菜")
    class_saleflow_correspond_to_increasement_of(item.class_code, item.class_name)
    item = Item.by_name("藕")
    class_saleflow_correspond_to_increasement_of(item.class_code, item.class_name)
    item = Item.by_name("紫茄子(2)")
    class_saleflow_correspond_to_increasement_of(item.class_code, item.class_name)
    item = Item.by_name("红尖椒")
    class_saleflow_correspond_to_increasement_of(item.class_code, item.class_name)
    item = Item.by_name("西峡花菇(1)")
    class_saleflow_correspond_to_increasement_of(item.class_code, item.class_name)
    item = Item.by_name("西兰花")
    class_saleflow_correspond_to_increasement_of(item.class_code, item.class_name)


if __name__ == "__main__":
    main()
