package com.mondragon.wanderlust_demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;

import com.mondragon.wanderlust_demo.model.Erabiltzailea;
import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class IkuspegiaController {

        final static String ERABILTZAILEA = "erabiltzailea";

    @Autowired
    ErabiltzaileaService erabiltzaileaService;

    @Autowired
    public IkuspegiaController(ErabiltzaileaService erabiltzaileaService) 
    {
        this.erabiltzaileaService = erabiltzaileaService;
    }
    
    @GetMapping("/ikuspegia")
    public ModelAndView getIkuspegia(HttpServletRequest request, Model model){
        HttpSession session = request.getSession();
        String mota;
        Erabiltzailea erabiltzailea = (Erabiltzailea) session.getAttribute(ERABILTZAILEA);
        if(erabiltzailea != null){
            model.addAttribute("herrialdea", erabiltzailea.getHerrialdea());
            model.addAttribute("hizkuntzak", erabiltzailea.getHizkuntzak());
            if(erabiltzailea.isErabiltzaileMota()){
                mota = "2";
            }else{
                mota = "1";
            }
        }else{
            mota = "0";
        }
        return new ModelAndView("redirect:http://localhost:5000/dashboard/?user_type=" + mota);
    }
}
