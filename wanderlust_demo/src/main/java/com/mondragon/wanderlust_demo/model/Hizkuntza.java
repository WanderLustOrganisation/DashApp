package com.mondragon.wanderlust_demo.model;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
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
@Table(name = "Hizkuntzak")
public class Hizkuntza {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int hizkuntzaID;

    @Column(nullable = false)
    private String hizkuntza;

    @ManyToMany(mappedBy = "hizkuntzak", cascade = CascadeType.ALL)
    List<Erabiltzailea> erabiltzaileak;
}
