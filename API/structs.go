package main

//import (
//
//)

type Item struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type Inventory []Item
