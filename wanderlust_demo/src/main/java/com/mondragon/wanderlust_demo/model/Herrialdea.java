package com.mondragon.wanderlust_demo.model;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "Herrialdeak")
public class Herrialdea {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int herrialdeaID;

    @Column(nullable = false)
    private String herrialdea;

    @Column(nullable = false)
    private String herrialdeISO;

    @OneToMany(mappedBy = "herrialdea", cascade = CascadeType.ALL)
    List<Erabiltzailea> erabiltzaileak;
}
