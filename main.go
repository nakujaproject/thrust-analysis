package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"time"

	controllers "thrust-analysis/controllers"

	influxdb2 "github.com/influxdata/influxdb-client-go"
	"github.com/influxdata/influxdb-client-go/api"
	"github.com/tarm/serial"
)

func WriteToFile(i float64, f *os.File) {
	//write to the file
	fmt.Fprintf(f, "%v\n", i)
	//write to stdout
	fmt.Printf("Printing out: %v\n", i)
}

func main() {
	d, err := os.Getwd()
	if err != nil {
		fmt.Println(err)
	}
	timestamp := time.Now().Format("2006-01-02 15-04-05")
	fileName := []string{"/", timestamp, ".csv"}
	filenameShort := strings.Join(fileName, "")
	filename := d + filenameShort

	f, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0666)

	if err != nil {
		fmt.Println(err)
	}

	//initialize influx db
	var writeAPI api.WriteAPI
	var influxClient influxdb2.Client
	writeAPI, influxClient = controllers.InitializeInfluxDb()

	c := &serial.Config{Name: "COM10", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}

	_, err = s.Write([]byte("1"))
	if err != nil {
		log.Fatal(err)
	}

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, os.Interrupt)
	go func() {
		<-sigs
		time.Sleep(1500 * time.Millisecond)
		f.Close()
		controllers.UploadToDrive(filename)
		controllers.CloseInfluxClient(writeAPI, influxClient)
		fmt.Println("Grace")
		s.Close()
		os.Exit(0)
	}()

	scanner := bufio.NewScanner(s)
	writeValues(scanner, writeAPI, f)
}

func writeValues(scanner *bufio.Scanner, writeAPI api.WriteAPI, f *os.File) {
	for scanner.Scan() {
		readings, _ := strconv.ParseFloat(scanner.Text(), 64)
		//fmt.Println(readings)
		go WriteToFile(readings, f)
		//add to influx db
		go controllers.PushToDb(readings, writeAPI)
	}
}
