package controllers

import (
	"time"

	influxdb2 "github.com/influxdata/influxdb-client-go"
	"github.com/influxdata/influxdb-client-go/api"
)

//InitializeInfluxDb and set up write api
func InitializeInfluxDb() (api.WriteAPI, influxdb2.Client) {
	const token = "R2I7-HM24bMp0SpIMAMFKwO2-Q68UV27-1ZplFeE3IJy-WTn8DB8npzZrLgcc7KGGE-YdW1IlAOIMIBdekwSTA=="
	const bucket = "test-stand"
	const org = "nakuja"
	clientInflux := influxdb2.NewClientWithOptions("http://localhost:8086", token,
		influxdb2.DefaultOptions().SetBatchSize(1))
	writeAPI := clientInflux.WriteAPI(org, bucket)
	return writeAPI, clientInflux
}

//PushToDb influxdb
func PushToDb(msg float64, w api.WriteAPI) {
	p := influxdb2.NewPoint(
		"thrust",
		map[string]string{"Unit": "grams"},
		map[string]interface{}{
			"thrust": msg,
		},
		time.Now())
	w.WritePoint(p)
}

//CloseInfluxClient close client
func CloseInfluxClient(w api.WriteAPI, clientInflux influxdb2.Client) {
	w.Flush()
	clientInflux.Close()
}
