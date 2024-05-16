package com.mondragon.wanderlust_demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;

import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class ChatController {

        final static String ERABILTZAILEA = "erabiltzailea";

    @Autowired
    ErabiltzaileaService erabiltzaileaService;

    @Autowired
    public ChatController(ErabiltzaileaService erabiltzaileaService) 
    {
        this.erabiltzaileaService = erabiltzaileaService;
    }

        @GetMapping("/chat")
    public ModelAndView getIndex(Model model, HttpServletRequest request){
        HttpSession session = request.getSession();
        String emaitza;
        if(session.getAttribute(ERABILTZAILEA) != null){
            emaitza = "chat";
        }else{
            emaitza = "/login";
        }
        return new ModelAndView(emaitza);
    }
}
