package com.mondragon.wanderlust_demo.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.mondragon.wanderlust_demo.model.Mezua;
import com.mondragon.wanderlust_demo.repository.MezuaRepository;

@Service
public class MezuServiceImpl implements MezuaService{

    @Autowired
    MezuaRepository mezuaRepository;

    @Override
    public List<Mezua> getMezuak() {
        return mezuaRepository.findAll();
    }

    @Override
    public Mezua saveMezua(Mezua mezua) {
        return mezuaRepository.save(mezua);
    }
    
}
