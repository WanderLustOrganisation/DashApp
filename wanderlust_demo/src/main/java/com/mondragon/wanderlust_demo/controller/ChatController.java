package com.mondragon.wanderlust_demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;

import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;
import com.mondragon.wanderlust_demo.services.MezuaService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class ChatController {

        final static String ERABILTZAILEA = "erabiltzailea";

    @Autowired
    ErabiltzaileaService erabiltzaileaService;

    @Autowired
    MezuaService mezuaService;

    @Autowired
    public ChatController(ErabiltzaileaService erabiltzaileaService, MezuaService mezuaService) 
    {
        this.erabiltzaileaService = erabiltzaileaService;
        this.mezuaService = mezuaService;
    }

    @GetMapping("/chat")
    public ModelAndView getIndex(Model model, HttpServletRequest request){
        HttpSession session = request.getSession();
        String emaitza;
        if(session.getAttribute(ERABILTZAILEA) != null){
            model.addAttribute("mezuak", mezuaService.getMezuak());
            emaitza = "chat";
        }else{
            emaitza = "/login";
        }
        return new ModelAndView(emaitza);
    }
}
