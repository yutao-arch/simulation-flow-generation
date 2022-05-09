package com.yu.tao.utils;


import com.yu.tao.constant.ConstantData;

import java.io.BufferedReader;
import java.io.InputStreamReader;

 /*
 java调用python的仿真流量生成脚本的方法
 */
public class CallPythonSimulate implements Runnable {

    private String agreement;
    private String sourceIp;
    private String targetIp;
    private Integer sourcePort;
    private Integer targetPort;

    public CallPythonSimulate(String agreement, String sourceIp, String targetIp, Integer sourcePort, Integer targetPort) {
        this.agreement = agreement;
        this.sourceIp = sourceIp;
        this.targetIp = targetIp;
        this.sourcePort = sourcePort;
        this.targetPort = targetPort;
    }

    @Override
    public void run() {
        try {
            // 参数分别为python路径，被调用的py文件路径，源ip地址，目的ip地址，源端口，目的端口（只有后面五个参数被传入python脚本）
            String[] args1 = new String[]{
                    ConstantData.PYTHON_PATH,
                    ConstantData.CALL_PYTHON_PATH + agreement,
                    sourceIp,
                    targetIp,
                    String.valueOf(sourcePort),
                    String.valueOf(targetPort)};
            Process pr = Runtime.getRuntime().exec(args1);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    pr.getInputStream()));
//            // 打印python文件的输出print
//            String line;
//            while ((line = in.readLine()) != null) {
//                System.out.println(line);
//            }
            in.close();
            pr.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
