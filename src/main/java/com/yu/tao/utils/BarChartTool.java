package com.yu.tao.utils;

import com.yu.tao.constant.ConstantData;
import com.yu.tao.entity.FlowGeneration;
import lombok.Data;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.BarRenderer;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.category.DefaultCategoryDataset;


import java.awt.*;
import java.util.List;

@Data
public class BarChartTool {

    private ChartPanel panel1;

    public BarChartTool(List<FlowGeneration> flowGenerations) {
        CategoryDataset dataset = getDataSet(flowGenerations);
        JFreeChart chart = ChartFactory.createBarChart("产生流量统计柱状图",  // 图表标题
                "协议类型",  // 目录轴的显示标签
                "产生流量数",  // 数值轴的显示标签
                dataset,  // 数据集
                PlotOrientation.VERTICAL,  // 图表方向：水平、垂直
                true,  // 是否显示图例(对于简单的柱状图必须是false)
                false,  // 是否生成工具
                false  // 是否生成URL链接
        );

        CategoryPlot plot = chart.getCategoryPlot(); // 获取图表区域对象

        BarRenderer renderer = (BarRenderer) plot.getRenderer();  // 获取渲染
        // 使用自定义的颜色
        renderer.setSeriesPaint(0, ConstantData.CHART_COLORS[0]);
        renderer.setSeriesPaint(1, ConstantData.CHART_COLORS[1]);
        renderer.setSeriesPaint(2, ConstantData.CHART_COLORS[2]);
        renderer.setSeriesPaint(3, ConstantData.CHART_COLORS[3]);
        renderer.setSeriesPaint(4, ConstantData.CHART_COLORS[4]);
        renderer.setSeriesPaint(5, ConstantData.CHART_COLORS[5]);

        renderer.setItemMargin(0.01); // 组内柱子间隔为组宽的0.01


        CategoryAxis domainAxis = plot.getDomainAxis();  // x轴
        domainAxis.setLabelFont(new Font("黑体", Font.BOLD, 14));  // 水平底部标题
        domainAxis.setTickLabelFont(new Font("宋体", Font.BOLD, 12));  // 垂直标题
        ValueAxis rangeAxis = plot.getRangeAxis();  // y轴
        rangeAxis.setLabelFont(new Font("黑体", Font.BOLD, 15));

        chart.getLegend().setItemFont(new Font("黑体", Font.BOLD, 15));
        chart.getTitle().setFont(new Font("宋体", Font.BOLD, 20));  // 设置标题字体
        // 到这里结束，虽然代码有点多，但只为一个目的，解决汉字乱码问题

        panel1 = new ChartPanel(chart, true);   // 这里也可以用chartFrame,可以直接生成一个独立的Frame
    }

    private static CategoryDataset getDataSet(List<FlowGeneration> flowGenerations) {
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        String agreement;
        Integer num;
        for (FlowGeneration flowGeneration : flowGenerations) {
            agreement = flowGeneration.getAgreement();
            num = flowGeneration.getNum();
            dataset.addValue(num, agreement, agreement);
        }
        return dataset;
    }

}
