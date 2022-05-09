package com.yu.tao.controller;

import com.yu.tao.entity.FlowGeneration;
import com.yu.tao.service.FlowGenerationService;
import com.yu.tao.utils.BarChartTool;
import com.yu.tao.utils.CallPythonAutomata;
import com.yu.tao.utils.CallPythonSimulate;
import com.yu.tao.utils.PieChartTool;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.swing.*;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

// 注解实现log
@Slf4j
@RestController
public class FlowGenerationController {

    @Autowired
    private FlowGenerationService flowGenerationService;

    private final ExecutorService threadPool =
            new ThreadPoolExecutor(100, 200, 60L,
                    TimeUnit.SECONDS, new LinkedBlockingQueue<Runnable>());

    @GetMapping("/http")
    public String httpSimulate(@RequestParam("sourceIp") String sourceIp, @RequestParam("targetIp") String targetIp,
                               @RequestParam("num") Integer num) {
        // http仿真
        for (int i = 0; i < num; i++) {
            CallPythonSimulate onceCall = new CallPythonSimulate("http_simulate.py", sourceIp, targetIp, 5000 + i, 80);
            threadPool.submit(onceCall);
        }
        flowGenerationService.updateFlowGenerationNumById(num, 1);
        String flowGenerationRecord = "[agreement: http]" + " [sourceIp: " + sourceIp + "] [targetIp: " + targetIp + "] [num: " + num + "]";
        log.info(flowGenerationRecord);
        String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的HTTP流量";
        System.out.println(result);
        return result;
    }

    @GetMapping("/smtp")
    public String smtpSimulate(@RequestParam("sourceIp") String sourceIp, @RequestParam("targetIp") String targetIp,
                               @RequestParam("num") Integer num) {
        // smtp仿真
        for (int i = 0; i < num; i++) {
            CallPythonSimulate onceCall = new CallPythonSimulate("smtp_simulate.py", sourceIp, targetIp, 10000 + i, 25);
            threadPool.submit(onceCall);
        }
        flowGenerationService.updateFlowGenerationNumById(num, 2);
        String flowGenerationRecord = "[agreement: smtp]" + " [sourceIp: " + sourceIp + "] [targetIp: " + targetIp + "] [num: " + num + "]";
        log.info(flowGenerationRecord);
        String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的SMTP流量";
        System.out.println(result);
        return result;
    }

    @GetMapping("/pop3")
    public String pop3Simulate(@RequestParam("sourceIp") String sourceIp, @RequestParam("targetIp") String targetIp,
                               @RequestParam("num") Integer num) {
        // pop3仿真
        for (int i = 0; i < num; i++) {
            CallPythonSimulate onceCall = new CallPythonSimulate("pop3_simulate.py", sourceIp, targetIp, 15000 + i, 110);
            threadPool.submit(onceCall);
        }
        flowGenerationService.updateFlowGenerationNumById(num, 3);
        String flowGenerationRecord = "[agreement: pop3]" + " [sourceIp: " + sourceIp + "] [targetIp: " + targetIp + "] [num: " + num + "]";
        log.info(flowGenerationRecord);
        String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的POP3流量";
        System.out.println(result);
        return result;
    }

    @GetMapping("/imap")
    public String imapSimulate(@RequestParam("sourceIp") String sourceIp, @RequestParam("targetIp") String targetIp,
                               @RequestParam("num") Integer num) {
        // imap仿真
        for (int i = 0; i < num; i++) {
            CallPythonSimulate onceCall = new CallPythonSimulate("imap_simulate.py", sourceIp, targetIp, 20000 + i, 143);
            threadPool.submit(onceCall);
        }
        flowGenerationService.updateFlowGenerationNumById(num, 4);
        String flowGenerationRecord = "[agreement: imap]" + " [sourceIp: " + sourceIp + "] [targetIp: " + targetIp + "] [num: " + num + "]";
        log.info(flowGenerationRecord);
        String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的IMAP流量";
        System.out.println(result);
        return result;
    }

    @GetMapping("/ssh")
    public String sshSimulate(@RequestParam("sourceIp") String sourceIp, @RequestParam("targetIp") String targetIp,
                               @RequestParam("num") Integer num) {
        // ssh仿真
        for (int i = 0; i < num; i++) {
            CallPythonSimulate onceCall = new CallPythonSimulate("ssh_simulate.py", sourceIp, targetIp, 25000 + i, 22);
            threadPool.submit(onceCall);
        }
        flowGenerationService.updateFlowGenerationNumById(num, 5);
        String flowGenerationRecord = "[agreement: ssh]" + " [sourceIp: " + sourceIp + "] [targetIp: " + targetIp + "] [num: " + num + "]";
        log.info(flowGenerationRecord);
        String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的SSH流量";
        System.out.println(result);
        return result;
    }

    @GetMapping("/telnet")
    public String telnetSimulate(@RequestParam("sourceIp") String sourceIp, @RequestParam("targetIp") String targetIp,
                              @RequestParam("num") Integer num) {
        // telnet仿真
        for (int i = 0; i < num; i++) {
            CallPythonSimulate onceCall = new CallPythonSimulate("telnet_simulate.py", sourceIp, targetIp, 30000 + i, 23);
            threadPool.submit(onceCall);
        }
        flowGenerationService.updateFlowGenerationNumById(num, 6);
        String flowGenerationRecord = "[agreement: telnet]" + " [sourceIp: " + sourceIp + "] [targetIp: " + targetIp + "] [num: " + num + "]";
        log.info(flowGenerationRecord);
        String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的TELNET流量";
        System.out.println(result);
        return result;
    }

    /**
     * 将flow_generation表的所有num置零
     */
    @PutMapping("/flow-generation-num")
    public void updateFlowGenerationAllNumToZero() {
        String flowGenerationRecord = "All flowGeneration num to zero";
        log.info(flowGenerationRecord);
        flowGenerationService.updateFlowGenerationAllNumToZero();
    }

    /**
     * 查询所有flow_generation
     * @return 所有flow_generation集合
     */
    @GetMapping("/flow-generations")
    public List<FlowGeneration> queryFlowGenerationAll() {
        String flowGenerationRecord = "query all flowGeneration";
        log.info(flowGenerationRecord);
        return flowGenerationService.queryFlowGenerationAll();
    }

    /**
     * 根据id查询flow_generation某条记录的num
     * @param id id
     * @return 查询的num数
     */
    @GetMapping("/flow-generation/{id}")
    public Integer queryFlowGenerationNumById(@PathVariable("id") Integer id) {
        String flowGenerationRecord = "query flowGeneration num which id = " + id;
        log.info(flowGenerationRecord);
        return flowGenerationService.queryFlowGenerationNumById(id);
    }

    /**
     * 根据id增加flow_generation某条记录的num
     * @param num 需要增加的num数量
     * @param id id
     */
    @PutMapping("/flow-generation-num/{id}")
    public void updateFlowGenerationNumById(@RequestParam("num") Integer num, @PathVariable("id") Integer id) {
        String flowGenerationRecord = "add flowGeneration num which id = " + id + " [num: " + num + "]";
        log.info(flowGenerationRecord);
        flowGenerationService.updateFlowGenerationNumById(num, id);
    }

    /**
     * 可视化柱状图
     */
    @GetMapping("/visualization-bar")
    public void visualizationBar() {
        List<FlowGeneration> flowGenerations = flowGenerationService.queryFlowGenerationAll();
        BarChartTool barChartTool = new BarChartTool(flowGenerations);
        JFrame frame = new JFrame("产生流量统计柱状图");
        frame.add(barChartTool.getPanel1()); // 加入柱形图
        frame.setBounds(50, 50, 900, 600);
        frame.setVisible(true);
        String flowGenerationRecord = "visualization bar";
        log.info(flowGenerationRecord);
    }

    /**
     * 可视化饼状图
     */
    @GetMapping("/visualization-pie")
    public void visualizationPie() {
        List<FlowGeneration> flowGenerations = flowGenerationService.queryFlowGenerationAll();
        PieChartTool pieChartTool = new PieChartTool(flowGenerations);
        JFrame frame = new JFrame("产生流量统计柱状图");
        frame.add(pieChartTool.getPanel1()); // 加入柱形图
        frame.setBounds(50, 50, 700, 600);
        frame.setVisible(true);
        String flowGenerationRecord = "visualization pie";
        log.info(flowGenerationRecord);
    }

    /**
     * 自动构建协议自动机
     * @param pcapName 原始pcap包名
     * @param automataName 生成的储存自动机代码的文件名
     */
    @GetMapping("/automata")
    public String generateAutomata(@RequestParam("pcapName") String pcapName,
                                   @RequestParam("automataName") String automataName) {
        CallPythonAutomata onceCall = new CallPythonAutomata(pcapName, automataName);
        threadPool.submit(onceCall);
        String result = pcapName + "成功构建了自动机，储存代码文件名为" + automataName;
        System.out.println(result);
        String generateAutomataRecord = pcapName + " generate automata finished";
        log.info(generateAutomataRecord);
        return result;
    }
}
