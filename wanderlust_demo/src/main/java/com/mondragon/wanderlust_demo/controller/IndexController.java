package com.mondragon.wanderlust_demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;

import com.mondragon.wanderlust_demo.model.Erabiltzailea;
import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class IndexController {

    @Autowired
    ErabiltzaileaService erabiltzaileaService;

    @Autowired
    public IndexController(ErabiltzaileaService erabiltzaileaService){
        this.erabiltzaileaService = erabiltzaileaService;
    }

    @GetMapping("/")
    public ModelAndView getIndex(Model model, HttpServletRequest request, Authentication authentication){
        if(authentication != null && authentication.isAuthenticated()){
            HttpSession session = request.getSession();
            Erabiltzailea erabiltzailea = erabiltzaileaService.getErabiltzaileaByUsername(authentication.getName());
            session.setAttribute("erabiltzailea", erabiltzailea);
        }

        return new ModelAndView("index");
    }
}
