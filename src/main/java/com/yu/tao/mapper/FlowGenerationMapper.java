package com.yu.tao.mapper;

import com.yu.tao.entity.FlowGeneration;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FlowGenerationMapper {

    List<FlowGeneration> queryFlowGenerationAll();

    void updateFlowGenerationAllNumToZero();

    void updateFlowGenerationNumById(Integer num, Integer id);

    Integer queryFlowGenerationNumById(Integer id);

}
