package com.fintuple.fund_rating.service;

import com.fintuple.fund_rating.entity.MasSecuritiesEntity;
import com.fintuple.fund_rating.repository.MasSecuritiesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MasSecuritiesService {
    @Autowired
    MasSecuritiesRepository masSecuritiesRepository;
    public MasSecuritiesEntity getSecurityDetails(String securityIsin) {
        return masSecuritiesRepository.findBySecurityIsin(securityIsin);
    }
}
