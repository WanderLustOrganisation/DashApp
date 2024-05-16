package com.mondragon.wanderlust_demo.services;

import java.util.List;

import com.mondragon.wanderlust_demo.model.Mezua;

public interface MezuaService {
    public List<Mezua> getMezuak();
    public Mezua saveMezua(Mezua mezua);
}
