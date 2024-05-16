package com.mondragon.wanderlust_demo.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.mondragon.wanderlust_demo.model.Herrialdea;
import com.mondragon.wanderlust_demo.repository.HerrialdeaRepository;

@Service
public class HerrialdeaServiceImpl implements HerrialdeaService{

    @Autowired
    HerrialdeaRepository herrialdeaRepository;

    @Override
    public List<Herrialdea> getHerrialdeak() {
        return herrialdeaRepository.findAll();
    }

    @Override
    public Herrialdea getHerrialdeabyHerrialdea(String izena) {
        return herrialdeaRepository.findByHerrialdea(izena);
    }

    @Override
    public Optional<Herrialdea> getHerrialdeaById(int id) {
        return herrialdeaRepository.findById(id);
    }
}
