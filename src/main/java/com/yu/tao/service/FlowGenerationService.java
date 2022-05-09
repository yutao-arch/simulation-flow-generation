package com.yu.tao.service;

import com.yu.tao.entity.FlowGeneration;

import java.util.List;

public interface FlowGenerationService {

    List<FlowGeneration> queryFlowGenerationAll();

    void updateFlowGenerationAllNumToZero();

    void updateFlowGenerationNumById(Integer num, Integer id);

    Integer queryFlowGenerationNumById(Integer id);
}
