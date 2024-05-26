package com.mondragon.paralelizacion_pruebas.sin_paralelizar;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class Slave {

    String topic;
    Date fechaInicio;
    Date fechaFinal;
    List<Double> numeros;
    Double media;

    private static final String DB_URL = "jdbc:mariadb://localhost:3307/probak_paralelizacion";
    private static final String USER = "wanderlust";
    private static final String PASSWORD = "wanderlust";

    public Slave(String topic, Date fechaInicio, Date fechaFinal) {
        this.topic = topic;
        this.fechaInicio = fechaInicio;
        this.fechaFinal = fechaFinal;
        media = 0.0;
        numeros = new ArrayList<>();

        for (int i = 0; i < 1; i++) {
            Connection connection = null;
            PreparedStatement preparedStatement = null;
            ResultSet resultSet = null;

            try {
                connection = DriverManager.getConnection(DB_URL, USER, PASSWORD);
                String sql = "SELECT fecha, valor1, valor2, valor3, valor4, valor5 FROM ejemplo WHERE fecha >= ? AND fecha <= ?";
                preparedStatement = connection.prepareStatement(sql);
                preparedStatement.setDate(1, new java.sql.Date(fechaInicio.getTime()));
                preparedStatement.setDate(2, new java.sql.Date(fechaFinal.getTime()));
                resultSet = preparedStatement.executeQuery();

                while (resultSet.next()) {
                    Date fecha = resultSet.getDate("fecha");
                    if (fecha.after(fechaInicio) && fecha.before(fechaFinal)) {
                        double suma = 0.0;
                        for (int j = 1; j <= 5; j++) {
                            suma += resultSet.getDouble(j + 1);
                        }
                        numeros.add(suma / 5);
                    }
                }

            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                try {
                    if (resultSet != null) resultSet.close();
                    if (preparedStatement != null) preparedStatement.close();
                    if (connection != null) connection.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            media = media(numeros, numeros.size());
        }
    }

    public Double media(List<Double> numeros, int size) {
        double suma = 0;
        for (int i = 0; i < size; i++) {
            suma += numeros.get(i);
        }
        return suma / size;
    }

    public Double getMedia() {
        return this.media;
    }
}
