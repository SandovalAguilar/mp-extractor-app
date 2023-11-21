import pandas as pd
import flet as ft

from distribution_table import table as t
from scripts import dataAnalyzer as da
from scripts import htmlToDataFrame as hd


def generate_bar_chart(grouped_table):
    class SampleRod(ft.BarChartRod):
        def __init__(self, y: float, hovered: bool = False):
            super().__init__()
            self.hovered = hovered
            self.y = y

        def _before_build_command(self):
            self.to_y = self.y + 1 if self.hovered else self.y
            self.color = ft.colors.YELLOW if self.hovered else ft.colors.WHITE
            self.border_side = (
                ft.BorderSide(width=1, color=ft.colors.GREY_700)
                if self.hovered
                else ft.BorderSide(width=0, color=ft.colors.WHITE)
            )
            super()._before_build_command()

        def _build(self):
            self.tooltip = str(self.y)
            self.width = 22
            self.color = ft.colors.WHITE
            self.bg_to_y = max(grouped_table.array_abs_freq) + 30
            self.bg_color = ft.colors.GREY_700
    
    def on_chart_event(e: ft.BarChartEvent):
        for group_index, group in enumerate(chart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                rod.hovered = e.group_index == group_index and e.rod_index == rod_index
        chart.update()

    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[0])],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[1])],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[2])],
            ),
            ft.BarChartGroup(
                x=3,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[3])],
            ),
            ft.BarChartGroup(
                x=4,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[4])],
            ),
            ft.BarChartGroup(
                x=5,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[5])],
            ),
            ft.BarChartGroup(
                x=6,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[6])],
            ),
            ft.BarChartGroup(
                x=7,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[7])],
            ),
            ft.BarChartGroup(
                x=8,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[8])],
            ),
            ft.BarChartGroup(
                x=9,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[9])],
            ),
            ft.BarChartGroup(
                x=10,
                bar_rods=[SampleRod(grouped_table.array_abs_freq[10])],
            ),
        ],
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=0, label=ft.Text(str(grouped_table.table['Intervals'].iloc[0]))),
                ft.ChartAxisLabel(value=1, label=ft.Text(str(grouped_table.table['Intervals'].iloc[1]))),
                ft.ChartAxisLabel(value=2, label=ft.Text(str(grouped_table.table['Intervals'].iloc[2]))),
                ft.ChartAxisLabel(value=3, label=ft.Text(str(grouped_table.table['Intervals'].iloc[3]))),
                ft.ChartAxisLabel(value=4, label=ft.Text(str(grouped_table.table['Intervals'].iloc[4]))),
                ft.ChartAxisLabel(value=5, label=ft.Text(str(grouped_table.table['Intervals'].iloc[5]))),
                ft.ChartAxisLabel(value=6, label=ft.Text(str(grouped_table.table['Intervals'].iloc[6]))),
                ft.ChartAxisLabel(value=7, label=ft.Text(str(grouped_table.table['Intervals'].iloc[7]))),
                ft.ChartAxisLabel(value=8, label=ft.Text(str(grouped_table.table['Intervals'].iloc[8]))),
                ft.ChartAxisLabel(value=9, label=ft.Text(str(grouped_table.table['Intervals'].iloc[9]))),
                ft.ChartAxisLabel(value=10, label=ft.Text(str(grouped_table.table['Intervals'].iloc[10]))),
            ],
        ),
        on_chart_event=on_chart_event,
        interactive=True,
    )

    return ft.Container(chart, bgcolor=ft.colors.GREY_800, padding=10, border_radius=5, expand=True)
