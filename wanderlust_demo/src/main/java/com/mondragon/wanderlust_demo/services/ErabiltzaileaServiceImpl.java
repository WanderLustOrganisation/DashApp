package com.mondragon.wanderlust_demo.services;

import java.time.chrono.Era;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.mondragon.wanderlust_demo.config.WebSecurityConfig;
import com.mondragon.wanderlust_demo.model.Erabiltzailea;
import com.mondragon.wanderlust_demo.model.Rol;
import com.mondragon.wanderlust_demo.repository.ErabiltzaileaRepository;

@Service
public class ErabiltzaileaServiceImpl implements ErabiltzaileaService {

    @Autowired
    ErabiltzaileaRepository erabiltzaileaRepository;

    @Override
    public Erabiltzailea getErabiltzaileaByUsername(String username) {
        return erabiltzaileaRepository.findErabiltzaileaByUsername(username);
    }

    @Override
    public Erabiltzailea getErabiltzaileaByEmail(String email) {
        return erabiltzaileaRepository.findErabiltzaileaByEmail(email);
    }

    @Override
    public List<Erabiltzailea> getErabiltzaileak() {
        return erabiltzaileaRepository.findAll();
    }

    @Override
    public Optional<Erabiltzailea> getErabiltzaileaByIid(int id) {
        return erabiltzaileaRepository.findById(id);
    }

    @Override
    public boolean erabiltzaileaExistitu(String username, String password) {
        Erabiltzailea erabiltzailea = erabiltzaileaRepository.findErabiltzaileaByUsername(username);
        if (erabiltzailea != null) {
            return erabiltzailea.getPasahitza().equals(password);
        } else {
            return false;
        }
    }
    

    @Override
    public Erabiltzailea erabiltzaileaSartu(Erabiltzailea erabiltzailea) {
        if(erabiltzailea.getRoles() == null)
        {
            Rol rol = new Rol("ROLE_USER");
            erabiltzailea.setRoles(Arrays.asList(rol));
        }
        BCryptPasswordEncoder passwordEncoder = WebSecurityConfig.passwordEncoder();

        erabiltzailea.setPasahitza(passwordEncoder.encode(erabiltzailea.getPasahitza()));

        erabiltzaileaRepository.save(erabiltzailea);

        loadUserByUsername(erabiltzailea.getUsername());

        return erabiltzailea;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Erabiltzailea erabiltzailea = this.getErabiltzaileaByUsername(username);

        if (erabiltzailea == null) {
            throw new UsernameNotFoundException("Usuario o password inválidos");
        }
        return new User(erabiltzailea.getUsername(), erabiltzailea.getPasahitza(),
                mapAuthorities(erabiltzailea.getRoles()));
    }

    private Collection<? extends GrantedAuthority> mapAuthorities(Collection<Rol> roles) {
        return roles.stream().map(role -> new SimpleGrantedAuthority(role.getIzena())).collect(Collectors.toList());
    }

}
