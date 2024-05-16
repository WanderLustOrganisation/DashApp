package com.mondragon.wanderlust_demo.model;

import java.time.LocalDateTime;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Builder
@Table(name = "Mezuak")
public class Mezua {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int mezuaID;

    @Column(nullable = false)
    private String edukia;

    @Column(nullable = false)
    private LocalDateTime data;

    @ManyToOne(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    @JoinColumn(name = "erabiltzaileaID")
    private Erabiltzailea erabiltzailea;
}
