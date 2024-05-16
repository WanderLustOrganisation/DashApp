package com.mondragon.wanderlust_demo.repository;

import java.time.chrono.Era;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.mondragon.wanderlust_demo.model.Erabiltzailea;

@Repository
public interface ErabiltzaileaRepository extends JpaRepository<Erabiltzailea, Integer>{
    public Erabiltzailea findErabiltzaileaByUsername(String username);
    public Erabiltzailea findErabiltzaileaByEmail(String email);
}
