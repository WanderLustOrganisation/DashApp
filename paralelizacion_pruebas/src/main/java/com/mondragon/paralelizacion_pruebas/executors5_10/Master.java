package com.mondragon.paralelizacion_pruebas.executors5_10;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.MessageProperties;

public class Master {

    private final static String TASK_QUEUE_NAME = "task_queue";
    private final static String RESULT_QUEUE_NAME = "result_queue";
    private ConnectionFactory factory;
    private Connection connection;
    private Channel channel;

    Date fechaInicio;
    Date fechaFinal;
    String topic;
    Double suma;
    int nodes;

    public Master(String topic, String fechaInicio, String fechaFin, int nodes) throws ParseException, IOException {

        this.topic = topic;
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.fechaInicio = dateFormat.parse(fechaInicio);
        this.fechaFinal = dateFormat.parse(fechaFin);
        suma = 0.0;
        this.nodes = nodes;

        factory = new ConnectionFactory();
        factory.setHost("localhost"); // replace with your RabbitMQ server IP
        try {
            connection = factory.newConnection();
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        channel = connection.createChannel();
        channel.queueDeclare(TASK_QUEUE_NAME, true, false, false, null);
        channel.queueDeclare(RESULT_QUEUE_NAME, true, false, false, null);
    }

    public void sendTask(String message) throws IOException {
        channel.basicPublish("", TASK_QUEUE_NAME, MessageProperties.PERSISTENT_TEXT_PLAIN,
                message.getBytes(StandardCharsets.UTF_8));
        System.out.println(" [x] Sent '" + message + "'");
    }

    public void receiveResults() throws Exception {
        channel.basicConsume(RESULT_QUEUE_NAME, true, (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), StandardCharsets.UTF_8);
            System.out.println(" [x] Received result '" + message + "'");
            suma += Double.parseDouble(message);
        }, consumerTag -> {
        });
    }

    public void close() throws Exception {
        channel.close();
        connection.close();
    }

    public void procesarFechasParalelo() throws Exception {
        long inicio = 0;
        long fin = 0;

        long diferenciaFechas = fechaFinal.getTime() - fechaInicio.getTime();
        long intervalo = diferenciaFechas / nodes;

        for (int i = 0; i < nodes; i++) {
            if (inicio == 0) {
                inicio = fechaInicio.getTime() + (intervalo * i);
            }
            fin = fechaInicio.getTime() + (intervalo * (i + 1));
            String message = topic + " " + new Date(inicio).toString() + " " + new Date(fin).toString();
            sendTask(message);
            inicio = fin + 24 * 60 * 60 * 1000;
        }
        String message = topic + " " + new Date(fin).toString() + " " + fechaFinal.toString();
        sendTask(message);

        receiveResults();
    }

    public static void main(String[] argv) throws Exception {
        if (argv.length < 4) {
            System.err.println("Usage: Master <topic> <fechaInicio> <fechaFin> <nodes>");
            System.exit(1);
        }

        String topic = argv[0];
        String fechaInicio = argv[1];
        String fechaFin = argv[2];
        int nodes = Integer.parseInt(argv[3]);

        Master master = new Master(topic, fechaInicio, fechaFin, nodes);
        long start = System.currentTimeMillis();
        master.procesarFechasParalelo();

        long end = System.currentTimeMillis();
        System.out.println("ha tardado: " + (end - start) + " milisegundos");
        System.out.println("Average: " + (master.suma / nodes));

        master.close();
    }
}
