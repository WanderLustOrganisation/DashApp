package com.mondragon.paralelizacion_pruebas.chat;

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

public class Master {

    Date fechaInicio;
    Date fechaFinal;
    String topic;
    CompletionService<Double> completionService;
    ExecutorService executor;
    Double suma;

    public Master(String topic, String fechaInicio, String fechaFin) throws ParseException {
        this.topic = topic;
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.fechaInicio = dateFormat.parse(fechaInicio);
        this.fechaFinal = dateFormat.parse(fechaFin);
        executor = Executors.newFixedThreadPool(3);
        completionService = new ExecutorCompletionService<Double>(executor);
        suma = 0.0;
    }

    public void procesarFechasParalelo() throws InterruptedException, ExecutionException {
        long inicio, fin = 0;
        long diferenciaFechas = fechaFinal.getTime() - fechaInicio.getTime();
        long intervalo = diferenciaFechas / 3;
        
        for (int i = 0; i < 2; i++) {
            inicio = fechaInicio.getTime() + (intervalo * i);
            fin = fechaInicio.getTime() + (intervalo * (i + 1));
            System.out.println(new Date(inicio).toString() + " " + new Date(fin).toString());
            completionService.submit(new Slave(topic, new Date(inicio), new Date(fin)));
        }
        fin = fin + 24 * 60 * 60 * 1000;
        completionService.submit(new Slave(topic, new Date(fin), fechaFinal));
        System.out.println(new Date(fin + 1).toString() + " " + fechaFinal.toString());

        executor.shutdown();

        for (int i = 0; i < 3; i++) {
            try {
                Future<Double> future = completionService.take();
                suma += future.get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        executor.awaitTermination(200, TimeUnit.SECONDS);
        System.out.println(suma / 3);
    }

    public static void main(String[] argv) throws Exception {
        if (argv.length < 3) {
            System.err.println("Usage: Master <tema> <fechaInicio> <fechaFin>");
            System.exit(1);
        }

        String tema = argv[0];
        String fechaInicio = argv[1];
        String fechaFin = argv[2];

        Master master = new Master(tema, fechaInicio, fechaFin);
        long inicio = System.currentTimeMillis();
        master.procesarFechasParalelo();
        
        long fin = System.currentTimeMillis();
        System.out.println("ha tardado: " + (fin - inicio) + " milisegundos");
    }
}

