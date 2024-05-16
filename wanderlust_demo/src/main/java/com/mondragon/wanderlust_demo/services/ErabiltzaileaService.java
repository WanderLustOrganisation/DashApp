package com.mondragon.wanderlust_demo.services;

import java.util.List;
import java.util.Optional;

import org.springframework.security.core.userdetails.UserDetailsService;

import com.mondragon.wanderlust_demo.model.Erabiltzailea;

public interface ErabiltzaileaService extends UserDetailsService{
    public Erabiltzailea getErabiltzaileaByUsername(String username);
    public Erabiltzailea getErabiltzaileaByEmail(String email);
    public List<Erabiltzailea> getErabiltzaileak();
    public Optional<Erabiltzailea> getErabiltzaileaByIid(int id);
    public boolean erabiltzaileaExistitu(String username, String password);
    public Erabiltzailea erabiltzaileaSartu(Erabiltzailea erabiltzailea);
}
