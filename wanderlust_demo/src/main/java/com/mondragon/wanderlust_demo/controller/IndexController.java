package com.mondragon.wanderlust_demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class IndexController {

    @GetMapping("/")
    public String getIndex(Model model, HttpServletRequest request){
        return "index";
    }
}
