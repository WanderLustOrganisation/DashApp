package com.mondragon.paralelizacion_pruebas.sin_paralelizar;

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

import com.mondragon.paralelizacion_pruebas.sin_paralelizar.Slave;

public class Master {

    Date fechaInicio;
    Date fechaFinal;
    String topic;
    Double suma;

    public Master(String topic, String fechaInicio, String fechaFin) throws ParseException {

        this.topic = topic;
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.fechaInicio = dateFormat.parse(fechaInicio);
        this.fechaFinal = dateFormat.parse(fechaFin);
        suma = 0.0;
        Slave slave = new Slave(topic, this.fechaInicio, fechaFinal);
        //System.out.println(slave.getMedia());
    }

   /*  public static void main(String[] argv) throws Exception {
        if (argv.length < 3) {
            System.err.println("Usage: Master <tema> <fechaInicio> <fechaFin>");
            System.exit(1);
        }

        String tema = argv[0];
        String fechaInicio = argv[1];
        String fechaFin = argv[2];
        long inicio = System.currentTimeMillis();
        Master master = new Master(tema, fechaInicio, fechaFin);

        long fin = System.currentTimeMillis();
        System.out.println("ha tardado: " + (fin - inicio) + " milisegundos");
    }*/
}
