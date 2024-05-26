package com.mondragon.paralelizacion_pruebas.chat_10;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.concurrent.*;

@RestController
public class SlaveController {

    private static final String DB_URL = "jdbc:mariadb://localhost:3307/probak_paralelizacion";
    private static final String USER = "wanderlust";
    private static final String PASSWORD = "wanderlust";

    @GetMapping("/process")
    public Double process(@RequestParam String topic, @RequestParam String fechaInicio, @RequestParam String fechaFinal) throws ParseException, ExecutionException, InterruptedException {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date startDate = dateFormat.parse(fechaInicio);
        Date endDate = dateFormat.parse(fechaFinal);

        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        CompletionService<Double> completionService = new ExecutorCompletionService<>(executor);

        long startTime = startDate.getTime();
        long endTime = endDate.getTime();
        int tasks = Runtime.getRuntime().availableProcessors();
        long interval = (endTime - startTime) / tasks;

        for (int i = 0; i < tasks; i++) {
            long taskStart = startTime + (i * interval);
            long taskEnd = (i == tasks - 1) ? endTime : (startTime + ((i + 1) * interval));
            completionService.submit(new DataFetcher(taskStart, taskEnd, topic));
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
        private String topic;

        public DataFetcher(long taskStart, long taskEnd, String topic) {
            this.taskStart = taskStart;
            this.taskEnd = taskEnd;
            this.topic = topic;
        }

        @Override
        public Double call() throws Exception {
            List<Double> numeros = fetchDataFromDatabase(taskStart, taskEnd, topic);
            return media(numeros);
        }

        private List<Double> fetchDataFromDatabase(long taskStart, long taskEnd, String topic) {
            // Implement the database fetching logic here similar to what you have in your original Slave class
            // ...

            return null;
        }

        private Double media(List<Double> numeros) {
            double suma = 0;
            for (Double numero : numeros) {
                suma += numero;
            }
            return suma / numeros.size();
        }
    }
}
