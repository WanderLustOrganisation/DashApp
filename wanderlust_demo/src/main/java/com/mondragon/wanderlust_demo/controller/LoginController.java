package com.mondragon.wanderlust_demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class LoginController {

    final static String ERABILTZAILEA = "erabiltzailea";

    @Autowired
    ErabiltzaileaService erabiltzaileaService;

    @Autowired
    public LoginController(ErabiltzaileaService erabiltzaileaService) 
    {
        this.erabiltzaileaService = erabiltzaileaService;
    }

    @GetMapping("/login")
    public ModelAndView getLogin(HttpServletRequest request) {
        HttpSession session = request.getSession();
        String emaitza;
        if(session.getAttribute(ERABILTZAILEA) == null){
            emaitza = "login";
        }else{
            emaitza = "redirect/ikuspegia";
        }
        return new ModelAndView(emaitza);
    }

    @PostMapping("/login")
    public ModelAndView login(@RequestParam("username") String username,
            @RequestParam("password") String password, HttpServletRequest request, Model model){
                HttpSession session = request.getSession();
                if(erabiltzaileaService.erabiltzaileaExistitu(username, password)){
                    session.setAttribute(ERABILTZAILEA, erabiltzaileaService.getErabiltzaileaByUsername(username));
                    return new ModelAndView("redirect:/ikuspegia");
                }else{
                    model.addAttribute("error", "Erabiltzailea edo pasahitza ez dira zuzenak");
                    return new ModelAndView("/login");
                }
            }
            
    @GetMapping("/logout")
    public ModelAndView logout(HttpServletRequest request) {
        HttpSession session = request.getSession(true);
        session.removeAttribute(ERABILTZAILEA);
        return new ModelAndView("redirect:/");
    }
}