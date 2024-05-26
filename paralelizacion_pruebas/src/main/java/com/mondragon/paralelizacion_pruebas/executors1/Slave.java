package com.mondragon.paralelizacion_pruebas.executors1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;

public class Slave implements Runnable{

    String topic;
    Date fechaInicio;
    Date fechaFinal;
    List<Double> numeros;
    Double media;


    public Slave(String topic, Date fechaInicio, Date fechaFinal ){
        this.topic = topic;
        this.fechaInicio = fechaInicio;
        this.fechaFinal = fechaFinal;
        numeros = new ArrayList<>();
        media = 0.0;
    }
    public Double media (List<Double> numeros, int size){
        double suma = 0;
        for(int i = 0; i < size; i++){
            suma += numeros.get(i);
        }

        return suma / size;
    }

    @Override
    public void run() {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        String csvFile = "C:\\Users\\julga\\Documents\\MU\\23-24\\wanderlust\\Web\\paralelizacion_pruebas\\src\\main\\java\\com\\mondragon\\paralelizacion_pruebas\\IBEX-1994-2023_finished.csv";
        
        for(int j = 0; j < 1000; j++){

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            // Leer la primera línea (encabezado) y descartarla
            br.readLine();
    
            String line;
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                String fechaString = data[0];
                String[] datosSinPrimeraColumna = new String[data.length - 1];
                System.arraycopy(data, 1, datosSinPrimeraColumna, 0, data.length - 1);
                Date fecha = dateFormat.parse(fechaString);
                if (fecha.after(fechaInicio) && fecha.before(fechaFinal)) {
                    Double suma = 0.0;
                    for(int i = 0; i < datosSinPrimeraColumna.length; i++){
                        if(datosSinPrimeraColumna[i] != null){
                            suma += Double.parseDouble(datosSinPrimeraColumna[i]);
                        }
                    }
                    numeros.add(suma / datosSinPrimeraColumna.length);
                }
            }
    
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
        media = media(numeros, numeros.size());
    }

    public Double getMedia(){
        return this.media;
    }
}
