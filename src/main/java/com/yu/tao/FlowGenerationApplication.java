package com.yu.tao;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;

@SpringBootApplication
@MapperScan("com.yu.tao.mapper")
public class FlowGenerationApplication {
    public static void main(String[] args) {
//        SpringApplication.run(FlowGenerationApplication.class, args); //原始版本
        SpringApplicationBuilder builder = new SpringApplicationBuilder(FlowGenerationApplication.class);
        builder.headless(false).run(args);
    }
}
