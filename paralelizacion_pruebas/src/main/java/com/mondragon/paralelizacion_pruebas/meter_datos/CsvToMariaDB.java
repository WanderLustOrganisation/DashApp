package com.mondragon.paralelizacion_pruebas.meter_datos;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CsvToMariaDB {

    private static final String DB_URL = "jdbc:mariadb://34.73.239.100:3306/probak";
    private static final String USER = "user";
    private static final String PASSWORD = "user";

    private static final String CSV_FILE_PATH = "C:\\Users\\julga\\Documents\\MU\\23-24\\wanderlust\\Web\\paralelizacion_pruebas\\src\\main\\java\\com\\mondragon\\paralelizacion_pruebas\\IBEX-1994-2023_finished.csv";

    public static void main(String[] args) {
        Connection connection = null;
        PreparedStatement preparedStatement = null;
        BufferedReader br = null;

        try {
            connection = DriverManager.getConnection(DB_URL, USER, PASSWORD);
            String sql = "INSERT INTO ejemplo (fecha, valor1, valor2, valor3, valor4, valor5) VALUES (?, ?, ?, ?, ?, ?)";
            preparedStatement = connection.prepareStatement(sql);

            br = new BufferedReader(new FileReader(CSV_FILE_PATH));
            String line;

            // Leer la primera línea (encabezado) y descartarla
            br.readLine();

            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                preparedStatement.setDate(1, java.sql.Date.valueOf(values[0]));
                preparedStatement.setDouble(2, Double.parseDouble(values[1]));
                preparedStatement.setDouble(3, Double.parseDouble(values[2]));
                preparedStatement.setDouble(4, Double.parseDouble(values[3]));
                preparedStatement.setDouble(5, Double.parseDouble(values[4]));
                preparedStatement.setDouble(6, Double.parseDouble(values[5]));
                preparedStatement.addBatch();
            }

            preparedStatement.executeBatch();
            System.out.println("Datos insertados con éxito.");

        } catch (SQLException | IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (br != null) br.close();
                if (preparedStatement != null) preparedStatement.close();
                if (connection != null) connection.close();
            } catch (IOException | SQLException ex) {
                ex.printStackTrace();
            }
        }
    }
}