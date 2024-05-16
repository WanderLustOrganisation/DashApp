package com.mondragon.wanderlust_demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.mondragon.wanderlust_demo.model.Mezua;

@Repository
public interface MezuaRepository extends JpaRepository<Mezua, Integer>{
    
}
