package com.fintuple.fund_rating.entity;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "mas_securities")
@Data
public class MasSecuritiesEntity {
    private String securityName;
    private String exchangeCode;
    @Id
    private String securityIsin;
}
