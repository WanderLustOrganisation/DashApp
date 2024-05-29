package com.mondragon.paralelizacion_pruebas.chat_10;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.Callable;

public class SlaveCaller implements Callable<Double> {

    private String slaveIp;
    private String topic;
    private Date fechaInicio;
    private Date fechaFinal;

    public SlaveCaller(String slaveIp, String topic, Date fechaInicio, Date fechaFinal) {
        this.slaveIp = slaveIp;
        this.topic = topic;
        this.fechaInicio = fechaInicio;
        this.fechaFinal = fechaFinal;
    }

    @Override
    public Double call() throws Exception {
        String urlStr = String.format("http://%s/process?topic=%s&fechaInicio=%s&fechaFinal=%s", slaveIp, topic, dateToString(fechaInicio), dateToString(fechaFinal));
        URL url = new URL(urlStr);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        
        if (conn.getResponseCode() != 200) {
            throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
        }

        BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
        String output;
        StringBuilder response = new StringBuilder();
        while ((output = br.readLine()) != null) {
            response.append(output);
        }
        conn.disconnect();

        return Double.parseDouble(response.toString());
    }

    private String dateToString(Date date) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        return dateFormat.format(date);
    }
}

