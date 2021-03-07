package main

import (
	"fmt"
	"log"

	"github.com/tarm/serial"
)

func main() {
	c := &serial.Config{Name: "COM4", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}

	n, err := s.Write([]byte("test"))
	if err != nil {
		log.Fatal(err)
	}

	for {
		buf := make([]byte, 128)
		n, err = s.Read(buf)
		if err != nil {
			log.Fatal(err)
		}
		s := string(buf[:n])
		fmt.Println(s)

	}
}
