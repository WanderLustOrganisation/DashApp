package com.mondragon.paralelizacion_pruebas.executors1;

import com.rabbitmq.client.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class Master {

    Date fechaInicio;
    Date fechaFinal;
    String topic;
    ExecutorService executor;
    Double suma;

    public Master(String topic, String fechaInicio, String fechaFin) throws ParseException, IOException {
        this.topic = topic;
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.fechaInicio = dateFormat.parse(fechaInicio);
        this.fechaFinal = dateFormat.parse(fechaFin);
        executor = Executors.newCachedThreadPool();
        suma = 0.0;
    }
    

    public void procesarFechasParalelo() throws InterruptedException{
        long inicio, fin = 0;

        long diferenciaFechas = fechaFinal.getTime() - fechaInicio.getTime();
        long intervalo = diferenciaFechas / 3;
        
        for (int i = 0; i < 2; i++) {
            inicio = fechaInicio.getTime() + (intervalo * i);
            fin = fechaInicio.getTime() + (intervalo * (i + 1));
            System.out.println(new Date(inicio).toString() + " " + new Date(fin).toString());
            executor.execute(new Slave(topic, fechaInicio, fechaFinal));
        }
        executor.execute(new Slave(topic, new Date(fin), fechaFinal));
        System.out.println(new Date(fin).toString() + " " + fechaFinal.toString());

        executor.shutdown();
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
		System.out.println ("ha tardado: "+(fin -inicio)+" milisegundos");
    }
}


