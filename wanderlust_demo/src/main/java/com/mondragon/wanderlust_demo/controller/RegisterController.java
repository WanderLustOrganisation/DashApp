package com.mondragon.wanderlust_demo.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.mondragon.wanderlust_demo.model.Erabiltzailea;
import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;
import com.mondragon.wanderlust_demo.services.HerrialdeaService;
import com.mondragon.wanderlust_demo.services.HizkuntzaService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Controller
public class RegisterController {

    final static String ERABILTZAILEA = "erabiltzailea";

    @Autowired
    ErabiltzaileaService erabiltzaileaService;

    @Autowired
    HizkuntzaService hizkuntzaService;

    @Autowired
    HerrialdeaService herrialdeaService;

    @Autowired
    public RegisterController(ErabiltzaileaService erabiltzaileaService, HizkuntzaService hizkuntzaService, HerrialdeaService herrialdeaService) {
        this.erabiltzaileaService = erabiltzaileaService;
        this.hizkuntzaService = hizkuntzaService;
        this.herrialdeaService = herrialdeaService;
    }

    @GetMapping("/register")
    public String getIndex(Model model, HttpServletRequest request) {
        HttpSession session = request.getSession();
        String emaitza;
        if(session.getAttribute(ERABILTZAILEA) == null){
            model.addAttribute("herrialdeak", herrialdeaService.getHerrialdeak());
            model.addAttribute("hizkuntzak", hizkuntzaService.getHizkuntzak());
            emaitza = "register";
        }else{
            emaitza = "ikuspegia";
        }
        return emaitza;
    }

    @PostMapping("/register")
    public String erabiltzaileBerriaSortu(@RequestParam("name") String izena,
            @RequestParam(name = "surname", required = true) String abizena,
            @RequestParam(name = "username-register", required = true) String username,
            @RequestParam(name = "password-register", required = true) String pasahitza,
            @RequestParam(name = "password-reply", required = true) String pasahitza_reply,
            @RequestParam(name = "mail", required = true) String email,
            @RequestParam(name = "age", required = true) int adina,
            @RequestParam(name = "premium", required = false) boolean mota,
            @RequestParam(name = "country", required = true) String herrialdea,
            @RequestParam(name = "languages", required = true) List<String> hizkuntzak,
            HttpServletRequest request, Model model) {
        HttpSession session = request.getSession(true);
        if (erabiltzaileaService.getErabiltzaileaByUsername(username) == null) {
            if (erabiltzaileaService.getErabiltzaileaByEmail(email) == null) {
                if (pasahitza.equals(pasahitza_reply)) {
                    Erabiltzailea erabiltzailea = Erabiltzailea.builder()
                            .izena(izena)
                            .abizena(abizena)
                            .username(username)
                            .pasahitza(pasahitza)
                            .email(email)
                            .adina(adina)
                            .erabiltzaileMota(mota)
                            .herrialdea(herrialdeaService.getHerrialdeabyHerrialdea(herrialdea))
                            .hizkuntzak(hizkuntzaService.getHizkuntzakByIzenak(hizkuntzak))
                            .build();
                    erabiltzaileaService.erabiltzaileaSartu(erabiltzailea);
                    session.setAttribute(ERABILTZAILEA, erabiltzailea);
    
                    return "redirect:/ikuspegia";
                } else {
                    model.addAttribute("error", "Pasahitzak ez datoz bat");
                }
            } else {
                model.addAttribute("error", "Email hau erabiltzen ari da");
            }
        } else {
            model.addAttribute("error", "Erabiltzaile hau erabiltzen ari da");
        }
        return "register";
    }
    
}