# -- stdlib --
from collections import defaultdict

# -- third party --
from pyecharts.charts import Bar, Timeline
from pyecharts.options import (
    InitOpts,
    ToolBoxFeatureDataZoomOpts,
    ToolboxOpts,
    ToolBoxFeatureOpts,
    DataZoomOpts,
    ToolBoxFeatureSaveAsImageOpts,
)

# -- own --
from common import SaleFlow, Item

# -- code --


def wholesale_for_each_classification():
    kinds = set()
    graph = defaultdict(lambda: 0)
    for sale in SaleFlow.Store:
        class_name = Item.Map[sale.item_code].class_name
        kinds.add(class_name)
        graph[class_name] += sale.volume
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
    bar.add_xaxis(kinds)
    bar.add_yaxis("各品类销售量", [graph[k] for k in kinds])
    bar.render("各品类销售量.html")


def wholesale_for_each_single_item():
    graph = {
        "花菜类": defaultdict(lambda: 0),
        "水生根茎类": defaultdict(lambda: 0),
        "辣椒类": defaultdict(lambda: 0),
        "食用菌": defaultdict(lambda: 0),
        "花叶类": defaultdict(lambda: 0),
        "茄类": defaultdict(lambda: 0),
    }
    for sale in SaleFlow.Store:
        class_name = Item.Map[sale.item_code].class_name
        item_name = Item.Map[sale.item_code].item_name
        graph[class_name][item_name] += sale.volume
    bar = Bar(InitOpts(width="100vw", height="100vh"))
    bar.set_global_opts(
        toolbox_opts=ToolboxOpts(
            feature=ToolBoxFeatureOpts(data_zoom=ToolBoxFeatureDataZoomOpts())
        ),
        datazoom_opts=[DataZoomOpts(), DataZoomOpts(type_="inside")],
    )
    # x_axis = (
    #     [k for k in graph["花菜类"]]
    #     + [k for k in graph["水生根茎类"]]
    #     + [k for k in graph["辣椒类"]]
    #     + [k for k in graph["食用菌"]]
    #     + [k for k in graph["花叶类"]]
    #     + [k for k in graph["茄类"]]
    # )
    # y_axis = (
    #     [graph["花菜类"][k] for k in graph["花菜类"]]
    #     + [graph["水生根茎类"][k] for k in graph["水生根茎类"]]
    #     + [graph["辣椒类"][k] for k in graph["辣椒类"]]
    #     + [graph["食用菌"][k] for k in graph["食用菌"]]
    #     + [graph["花叶类"][k] for k in graph["花叶类"]]
    #     + [graph["茄类"][k] for k in graph["茄类"]]
    # )
    # bar.add_xaxis(x_axis)
    # bar.add_yaxis("各商品销售量", y_axis)
    # bar.render("各商品销售量.html")

    bar.add_xaxis(["花菜类", "水生根茎类", "辣椒类", "食用菌", "花叶类", "茄类"])
    for k in graph["花菜类"]:
        bar.add_yaxis(k, [graph["花菜类"][k], None, None, None, None, None])
    for k in graph["水生根茎类"]:
        bar.add_yaxis(k, [None, graph["水生根茎类"][k], None, None, None, None])
    for k in graph["辣椒类"]:
        bar.add_yaxis(k, [None, None, graph["辣椒类"][k], None, None, None])
    for k in graph["食用菌"]:
        bar.add_yaxis(k, [None, None, None, graph["食用菌"][k], None, None])
    for k in graph["花叶类"]:
        bar.add_yaxis(k, [None, None, None, None, graph["花叶类"][k], None])
    for k in graph["茄类"]:
        bar.add_yaxis(k, [None, None, None, None, None, graph["茄类"][k]])

    bar.render("各商品销售量(2).html")


def find_volume_of(item_code: int):
    volume = 0.0
    for i in SaleFlow.Store:
        if i.item_code == item_code:
            volume += i.volume
    return volume


def saleflow_with_timeline_of(item_code: int):
    item_name = Item.by_code(item_code).item_name
    store = [i for i in SaleFlow.Store if i.item_code == item_code]
    volumes = defaultdict(lambda: 0)  # type: ignore
    times = sorted({i.date for i in store})
    for i in store:
        volumes[i.date] += i.volume
    bar = Bar(InitOpts(width="100vw", height="100vh"))
    bar.set_global_opts(
        toolbox_opts=ToolboxOpts(
            feature=ToolBoxFeatureOpts(data_zoom=ToolBoxFeatureDataZoomOpts())
        ),
        datazoom_opts=[DataZoomOpts(), DataZoomOpts(type_="inside")],
    )
    bar.add_xaxis(list(map(lambda t: f"{t.year}-{t.month}-{t.day}", times)))
    bar.add_yaxis(item_name, [volumes[d] for d in times])
    bar.render(f"{item_name}销量时间线.html")


def classsale_with_timeline_of(class_name: str):
    store = [
        i for i in SaleFlow.Store if Item.by_code(i.item_code).class_name == class_name
    ]
    volumes = defaultdict(lambda: 0)  # type: ignore
    times = sorted({i.date for i in store})
    for i in store:
        volumes[i.date] += i.volume
    bar = Bar(InitOpts(width="100vw", height="100vh"))
    bar.set_global_opts(
        toolbox_opts=ToolboxOpts(
            feature=ToolBoxFeatureOpts(data_zoom=ToolBoxFeatureDataZoomOpts())
        ),
        datazoom_opts=[DataZoomOpts(), DataZoomOpts(type_="inside")],
    )
    bar.add_xaxis(list(map(lambda t: f"{t.year}-{t.month}-{t.day}", times)))
    bar.add_yaxis(class_name, [volumes[d] for d in times])
    bar.render(f"(类){class_name}销量时间线.html")


def main():
    wholesale_for_each_classification()
    # wholesale_for_each_single_item()
    # saleflow_with_timeline_of(Item.by_name("西兰花").item_code)
    # saleflow_with_timeline_of(Item.by_name("净藕(1)").item_code)
    # saleflow_with_timeline_of(Item.by_name("芜湖青椒(1)").item_code)
    # for cls in ["花菜类", "水生根茎类", "辣椒类", "食用菌", "花叶类", "茄类"]:
    #     classsale_with_timeline_of(cls)


if __name__ == "__main__":
    main()
