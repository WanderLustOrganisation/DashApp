package com.mondragon.paralelizacion_pruebas.chat_10;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.*;

public class Master {

    Date fechaInicio;
    Date fechaFinal;
    String topic;
    CompletionService<Double> completionService;
    ExecutorService executor;
    Double suma;
    List<String> slaveIps;

    public Master(String topic, String fechaInicio, String fechaFin, List<String> slaveIps) throws ParseException {
        this.topic = topic;
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.fechaInicio = dateFormat.parse(fechaInicio);
        this.fechaFinal = dateFormat.parse(fechaFin);
        this.executor = Executors.newFixedThreadPool(slaveIps.size());
        this.completionService = new ExecutorCompletionService<>(executor);
        this.suma = 0.0;
        this.slaveIps = slaveIps;
    }

    public void procesarFechasParalelo() throws InterruptedException, ExecutionException {
        long inicio, fin = 0;
        long diferenciaFechas = fechaFinal.getTime() - fechaInicio.getTime();
        long intervalo = diferenciaFechas / slaveIps.size();
        
        for (int i = 0; i < slaveIps.size(); i++) {
            inicio = fechaInicio.getTime() + (intervalo * i);
            fin = (i == slaveIps.size() - 1) ? fechaFinal.getTime() : fechaInicio.getTime() + (intervalo * (i + 1));
            System.out.println(new Date(inicio).toString() + " " + new Date(fin).toString());
            completionService.submit(new SlaveCaller(slaveIps.get(i), topic, new Date(inicio), new Date(fin)));
        }

        executor.shutdown();

        for (int i = 0; i < slaveIps.size(); i++) {
            try {
                Future<Double> future = completionService.take();
                suma += future.get();
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }
        
        executor.awaitTermination(200, TimeUnit.SECONDS);
        System.out.println(suma / slaveIps.size());
    }

    public static void main(String[] argv) throws Exception {
        if (argv.length < 4) {
            System.err.println("Usage: Master <tema> <fechaInicio> <fechaFin> <slaveIp1> <slaveIp2> ... <slaveIpN>");
            System.exit(1);
        }

        String tema = argv[0];
        String fechaInicio = argv[1];
        String fechaFin = argv[2];
        List<String> slaveIps = new ArrayList<>();
        for (int i = 3; i < argv.length; i++) {
            slaveIps.add(argv[i]);
        }

        Master master = new Master(tema, fechaInicio, fechaFin, slaveIps);
        long inicio = System.currentTimeMillis();
        master.procesarFechasParalelo();
        
        long fin = System.currentTimeMillis();
        System.out.println("ha tardado: " + (fin - inicio) + " milisegundos");
    }
}
