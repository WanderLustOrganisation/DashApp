package com.mondragon.paralelizacion_pruebas.paralelizacion_10;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.sql.Time;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.TimeoutException;

import com.mondragon.paralelizacion_pruebas.paralelizacion_10.Slave.MiConsumer;
import com.rabbitmq.client.AMQP.BasicProperties;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;
import com.rabbitmq.client.MessageProperties;

public class Master {

    private final static String EXCHANGE_NAME = "tasks";
    private final static String RESULT_QUEUE_NAME = "result_queue";
    private ConnectionFactory factory;
    private Connection connection;
    private Channel channel;

    HiloEspera hiloEspera;
    Date fechaInicio;
    Date fechaFinal;
    String topic;
    Double suma;
    int hilosLlegados;
    int nodes;
    volatile boolean fin = false;

    public Master(String topic, String fechaInicio, String fechaFin, int nodes) throws ParseException, IOException {

        this.topic = topic;
        this.hilosLlegados = 0;
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.fechaInicio = dateFormat.parse(fechaInicio);
        this.fechaFinal = dateFormat.parse(fechaFin);
        suma = 0.0;
        this.nodes = nodes;
        factory = new ConnectionFactory();
        factory.setHost("localhost");
    }

    public void connect() {
        try {
            connection = factory.newConnection();
            channel = connection.createChannel();
            channel.exchangeDeclare(EXCHANGE_NAME, "direct");
            channel.exchangeDeclare(RESULT_QUEUE_NAME, "direct");

            String queueName = channel.queueDeclare().getQueue();
            channel.queueBind(queueName, RESULT_QUEUE_NAME, "0");

            DefaultConsumer consumer = new MiConsumer(channel);
            boolean autohack = true;
            channel.basicConsume(queueName, autohack, consumer);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public class MiConsumer extends DefaultConsumer {
        public MiConsumer(Channel channel) {
            super(channel);

        }

        @Override
        public void handleDelivery(String consumerTag, Envelope envelope, BasicProperties properties, byte[] body)
                throws IOException {
            hilosLlegados += 1;
            String valor = new String(body, "UTF-8");
            suma += Double.parseDouble(valor);
            if(hilosLlegados == nodes){
                fin = true;
            }
        }
    }

    public class HiloEspera extends Thread {
        @Override
        public void run() {
            while (!fin) {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            System.out.println(suma/nodes);
        }
    }

    public void sendTask(String message, String node) {
        try {
            channel.basicPublish(EXCHANGE_NAME, node, MessageProperties.PERSISTENT_TEXT_PLAIN, message.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void desconectar() {
        try {
            if(channel != null){
                channel.close();
            }
            if(connection != null){
                channel.close();
            }
        } catch (IOException | TimeoutException e) {
            e.printStackTrace();
        }
    }

    public void iniciarEspera(){
        hiloEspera = new HiloEspera();
        hiloEspera.start();
    }

    public void procesarFechasParalelo() throws Exception {
        long inicio = 0;
        long fin = 0;
        int i = 0;

        long diferenciaFechas = fechaFinal.getTime() - fechaInicio.getTime();
        long intervalo = diferenciaFechas / nodes;

        for (i = 0; i < nodes; i++) {
            if (inicio == 0) {
                inicio = fechaInicio.getTime() + (intervalo * i);
            }
            fin = fechaInicio.getTime() + (intervalo * (i + 1));
            String message = topic + " " + inicio + " " + fin;
            iniciarEspera();
            sendTask(message, String.valueOf(i + 1));
            inicio = fin + 24 * 60 * 60 * 1000;
        }
        String message = topic + " " + fin + " " + fechaFinal;
        sendTask(message, String.valueOf(i + 1));
    }

    public void parar() {
        fin = true;
        if(hiloEspera != null && hiloEspera.isAlive()){
            hiloEspera.interrupt();
        }
        desconectar();
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

        new Thread(() -> {
            try{
                master.parar();
            } catch (Exception e){
                e.printStackTrace();
            }
        });
        master.connect();
        master.procesarFechasParalelo();
    }
}
