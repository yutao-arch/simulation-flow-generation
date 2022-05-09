package com.yu.tao.utils;

import com.yu.tao.constant.ConstantData;
import com.yu.tao.entity.FlowGeneration;
import lombok.Data;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.labels.StandardPieSectionLabelGenerator;
import org.jfree.chart.plot.PiePlot;
import org.jfree.data.general.DefaultPieDataset;

import java.awt.*;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.List;

@Data
public class PieChartTool {

    public ChartPanel panel1;

    public PieChartTool(List<FlowGeneration> flowGenerations) {
        DefaultPieDataset dataset = getDataSet(flowGenerations);
        JFreeChart chart = ChartFactory.createPieChart(
                "产生流量统计饼状图",
                dataset,
                true,
                false,
                false);

        // 设置百分比
        PiePlot pieplot = (PiePlot) chart.getPlot();


        DecimalFormat df = new DecimalFormat("0.00%");  // 获得一个DecimalFormat对象，主要是设置小数问题
        NumberFormat nf = NumberFormat.getNumberInstance();  // 获得一个NumberFormat对象
        // 获得StandardPieSectionLabelGenerator对象, {0}为选项，{1}为数值，{2}为百分比
        StandardPieSectionLabelGenerator sp1 = new StandardPieSectionLabelGenerator("{0} {1} ({2})", nf, df);
        pieplot.setLabelGenerator(sp1);  // 设置饼图显示百分比
        pieplot.setCircular(true);  // 设置饼图为正圆
        // 设置颜色
        pieplot.setSectionPaint( "http", ConstantData.CHART_COLORS[0]);
        pieplot.setSectionPaint( "smtp", ConstantData.CHART_COLORS[1]);
        pieplot.setSectionPaint( "pop3", ConstantData.CHART_COLORS[2]);
        pieplot.setSectionPaint( "imap", ConstantData.CHART_COLORS[3]);
        pieplot.setSectionPaint( "ssh", ConstantData.CHART_COLORS[4]);
        pieplot.setSectionPaint( "telnet", ConstantData.CHART_COLORS[5]);

        //设定背景透明度（0-1.0之间）
        pieplot.setBackgroundAlpha(0.6f);
//        //设定前景透明度（0-1.0之间）
//        pieplot.setForegroundAlpha(0.8f);

        // 没有数据的时候显示的内容
        pieplot.setNoDataMessage("无数据显示");
        pieplot.setCircular(false);
        pieplot.setLabelGap(0.02D);

        pieplot.setIgnoreNullValues(true);  // 设置不显示空值
        pieplot.setIgnoreZeroValues(true);  // 设置不显示负值
        chart.getTitle().setFont(new Font("宋体", Font.BOLD, 20));  // 设置标题字体
        pieplot.setLabelFont(new Font("宋体", Font.BOLD, 10));  // 解决乱码
        chart.getLegend().setItemFont(new Font("黑体", Font.BOLD, 10));

        panel1 = new ChartPanel(chart, true);
    }

    private static DefaultPieDataset getDataSet(List<FlowGeneration> flowGenerations) {
        DefaultPieDataset dataset = new DefaultPieDataset();
        Integer id;
        String agreement;
        Integer num;
        for (FlowGeneration flowGeneration : flowGenerations) {
            agreement = flowGeneration.getAgreement();
            num = flowGeneration.getNum();
            dataset.setValue(agreement, num);
        }
        return dataset;
    }
}
