package com.mondragon.wanderlust_demo.model;

import java.util.Collection;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import jakarta.persistence.GenerationType;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Entity
@AllArgsConstructor
@Builder
@NoArgsConstructor
@Table(name = "Erabiltzaileak")
public class Erabiltzailea {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int erabiltzaileaID;

    @Column(nullable = false)
    private String izena;

    @Column(nullable = false)
    private String abizena;

    @Column(nullable = false)
    private String username;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String pasahitza;

    @Column(nullable = false)
    private int adina;

    @Column(nullable = false)
    private boolean erabiltzaileMota;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "herrialdeaID")
    private  Herrialdea herrialdea;

    @OneToMany(mappedBy = "erabiltzailea", cascade = CascadeType.ALL)
    List<Mezua> mezuak;

    @ManyToMany(cascade = CascadeType.ALL)
    @JoinTable(name = "Erabiltzaileen_hizkuntzak", joinColumns = @JoinColumn(name = "erabiltzaileaID"), inverseJoinColumns = @JoinColumn(name = "hizkuntzaID"))
    List<Hizkuntza> hizkuntzak;

    @ManyToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	@JoinTable(
			name = "Erabiltzaileen_rolak",
			joinColumns = @JoinColumn(name = "erabiltzaileID"),
			inverseJoinColumns = @JoinColumn(name = "rolID")
			)
	Collection<Rol> roles;
}
