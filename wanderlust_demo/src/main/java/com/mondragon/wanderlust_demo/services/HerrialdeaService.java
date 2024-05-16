package com.mondragon.wanderlust_demo.services;

import java.util.List;
import java.util.Optional;

import com.mondragon.wanderlust_demo.model.Herrialdea;

public interface HerrialdeaService {
    public List<Herrialdea> getHerrialdeak();
    public Herrialdea getHerrialdeabyHerrialdea(String herrialdea);
    public Optional<Herrialdea> getHerrialdeaById(int id);
}
