package com.yu.tao.utils;

import com.yu.tao.constant.ConstantData;

import java.io.BufferedReader;
import java.io.InputStreamReader;

/*
java调用python的自动生成自动机的方法
*/
public class CallPythonAutomata implements Runnable{

    private String pcapName;
    private String automataName;

    public CallPythonAutomata(String pcapName, String automataName) {
        this.pcapName = pcapName;
        this.automataName = automataName;
    }

    @Override
    public void run() {
        try {
            // 参数分别为python路径，被调用的py文件路径，原始pcap文件路径，生成的自动机代码的储存路径（只有后面两个参数被传入python脚本）
            String[] args1 = new String[]{
                    ConstantData.PYTHON_PATH,
                    ConstantData.CALL_PYTHON_PATH + "generate_automata.py",
                    ConstantData.CALL_PYTHON_PATH + "pcap\\" + pcapName,
                    ConstantData.CALL_PYTHON_PATH + "automata\\" + automataName};
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
