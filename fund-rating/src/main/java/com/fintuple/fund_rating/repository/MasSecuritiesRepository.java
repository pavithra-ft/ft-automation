package com.fintuple.fund_rating.repository;

import com.fintuple.fund_rating.entity.MasSecuritiesEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MasSecuritiesRepository extends JpaRepository<MasSecuritiesEntity, String>{
    MasSecuritiesEntity findBySecurityIsin(String securityIsin);
}
