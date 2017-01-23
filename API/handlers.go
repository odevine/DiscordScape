package main

import (
	"fmt"
	"net/http"
)

func Index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello world\n")
}

func GetInventory(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello world\n")
}

func GiveItem(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello world\n")
}
