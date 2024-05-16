package com.mondragon.wanderlust_demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.mondragon.wanderlust_demo.model.Hizkuntza;

public interface HizkuntzaRepository extends JpaRepository<Hizkuntza, Integer>{
    public Hizkuntza findHizkuntzaByHizkuntza(String hizkuntza);
}
