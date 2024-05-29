package com.mondragon.paralelizacion_pruebas.executors5_10;

import java.io.FileWriter;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.concurrent.ExecutionException;

import com.opencsv.CSVWriter;

public class Correr {

    final static int COLUMNAS = 5;

    public static void main(String[] args) throws ParseException, InterruptedException, ExecutionException {
        String tema = "Tema";
        String fechaInicio = "1994-01-01";
        String fechaFin = "1995-01-01";
        int numEjecuciones = 10;
        long sumaTiempos = 0;
        int años = 1;
        int filas = 0;

        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");

        for (int k = 1; k <= 5; k++) {
            try (CSVWriter writer = new CSVWriter(new FileWriter("con_paralelizar_00" + k + ".csv"))) {
                String[] header = { "cantidad_de_datos", "tiempo_en_milisegundos", "nodos_threadpool" };
                writer.writeNext(header);
                for (int j = 2; j <= 4; j++) {
                    fechaFin = "1995-01-01";
                    años = 1;
                    while (!fechaFin.equals("2024-01-01")) {
                        filas = 365 * años;
                        sumaTiempos = 0;

                        for (int i = 0; i < numEjecuciones; i++) {
                            long inicio = System.currentTimeMillis();
                            Master master = new Master(tema, fechaInicio, fechaFin, j);
                            master.procesarFechasParalelo();
                            long fin = System.currentTimeMillis();
                            long tiempoEjecucion = fin - inicio;
                            sumaTiempos += tiempoEjecucion;
                        }
                        long tiempoMedio = sumaTiempos / numEjecuciones;
                        System.out.println("Tiempo medio de ejecución: " + tiempoMedio + " milisegundos.");
                        System.out.println("Cantidad de datos aprox: " + filas * COLUMNAS);
                        String[] data = { String.valueOf(COLUMNAS * filas), String.valueOf(tiempoMedio),
                                String.valueOf(j) };
                        writer.writeNext(data);
                        Calendar calendar = Calendar.getInstance();
                        calendar.setTime(dateFormat.parse(fechaFin));
                        calendar.add(Calendar.YEAR, 1);
                        fechaFin = dateFormat.format(calendar.getTime());
                        años += 1;
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
