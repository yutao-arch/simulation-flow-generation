package com.yu.tao;

import com.yu.tao.view.FlowGenerationUiView;
import de.felixroske.jfxsupport.AbstractJavaFxApplicationSupport;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.yu.tao.mapper")
public class FlowGenerationApplicationUi extends AbstractJavaFxApplicationSupport {
    public static void main(String[] args) {
        launch(FlowGenerationApplicationUi.class, FlowGenerationUiView.class, args);
    }
}
