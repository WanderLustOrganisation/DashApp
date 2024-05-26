package com.mondragon.paralelizacion_pruebas.chat;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Slave implements Callable<Double> {

    String topic;
    Date fechaInicio;
    Date fechaFinal;
    List<Double> numeros;
    private static final String DB_URL = "jdbc:mariadb://localhost:3307/probak_paralelizacion";
    private static final String USER = "wanderlust";
    private static final String PASSWORD = "wanderlust";
    private ExecutorService executor;
    private CompletionService<Double> completionService;

    public Slave(String topic, Date fechaInicio, Date fechaFinal) {
        this.topic = topic;
        this.fechaInicio = fechaInicio;
        this.fechaFinal = fechaFinal;
        this.numeros = new ArrayList<>();
        this.executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        this.completionService = new ExecutorCompletionService<>(executor);
    }

    @Override
    public Double call() throws Exception {
        int tasks = Runtime.getRuntime().availableProcessors();
        long startTime = fechaInicio.getTime();
        long endTime = fechaFinal.getTime();
        long interval = (endTime - startTime) / tasks;

        for (int i = 0; i < tasks; i++) {
            long taskStart = startTime + (i * interval);
            long taskEnd = (i == tasks - 1) ? endTime : (startTime + ((i + 1) * interval));
            completionService.submit(new DataFetcher(taskStart, taskEnd));
        }

        executor.shutdown();

        double totalSum = 0.0;
        int completedTasks = 0;
        while (completedTasks < tasks) {
            Future<Double> future = completionService.take();
            totalSum += future.get();
            completedTasks++;
        }

        return totalSum / tasks;
    }

    private class DataFetcher implements Callable<Double> {
        private long taskStart;
        private long taskEnd;

        public DataFetcher(long taskStart, long taskEnd) {
            this.taskStart = taskStart;
            this.taskEnd = taskEnd;
        }

        @Override
        public Double call() throws Exception {
            List<Double> localNumeros = new ArrayList<>();
            Connection connection = null;
            PreparedStatement preparedStatement = null;
            ResultSet resultSet = null;

            for (int j = 0; j < 100; j++) {

                try {
                    connection = DriverManager.getConnection(DB_URL, USER, PASSWORD);
                    String sql = "SELECT fecha, valor1, valor2, valor3, valor4, valor5 FROM ejemplo WHERE fecha > ? AND fecha < ?";
                    preparedStatement = connection.prepareStatement(sql);
                    preparedStatement.setDate(1, new java.sql.Date(taskStart));
                    preparedStatement.setDate(2, new java.sql.Date(taskEnd));
                    resultSet = preparedStatement.executeQuery();

                    while (resultSet.next()) {
                        Date fecha = resultSet.getDate("fecha");
                        if (fecha.getTime() > taskStart && fecha.getTime() < taskEnd) {
                            double suma = 0.0;
                            for (int i = 1; i <= 5; i++) {
                                suma += resultSet.getDouble(i + 1);
                            }
                            localNumeros.add(suma / 5);
                        }
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    if (resultSet != null)
                        try {
                            resultSet.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    if (preparedStatement != null)
                        try {
                            preparedStatement.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    if (connection != null)
                        try {
                            connection.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                }
            }

            return media(localNumeros);
        }
    }

    private Double media(List<Double> numeros) {
        double suma = 0;
        for (Double numero : numeros) {
            suma += numero;
        }
        return suma / numeros.size();
    }
}
