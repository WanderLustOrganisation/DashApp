package com.mondragon.wanderlust_demo.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;
import org.springframework.security.web.authentication.logout.LogoutSuccessHandler;
import org.springframework.security.web.authentication.logout.SimpleUrlLogoutSuccessHandler;
import org.springframework.security.web.authentication.logout.HttpStatusReturningLogoutSuccessHandler;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.web.SecurityFilterChain;


import java.io.IOException;

import com.mondragon.wanderlust_demo.services.ErabiltzaileaService;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import com.mondragon.wanderlust_demo.model.Erabiltzailea;

@Configuration
@EnableWebSecurity
public class WebSecurityConfig {

    private static final String[] ENDPOINTS_WHITELIST = { "/", "/register", "/ikuspegia", "/aboutus", "/login", "/logout", "/css/**", "/js/**", "/images/**", "/videos/**", "/sass/**", "/locale/**", "/user/edit/**", "/webjars/**"};
    private static final String LOGIN_URL = "/login";
    private static final String LOGIN_FAIL_URL = LOGIN_URL + "?error";
    private static final String DEFAULT_SUCCESS_URL = "/";

    @Autowired
    private ErabiltzaileaService erabiltzaileaService;

    @Bean
    public static BCryptPasswordEncoder passwordEncoder()
    {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider(ApplicationContext applicationContext) {
        DaoAuthenticationProvider auth = new DaoAuthenticationProvider();
        ErabiltzaileaService erabiltzaileaService = applicationContext.getBean(ErabiltzaileaService.class);
        auth.setUserDetailsService(erabiltzaileaService);
        auth.setPasswordEncoder(passwordEncoder());
        return auth;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authorize -> authorize
                .requestMatchers(ENDPOINTS_WHITELIST).permitAll()
                .anyRequest().authenticated()
            )
            .formLogin((form) -> form
				.loginPage("/login")
				.permitAll()
                .defaultSuccessUrl("/ikuspegia", true)
                .successHandler(authenticationSuccessHandler())
            )
            .logout((logout) -> logout
                .logoutSuccessUrl("/")
                .permitAll()
            );
    
        return http.build();
    }

    @Bean
    public AuthenticationSuccessHandler authenticationSuccessHandler() {
        return new CustomAuthenticationSuccessHandler();
    }

    public class CustomAuthenticationSuccessHandler extends SimpleUrlAuthenticationSuccessHandler {

        @Override
        public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response,
                                            Authentication authentication) throws IOException, ServletException {
            HttpSession session = request.getSession();
            User user = (User) authentication.getPrincipal();
            Erabiltzailea erabiltzailea = erabiltzaileaService.getErabiltzaileaByUsername(user.getUsername());
            session.setAttribute("erabiltzailea", erabiltzailea);


            getRedirectStrategy().sendRedirect(request, response, "/ikuspegia");
        }
    }
}
