package controllers

import (
	"time"

	influxdb2 "github.com/influxdata/influxdb-client-go"
	"github.com/influxdata/influxdb-client-go/api"
)

//InitializeInfluxDb and set up write api
func InitializeInfluxDb() (api.WriteAPI, influxdb2.Client) {
	const token = "cGw69KfelV-nDOGiZ5Gd_IN-B3WZKhQ7Km0zpTn1faLnDYirsGm3Z7sBxD_gBWq1uxUydRMQm1wML5Tnal8hQg=="
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
