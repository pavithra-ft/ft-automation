package com.fintuple.fund_rating.controller;

import com.fintuple.fund_rating.entity.MasSecuritiesEntity;
import com.fintuple.fund_rating.service.MasSecuritiesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("crf")
public class MasSecuritiesController {
    @Autowired
    MasSecuritiesService masSecuritiesService;
    @GetMapping("{value}")
    public MasSecuritiesEntity getSecDetails(@PathVariable(name = "value") String secIsin) {
        return masSecuritiesService.getSecurityDetails(secIsin);
    }
}
