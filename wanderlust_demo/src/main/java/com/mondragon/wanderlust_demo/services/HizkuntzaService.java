package com.mondragon.wanderlust_demo.services;

import java.util.List;
import java.util.Optional;

import com.mondragon.wanderlust_demo.model.Hizkuntza;

public interface HizkuntzaService {
    public List<Hizkuntza> getHizkuntzak();
    public Optional<Hizkuntza> getHizkuntzabyId(int id);
    public Hizkuntza getHizkuntza(String hizkuntza);
    public List<Hizkuntza> getHizkuntzakByIzenak(List<String> hizkuntzak);
}