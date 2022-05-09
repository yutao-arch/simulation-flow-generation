package com.yu.tao.service.impl;

import com.yu.tao.entity.FlowGeneration;
import com.yu.tao.mapper.FlowGenerationMapper;
import com.yu.tao.service.FlowGenerationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class FlowGenerationServiceImpl implements FlowGenerationService {

    @Autowired
    private FlowGenerationMapper flowGenerationMapper;


    @Override
    public List<FlowGeneration> queryFlowGenerationAll() {
        return flowGenerationMapper.queryFlowGenerationAll();
    }

    @Override
    public void updateFlowGenerationAllNumToZero() {
        flowGenerationMapper.updateFlowGenerationAllNumToZero();
    }

    @Override
    public void updateFlowGenerationNumById(Integer num, Integer id) {
        flowGenerationMapper.updateFlowGenerationNumById(num, id);
    }

    @Override
    public Integer queryFlowGenerationNumById(Integer id) {
        return flowGenerationMapper.queryFlowGenerationNumById(id);
    }
}
