package com.mondragon.wanderlust_demo.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.mondragon.wanderlust_demo.model.Hizkuntza;
import com.mondragon.wanderlust_demo.repository.HizkuntzaRepository;

@Service
public class HizkuntzaServiceImpl implements HizkuntzaService{

    @Autowired
    HizkuntzaRepository hizkuntzaRepository;

    @Override
    public List<Hizkuntza> getHizkuntzak() {
        return hizkuntzaRepository.findAll();
    }

    @Override
    public Optional<Hizkuntza> getHizkuntzabyId(int id) {
        return hizkuntzaRepository.findById(id);
    }

    @Override
    public Hizkuntza getHizkuntza(String hizkuntza) {
        return hizkuntzaRepository.findHizkuntzaByHizkuntza(hizkuntza);
    }

    @Override
    public List<Hizkuntza> getHizkuntzakByIzenak(List<String> hizkuntzak) {
        List<Hizkuntza> hizkuntzakObj = new ArrayList<>();
        for(String izena : hizkuntzak){
            hizkuntzakObj.add(this.getHizkuntza(izena));
        }
        return hizkuntzakObj;
    }
    
}
