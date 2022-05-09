package com.yu.tao.entity;

import lombok.Data;

import javax.persistence.*;

@Data
@Table(name = "flow_generation")
public class FlowGeneration {
    @Id
    @GeneratedValue(generator = "JDBC")
    @Column(name = "id")
    private Integer id;

    @Column(name = "agreement")
    private String agreement;

    @Column(name = "num")
    private Integer num;
}
