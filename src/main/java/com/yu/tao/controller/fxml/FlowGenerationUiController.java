package com.yu.tao.controller.fxml;

import com.yu.tao.FlowGenerationApplicationUi;
import com.yu.tao.constant.ConstantData;
import de.felixroske.jfxsupport.FXMLController;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.stage.Stage;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ResourceBundle;

@FXMLController
public class FlowGenerationUiController implements Initializable {

    private Stage primaryStage;

    @FXML
    public ComboBox<String> comboBox1;

    @FXML
    public TextField textField1;

    @FXML
    public TextField textField2;

    @FXML
    public TextField textField3;

    @FXML
    public Button button1;

    @FXML
    public Button button2;

    @FXML
    public Button button3;

    @FXML
    public TextArea textArea1;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        primaryStage = FlowGenerationApplicationUi.getStage();

        button1.setOnAction(event -> {
            try {
                int length = String.valueOf(comboBox1.getValue()).length();
                // 截取出comboBox1中的选中的协议字段
                String agreement = "";
                if (String.valueOf(comboBox1.getValue()).substring(length - 5, length - 1).equals(ConstantData.AGREEMENTS[0])) {
                    agreement = ConstantData.AGREEMENTS[0];
                }
                if (String.valueOf(comboBox1.getValue()).substring(length - 5, length - 1).equals(ConstantData.AGREEMENTS[1])) {
                    agreement = ConstantData.AGREEMENTS[1];
                }
                if (String.valueOf(comboBox1.getValue()).substring(length - 5, length - 1).equals(ConstantData.AGREEMENTS[2])) {
                    agreement = ConstantData.AGREEMENTS[2];
                }
                if (String.valueOf(comboBox1.getValue()).substring(length - 5, length - 1).equals(ConstantData.AGREEMENTS[3])) {
                    agreement = ConstantData.AGREEMENTS[3];
                }
                if (String.valueOf(comboBox1.getValue()).substring(length - 4, length - 1).equals(ConstantData.AGREEMENTS[4])) {
                    agreement = ConstantData.AGREEMENTS[4];
                }
                if (String.valueOf(comboBox1.getValue()).substring(length - 7, length - 1).equals(ConstantData.AGREEMENTS[5])) {
                    agreement = ConstantData.AGREEMENTS[5];
                }
                String sourceIp = textField1.getText();
                String targetIp = textField2.getText();
                int num = Integer.parseInt(textField3.getText());
                if (sourceIp.equals("") || targetIp.equals("")) {
                    Alert alert = new Alert(Alert.AlertType.INFORMATION, "请补全SOURCE_IP和TARGET_IP");
                    alert.initOwner(primaryStage);
                    alert.showAndWait();
                }
                String finalAgreement = agreement;
                // 创建一个线程调用接口
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            String url = ConstantData.HOST + finalAgreement.toLowerCase() + "?sourceIp=" + sourceIp +
                                    "&targetIp=" + targetIp + "&num=" + num;
                            System.out.println(url);
                            URL url1 = new URL(url);
                            // 得到connection对象。
                            HttpURLConnection connection = (HttpURLConnection) url1.openConnection();
                            // 设置请求方式
                            connection.setRequestMethod("GET");
                            // 连接
                            connection.connect();
                            // 得到响应码
                            int responseCode = connection.getResponseCode();
                            if (responseCode == HttpURLConnection.HTTP_OK) {
//                                // 得到响应流
//                                InputStream inputStream = connection.getInputStream();
//                                // 将响应流转换成字符串
//                                String result = inputStream.toString();  // 将流转换为字符串。
                                String result = "成功产生" + num + "条从" + sourceIp + "到" + targetIp + "的" +
                                        finalAgreement + "流量";
                                textArea1.setText(result);
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }).start();
            } catch (StringIndexOutOfBoundsException e) {
                Alert alert = new Alert(Alert.AlertType.INFORMATION, "请选择协议类型");
                alert.initOwner(primaryStage);
                alert.showAndWait();
            } catch (NumberFormatException e) {
                Alert alert = new Alert(Alert.AlertType.INFORMATION, "请输入num");
                alert.initOwner(primaryStage);
                alert.showAndWait();
            }
        });

        button2.setOnAction(event -> {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String url = ConstantData.HOST + "visualization-bar";
                        System.out.println(url);
                        URL url1 = new URL(url);
                        // 得到connection对象。
                        HttpURLConnection connection = (HttpURLConnection) url1.openConnection();
                        // 设置请求方式
                        connection.setRequestMethod("GET");
                        // 连接
                        connection.connect();
                        // 得到响应码
                        int responseCode = connection.getResponseCode();
                        if (responseCode == HttpURLConnection.HTTP_OK) {
                            String result = "柱状图已生成";
                            textArea1.setText(result);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }).start();
        });

        button3.setOnAction(event -> {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String url = ConstantData.HOST + "visualization-pie";
                        System.out.println(url);
                        URL url1 = new URL(url);
                        // 得到connection对象。
                        HttpURLConnection connection = (HttpURLConnection) url1.openConnection();
                        // 设置请求方式
                        connection.setRequestMethod("GET");
                        // 连接
                        connection.connect();
                        // 得到响应码
                        int responseCode = connection.getResponseCode();
                        if (responseCode == HttpURLConnection.HTTP_OK) {
                            String result = "饼状图已生成";
                            textArea1.setText(result);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }).start();
        });
    }
}
