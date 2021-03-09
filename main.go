package main

import (
	"bufio"
	"fmt"
	"log"
	"strconv"

	controllers "thrust-analysis/controllers"

	influxdb2 "github.com/influxdata/influxdb-client-go"
	"github.com/influxdata/influxdb-client-go/api"
	"github.com/tarm/serial"
)

func main() {
	//initialize influx db
	var writeAPI api.WriteAPI
	var influxClient influxdb2.Client
	writeAPI, influxClient = controllers.InitializeInfluxDb()

	c := &serial.Config{Name: "COM5", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}

	//n, err := s.Write([]byte("test"))
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(s)
	for scanner.Scan() {
		readings, _ := strconv.ParseFloat(scanner.Text(), 64)
		fmt.Println(readings)
		//add to influx db
		controllers.PushToDb(readings, writeAPI)
	}

	//close influx client
	controllers.CloseInfluxClient(writeAPI, influxClient)
}
