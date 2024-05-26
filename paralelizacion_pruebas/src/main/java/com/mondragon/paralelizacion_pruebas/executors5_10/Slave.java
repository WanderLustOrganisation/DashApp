package com.mondragon.paralelizacion_pruebas.executors5_10;


public class Slave {

    private final static String TASK_QUEUE_NAME = "task_queue";
    private final static String RESULT_QUEUE_NAME = "result_queue";
    private final static String DB_URL = "jdbc:mariadb://localhost:3307/probak_paralelizacion";
    private final static String USER = "wanderlust";
    private final static String PASSWORD = "wanderlust";


    public Slave(){
    }

    public static void main(String[] argv) throws Exception {
        if (argv.length < 1) {
            System.err.println("Usage: Slave <RabbitMQ_host>");
            System.exit(1);
        }

        String rabbitMQHost = argv[0];
        Slave slave = new Slave();
    }
}
