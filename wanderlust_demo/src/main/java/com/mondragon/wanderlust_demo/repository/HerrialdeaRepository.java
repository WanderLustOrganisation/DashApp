package com.mondragon.wanderlust_demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.mondragon.wanderlust_demo.model.Herrialdea;

@Repository
public interface HerrialdeaRepository extends JpaRepository<Herrialdea, Integer>{
    public Herrialdea findByHerrialdea(String herrialdea);
}
