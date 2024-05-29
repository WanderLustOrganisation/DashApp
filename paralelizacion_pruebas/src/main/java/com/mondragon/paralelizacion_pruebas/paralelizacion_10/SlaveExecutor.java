package com.mondragon.paralelizacion_pruebas.paralelizacion_10;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;
import java.sql.*;

public class SlaveExecutor implements Callable<Double> {

    private final static String DB_URL = "jdbc:mariadb://localhost:3307/probak_paralelizacion";
    private final static String USER = "wanderlust";
    private final static String PASSWORD = "wanderlust";

    String topic;
    Date fechaInicio;
    Date fechaFinal;

    Connection connection;
    PreparedStatement preparedStatement;
    ResultSet resultSet;

    public SlaveExecutor(String topic, Date fechaInicio, Date fechaFinal) {
        this.topic = topic;
        this.fechaInicio = fechaInicio;
        this.fechaFinal = fechaFinal;
        this.connection = null;
        this.preparedStatement = null;
        this.resultSet = null;
    }

@Override
public Double call() throws Exception {
    try {
        connection = DriverManager.getConnection(DB_URL, USER, PASSWORD);
        preparedStatement = connection.prepareStatement(
                "SELECT fecha, valor1, valor2, valor3, valor4, valor5 FROM ejemplo WHERE fecha >= ? AND fecha <= ?");
        preparedStatement.setDate(1, new java.sql.Date(fechaInicio.getTime()));
        preparedStatement.setDate(2, new java.sql.Date(fechaFinal.getTime()));
        resultSet = preparedStatement.executeQuery();

        List<Double> valores = new ArrayList<>();
        while (resultSet.next()) {
            double sum = 0.0;
            for (int i = 1; i <= 5; i++) {
                sum += resultSet.getDouble(i + 1);
            }
            valores.add(sum / 5);
        }

        double totalSum = 0.0;
        for (Double valor : valores) {
            totalSum += valor;
        }
        return valores.isEmpty() ? 0.0 : totalSum / valores.size();
    } catch (SQLException e) {
        e.printStackTrace();
        return null;
    } finally {
        if (resultSet != null) resultSet.close();
        if (preparedStatement != null) preparedStatement.close();
        if (connection != null) connection.close();
    }
}


}
