package com.mondragon.paralelizacion_pruebas.paralelizacion_10;

import com.rabbitmq.client.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import com.rabbitmq.client.AMQP.BasicProperties;
import java.sql.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

import com.rabbitmq.client.Connection;

public class Slave {

    private final static String EXCHANGE_NAME = "tasks";
    private final static String RESULT_QUEUE_NAME = "result_queue";

    ExecutorService executor;
    CompletionService<Double> completionService;

    String numeroNodo;
    Double media;

    private ConnectionFactory factory;
    private Connection connection;
    private Channel channel;

    public Slave(String rabbitMQHost, String numeroNodo) {
        factory = new ConnectionFactory();
        factory.setHost(rabbitMQHost);
        factory.setUsername("guest");
        factory.setPassword("guest");
        this.numeroNodo = numeroNodo;
    }

    public void connect() {
        try {
            connection = factory.newConnection();
            channel = connection.createChannel();
            channel.exchangeDeclare(EXCHANGE_NAME, "direct");

            String queueName = channel.queueDeclare().getQueue();
            channel.queueBind(queueName, EXCHANGE_NAME, numeroNodo);

            DefaultConsumer consumer = new MiConsumer(channel);
            boolean autohack = true;
            channel.basicConsume(queueName, autohack, consumer);

            synchronized (this) {
                try {
                    this.wait();
                } catch (Exception e) {
                    Thread.currentThread().interrupt();
                    e.printStackTrace();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void desconectar() {
        try {
            if (channel != null) {
                channel.close();
            }
            if (connection != null) {
                connection.close();
            }
        } catch (IOException | TimeoutException e) {
            e.printStackTrace();
        }
    }

    public class MiConsumer extends DefaultConsumer {
        public MiConsumer(Channel channel) {
            super(channel);

        }

        private double processTaskInParallel(String topic, Date fechaInicio, Date fechaFinal) {
            int numProcessors = Runtime.getRuntime().availableProcessors();
            executor = Executors.newFixedThreadPool(numProcessors);
            completionService = new ExecutorCompletionService<>(executor);
            
            long inicio = fechaInicio.getTime();
            long diferenciaFechas = fechaFinal.getTime() - fechaInicio.getTime();
            long intervalo = diferenciaFechas / numProcessors;
            for (int i = 0; i < numProcessors - 1; i++) {
                long fin = inicio + intervalo;
                completionService.submit(new SlaveExecutor(topic, new Date(inicio), new Date(fin)));
                System.out.println(new Date(inicio).toString() + " " + new Date(fin).toString());
                System.out.println(fin - inicio);
                inicio = fin + (24 * 60 * 60 * 1000);
            }
            completionService.submit(new SlaveExecutor(topic, new Date(inicio), fechaFinal));
            System.out.println(new Date(inicio).toString() + " " + fechaFinal.toString());
            System.out.println(fechaFinal.getTime() - inicio);

            executor.shutdown();
    
            double totalSum = 0.0;
            int count = 0;
            try {
                while (count < numProcessors) {
                    Future<Double> future = completionService.take();
                    totalSum += future.get();
                    count++;
                }
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
            return count > 0 ? totalSum / count : 0.0;
        }
    

        @Override
        public void handleDelivery(String consumerTag, Envelope envelope, BasicProperties properties, byte[] body)
                throws IOException {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd");
            String valor = new String(body, "UTF-8");
            String[] valores = valor.split(" ");
            media = processTaskInParallel(valores[0], new Date(Long.parseLong(valores[1])), new Date(Long.parseLong(valores[2])));
            channel.basicPublish(RESULT_QUEUE_NAME, "0", MessageProperties.PERSISTENT_TEXT_PLAIN, String.valueOf(media).getBytes());
        }
    }

    public void stop() {
        synchronized(this){
            this.notify();
        }
    }

    public static void main(String[] argv) throws Exception {

        if (argv.length < 1) {
            System.exit(1);
        }

        String numeroNodo = argv[0];

        Slave slave = new Slave("localhost", numeroNodo);
        synchronized(slave){
            Thread hiloEspera = new Thread(() -> {
                slave.stop();
            });
            hiloEspera.start();
            slave.connect();
        }
    }
}
